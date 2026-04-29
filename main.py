#trying to figure out what code my transpiler should create! :)
import os
from typing import Literal
from pydantic import BaseModel, ConfigDict, ValidationError
from litellm import completion
import os
import json 
api_key = os.environ.get("API_KEY")
os.environ["MISTRAL_API_KEY"] = api_key
system_prompt = 'You are a mathematical genius. You can only respond with one of two formats: one for calling tools: {"state": "tool", "tool_name": "tool", "tool_args": {"a": x, "b": y} } or one for stating an answer: {"state": "final", "final_answer": "blah blah blah"} Respond only in JSON'
user_prompt = 'Hello, how are you?'
response = completion(
  model="mistral/mistral-tiny",
  messages=[{"role": "user", "content": f"System Prompt: {system_prompt} Prompt: {user_prompt}"}]
)
response = response.choices[0].message.content
data = json.loads(response[7:-3].strip())
class LLMResponse(BaseModel): #validating llm output ... how do i run it through lol
    state: Literal['tool', 'final']
try:
  LLMResponse.model_validate(data)  
except ValidationError as e:
  print(e)