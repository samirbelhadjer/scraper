from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
from .add_prodcut import AddProduct
from random import randint
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.proxy import Proxy, ProxyType
import os
from selenium.webdriver.chrome.service import Service 

from random_user_agent.user_agent import UserAgent
from random_user_agent.params import SoftwareName, OperatingSystem


def get_random_user_agent():
    
    software_names = [SoftwareName.CHROME.value, SoftwareName.FIREFOX.value, SoftwareName.BRAVE.value]
    operating_systems = [OperatingSystem.WINDOWS.value, OperatingSystem.LINUX.value]   
    user_agent_rotator = UserAgent(software_names=software_names, operating_systems=operating_systems, limit=100)
    user_agents = user_agent_rotator.get_user_agents()
    user_agent = user_agent_rotator.get_random_user_agent()
    return user_agent



def scrap_sephora(url, perc, store, cate,sous_category, maxVal, more, less):
    homedir = os.path.expanduser("~")
    webdriver_service = Service(f"{homedir}/chromedriver/stable/chromedriver")


    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("start-maximized")
    options.add_argument("--disable-dev-shm-usage")

    options.add_argument("--disable-setuid-sandbox") 

    options.add_argument("--disable-dev-shm-using") 
    options.add_argument("--disable-extensions") 
    options.add_argument("--disable-gpu") 
    options.add_argument("start-maximized") 
    options.add_argument("disable-infobars")
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    driver = webdriver.Chrome(options=options, service=webdriver_service)
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

    user_agent = get_random_user_agent()

    driver.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent": user_agent})
    
    driver.implicitly_wait(5)
    driver.get(url)
    sleep(6)
    htmlElement = driver.find_element(By.TAG_NAME, "html")
    dom = htmlElement.get_attribute("outerHTML")
    html2 = htmlElement.get_attribute("outerHTML")
    html = driver.page_source

    driver.execute_script("window.scrollTo({ top: document.body.scrollHeight, behavior: 'smooth' })")
    sleep(2)
    driver.execute_script("window.scrollTo({ top: document.body.scrollHeight, behavior: 'smooth' })")
    sleep(2)

    products = []
    for product in driver.find_elements(By.XPATH, '/html/body/div[2]/div/div/div/div[2]/main/div[2]/div[2]/div/a'):
        original_link = product.get_attribute('href')
        try:
            photo = product.find_element(By.XPATH, './/picture/img').get_attribute('src')
        except:
            continue
        
        brand = product.find_element(By.XPATH, './span[1]').get_attribute("textContent")
        full_name = product.find_element(By.XPATH, './span[2]').get_attribute("textContent")

        price = float(product.find_element(By.XPATH, './/b/span').get_attribute("textContent").replace('$','').split(' ')[0]) * perc
        staff_pick = float(product.find_element(By.XPATH, './div[2]/span[1]').get_attribute('aria-label').split(" ")[0]) > 4
        driver.execute_script("window.open('');")
        driver.switch_to.window(driver.window_handles[1])
        driver.get(original_link)
        description = []
        for i in driver.find_elements(By.XPATH, '/html/body/div[2]/main/div[1]/div[6]/div[2]/div/div'):
            description.append("".join(i.get_attribute("innerText")))
        driver.close()
        driver.switch_to.window(driver.window_handles[0])


        AddProduct(dict(
            original_link=original_link,
            full_name=full_name,
            photo=photo,
            price=price,
            brand=brand,
            staff_pick=staff_pick,
            description="\n".join(description),
        ), store, cate, sous_category, maxVal, more, less)
        sleep(randint(12,25))


