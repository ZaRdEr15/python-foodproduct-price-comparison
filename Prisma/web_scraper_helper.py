from bs4 import BeautifulSoup
import os.path
import datetime
import json

def get_list_from_html(tag: str, attribute: str, html_data: BeautifulSoup) -> list:
    result = html_data.find_all(tag, class_ = attribute)
    return [item.text for item in result]

def cmp_dates(file_name: str) -> bool:
    file_creation_time = os.path.getctime(file_name)
    file_creation_time = datetime.datetime.fromtimestamp(file_creation_time)
    file_creation_date = file_creation_time.date()

    current_date = datetime.date.today()
    
    if current_date == file_creation_date:
         return True
    
    return False

# Load data from JSON file as dictionary
def load_json(file_path) -> dict:
    with open(file_path, 'r') as file:
        return json.load(file)
    
# Get urls from JSON file
def get_urls(file_path) -> list:
    data_json = load_json(file_path)
    urls = []
    for category in data_json.values():
            for url in category.values():
                urls.append(url)
    return urls
    
def save_json(file_path, all_products):
    with open(file_path, 'w') as prisma_products:
        json.dump(all_products, prisma_products, indent=4)

