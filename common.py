import os.path
import datetime
import time
import json

# Compares current date with file creation date
# If both match, return true, otherwise false
def cmp_dates(file_name: str) -> bool:
    file_creation_time = os.path.getctime(file_name)
    file_creation_time = datetime.datetime.fromtimestamp(file_creation_time)
    file_creation_date = file_creation_time.date()

    current_date = datetime.date.today()
    
    if current_date == file_creation_date:
         return True
    
    return False

def save_json(file_path, all_products):
    with open(file_path, 'w') as products:
        json.dump(all_products, products, indent=4)

# Load data from JSON file as dictionary
def load_json(file_path) -> list:
    with open(file_path, 'r') as file:
        return json.load(file)