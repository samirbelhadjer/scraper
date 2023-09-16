from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import  By
from selenium.webdriver.chrome.service import Service 
from webdriver_manager.core.utils import ChromeType
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.expected_conditions import staleness_of




from webdriver_manager.chrome import ChromeDriverManager
import os

from .add_prodcut import AddProduct
from random import randint

def get_price(price):
    print('inside get price')
    price = price.replace(',','.')
    split_price = price.split('.')
    if len(split_price) > 2 :
        befor_comma = ''.join(split_price[:-1])
        string_price =befor_comma +'.' +split_price[-1] 
        return string_price
    else :
        return price


def scrap_aliexpress(url, perc, store, cate, maxVal, more, less):
    chrome_options = webdriver.ChromeOptions()
    

    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--disable-dev-shm-using") 
    chrome_options.add_argument("--disable-extensions") 
    chrome_options.add_argument("--disable-gpu") 

    homedir = os.getcwd()
    print('---->',homedir)
    webdriver_service = Service(homedir+"\\product\\scripts\\chromedriver_win32\chromedriver.exe")

    driver = webdriver.Chrome(chrome_options=chrome_options, service=webdriver_service)
    driver.get(url)

    wait = WebDriverWait(driver, 20)
    driver.get(url)

    try:
        wait.until(EC.element_to_be_clickable((By.XPATH, "//div[contains(@style,'display: block')]//img[contains(@src,'TB1')]"))).click()
    except:
        pass

    try:
        wait.until(EC.element_to_be_clickable((By.XPATH, "//img[@class='_24EHh']"))).click()
    except:
        pass

    
    try : 
        cookies = driver.find_element(By.CSS_SELECTOR, '#gdpr-new-container > div > div.global-gdpr-btn-wrap > button:nth-child(2)')
        cookies.click()
    except : 
        pass


    language = driver.find_element(By.CSS_SELECTOR, '#switcher-info')
    ActionChains(driver).move_to_element(language).click(language).perform()
    sleep(1)
    language = driver.find_element(By.CSS_SELECTOR, '#nav-global > div.ng-item-wrap.ng-item.ng-switcher.active > div > div > div > div.switcher-language.item.util-clearfix > div > span')
    language.click()
    sleep(1)
    language = driver.find_element(By.CSS_SELECTOR, '#nav-global > div.ng-item-wrap.ng-item.ng-switcher.active > div > div > div > div.switcher-language.item.util-clearfix > div > ul > li:nth-child(5) > a')
    language.click()
    sleep(1)
    language = driver.find_element(By.CSS_SELECTOR, '#nav-global > div.ng-item-wrap.ng-item.ng-switcher.active > div > div > div > div.switcher-currency.item.util-clearfix > div > span')
    language.click()
    sleep(1)
    language = driver.find_element(By.CSS_SELECTOR, '#nav-global > div.ng-item-wrap.ng-item.ng-switcher.active > div > div > div > div.switcher-currency.item.util-clearfix > div > ul > li:nth-child(3) > a')
    language.click()
    sleep(1)
    language = driver.find_element(By.CSS_SELECTOR, '#nav-global > div.ng-item-wrap.ng-item.ng-switcher.active > div > div > div > div.switcher-btn.item.util-clearfix > button')
    language.click()
    sleep(1)
    driver.execute_script("window.scrollTo({ top: document.body.scrollHeight, behavior: 'smooth' })")
    sleep(2)
    driver.execute_script("window.scrollTo({ top: document.body.scrollHeight, behavior: 'smooth' })")
    sleep(5)
    products = []
    prod_divs = driver.find_elements(By.XPATH, '/html/body/div/div/div/div/div/div/div/a')



    for product in prod_divs :
        try:
            try:
                original_link = product.get_attribute('href')
            except Exception as  e :
                print('error: ',e)
                continue

            photo = product.find_element(By.XPATH, './/div/img').get_attribute('src')
            driver.execute_script("window.open('');")
            driver.switch_to.window(driver.window_handles[1])    
            driver.get(original_link)
            driver.implicitly_wait(5)
            wait = WebDriverWait(driver, 10)
            try : 
                cookies = driver.find_element(By.CSS_SELECTOR, '#gdpr-new-container > div > div.global-gdpr-btn-wrap > button:nth-child(2)')
                cookies.click()
            except : 
                pass
            sleep(1)
            try : 
                notification = driver.find_element(By.XPATH, '/html/body/div[11]/div/div[2]/div[3]/div[2]')
                notification.click()
            except : 
                pass

            full_name = driver.find_element(By.XPATH, '//*[@id="root"]/div[3]/div[1]/div[1]/div[2]/div[1]/h1').text 
            print("----------->>",full_name)
       
            try :
                #shipping = driver.find_element(By.CSS_SELECTOR,'#root > div.pdp-wrap.pdp-body > div.pdp-body-right > div > div > div.shipping--wrap--Dhb61O7 > div > div > div.dynamic-shipping-line.dynamic-shipping-titleLayout > span > span > strong').text.split("€")[-1]
                shipping = "0"
            except : 
                shipping = ' 0'
            price_driver = driver.find_elements(By.CSS_SELECTOR, '#root > div.pdp-wrap.pdp-body > div.pdp-body-left > div.pdp-info > div.pdp-info-right > div.price--wrap--tA4MDk4.product-price > div.price--current--H7sGzqb.product-price-current > div')
                                                            
            price = price_driver[0].text.split("€")[-1]       
            price = float("{:.2f}".format(float(price))) * perc
            shipping = get_price(shipping)
            shipping = float("{:.2f}".format(float(shipping))) * perc

            price = price + shipping
            description = full_name

            driver.close()
            driver.switch_to.window(driver.window_handles[0])
            images = {"images_url": [photo]}

            try : 
                AddProduct(dict(
                original_link=original_link,
                name=full_name,
                images=images,
                price=price,
                description=description,
                ), store, cate, maxVal, more, less)
                sleep(randint(15,30))
            except Exception as e: 
                print('error : ',e)
                pass
        except Exception:
            continue

