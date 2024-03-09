from web_scraper_helper import *
import asyncio
import aiohttp

all_urls_count = 0
count = 1

def show_progress():
    global count
    print(f"[{round((count / all_urls_count) * 100, 2)}%] done")
    count += 1

async def get_subcategory_products(current_page: str, session: aiohttp.ClientSession):
    
    async with session.get(current_page) as response:

        if response.status != 200:
            print(f'Error getting a response from {current_page}.')
            exit()

        html = await response.text()

        products_html = BeautifulSoup(html, 'html.parser')

        # Searches the html content for names
        names_list = get_list_from_html('div', 'name', products_html)

        # Gets rid of root 'Tootevalik', category and subcategory
        names_list = names_list[3:]

        # Searches the html content for prices
        prices_list = get_list_from_html('div', 'js-info-price', products_html)

        # Remove newline character and 'tk' and add comma between numbers
        for i, price in enumerate(prices_list):
            prices_list[i] = price[:-4].replace('\n', ',')
        
        # Save a list of dictionaries
        subcategory_products = [{"name": name, "price": price} for name, price in zip(names_list, prices_list)]

        show_progress()

        return subcategory_products

async def main(urls: list):
    async with aiohttp.ClientSession() as session:
        
        # Use a single session for connection pooling
        tasks = [get_subcategory_products(url, session) for url in urls]
        
        # Wait for all coroutines to finish
        results = await asyncio.gather(*tasks)
        
        return results

if __name__ == '__main__':
    
    file = 'products.json'

    # Check if the file with products already exists
    if os.path.exists(file) and cmp_dates(file):
            print('File exists and dates are the same.')
            exit()
    # Only create a file if it doesnt exist and the date is different
    else:
        urls = get_urls('urls.json')

        # Keep track of progress
        all_urls_count = len(urls)

        data = asyncio.run(main(urls))

        save_json(file, data)