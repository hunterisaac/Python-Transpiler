import os

api_key = os.environ.get("API_KEY")
from litellm import completion
import os

os.environ["MISTRAL_API_KEY"] = api_key

response = completion(
  model="mistral/mistral-tiny",
  messages=[{"role": "user", "content": "Hello, how are you?"}]
)
print(response.choices[0].message.content)