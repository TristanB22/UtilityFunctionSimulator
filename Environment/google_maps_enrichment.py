import os
import time
import logging
import geopandas as gpd
import pandas as pd
import requests
from typing import Dict, List, Optional, Tuple
from pathlib import Path
from dotenv import load_dotenv
import json
from ratelimit import limits, sleep_and_retry
from datetime import datetime
import warnings
import multiprocessing as mp
from queue import Empty
import threading
from concurrent.futures import ThreadPoolExecutor
import backoff

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Get API key from environment
GOOGLE_MAPS_API_KEY = os.getenv('GOOGLE_MAPS_API_KEY')
if not GOOGLE_MAPS_API_KEY:
    raise ValueError("GOOGLE_MAPS_API_KEY environment variable is not set")

# Rate limiting constants
CALLS = 1  # Number of calls allowed per period
RATE_LIMIT_PERIOD = 1  # Time period in seconds
MAX_RETRIES = 3  # Maximum number of retries for API calls
BACKOFF_FACTOR = 2  # Exponential backoff factor

# Global counter for API calls
api_call_counter = None
api_call_lock = None

def init_worker():
    """Initialize worker process with global counter and lock."""
    global api_call_counter, api_call_lock
    api_call_counter = mp.Value('i', 0)
    api_call_lock = mp.Lock()

@backoff.on_exception(
    backoff.expo,
    (requests.exceptions.RequestException, requests.exceptions.HTTPError),
    max_tries=MAX_RETRIES,
    factor=BACKOFF_FACTOR
)
def make_api_request(url: str, params: Dict) -> Dict:
    """
    Make an API request with exponential backoff retry.
    
    Args:
        url (str): API endpoint URL
        params (Dict): Request parameters
        
    Returns:
        Dict: API response data
    """
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()

def get_place_data(lat: float, lng: float, max_calls: Optional[int] = None) -> Optional[Dict]:
    """
    Get place data from Google Maps API with caching and rate limiting.
    
    Args:
        lat (float): Latitude
        lng (float): Longitude
        max_calls (int, optional): Maximum number of API calls allowed
        
    Returns:
        Optional[Dict]: Place data or None if not found
    """
    global api_call_counter, api_call_lock
    
    # Check if we've hit the API call limit
    with api_call_lock:
        if max_calls is not None and api_call_counter.value >= max_calls:
            return None
        api_call_counter.value += 1
    
    # Create cache directory if it doesn't exist
    cache_dir = Path('cache/google_maps')
    cache_dir.mkdir(parents=True, exist_ok=True)
    
    # Create cache key from coordinates
    cache_key = f"{lat:.6f}_{lng:.6f}"
    cache_file = cache_dir / f"{cache_key}.json"
    
    # Check cache first
    if cache_file.exists():
        try:
            with open(cache_file, 'r') as f:
                cached_data = json.load(f)
                # Check if cache is less than 30 days old
                cache_time = datetime.fromisoformat(cached_data.get('cache_time', '2000-01-01'))
                if (datetime.now() - cache_time).days < 30:
                    return cached_data
        except Exception as e:
            logger.warning(f"Error reading cache: {str(e)}")
    
    try:
        # Make API request with rate limiting
        time.sleep(1)  # Basic rate limiting
        url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
        params = {
            'location': f"{lat},{lng}",
            'radius': '50',  # 50 meters radius
            'key': GOOGLE_MAPS_API_KEY
        }
        
        data = make_api_request(url, params)
        
        if data['status'] == 'OK' and data['results']:
            # Get the first result
            result = data['results'][0]
            
            # Extract relevant data
            place_data = {
                'place_id': result.get('place_id'),
                'name': result.get('name'),
                'types': result.get('types', []),
                'vicinity': result.get('vicinity'),
                'rating': result.get('rating'),
                'user_ratings_total': result.get('user_ratings_total'),
                'cache_time': datetime.now().isoformat()
            }
            
            # Cache the result
            try:
                with open(cache_file, 'w') as f:
                    json.dump(place_data, f)
            except Exception as e:
                logger.warning(f"Error writing to cache: {str(e)}")
            
            return place_data
            
        return None
        
    except Exception as e:
        logger.error(f"API request failed: {str(e)}")
        return None

