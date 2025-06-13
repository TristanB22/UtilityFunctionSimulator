# run.py
# Author: Tristan Brigham
# Date: 2025-06-09
# Description: This file is used to run the World_Sim program.

# import the necessary libraries
from Agent import Agent
from Labor import Labor
import argparse
import os
import pandas as pd
from Agent import L2_Data_Object
from Environment.osm_pull import pull_osm_data, parse_place_name, check_osm_data_exists
from Environment.google_maps_enrichment import enrich_osm_data
from Environment.visualization import create_interactive_map
from dotenv import load_dotenv
import logging
from pathlib import Path
import sys

# Define custom logging levels
logging.TRACE = 5
logging.addLevelName(logging.TRACE, 'TRACE')

def trace(self, message, *args, **kwargs):
	if self.isEnabledFor(logging.TRACE):
		self._log(logging.TRACE, message, args, **kwargs)

logging.Logger.trace = trace

# Configure logging
logging.basicConfig(
	level=logging.INFO,
	format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

def set_log_level(verbosity: int) -> None:
	"""
	Set the logging level based on verbosity.
	
	Args:
		verbosity (int): Verbosity level (1-3)
			1: INFO (default)
			2: DEBUG
			3: TRACE (most verbose)
	"""
	if verbosity == 1:
		logging.getLogger().setLevel(logging.INFO)
	elif verbosity == 2:
		logging.getLogger().setLevel(logging.DEBUG)
	elif verbosity == 3:
		# Create a custom TRACE level
		logging.TRACE = 5  # Between DEBUG and INFO
		logging.addLevelName(logging.TRACE, 'TRACE')
		logging.getLogger().setLevel(logging.TRACE)
		# Add trace method to logger
		def trace(self, message, *args, **kwargs):
			if self.isEnabledFor(logging.TRACE):
				self._log(logging.TRACE, message, args, **kwargs)
		logging.Logger.trace = trace

def get_l2_data_directory() -> str:
	"""
	Get the L2 data directory from environment variables.
	
	Returns:
		str: The L2 data directory path
		
	Raises:
		ValueError: If the L2_DATA_DIRECTORY environment variable is not set
	"""
	directory = os.getenv('L2_DATA_DIRECTORY')
	if not directory:
		raise ValueError("Environment variable L2_DATA_DIRECTORY is not set")
	return directory

def get_osm_data_directory(testing: bool) -> str:
	"""
	Get the OSM data directory from environment variables.
	
	Args:
		testing (bool): Whether we're in testing mode
		
	Returns:
		str: The OSM data directory path
		
	Raises:
		ValueError: If the required environment variable is not set
	"""
	env_var = 'TESTING_OSM_DATA_DIRECTORY' if testing else 'OSM_DATA_DIRECTORY'
	directory = os.getenv(env_var)
	
	if not directory:
		raise ValueError(f"Environment variable {env_var} is not set")
	
	return directory

def validate_location_args(args: argparse.Namespace) -> None:
	"""
	Validate location-related command line arguments.
	
	Args:
		args: Command line arguments
		
	Raises:
		ValueError: If arguments are invalid or missing
	"""
	# Check if any location data is provided
	has_place = bool(args.place)
	has_components = all([args.city, args.state_name, args.country])
	
	if not (has_place or has_components):
		raise ValueError(
			"No location data provided. Please use either:\n"
			"  --place 'City, State, Country' (e.g., 'Bar Harbor, Maine, USA')\n"
			"  OR\n"
			"  --city 'City' --state-name 'State' --country 'Country' (e.g., --city 'Bar Harbor' --state-name 'Maine' --country 'USA')"
		)
	
	# If using individual components, check for partial specifications
	if not has_place and not has_components:
		missing = []
		if not args.city:
			missing.append("--city")
		if not args.state_name:
			missing.append("--state-name")
		if not args.country:
			missing.append("--country")
		
		if missing:
			raise ValueError(
				f"Missing required location components: {', '.join(missing)}\n"
				"When using individual components, all of --city, --state-name, and --country must be provided.\n"
				"Example: --city 'Bar Harbor' --state-name 'Maine' --country 'USA'"
			)
	
	# If using --place, validate format
	if has_place:
		try:
			city, state, country = parse_place_name(args.place)
		except ValueError as e:
			raise ValueError(
				f"Invalid --place format: {str(e)}\n"
				"Please use format: 'City, State, Country'\n"
				"Example: 'Bar Harbor, Maine, USA'"
			)

def validate_state_arg(args: argparse.Namespace) -> None:
	"""
	Validate state abbreviation argument.
	
	Args:
		args: Command line arguments
		
	Raises:
		ValueError: If state abbreviation is invalid
	"""
	if args.state:
		if not args.state.isalpha() or len(args.state) != 2:
			raise ValueError(
				f"Invalid state abbreviation: {args.state}\n"
				"State abbreviation must be exactly 2 letters.\n"
				"Example: --state DE"
			)

# function to find the state file
def find_state_file(state_abbr: str) -> str:
	"""
	Return the path to the state file for the given state abbreviation, or None if not found.
	Args:
		state_abbr (str): The two-letter state abbreviation (e.g., AZ, CA)
	Returns:
		str: The path to the state file, or None if not found
	"""
	l2_dir = get_l2_data_directory()
	
	# try the uniform file first
	uniform_file = f'VM2Uniform--{state_abbr.upper()}.tab'
	uniform_path = os.path.join(l2_dir, uniform_file)
	
	# check if the uniform file exists
	if os.path.exists(uniform_path):
		return uniform_path
	
	# try the demographic file as fallback
	demo_file = f'VM2--{state_abbr.upper()}-DEMOGRAPHIC-FillRate.tab'
	demo_path = os.path.join(l2_dir, demo_file)
	
	# check if the demographic file exists
	if os.path.exists(demo_path):
		return demo_path
	
	# if neither file exists, return None
	return None

def main():
	# initialize the parser
	parser = argparse.ArgumentParser(
		description='Run World_Sim with optional L2 state data or OSM place data.',
		formatter_class=argparse.RawDescriptionHelpFormatter,
		epilog="""
Examples:
  # Using full place name
  python run.py --place "Bar Harbor, Maine, USA"
  
  # Using individual components
  python run.py --city "Bar Harbor" --state-name "Maine" --country "USA"
  
  # Using L2 state data
  python run.py --state DE
  
  # Force re-download of existing OSM data
  python run.py --place "Bar Harbor, Maine, USA" --force-osm
  
  # Testing mode
  python run.py --place "Bar Harbor, Maine, USA" --testing
  
  # Enable Google Maps enrichment
  python run.py --place "Bar Harbor, Maine, USA" --enrich-google
  
  # Set verbosity level
  python run.py --place "Bar Harbor, Maine, USA" --verbosity 3
  
  # Create interactive map
  python run.py --place "Bar Harbor, Maine, USA" --visualize
  
  # Limit API calls
  python run.py --place "Bar Harbor, Maine, USA" --enrich-google --max-calls 100
		"""
	)
	parser.add_argument('--state', type=str, help='Two-letter state abbreviation (e.g., AZ, CA)')
	parser.add_argument('--place', type=str, help='Full place name (e.g., "Bar Harbor, Maine, USA")')
	parser.add_argument('--city', type=str, help='City name')
	parser.add_argument('--state-name', type=str, help='State name')
	parser.add_argument('--country', type=str, help='Country name')
	parser.add_argument('--testing', action='store_true', help='If set, use testing data directory and limit simulation depth')
	parser.add_argument('--force-osm', action='store_true', help='Force re-download of OSM data even if it already exists')
	parser.add_argument('--enrich-google', action='store_true', help='Enable Google Maps data enrichment for buildings')
	parser.add_argument('--verbosity', type=int, choices=[1, 2, 3], default=1,
		help='Set the verbosity level (1: INFO, 2: DEBUG, 3: TRACE)')
	parser.add_argument('--visualize', action='store_true', help='Create an interactive map visualization')
	parser.add_argument('--max-calls', type=int, help='Maximum number of API calls to make during enrichment')
	args = parser.parse_args()

	try:
		# Set logging level based on verbosity
		set_log_level(args.verbosity)
		logger.debug(f"Logging level set to verbosity {args.verbosity}")

		# Validate arguments
		validate_location_args(args)
		validate_state_arg(args)

		# Handle OSM place data
		if args.place or (args.city and args.state_name and args.country):
			try:
				# Get place components either from --place or individual arguments
				if args.place:
					city, state, country = parse_place_name(args.place)
				else:
					city, state, country = args.city, args.state_name, args.country
				
				osm_dir = get_osm_data_directory(args.testing)
				
				# Construct full place name
				place = f"{city}, {state}, {country}"
				logger.info(f"Pulling OSM data for place: {place}")
				if logger.isEnabledFor(logging.DEBUG):
					logger.debug(f"Using OSM directory: {osm_dir}")
				
				network_path, features_path, boundary_path = pull_osm_data(place, osm_dir, force=args.force_osm)
				logger.info(f"OSM data saved to:\nNetwork: {network_path}\nFeatures: {features_path}\nBoundary: {boundary_path}")
				
				# If Google Maps enrichment is enabled, enrich the data
				if args.enrich_google:
					logger.info("Enriching OSM data with Google Maps data...")
					if logger.isEnabledFor(logging.DEBUG):
						logger.debug("Starting Google Maps enrichment process")
					enriched_path = enrich_osm_data(
						features_path,
						features_path,
						testing=args.testing,
						max_calls=args.max_calls
					)
					logger.info(f"Enriched data saved to: {enriched_path}")
					if logger.isEnabledFor(logging.TRACE):
						logger.trace("Detailed enrichment process completed")
				
				# Create interactive map if requested
				if args.visualize:
					logger.info("Creating interactive map visualization...")
					map_path = create_interactive_map(network_path, features_path, boundary_path)
					logger.info(f"Interactive map saved to: {map_path}")
				
			except Exception as e:
				logger.error(f"Failed to pull OSM data: {str(e)}")
				if logger.isEnabledFor(logging.DEBUG):
					logger.debug(f"Error details: {str(e)}", exc_info=True)
				return

		# Handle L2 state data if provided
		if args.state:
			try:
				# find the state file
				state_file = find_state_file(args.state)
				if not state_file:
					logger.error(f"Error: No L2 data file found for state '{args.state}'.")
					return
				# print the state file
				logger.info(f"Loading L2 data from: {state_file}")
				if logger.isEnabledFor(logging.DEBUG):
					logger.debug(f"State file details: {state_file}")
				
				# read the state file
				nrows = 10000 if args.testing else None
				if logger.isEnabledFor(logging.DEBUG):
					logger.debug(f"Reading {nrows if nrows else 'all'} rows from state file")
				
				df = pd.read_csv(state_file, delimiter='\t', dtype=str, nrows=nrows, on_bad_lines='skip', encoding='latin1')
				# check if the state file is empty
				if df.empty:
					logger.error(f"No data found in {state_file}.")
					return
				
				# create Agent instances for each row
				agents = []
				for idx, row in df.iterrows():
					if logger.isEnabledFor(logging.TRACE):
						logger.trace(f"Processing row {idx}")
					l2_obj = L2_Data_Object(row)
					agent = Agent(id=idx, l2_object=l2_obj)
					agents.append(agent)
				
				logger.info(f"Created {len(agents)} Agent objects for state {args.state}.")
				if agents:
					logger.info("First agent:")
					logger.info(agents[0])
					if logger.isEnabledFor(logging.DEBUG):
						logger.debug(f"First agent details: {agents[0].__dict__}")
				else:
					logger.info("No agents created.")
			except Exception as e:
				logger.error(f"Failed to process L2 data: {str(e)}")
				if logger.isEnabledFor(logging.DEBUG):
					logger.debug(f"Error details: {str(e)}", exc_info=True)
				return

	except ValueError as e:
		logger.error(str(e))
		parser.print_help()
		sys.exit(1)

if __name__ == "__main__":
	main()

