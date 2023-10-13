import os
import json

with open("models.json", "r", encoding='utf-8') as models_list:
        models = json.load(models_list)
        
os.remove(models['14'][-1])