def get_place_details(place_id: str, max_calls: Optional[int] = None) -> Dict:
    """
    Get detailed place information from Google Maps API.
    
    Args:
        place_id (str): Google Maps place ID
        max_calls (int, optional): Maximum number of API calls allowed
        
    Returns:
        Dict: Place details
    """
    global api_call_counter, api_call_lock
    
    # Check if we've hit the API call limit
    with api_call_lock:
        if max_calls is not None and api_call_counter.value >= max_calls:
            return {'status': 'OVER_QUERY_LIMIT'}
        api_call_counter.value += 1
    
    try:
        # Make API request with rate limiting
        time.sleep(1)  # Basic rate limiting
        url = "https://maps.googleapis.com/maps/api/place/details/json"
        params = {
            'place_id': place_id,
            'key': GOOGLE_MAPS_API_KEY
        }
        
        return make_api_request(url, params)
        
    except Exception as e:
        logger.error(f"API request failed: {str(e)}")
        return {'status': 'ERROR', 'error': str(e)}

def process_building(args: Tuple) -> Optional[Dict]:
    """
    Process a single building for enrichment.
    
    Args:
        args (Tuple): Tuple containing (building_data, max_calls, counter, lock)
        
    Returns:
        Optional[Dict]: Enriched building data or None if processing failed
    """
    building_data, max_calls, counter, lock = args
    try:
        # Check if we've hit the API call limit
        with lock:
            if max_calls is not None and counter.value >= max_calls:
                return None
            counter.value += 1
            current_calls = counter.value
        
        # Get initial place data
        place_data = get_place_data(building_data['lat'], building_data['lng'])
        if not place_data:
            return None
            
        # Get place details if we have a place_id
        if place_data.get('place_id'):
            with lock:
                if max_calls is not None and counter.value >= max_calls:
                    return place_data
                counter.value += 1
                current_calls = counter.value
            
            details = get_place_details(place_data['place_id'])
            if details['status'] == 'OK':
                result = details['result']
                place_data['rating'] = result.get('rating')
                place_data['website'] = result.get('website')
        
        return place_data
        
    except Exception as e:
        logger.error(f"Error processing building: {str(e)}")
        return None

def enrich_osm_data(input_path: str, output_path: str, testing: bool = False, max_calls: int = None) -> str:
    """
    Enrich OSM building data with Google Maps data using multiprocessing.
    
    Args:
        input_path (str): Path to input GeoJSON file
        output_path (str): Path to save enriched data
        testing (bool): Whether we're in testing mode (affects data directory only)
        max_calls (int, optional): Maximum number of API calls to make. If None, no limit.
        
    Returns:
        str: Path to enriched data file
    """
    try:
        # Read the input data
        buildings = gpd.read_file(input_path)
        logger.info(f"Loaded {len(buildings)} total features")
        
        # Filter for buildings only
        buildings = buildings[buildings['building'].notna()]
        logger.info(f"Found {len(buildings)} buildings")
        
        # Identify buildings that need enrichment
        needs_enrichment_mask = (
            buildings['name'].isna() |
            buildings['building'].isin(['yes', 'unknown']) |
            ~buildings.get('place_id', pd.Series([None]*len(buildings), index=buildings.index)).notna()
        )
        needs_enrichment = buildings[needs_enrichment_mask]
        logger.info(f"Found {len(needs_enrichment)} buildings that need enrichment")
        
        # Calculate centroids efficiently (suppress coordinate warnings)
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            buildings_copy = buildings.copy()
            centroids = buildings_copy.geometry.centroid
            buildings_copy['lat'] = centroids.y
            buildings_copy['lng'] = centroids.x
        
        # Filter to only buildings that need enrichment
        buildings_to_enrich = buildings_copy[needs_enrichment_mask]
        
        # Initialize manager for shared counter
        manager = mp.Manager()
        counter = manager.Value('i', 0)
        lock = manager.Lock()
        
        # Prepare data for multiprocessing
        building_data = buildings_to_enrich[['lat', 'lng']].to_dict('records')
        process_args = [(data, max_calls, counter, lock) for data in building_data]
        
        # Determine number of workers (use 75% of available CPUs)
        num_workers = max(1, int(mp.cpu_count() * 0.75))
        logger.info(f"Using {num_workers} worker processes")
        
        # Process buildings in parallel
        enriched_count = 0
        with mp.Pool(processes=num_workers) as pool:
            for i, result in enumerate(pool.imap_unordered(process_building, process_args)):
                if result:
                    idx = buildings_to_enrich.index[i]
                    # Update the building row with enriched data
                    for key, value in result.items():
                        if key != 'cache_time':  # Don't add cache_time to the building data
                            buildings_copy.at[idx, key] = value
                    enriched_count += 1
                
                # Save progress every 10 buildings
                if (enriched_count % 10 == 0) or (i == len(process_args) - 1):
                    logger.info(f"Saving progress... ({enriched_count} buildings enriched, {counter.value} API calls made)")
                    buildings_copy.to_file(output_path, driver='GeoJSON')
        
        # Final save
        buildings_copy.to_file(output_path, driver='GeoJSON')
        logger.info(f"Final save complete: {len(buildings_copy)} total records")
        logger.info(f"Made {counter.value} API calls")
        logger.info(f"Enriched {enriched_count} buildings")
        
        return output_path
        
    except Exception as e:
        logger.error(f"Error in enrich_osm_data: {str(e)}")
        raise

