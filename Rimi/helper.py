from bs4 import BeautifulSoup
import json
from progress.bar import Bar
from progress.spinner import Spinner
import asyncio
import aiohttp
import requests

def get_last_page() -> int:
    try:
        response = requests.get('https://www.rimi.ee/epood/ee/otsing?currentPage=1&pageSize=20&query=')
        response.raise_for_status()  # Raises an exception for unsuccessful responses
    except requests.exceptions.HTTPError as e:
        print(f"Error: {e}")
    
    html_content = BeautifulSoup(response.text, 'html.parser')

    result = html_content.find_all('a', {'data-page': True})

    print(result)
    
    return 1

get_last_page()