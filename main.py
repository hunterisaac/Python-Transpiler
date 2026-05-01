#trying to figure out what python code my transpiler should create! :)
import os
from typing import Literal, Union
from pydantic import BaseModel, ConfigDict, ValidationError, Field
from litellm import completion
import os
import json 
api_key = os.environ.get("API_KEY")
os.environ["MISTRAL_API_KEY"] = api_key

system_prompt = 'You are a mathematical genius. You can only respond with one of two formats: one for calling tools: {"state": "tool", "tool_name": "tool", "tool_args": {"a": x, "b": y} } or one for stating an answer: {"state": "final", "final_answer": "blah blah blah"} Respond only in JSON'
user_prompt = 'Hello, how are you?'

message_history = [{"role": "system", "content": system_prompt}, {"role": "user", "content": user_prompt}]
#Storing tool calls using decorators
tool_list = []

def tool(func):
   tool_list.append({'tool_name': func.__name__, 'description': func.__doc__, 'function': func  }) #stores with tool name, desecription, and the callable function.
@tool
def add(numbers):
   """Tool to add all # in a dict"""
   total = 0
   for x in numbers:
      total += numbers[x]
   return total
@tool
def subtract(numbers):
   """Tool to subtract all # in a dict"""
   total = 0
   for x in numbers:
      total -= numbers[x]
   return total


      
#Executing Tool Calls
#Registering tool calls
class ToolResponse(BaseModel):
    state: Literal['tool']
    tool_name: str
    tool_args: dict
class FinalResponse(BaseModel):
    state: Literal['final']
    final_answer: str
class LLMResponse(BaseModel):
    response_type: Union[ToolResponse, FinalResponse] = Field(discriminator='state')
while True:
  response = completion(
    model="mistral/mistral-tiny",
    messages=message_history
  )
  response = response.choices[0].message.content
  message_history.append({"role":"assistant", "content": response})
  print(message_history)
  try:
    amount_chars = len(response) #getting json
    start_index = response.index("{") 
    end_index = response.rfind("}", start_index, amount_chars)
    data = json.loads(response[start_index:end_index+1])
    try:
      response = LLMResponse(response_type=data)
      result = response.response_type #need to extract data from response
      if result.state == "final":
        print(result.final_answer)
        break
      if result.state =="tool":
         
    except ValidationError as e:
      message_history.append({"role": "system", "content": e})
  except Exception as e:
     message_history.append({"role": "system", "content": "Invalid JSON"})

  
  