def get_reverse_geocode(lat: float, lng: float) -> Dict:
    """
    Get reverse geocoding information for a location.
    
    Args:
        lat (float): Latitude
        lng (float): Longitude
        
    Returns:
        Dict: Geocoding information
    """
    url = f"https://maps.googleapis.com/maps/api/geocode/json?latlng={lat},{lng}&key={GOOGLE_MAPS_API_KEY}"
    return make_api_request(url, {})

def get_nearby_places(lat: float, lng: float, radius: int = 25) -> Dict:
    """
    Get nearby places for a location.
    
    Args:
        lat (float): Latitude
        lng (float): Longitude
        radius (int): Search radius in meters
        
    Returns:
        Dict: Nearby places information
    """
    url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={lat},{lng}&radius={radius}&type=establishment&key={GOOGLE_MAPS_API_KEY}"
    return make_api_request(url, {})

def extract_building_centroids(buildings_gdf: gpd.GeoDataFrame) -> pd.DataFrame:
    """
    Extract centroids from building geometries.
    
    Args:
        buildings_gdf (gpd.GeoDataFrame): Buildings GeoDataFrame
        
    Returns:
        pd.DataFrame: DataFrame with building centroids
    """
    centroids = buildings_gdf.copy()
    centroids['centroid'] = centroids.geometry.centroid
    centroids['lat'] = centroids.centroid.y
    centroids['lng'] = centroids.centroid.x
    return centroids

def identify_candidate_buildings(buildings_gdf: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
    """
    Identify buildings that need enrichment.
    
    Args:
        buildings_gdf (gpd.GeoDataFrame): Buildings GeoDataFrame
        
    Returns:
        gpd.GeoDataFrame: Filtered buildings that need enrichment
    """
    return buildings_gdf[
        buildings_gdf["name"].isna() | 
        (buildings_gdf["building"].isin(["yes", None, "unknown"]))
    ]

def enrich_building_data(building_row: pd.Series) -> Dict:
    """
    Enrich a single building with Google Maps data.
    
    Args:
        building_row (pd.Series): Building data
        
    Returns:
        Dict: Enriched building data
    """
    enriched_data = {
        "osmBuildingType": building_row.get("building", "unknown"),
        "googleName": None,
        "googleTypes": None,
        "googleVicinity": None,
        "googleAddress": None,
        "googleRating": None,
        "googlePlaceId": None,
        "googleWebsite": None
    }
    
    try:
        # Get reverse geocoding data
        geocode_data = get_reverse_geocode(building_row['lat'], building_row['lng'])
        if geocode_data['status'] == 'OK':
            result = geocode_data['results'][0]
            enriched_data['googleAddress'] = result['formatted_address']
            
            # Extract address components
            for component in result['address_components']:
                if 'locality' in component['types']:
                    enriched_data['googleVicinity'] = component['long_name']
        
        # Get nearby places
        nearby_data = get_nearby_places(building_row['lat'], building_row['lng'])
        if nearby_data['status'] == 'OK' and nearby_data['results']:
            place = nearby_data['results'][0]
            enriched_data['googleName'] = place.get('name')
            enriched_data['googleTypes'] = place.get('types', [])
            enriched_data['googleVicinity'] = place.get('vicinity')
            enriched_data['googlePlaceId'] = place.get('place_id')
            
            # Get place details if we have a place_id
            if enriched_data['googlePlaceId']:
                details = get_place_details(enriched_data['googlePlaceId'])
                if details['status'] == 'OK':
                    result = details['result']
                    enriched_data['googleRating'] = result.get('rating')
                    enriched_data['googleWebsite'] = result.get('website')
        
    except Exception as e:
        logger.error(f"Error enriching building data: {str(e)}")
    
    return enriched_data 