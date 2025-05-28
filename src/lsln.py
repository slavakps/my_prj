import json

with open("data/operations.json") as f:
    data = json.load(f)

print(data)
