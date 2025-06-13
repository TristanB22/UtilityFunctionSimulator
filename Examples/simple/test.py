import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

# this is the file that is going to actually run the test
# make sure that all of the imports are imported from the requirements
# file before running the test

# import the necessary libraries
from World_Sim.Agent import Agent
from World_Sim.Labor import Labor

# set up a job for the agent
job = Labor(job_id=1, job_name="Software Engineer", job_description="A software engineer is a professional who designs, develops, and maintains software systems.")

# create the agent
agent = Agent(id=1, name="John Doe", attributes={"age": 30, "gender": "male"}, abilities={"can_read": True, "can_write": True}, constraints={"can_move": True}, job=Labor(job_id=1, job_name="Software Engineer", job_description="A software engineer is a professional who designs, develops, and maintains software systems."))

# print the agent	
print("we have created agent:")
print(agent)
print(f"The agent has the following job: {agent.job}")
print("Success!")