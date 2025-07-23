import json

with open('data/telegram_full/result.json') as f:
    full_chat = json.load(f)
    
print(full_chat["messages"])