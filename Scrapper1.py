from bs4 import BeautifulSoup
import requests
import csv

def get_title(soup):
    try:
        title = soup.find("span", attrs={"id": 'productTitle'})
        title_value = title.string
        title_string = title_value.strip()
    except AttributeError:
        title_string = ""
    return title_string

def get_price(soup):
    try:
        price = soup.find("span", attrs={'id': 'priceblock_ourprice'}).string.strip()
    except AttributeError:
        try:
            price = soup.find("span", attrs={'id': 'priceblock_dealprice'}).string.strip()
        except:
            price = ""
    return price

def get_rating(soup):
    try:
        rating = soup.find("i", attrs={'class': 'a-icon a-icon-star a-star-4-5'}).string.strip()
    except AttributeError:
        try:
            rating = soup.find("span", attrs={'class': 'a-icon-alt'}).string.strip()
        except:
            rating = ""
    return rating

def get_review_count(soup):
    try:
        review_count = soup.find("span", attrs={'id': 'acrCustomerReviewText'}).string.strip()
    except AttributeError:
        review_count = ""
    return review_count

if __name__ == '__main__':
    
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
        'Accept-Language': 'en-US'
    }

    base_url = "https://www.amazon.in/s?k=bags&page="

    num_pages = 20

    product_details = []

    for page in range(1, num_pages + 1):

        url = base_url + str(page) + "&crid=2M096C61O4MLT&qid=1688575837&sprefix=ba%2Caps%2C283&ref=sr_pg_" + str(page)

        webpage = requests.get(url, headers=HEADERS)

        soup = BeautifulSoup(webpage.content, "lxml")

        containers = soup.find_all("div", class_="sg-col-inner")

        for container in containers:
            
            link = container.find("a", class_="a-link-normal s-no-outline")
            if link:
                product_url = "https://www.amazon.in" + link["href"]

                product_webpage = requests.get(product_url, headers=HEADERS)
                product_soup = BeautifulSoup(product_webpage.content, "lxml")

                product_name = get_title(product_soup)
                product_price = get_price(product_soup)
                rating = get_rating(product_soup)
                review_count = get_review_count(product_soup)

                product_details.append([product_url, product_name, product_price, rating, review_count ])

    with open('products.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Product URL','Product Name', 'Product Price', 'Rating', 'Number of reviews']) 

        for detail in product_details:
            writer.writerow(detail)

    print("Product details saved in products.csv file.")
