from bs4 import BeautifulSoup
import os.path
import datetime
import json
from progress.bar import Bar
from progress.spinner import Spinner
import asyncio
import aiohttp

def next_page(url: str) -> str:
    page_prefix = '/page/'
    prefix_offset = 6
    if page_prefix in url:
        num_pos = url.index(page_prefix) + prefix_offset
        number = int(url[num_pos:]) + 1
        url = url[:num_pos] + str(number)
    else:
        url += page_prefix + '2'
    return url

def get_products_total(soup: BeautifulSoup):
    amount_of_products = soup.find_all('b')
    amount_of_products = int(amount_of_products[1].text)
    return amount_of_products

def get_products_list(tag: str, attribute: str, html_data: BeautifulSoup) -> list:
    result = html_data.find_all(tag, class_ = attribute)
    products = [construct_product(product) for product in result]
    return products

def construct_product(result_data):
    name = result_data.find('div', class_ = 'name').text
    subname = result_data.find('span', class_ = 'subname')
    subname = None if subname is None else subname.text # Not every product contains 'subname'
    price = result_data.find('div', class_ = 'js-info-price').text
    price = price[:-4].replace('\n', ',') # Remove newline character and 'tk' and add comma between numbers
    return {"name": name, "subname": subname, "price": price}

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

# Load data from JSON file as dictionary
def load_json(file_path) -> list:
    with open(file_path, 'r') as file:
        return json.load(file)
    
# Get urls from JSON file
def get_urls_and_len(file_path):
    urls = load_json(file_path)
    return urls, len(urls)
    
def save_json(file_path, all_products):
    with open(file_path, 'w') as products:
        json.dump(all_products, products, indent=4)