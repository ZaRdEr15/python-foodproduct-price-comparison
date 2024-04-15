import Prisma.helper as wb

async def get_urls_list(current_page: str, session: wb.aiohttp.ClientSession, progress: wb.Spinner) -> list:
    
    try:
        async with session.get(current_page) as response:
            
            if response.status != 200:
                raise wb.aiohttp.ClientResponseError

            html = await response.text()

            selection_html = wb.BeautifulSoup(html, 'html.parser')

            # Getting category names
            categories = selection_html.find_all('a', class_ = 'name js-category-item')

            # Getting links to these categories
            links_list = [link.get('href') for link in categories]
            base_link = 'https://www.prismamarket.ee'
            links_list = [base_link + link for link in links_list]

            progress.next()

            return links_list
        
    except wb.aiohttp.ClientResponseError as e:
        print(f"Error fetching {current_page}: {e}")
        return None

async def main(main_page: str, progress: wb.Spinner):

    # Use a single session for connection pooling to reduce requests time
    async with wb.aiohttp.ClientSession() as session:

        # Get categories urls list
        categories_urls = await get_urls_list(main_page, session, progress)
        
        # Get subcategories urls list
        tasks = [get_urls_list(category_url, session, progress) for category_url in categories_urls]
        
        # Wait for all coroutines to finish
        results = await wb.asyncio.gather(*tasks)
        
        return results

def fetch_urls():
    # Prisma website product selection
    prisma_selection = 'https://www.prismamarket.ee/products/selection'

    progress = wb.Spinner('Fetching urls ')

    subcategories_urls = wb.asyncio.run(main(prisma_selection, progress))

    progress.finish()

    # Flat out data, taking each url from the list of lists and
    # Putting into one list
    urls = [url for subcategory in subcategories_urls for url in subcategory]

    with open('data/urls.json', 'w') as urls_file:
        wb.json.dump(urls, urls_file, indent=4)
