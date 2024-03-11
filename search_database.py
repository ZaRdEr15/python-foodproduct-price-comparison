import json

search_phrase = input('Enter a search phrase: ')
search_phrase = search_phrase.lower()

shop = 'Prisma'

shop_products = shop + '/data/products.json'

with open(shop_products, 'r') as search_file:
    json_data = json.load(search_file)

found = 0
column_width = 50

# Search Prisma JSON data file for search phrase matches
for object in json_data:
    name = object['name']
    subname = object['subname']
    price = object['price']
    if search_phrase in name.lower() or search_phrase in subname.lower():
        found += 1
        print(f'{name:<80}| {subname:<25}: {price:>6}€ -> {shop}')

# When searching is finished, show amount of results
print()
if found:
    print(f'{found} results found.')
else:
    print('No results match the search phrase.')

