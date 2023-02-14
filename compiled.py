import requests
from bs4 import BeautifulSoup
import json
from threading import Thread 

data = []
threads = []
pages = ["https://smpnutra.com/product-category/stock-private-label-supplements", "https://smpnutra.com/product-category/stock-private-label-supplements/page/2", "https://smpnutra.com/product-category/stock-private-label-supplements/page/3", "https://smpnutra.com/product-category/stock-private-label-supplements/page/4", "https://smpnutra.com/product-category/stock-private-label-supplements/page/5", "https://smpnutra.com/product-category/stock-private-label-supplements/page/6"]

# Request the website HTML content
url = "https://smpnutra.com/product-category/stock-private-label-supplements/page/4"
HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36', "Upgrade-Insecure-Requests": "1","DNT": "1","Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8","Accept-Language": "en-US,en;q=0.5","Accept-Encoding": "gzip, deflate"}
# response = requests.get(url)
# soup = BeautifulSoup(response.content, 'html.parser')

def scrap(link):
    if link[0] == '/':
        link = url + link
    try:
        response = requests.get(link, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36', "Upgrade-Insecure-Requests": "1","DNT": "1","Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8","Accept-Language": "en-US,en;q=0.5","Accept-Encoding": "gzip, deflate"})
        soup = BeautifulSoup(response.text, "html.parser")
    except:
        print("ERR")
        return
    return soup

def productPage(url):
    obj = {}
    soup = scrap(url)
    obj['name'] = soup.find('h2', attrs={'class' : 'product_title entry-title'}).text
    obj['link'] = url
    obj['sku'] = ''
    try:
        tableDiv = soup.find('div', attrs={'class':'woocommerce-product-details__short-description'})
        tr = tableDiv.find_all('tr')[0]
        td = tr.find_all('td')[-1].text
        obj['sku'] = td
    except:
        pass
    print(obj)
    data.append(obj)

def getAllLinks():
    for page in pages:
        soup = scrap(url)
        # print(productPage(testURL))
        for link in soup.findAll('a', attrs={'class' : 'man_product_photo_link'}):
            threads.append(Thread(target=productPage, args=(link["href"],)))
            # productPage(link['href'])
    for thread in threads:
        thread.start()
    for thread in threads:
            thread.join()
    with open('compiled.json', 'a+') as f:
        json.dump(data, f)
    print("END")

getAllLinks()