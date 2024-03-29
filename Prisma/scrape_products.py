from web_scraper_helper import *
from fetch_urls import fetch_urls

async def get_products_from_html(html):
    products_html = BeautifulSoup(html, 'html.parser')

    names_list = get_list_from_html('div', 'name', products_html)

    # Gets rid of root 'Tootevalik', category and subcategory
    names_list = names_list[3:]

    print(f'All products on link {get_products_total(products_html)}')
    print(f'Products per page {len(names_list)}') 

    subnames_list = get_list_from_html('span', 'subname', products_html)

    prices_list = get_list_from_html('div', 'js-info-price', products_html)

    # Remove newline character and 'tk' and add comma between numbers
    for i, price in enumerate(prices_list):
        prices_list[i] = price[:-4].replace('\n', ',')
    
    # Save a list of dictionaries
    subcategory_products = [{"name": name, "subname": subname, "price": price} for name, subname, price in zip(names_list, subnames_list, prices_list)]
    
    return subcategory_products

async def get_page_products(current_page: str, session: aiohttp.ClientSession, progress: Bar):
    
    try:
        async with session.get(current_page) as response:

            if response.status != 200:
                print(f'Error at {current_page} status: {response.status}.')
                raise aiohttp.ClientResponseError
            else:
                print(f'Successfull connection to {current_page}.')

            html = await response.text()

    except aiohttp.ClientResponseError as e:
        print(f'Error in connection: {str(e)}')
        return None

    else:
        products = await get_products_from_html(html)

    finally: 
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