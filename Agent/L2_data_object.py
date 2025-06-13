import pandas as pd
from typing import Dict, Any, Optional

class L2_Data_Object:
	"""
	Stores a single L2 voter/person data instance with their attributes.
	Provides access to the person's data as a dictionary.
	"""
	def __init__(self, data: Dict[str, Any]):
		"""
		Initialize with a single person's data.
		
		Args:
			data (Dict[str, Any]): Dictionary containing the person's attributes
		"""
		
		# store the data
		self.data = data
		
		# store the lalvoterid
		self.lalvoterid = self.get_data_point('LALVOTERID')

	def all_data(self) -> Dict[str, Any]:
		"""Return the person's data as a dictionary."""
		return self.data
	
	def get_data_point(self, key: str) -> Any:
		"""Return a specific data point from the person's data."""
		return self.data.get(key, '')

	def get_lalvoterid(self) -> str:
		"""Return the person's LALVOTERID."""
		return self.lalvoterid

	def __str__(self):
		output = f"L2_Data_Object for {self.lalvoterid}\n"
		for key, value in self.data.items():
			if key != 'SEQUENCE':  # Skip SEQUENCE since it is not an attribute
				output += f"  {key}: {value}\n"
		return output


# get an example of the data and print it
if __name__ == "__main__":
    
	# Read just the first row of the tab-delimited file
    data = pd.read_csv('/Users/tristanbrigham/Desktop/Classes/Thesis/code_for_me/example_l2_data.txt', nrows=1)
    
    # Convert the single row to dictionary
    first_person = data.iloc[0].to_dict()
    
    # Create L2_Data_Object instance
    person = L2_Data_Object(first_person)
    
    # Print the person's data
    print(person)