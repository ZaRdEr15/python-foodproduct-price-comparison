from bs4 import BeautifulSoup
import json
from progress.bar import Bar
from progress.spinner import Spinner
import asyncio
import aiohttp

# Switch to the next possible page in the subcategory
# If on the first page, add /page/2, otherwise increase page
# Returns next page url
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

# Get total amoun of products from the subcategory page
def get_products_total(soup: BeautifulSoup) -> int:
    amount_of_products = soup.find_all('b')
    amount_of_products = int(amount_of_products[1].text)
    return amount_of_products

# Get a list of all products from the single page
def get_products_list(tag: str, attribute: str, html_data: BeautifulSoup) -> list:
    result = html_data.find_all(tag, class_ = attribute)
    products = [construct_product(product) for product in result]
    return products

# Construct a dictionary with "name" and "price" keys
# Name can have a subname inside if present
def construct_product(result_data) -> dict:
    name = result_data.find('div', class_ = 'name').text
    subname = result_data.find('span', class_ = 'subname')
    # Combine name with subname
    if subname is not None: # Not every product contains 'subname'
        name = name + ' ' + subname.text
    price: str = result_data.find('div', class_ = 'js-info-price').text
    price = price.replace('\n', ',') # Remove newline character and add comma between numbers (keep tk/kg)
    price = price[:-4] + price[len(price) - 3:] # Remove last comma (12,99,/tk)
    return {"name": name, "price": price}

# Removes duplicate dictionaries inside the list if both name and price match
# BUT it needs more testing to make sure
# The returned list will be unorganized making testing harder!
def remove_duplicates(data: list) -> list:
    unique_data = {tuple(d.values()) for d in data}
    return [{"name": item[0], "price": item[1]} for item in unique_data]