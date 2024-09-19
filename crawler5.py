import requests
from bs4 import BeautifulSoup
import csv
import queue
import re
from threading import Thread

# initialize the data structure where to
# store the scraped data
products = []

def queue_worker(i, urls, visited_urls):
    while not urls.empty() and visited_urls.qsize() < 50:

        _, current_url = urls.get()

        response = requests.get(current_url)
        soup = BeautifulSoup(response.content, "html.parser")

        # mark the current URL as visited
        visited_urls.put(current_url)

        link_elements = soup.select("a[href]")
        for link_element in link_elements:
            url = link_element['href']
            # if the URL is relative to scrapingcourse.com or
            # any of its subdomains
            if re.match(r"https://(?:.*\.)?scrapingcourse\.com", url):
                # if the URL discovered is new
                if url not in [item for item in visited_urls.queue] and url not in [item[1] for item in urls.queue]:
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

        urls.task_done()

urls = queue.PriorityQueue()
urls.put((0.5, "https://www.scrapingcourse.com/ecommerce/"))

visited_urls = queue.Queue()

num_workers = 4

for i in range(num_workers):
    Thread(target=queue_worker, args=(i, urls, visited_urls), daemon=True).start()
urls.join()

# initialize the CSV output file
with open('products5.csv', 'w') as csv_file:
    writer = csv.writer(csv_file)

    # populating the CSV
    for product in products:
        writer.writerow(product.values())
