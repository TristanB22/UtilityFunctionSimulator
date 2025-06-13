import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

# This script tests the Groq backend basic model using GroqEvalEngine.
# Make sure the environment variables GROQ_API_KEY and BASIC_MODEL_NAME are set.

from Environment.eval_engine import GroqEvalEngine, ModelType

# Instantiate the evaluation engine
engine = GroqEvalEngine()

# Example: Agent wants to get a job offer at a top tech company
current_state = "An agent named Alice is a recent computer science graduate with a 3.8 GPA from a state university. She has completed two internships at local companies and is actively applying for jobs."
target_state = "Alice receives a job offer from Google as a software engineer within the next 6 months."

# Send the request to the basic model
result = engine.call_groq_api(current_state=current_state, target_state=target_state, model_type=ModelType.BASIC, response_file="/Users/tristanbrigham/Desktop/Classes/Thesis/World_Sim/Examples/feasibility_evaluation/response.txt")

print(f"Raw response: {result['raw_response']}")

# Print the results
print("Groq Basic Model Context:")
print(result["context"])
print("Groq Basic Model Answer:")
print(result["answer"])
print("Groq Basic Model Reasoning:")
print(result["reasoning"])