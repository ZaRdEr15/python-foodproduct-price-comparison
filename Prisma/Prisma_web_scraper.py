from bs4 import BeautifulSoup
import requests
import os.path
import datetime
import json

all_products = []

def append_subcategory_products(current_page: str, session: requests.Session):
    products = session.get(current_page)

    products_html = BeautifulSoup(products.text, 'html.parser')

    # Searches the html content for names
    names = products_html.find_all('div', class_ = 'name')
    names_list = [name.text for name in names]

    # Gets rid of root 'Tootevalik', category and subcategory
    names_list = names_list[3:]

    # Searches the html content for prices
    prices = products_html.find_all('div', class_ = 'js-info-price')
    prices_list = [price.text for price in prices]

    # Remove newline character and 'tk' and add comma between numbers
    for i, price in enumerate(prices_list):
        prices_list[i] = price[:-4].replace('\n', ',')

    # Save JSON objects to file
    subcategory_products = [{"name": name, "price": price} for name, price in zip(names_list, prices_list)]
    all_products.append(subcategory_products)

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
    
def get_urls_count(urls: dict) -> int:
    count = 0
    for category in urls.values():
            for url in category.values():
                count += 1
    return count

file = 'Prisma_products.json'

# Check if the file with products already exists
if os.path.exists(file) and cmp_dates(file):
        print('File exists and dates are the same.')
        exit()

# Only create a file if it doesnt exist and the date is different
else:

    with open(file, 'w') as prisma_products:

        # Use a single session to reduce requests time
        session = requests.Session()

        urls = load_json('Prisma_categories.json')

        # Keep track of progress
        all_urls_count = get_urls_count(urls)
        i = 0

        for category in urls.values():
            for url in category.values():
                append_subcategory_products(url, session)
            i += len(category)
            print(f"[{round((i / all_urls_count) * 100, 2)}%] done")

        json.dump(all_products, prisma_products, indent=4)