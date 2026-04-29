import os

api_key = os.environ.get("API_KEY")
from litellm import completion
import os

os.environ["MISTRAL_API_KEY"] = api_key
system_prompt = 'You are a mathematical genius. You can only respond with one of two formats: one for calling tools: {"state": "tool", "tool_name": "tool", "tool_args": {"a": x, "b": y} } or one for stating an answer: {"state": "final", "final_answer": "blah blah blah"} Respond only in JSON'
user_prompt = 'Hello, how are you?'
response = completion(
  model="mistral/mistral-tiny",
  messages=[{"role": "user", "content": f"System Prompt: {system_prompt} Prompt: {user_prompt}"}]
)
print(response.choices[0].message.content)