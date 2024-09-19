import requests
from bs4 import BeautifulSoup
import csv


# initialize the data structure where to
# store the scraped data
products = []
urls = ["https://www.scrapingcourse.com/ecommerce/"]
# to store the pages already visited
visited_urls = []

while len(urls) != 0:

    print(f"urls = {urls}")
    print()
    print(f"visited_urls = {visited_urls}")
    print()
    current_url = urls.pop()

    response = requests.get(current_url)
    soup = BeautifulSoup(response.content, "html.parser")

    # mark the current URL as visited
    visited_urls.append(current_url)

    link_elements = soup.select("a[href]")
    for link_element in link_elements:
        url = link_element['href']
        if "https://www.scrapingcourse.com/ecommerce/" in url:
            # if the URL discovered is new
            if url not in visited_urls and url not in urls:
                urls.append(url)

    # if current_url is product page
    if(soup.select_one(".price")):
        product = {}
        product["url"] = current_url
        product["image"] = soup.select_one(".wp-post-image")
        product["name"] = soup.select_one(".product_title")
        product["price"] = soup.select_one(".price")

        products.append(product)
    
    if(len(products) == 10):
        break

# initialize the CSV output file
with open('products.csv', 'w') as csv_file:
    writer = csv.writer(csv_file)

    # populating the CSV
    for product in products:
        writer.writerow(product.values())