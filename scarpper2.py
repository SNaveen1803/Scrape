import csv
from bs4 import BeautifulSoup
import requests

def get_asin(soup):
    try:
        asin = soup.find("th", string="ASIN").find_next_sibling("td").text.strip()
    except AttributeError:
        asin = ""
    return asin

def get_description(soup):
    try:
        description = soup.find("div", attrs={'id':'productDescription'}).text.strip()
    except AttributeError:
        description = ""
    return description

def get_manufacturer(soup):
    try:
        manufacturer = soup.find("a", attrs={'id':'bylineInfo'}).text.strip()
    except AttributeError:
        manufacturer = ""
    return manufacturer

if __name__ == '__main__':

    Product_URL = []
    with open('products.csv', newline='', encoding='utf-8-sig') as csvfile:
        data = csv.DictReader(csvfile)
        for r in data:
            Product_URL.append(r['Product URL'])
    
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
        'Accept-Language': 'en-US, en;q=0.5'
    }

    for url in Product_URL:

        webpage = requests.get(url, headers=HEADERS)

        soup = BeautifulSoup(webpage.content, "lxml")

        print("ASIN =", get_asin(soup))
        print("Product Description =", get_description(soup))
        print("Manufacturer =", get_manufacturer(soup))
        print()
        print()
