import requests
from bs4 import BeautifulSoup
from .add_prodcut import AddProduct
from random import randint
from time import sleep


def scrape_amazon(url, perc, store, cate, sous_category, maxVal, more, less):
    headers = {
        'dnt': '1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-user': '?1',
        'sec-fetch-dest': 'document',
        'referer': 'https://www.amazon.com/',
        'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
    }

    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.content, 'html5lib')
    products = []
    tab = soup.findAll('div', attrs={"data-component-type": "s-search-result"})
    
    for prod in tab:
        
        tmp = {'photo': prod.find('img')['src'], 'full_name': str(prod.find(class_='a-text-normal').text.strip())}
        link = prod.find(class_='a-link-normal')['href']
        
        if "https://www.amazon.com" in link:
            tmp['original_link'] = link
        else:
            tmp['original_link'] = "https://www.amazon.com" + link
        try:
            tmp['price'] = (int(prod.find(class_='a-price-whole').text.strip().replace(".", ""))+1) * perc
        except:
            continue
        try:
            brand = prod.find('div', class_='a-color-secondary').text.strip()
            if 'by' in brand:
                tmp['brand'] = brand.split("by")[-1].strip()
            else:
                tmp['brand'] = ""
        except:
            tmp['brand'] = ""
        try:
            if float(prod.find('i',
                               class_=['a-icon', 'a-icon-star-small', 'a-star-small-5', 'aok-align-bottom']).text.split(" ")[0]) > 4.5:
                tmp['staff_pick'] = True
            else:
                tmp['staff_pick'] = False
        except:
            tmp['staff_pick'] = False
        try:
            tmp['description'] = get_descibtion(tmp['original_link'])
        except:
            tmp['description'] = ""
        AddProduct(tmp, store, cate, sous_category, maxVal, more, less)
        sleep(randint(15,30))
        


def get_descibtion(url):
    headers = {
        'dnt': '1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-user': '?1',
        'sec-fetch-dest': 'document',
        'referer': 'https://www.amazon.com/',
        'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
    }
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.content, 'html5lib')
    li = soup.find(id='feature-bullets')
    desc = []
    for i in li.findAll(class_='a-list-item'):
        desc.append(i.text.strip())
    return "\n".join(desc)
