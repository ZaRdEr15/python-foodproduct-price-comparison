import helper as wb
import sys, os
sys.path.append(os.path.abspath(os.pardir)) # Move up one directory to access common.py
import common
from fetch_urls import fetch_urls

# Collect all products from a single page
# If the amount of products collected is less than total,
# then open next page and repeat the process
async def collect_products(html: wb.BeautifulSoup, products_left: int, url: str, session: wb.aiohttp.ClientSession) -> list:

    # Save a list of dictionaries
    products = wb.get_products_list('div', 'info relative clear', html)
    
    products_per_page = len(products)

    #print(f'{url}: current: {products_per_page}, left: {products_left}') # Debug

    # If more products left, open next page, scrape products until all are done, append to the end of the list
    if products_left > products_per_page:
        products_left -= products_per_page
        url = wb.next_page(url)
        async with session.get(url) as response:

            if response.status != 200:
                print(f'Error at {url} status: {response.status}.')
                raise wb.aiohttp.ClientResponseError

            html = await response.text()
            html = wb.BeautifulSoup(html, 'html.parser')
            add_products = await collect_products(html, products_left, url, session)
            products.extend(add_products)

    return products

# Collect all products from a single page
# Get the total amount of all products on a single subcategory
# Returns all combined 
async def get_products_from_html(html, url: str, session: wb.aiohttp.ClientSession) -> list:
    products_html = wb.BeautifulSoup(html, 'html.parser')

    all_products_count = wb.get_products_total(products_html)

    # Collect products and open new url pages if not all products collected
    products = await collect_products(products_html, all_products_count, url, session)

    return products
    
# Get all products from a single subcategory
async def get_page_products(current_page: str, session: wb.aiohttp.ClientSession, progress: wb.Bar):
    
    try:
        async with session.get(current_page) as response:

            if response.status != 200:
                print(f'Error at {current_page} status: {response.status}.')
                raise wb.aiohttp.ClientResponseError

            html = await response.text()
            products = await get_products_from_html(html, current_page, session)

    except wb.aiohttp.ClientResponseError as e:
        print(f'Error in connection: {str(e)}')
        return None
        
    progress.next()

    return products

# Run the async functions to collect products
async def main(urls: list, progress):
    async with wb.aiohttp.ClientSession() as session:
        
        # Use a single session for connection pooling
        tasks = [get_page_products(url, session, progress) for url in urls]
        
        # Wait for all coroutines to finish
        results = await wb.asyncio.gather(*tasks)
        
        return results

if __name__ == '__main__':
    
    products_file = 'data/products.json'
    urls_file = 'data/urls.json'

    # Check if the file with products already exists
    if common.os.path.exists(products_file) and common.cmp_dates(products_file):
            print('File exists and dates are the same.')
            exit()
    # Only create a file if it doesnt exist and the date is different
    else:
        scrape_start = common.time.time()
        # If urls file doesnt exist, fetch urls
        if not common.os.path.exists(urls_file):
            fetch_urls()
        urls = common.load_json(urls_file)

        progress = wb.Bar('Collecting products', max=len(urls), suffix='%(percent)d%%')

        data = wb.asyncio.run(main(urls, progress))

        # Flat out data, taking each product from the list of lists and
        # Putting into one list
        data = [product for sublist in data for product in sublist]

        # Remove any duplicate elements
        data = wb.remove_duplicates(data)

        progress.finish()
        scrape_end = common.time.time()
        scrape_time = scrape_end - scrape_start
        print(f'Finished scraping products from Prisma. Took {scrape_time:.2f} s.')

        common.save_json(products_file, data)