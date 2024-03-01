from bs4 import BeautifulSoup
import requests

# Testing Prisma website Liha - Hakkliha subcategory
url = 'https://www.prismamarket.ee/products/19273'

page = requests.get(url)

soup = BeautifulSoup(page.text, 'html.parser')

names   = soup.find_all('div', class_ = 'name')
names_list = [name.text for name in names]

# Gets rid of root 'Tootevalik', category 'Liha' and subcategory 'Hakkliha'
names_list = names_list[3:]

prices  = soup.find_all('div', class_ = 'js-info-price')
prices_list = [price.text for price in prices]

for i, price in enumerate(prices_list):
    prices_list[i] = price[:-4].replace('\n', ',')

print(prices_list)