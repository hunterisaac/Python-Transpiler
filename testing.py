tool_list = {}
def tool(func):
   tool_list[func.__name__] = {'description': func.__doc__, 'function': func} #stores with tool name, desecription, and the callable function.
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
