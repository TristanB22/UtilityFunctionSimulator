# eval_engine.py
# Author: Tristan Brigham
# This file contains the GroqEvalEngine class for interfacing with the Groq API (Qwen 32B model) for evaluation tasks in the world simulation environment.
# It is specifically designed to judge the feasibility of a given task and assign a probability of success to the task. We use
# langauge models in order to judge the feasibility of the given task by breaking it down into its constituent parts
# and then modelling out the combined probability of all of the parts being successful. 

import os
from enum import Enum
from dotenv import load_dotenv, find_dotenv
from groq import Groq
import re
from Toools.safe_utils import safe_for, RetryableError
import logging

# Load environment variables from .env file if present
load_dotenv(find_dotenv())

# enum so that we can get 
# the model type as a string
class ModelType(Enum):
	BASIC = "basic"
	REASONING = "reasoning"



class GroqEvalEngine:
	"""
	A utility class to interface with the Groq API (Qwen 32B model) for evaluation tasks.
	Can be imported and used anywhere in the program.
	"""
	def __init__(self, api_key: str = None):
		"""
		Initialize the GroqEvalEngine.
		Args:
			api_key (str, optional): Groq API key. If not provided, will use GROQ_API_KEY env variable.
		"""
		self.api_key = api_key or os.getenv("GROQ_API_KEY")
		self.reasoning_model_name = os.getenv("REASONING_MODEL_NAME")
		self.basic_model_name = os.getenv("BASIC_MODEL_NAME")
		self.client = Groq(api_key=self.api_key)


	def _parse_groq_response(self, response: str):
		"""
		Manually parse the response from the Groq model to extract context, answer, reasoning, and think (if present).
		Returns (context: str, answer: float or None, reasoning: str or None, think: str or None)
		"""
		def extract_tag(text, tag):
			# Try both closing styles: !<\TAG>! and !</TAG>!
			open_tag = f"!<{tag}>!"
			close_tag1 = f"!<\\{tag}>!"
			close_tag2 = f"!</{tag}>!"
			start = text.find(open_tag)
			if start == -1:
				return None
			start += len(open_tag)
			end1 = text.find(close_tag1, start)
			end2 = text.find(close_tag2, start)
			# Pick the first valid closing tag
			if end1 != -1 and (end2 == -1 or end1 < end2):
				end = end1
			elif end2 != -1:
				end = end2
			else:
				return None
			return text[start:end].strip()

		context = extract_tag(response, "CONTEXT")
		answer_raw = extract_tag(response, "ANSWER")
		reasoning = extract_tag(response, "REASONING")
		think = extract_tag(response, "think")

		# Process the answer
		answer = None
		if answer_raw:
			try:
				if answer_raw.startswith("eval(") and answer_raw.endswith(")"):
					expr = answer_raw[5:-1]
					# Remove any quotes around the expression
					expr = expr.strip("'\"")
					answer = float(eval(expr, {"__builtins__": {}}))
				elif answer_raw.replace('.', '', 1).isdigit():
					answer = float(answer_raw)
				else:
					answer = float(answer_raw)
			except Exception:
				answer = None
		return context, answer, reasoning, think

	@safe_for(Exception, default=None, handler=lambda e, fn, a, k: (_ for _ in ()).throw(RetryableError()) if 'network' in str(e).lower() or 'api' in str(e).lower() else None, max_retries=3, retry_delay=2)
	def _call_groq_with_retry(self, *args, **kwargs):
		return self.client.chat.completions.create(*args, **kwargs)

	def call_groq_api(self, current_state: str, target_state: str, model_type: ModelType = ModelType.BASIC, response_file: str = None, **kwargs) -> dict:
		"""
		Call the Groq API with a prompt constructed from current and target state, or read from a file if provided.
		Args:
			current_state (str): The current state of the world/task.
			target_state (str): The desired future state of the world/task.
			model_type (ModelType, optional): Type of model to use (REASONING or BASIC). Defaults to BASIC.
			response_file (str, optional): Path to a file containing a pre-generated response. If provided, will read from this file instead of calling the API.
			**kwargs: Additional arguments for client.chat.completions.create (see Groq API spec).
		Returns:
			A dict with 'context', 'answer', 'reasoning', 'think', and 'raw_response'.
		"""
		# If response_file is provided, read from it instead of calling the API
		if response_file:
			try:
				with open(response_file, 'r') as f:
					content = f.read().strip()
				context, answer, reasoning, think = self._parse_groq_response(content)
				return {"context": context, "answer": answer, "reasoning": reasoning, "think": think, "raw_response": content}
			except FileNotFoundError:
				# If file doesn't exist, we'll continue with API call and write response to file
				pass
			except Exception as e:
				print(f"Error reading response file: {e}")
				return None

		if model_type == ModelType.REASONING:
			prompt = (
				"Given the current state of affairs and a potential future state, "
				"break down the key steps required for the future state to occur. "
				"Estimate the probability of each step (assuming independence if reasonable), "
				"and combine them (using a Python eval() statement if appropriate) to estimate the overall probability. "
				"Be succinct in your analysis. "
				"Output your reasoning and beliefs between !<CONTEXT>! and !<\CONTEXT>!, "
				"then output your answer between !<ANSWER>! and !<\ANSWER>!. "
				"If using eval(), make sure the answer is a valid Python float expression. "
				"You must always include the !<CONTEXT>!...!<\CONTEXT>! and !<ANSWER>!...!<\ANSWER>! tags, even if the answer is a single number.\n"
				f"Current state: {current_state}\nTarget state: {target_state}"
			)
		else:
			prompt = (
				"Given the current state of affairs and a potential future state, "
				"immediately provide context for your decision and then estimate the probability (0 to 1) that the future state will occur. "
				"Be succinct in your analysis. "
				"It is advantageous for you to break down the task into smaller steps and estimate the probability of each step. "
				"Then, you can output a python eval() function with a proper argument in it with the probabilities of each step given you"
				"assume that each of the steps are almost entirely independent of each other. "
				"If you do this, do not include anything else in your response besides the python eval() function. For example eval('1 * 0.2 * 0.8 * 0.3 * 0.5 * 0.2') is a valid response. "
				"For example, if the task is to get a job offer from a top tech company, you can break down the task into the following steps: "
				"1. Get a degree in computer science "
				"2. Get relevant experience "
				"3. Apply to a top tech company "
				"4. Get an interview from a top tech company "
				"5. Pass each step of the interview process "
				"6. Get a job offer from a top tech company "
				"Then, you can estimate the probability of each step and output a python eval() function with a proper argument in it with the probabilities of each step given you"
				"assume that each of the steps are almost entirely independent of each other. "
				"Output your context between !<CONTEXT>! and !<\CONTEXT>!, then output your answer between !<ANSWER>! and !<\ANSWER>!. "
				"Any reasoning, assumptions, justifications, or steps that you believe are important to the task should be included in the context."
				"You must always include the !<CONTEXT>!...!<\CONTEXT>! and !<ANSWER>!...!<\ANSWER>! tags, even if the answer is a single number.\n"
				f"Current state: {current_state}\nTarget state: {target_state}"
			)
		
		# Extract messages from kwargs if provided, otherwise None
		messages = kwargs.pop("messages", None)
		
		# If no messages provided, create a default message with the prompt
		if not messages:
			messages = [{"role": "user", "content": prompt}]
		
		# Select model name based on model type (reasoning or basic)
		model = self.reasoning_model_name if model_type == ModelType.REASONING else self.basic_model_name
		
		# Make API call to Groq with selected model and messages
		response = self._call_groq_with_retry(
			model=model,
			messages=messages,
			max_tokens=100000 if model_type == ModelType.REASONING else 5000,
			**kwargs
		)
		if response is None:
			logging.error("Groq API call failed after retries.")
			return None

		# If response_file was provided but didn't exist, write the response to it
		if response_file:
			try:
				with open(response_file, 'w') as f:
					f.write(response.choices[0].message.content.strip())
			except Exception as e:
				print(f"Error writing response to file: {e}")
		
		# Extract and clean the response content
		content = response.choices[0].message.content.strip()
		
		# Parse the response into context, answer, reasoning, and think components
		context, answer, reasoning, think = self._parse_groq_response(content)
		
		# Return structured response dictionary
		return {"context": context, "answer": answer, "reasoning": reasoning, "think": think, "raw_response": content}
