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


    language = driver.find_element(By.CSS_SELECTOR, '#_full_container_header_23_ > div.pc-header--right--2cV7LB8 > div > div.pc-header--items--tL_sfQ4 > div.es--wrap--RYjm1RT')
    language.click()
    sleep(1)
    language = driver.find_element(By.CSS_SELECTOR, '#_full_container_header_23_ > div.pc-header--right--2cV7LB8 > div > div.pc-header--items--tL_sfQ4 > div.es--wrap--RYjm1RT > div.es--contentWrap--ypzOXHr.es--visible--12ePDdG > div:nth-child(4) > div')
    language.click()
    sleep(1)
    language = driver.find_element(By.CSS_SELECTOR, '#_full_container_header_23_ > div.pc-header--right--2cV7LB8 > div > div.pc-header--items--tL_sfQ4 > div.es--wrap--RYjm1RT > div.es--contentWrap--ypzOXHr.es--visible--12ePDdG > div:nth-child(4) > div > div.select--popup--W2YwXWt.select--visiblePopup--VUtkTX2 > div:nth-child(3)')
    language.click()
    sleep(1)
  
    language = driver.find_element(By.CSS_SELECTOR, '#_full_container_header_23_ > div.pc-header--right--2cV7LB8 > div > div.pc-header--items--tL_sfQ4 > div.es--wrap--RYjm1RT > div.es--contentWrap--ypzOXHr.es--visible--12ePDdG > div:nth-child(6) > div')
    language.click()
    sleep(1)
    language = driver.find_element(By.CSS_SELECTOR, '#_full_container_header_23_ > div.pc-header--right--2cV7LB8 > div > div.pc-header--items--tL_sfQ4 > div.es--wrap--RYjm1RT > div.es--contentWrap--ypzOXHr.es--visible--12ePDdG > div:nth-child(6) > div > div.select--popup--W2YwXWt.select--visiblePopup--VUtkTX2 > div:nth-child(2)')
    language.click()
    sleep(1)
    language = driver.find_element(By.CSS_SELECTOR, '#_full_container_header_23_ > div.pc-header--right--2cV7LB8 > div > div.pc-header--items--tL_sfQ4 > div.es--wrap--RYjm1RT > div.es--contentWrap--ypzOXHr.es--visible--12ePDdG > div.es--saveBtn--w8EuBuy')
    language.click()
    sleep(3)
    driver.get(url)
    try : 
        cookies = driver.find_element(By.CSS_SELECTOR, '#gdpr-new-container > div > div.global-gdpr-btn-wrap > button.btn-accept')
        cookies.click()
    except : 
        pass
    sleep(3)
    driver.execute_script("window.scrollTo({ top: document.body.scrollHeight, behavior: 'smooth' })")
    sleep(1.5)
    driver.execute_script("window.scrollTo({ top: document.body.scrollHeight, behavior: 'smooth' })")
    sleep(3)
    products = []
    prod_divs = driver.find_elements(By.XPATH, '/html/body/div[5]/div[1]/div/div[2]/div[2]/div/div')



    for product in prod_divs :
        try:
            try:
                a_el = product.find_element(By.XPATH, './/div/a')
                original_link = a_el.get_attribute('href')
            except Exception as  e :
                print('error: ',e)
                continue

            driver.execute_script("window.open('');")
            driver.switch_to.window(driver.window_handles[1])    
            driver.get(str(original_link))
            sleep(4)
            driver.implicitly_wait(7)
            wait = WebDriverWait(driver, 10)
            try : 
                cookies = driver.find_element(By.CSS_SELECTOR, '#gdpr-new-container > div > div.global-gdpr-btn-wrap > button:nth-child(2)')
                cookies.click()
            except : 
                pass
            sleep(3)
            try : 
                notification = driver.find_element(By.XPATH,'/html/body/div[9]/div/div[2]/div[3]/div[2]')
                notification.click()
            except Exception: 
                pass

            full_name = driver.find_element(By.XPATH, '//*[@id="root"]/div/div[3]/div/div[1]/div[1]/div[2]/div[4]/h1').text 
                                                       
            shipping_div = driver.find_element(By.CLASS_NAME,'dynamic-shipping-line')
            shipping = shipping_div.text.split("€")[-1] 
            if 'Livraison gratuite' in shipping:
                shipping = '0'

            price_div = driver.find_element(By.CSS_SELECTOR,'div[data-pl="product-price"]')
            price_element = price_div.find_element(By.CLASS_NAME,'product-price-current')
            price = price_element.text.split("€")[-1] 
            price = get_price(price)
            price = float("{:.2f}".format(float(price))) * perc
            shipping = get_price(shipping)
            shipping = float("{:.2f}".format(float(shipping))) * perc

            price = price + shipping
            description = full_name
            images_src = []

            images  = driver.find_element(By.CLASS_NAME, 'pdp-info-left')


            if images:
                images = images.find_elements(By.CSS_SELECTOR,'img')
                if len(images) > 0 :
                    images_src = []
                    for img in images:
                        img_url = img.get_attribute("src").replace('220x220','').replace('200*200','').replace('.jpg_80x80','')
                        images_src.append(img_url)
                    
            driver.close()
            driver.switch_to.window(driver.window_handles[0])
            

            try : 
                AddProduct(dict(
                original_link=original_link,
                name=full_name,
                images=images_src,
                price=price,
                description=description,
                ), store, cate, maxVal, more, less)
                sleep(randint(15,30))
            except Exception as e: 
                print('error : ',e)
                pass
        except Exception as e:
            continue
