import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager


def open_amazon(item):
    global driver
    options = Options()
    service = Service(ChromeDriverManager().install())

    driver = webdriver.Chrome(options=options, service=service)

    driver.get(r'https://www.amazon.com/')

    inp = wait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'input[id="twotabsearchtextbox"]'))
    )
    time.sleep(4)

    inp.send_keys(item)
    time.sleep(2)
    inp.send_keys(Keys.ENTER)


def add_to_cart():
    global driver

    wait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'div[id="search"]'))
    )
    time.sleep(3)

    item_lists = driver.find_elements(by=By.CSS_SELECTOR, value='div[class="sg-col-inner"]')

    item_lists[5].find_element(by=By.TAG_NAME, value='a').click()

    inner_box = wait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'div[class="a-box-inner"]'))
    )
    time.sleep(2)

    try:
        inner_box.find_element(by=By.CSS_SELECTOR, value='input[id="add-to-cart-button"]').click()
    
    except:
        driver.back()
        add_to_cart()


def remove_from_cart():
    global driver
    cart_path = wait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'a[id="nav-cart"]'))
    )
    time.sleep(2)
    cart_path.click()

    cart = wait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'form[id="activeCartViewForm"]'))
    )
    time.sleep(2)

    cart.find_element(by=By.CSS_SELECTOR, value='input[value="Delete"]').click()
    time.sleep(10)


if __name__ == '__main__':
    driver = None
    open_amazon("pot")
    add_to_cart()
    remove_from_cart()