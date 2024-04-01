from web_scraper_helper import *
from fetch_urls import fetch_urls

async def collect_products(html: BeautifulSoup, products_left: int, url: str, session: aiohttp.ClientSession):

    # Save a list of dictionaries
    products = get_products_list('div', 'info relative clear', html)
    
    products_per_page = len(products)

    # If more products left, open next page, scrape products until all are done, append to the end of the list
    if products_left > products_per_page:
        products_left -= products_per_page
        url = next_page(url)
        async with session.get(url) as response:

            if response.status != 200:
                print(f'Error at {url} status: {response.status}.')
                raise aiohttp.ClientResponseError

            html = await response.text()
            html = BeautifulSoup(html, 'html.parser')
            add_products = await collect_products(html, products_left, url, session)
            products.extend(add_products)

    return products

async def get_products_from_html(html, url: str, session: aiohttp.ClientSession):
    products_html = BeautifulSoup(html, 'html.parser')

    all_products_count = get_products_total(products_html)

    # Collect products and open new url pages if not all products collected
    products = await collect_products(products_html, all_products_count, url, session)

    return products
    

async def get_page_products(current_page: str, session: aiohttp.ClientSession, progress: Bar):
    
    try:
        async with session.get(current_page) as response:

            if response.status != 200:
                print(f'Error at {current_page} status: {response.status}.')
                raise aiohttp.ClientResponseError

            html = await response.text()
            products = await get_products_from_html(html, current_page, session)

    except aiohttp.ClientResponseError as e:
        print(f'Error in connection: {str(e)}')
        return None
        
    progress.next()

    return products

async def main(urls: list, progress):
    async with aiohttp.ClientSession() as session:
        
        # Use a single session for connection pooling
        tasks = [get_page_products(url, session, progress) for url in urls]
        
        # Wait for all coroutines to finish
        results = await asyncio.gather(*tasks)
        
        return results

if __name__ == '__main__':
    
    products_file = 'data/products.json'
    urls_file = 'data/urls.json'

    # Check if the file with products already exists
    if os.path.exists(products_file) and cmp_dates(products_file):
            print('File exists and dates are the same.')
            exit()
    # Only create a file if it doesnt exist and the date is different
    else:
        # If urls file doesnt exist, fetch urls
        if not os.path.exists(urls_file):
            fetch_urls()
        urls, all_urls_count = get_urls_and_len(urls_file)

        progress = Bar('Collecting products', max=all_urls_count, suffix='%(percent)d%%')

        data = asyncio.run(main(urls, progress))

        # Flat out data, taking each product from the list of lists and
        # Putting into one list
        data = [product for sublist in data for product in sublist]

        progress.finish()
        print('Finished scraping products from Prisma')

        save_json(products_file, data)