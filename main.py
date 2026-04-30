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

message_history = [system_prompt, user_prompt]
total_prompt = "System Prompt: " + system_prompt + "User Prompt:" + user_prompt
while True:
  response = completion(
    model="mistral/mistral-tiny",
    messages=[{"role": "user", "content": total_prompt}]
  )
  response = response.choices[0].message.content
  message_history.append(response)

  amount_chars = len(response) #getting json
  start_index = response.index("{") 
  end_index = response.rfind("}", start_index, amount_chars)
  data = json.loads(response[start_index:end_index+1])

  class ToolResponse(BaseModel):
    state: Literal['tool']
    tool_name: str
    tool_args: dict
  class FinalResponse(BaseModel):
    state: Literal['final']
    final_answer: str
  class LLMResponse(BaseModel):
      response_type: Union[ToolResponse, FinalResponse] = Field(discriminator='state')
  try:
    response = LLMResponse(response_type=data)
    result = response.response_type #need to extract data from response
    if result.state == "final":
      print(result.final_answer)
      break
  except ValidationError as e:
    print(e)
