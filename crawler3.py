import requests
from bs4 import BeautifulSoup
import csv
import queue
import re
import time


# initialize the data structure where to
# store the scraped data
products = []
urls = queue.PriorityQueue()
urls.put((0.5, "https://www.scrapingcourse.com/ecommerce/"))
# to store the pages already visited
visited_urls = []

while not urls.empty() and len(visited_urls) < 50:

    _, current_url = urls.get()

    response = requests.get(current_url)
    soup = BeautifulSoup(response.content, "html.parser")

    # mark the current URL as visited
    visited_urls.append(current_url)

    link_elements = soup.select("a[href]")
    for link_element in link_elements:
        url = link_element['href']
        if "https://www.scrapingcourse.com/ecommerce/" in url:
            # if the URL discovered is new
            if url not in visited_urls and url not in [item[1] for item in urls.queue]:
                # default priority score                
                priority_score = 1
                if re.match(r"^https://www.scrapingcourse\.com/ecommerce/page/\d+/?$", url):
                    priority_score = 0.5
                urls.put((priority_score, url))

    # if current_url is product page
    if(soup.select_one(".price")):
        product = {}
        product["url"] = current_url
        product["image"] = soup.select_one(".wp-post-image")
        product["name"] = soup.select_one(".product_title")
        product["price"] = soup.select_one(".price")

        products.append(product)

# initialize the CSV output file
with open('products.csv', 'w') as csv_file:
    writer = csv.writer(csv_file)

    # populating the CSV
    for product in products:
        writer.writerow(product.values())
