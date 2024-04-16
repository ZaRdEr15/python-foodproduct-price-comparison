import json

shops = ['Prisma']

shop_products = shops[0] + '/data/products.json'

with open(shop_products, 'r') as search_file:
    json_data = json.load(search_file)

while(True):
    search_phrase = input('Enter a search phrase: ')
    search_phrase = search_phrase.lower()

    found = 0
    column_width = 50

    # Search Prisma JSON data file for search phrase matches
    for object in json_data:
        name    =   object['name']
        price   =   object['price']
        if search_phrase in name.lower():
            found += 1
            print(f'{name:<120}| {price:>6}€ -> {shops[0]}')

    # When searching is finished, show amount of results
    print()
    if found:
        print(f'{found} results found.')
    else:
        print('No results match the search phrase.')

