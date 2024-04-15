# Different food market online shops product and price scraping with a search made with Python3

## Python script to scrape food products (name and price) from websites (Prisma, Selver, etc) to compare prices.

### Reason

The reason for the project is that there are currently no sources available that would list products from different shops in Estonia and allow comparing same product's price in different shops.

One of the possible solutions is to just open all the resources, find the product you are looking for, mark down the prices, and decide which one should be the best shop to go to to save money. But, this takes time.

Upon first notice, this script scraping does take quite some time indeed, but in the future an automatic script running would be implemented to make it instantaneous.

### Made with

[aiohttp](https://pypi.org/project/aiohttp/) is used to asynchronously get html contents of the shop pages.
[BeautifulSoup](https://pypi.org/project/beautifulsoup4/) is used to scrape data from the html content.
[Progress](https://pypi.org/project/progress/) is used to indicate the current progress of scraping 

### Installation

Clone the repository to your system:

```sh
git clone https://github.com/ZaRdEr15/python-foodproduct-price-comparison.git
```

To install all necessary Python packages run the **install.sh** bash script:
```sh
./install.sh
```

### Usage

UPDATE LATER
Run the **search.py** file from the root to search for products:

```sh
python3 search.py
```

Example usage and output (for now):

```sh
Enter a search phrase: õun
Rukkitäistera leib, 310 g                                                       | LÕUNA PAGARID, Eesti     :   1,19€ -> Prisma
ÕUNATÄIDISEGA PONTŠIK                                                           | FAZER, Soome             :  16,99€ -> Prisma
Õunatäidisega pontšik                                                           | FAZER, Soome             :   1,59€ -> Prisma
Kõrvitsasai 300 g                                                               | LÕUNA PAGARID, Eesti     :   1,39€ -> Prisma
Õunasaiake                                                                      | RAINBOW, Soome           :   0,60€ -> Prisma
Õuna-kaneelitasku, 120 g                                                        | MARTA PAGAR, Eesti       :   1,49€ -> Prisma
Õunasaiake                                                                      | RAINBOW, Soome           :   0,60€ -> Prisma
Kohupiimataskud 250 g                                                           | LÕUNA PAGARID, Eesti     :   4,09€ -> Prisma
Tordipõhi 300 g                                                                 | LÕUNA PAGARID, Eesti     :   2,99€ -> Prisma
Moorapead, 165 g                                                                | LÕUNA PAGARID, Eesti     :   2,99€ -> Prisma
Õuna-laimi tort, laktoosivaba 700 g                                             | PAGARINI, Eesti          :  14,02€ -> Prisma
...
```

### Roadmap

Currently, data is scraped from:

- [x] Prisma
- [ ] Rimi
- [ ] Selver
- [ ] Maxima (Barbora)
- [ ] Coop

### License

Distributed under the MIT License. See LICENSE.txt for more information.
