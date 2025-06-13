# Labor.py
# Author: Tristan Brigham
# This file contains the labor class for the world simulation. It defines the job function that an agent has
# along with other basic information about their occupational status. 

# Labor is going to additionally contain the functions that a given job has access to and that the agent can
# perform. Each of the job functions will have an associated description with time estimates. Universal job functions
# will also exist which include things like quit, apply, and other basic functions. 

class Labor:
	
	def __init__(self, 
					job_id: int,
					job_name: str,
					job_description: str = None,
					employer: str = None,
					job_location: str = None,
					job_address: str = None,
					job_is_remote: bool = False,
					job_salary: float = None,
					job_hours: int = None,
					job_experience: int = None,
					job_min_education: str = None,
					job_skills: list[str] = None
				):
		
		self.assign_labor_information(job_id, job_name, job_description, job_location, job_is_remote, job_salary, job_hours, job_experience, job_min_education, job_skills)
		
		
	def assign_labor_information(self, job_id, job_name, job_description, job_location, job_is_remote, job_salary, job_hours, job_experience, job_min_education, job_skills):
		
		self.job_id = job_id
		self.job_name = job_name
		self.job_description = job_description
		self.job_location = job_location
		self.job_is_remote = job_is_remote
		self.job_salary = job_salary
		self.job_hours = job_hours
		self.job_experience = job_experience
		self.job_min_education = job_min_education
		self.job_skills = job_skills
		

	def __str__(self):
		return f"Job ID: {self.job_id}\nJob Name: {self.job_name}\nJob Description: {self.job_description}\nJob Location: {self.job_location}\nJob Is Remote: {self.job_is_remote}\nJob Salary: {self.job_salary}\nJob Hours: {self.job_hours}\nJob Experience: {self.job_experience}\nJob Minimum Education: {self.job_min_education}\nJob Skills: {self.job_skills}"
		
		
		