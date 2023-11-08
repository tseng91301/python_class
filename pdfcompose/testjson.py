import json
text='{"name": "John", "age": 30, "city": "New York"}'
print(json.loads(text)['name'])