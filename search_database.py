search_phrase = input('Enter a search phrase: ')

shop = 'Prisma'

prisma_products = 'Prisma/Prisma_products.txt'

with open(prisma_products, 'r') as search_file:
    for index, line in enumerate(search_file):
        if search_phrase in line:
            print(f"{line} -> {shop}")

