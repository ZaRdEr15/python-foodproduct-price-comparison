from bs4 import BeautifulSoup
import requests
import json

def make_category_url_dict(current_page: str, session: requests.Session) -> dict:
    selection_page = session.get(current_page)

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

with open('Prisma_categories.json', 'w') as urls_file:

    # Prisma website product selection
    prisma_selection = 'https://www.prismamarket.ee/products/selection'

    # Use a single session to reduce requests time
    session = requests.Session()

    categories_urls = make_category_url_dict(prisma_selection, session)

    urls = {}

    # Search each category for a subcategory
    for category, category_url in categories_urls.items():
        subcategories_urls = make_category_url_dict(category_url, session)
        urls[category] = subcategories_urls

    json.dump(urls, urls_file, indent=4)