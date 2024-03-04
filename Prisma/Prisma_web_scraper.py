from bs4 import BeautifulSoup
import requests
import os.path
import datetime

def make_category_url_dict(current_page: str) -> BeautifulSoup:
    selection_page = requests.get(current_page)

    selection_html = BeautifulSoup(selection_page.text, 'html.parser')

    # Getting category names
    categories = selection_html.find_all('a', class_ = 'name js-category-item')
    categories_list = [category.text for category in categories]

    # Getting links to these categories
    links_list = [link.get('href') for link in categories]
    base_link = 'https://www.prismamarket.ee'
    links_list = [base_link + link for link in links_list]

    # Prisma website urls for each subcategory
    categories_urls = dict(zip(categories_list, links_list))

    return categories_urls

def append_subcategory_products(output_file, current_page: str, subcategory: str):
    products = requests.get(current_page)

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

    # Createa a list of tuples with a name and a price of the product
    products = list(zip(names_list, prices_list))

    # Save the pairs of name-price to file
    for product in products:
        output_file.write(str(product) + '\n')

def cmp_dates(file_name: str) -> bool:
    file_creation_time = os.path.getctime(file_name)
    file_creation_time = datetime.datetime.fromtimestamp(file_creation_time)

    current_day = datetime.date.today()
    if current_day.year != file_creation_time.year or \
       current_day.month != file_creation_time.month or \
       current_day.day != file_creation_time.day:
        return False
    
    return True

file = 'Prisma_products.txt'

# Check if the file with products already exists
if os.path.exists(file):
    if cmp_dates(file):
        print('File exists and dates are the same.')
        exit()
# Only create a file if it doesnt exist and the date is different
else:

    prisma_products = open(file, 'w')

    # Prisma website product selection
    prisma_selection = 'https://www.prismamarket.ee/products/selection'

    categories_urls = make_category_url_dict(prisma_selection)

    # Search each category for a subcategory
    for category, url in categories_urls.items():
        #print(f"{category}: {url}") # Debug
        subcategories_urls = make_category_url_dict(url)
        for subcategory, sub_url in subcategories_urls.items():
            #print(f"{subcategory}: {sub_url}") # Debug
            append_subcategory_products(prisma_products, sub_url, subcategory)
        #print()
            
    prisma_products.close()