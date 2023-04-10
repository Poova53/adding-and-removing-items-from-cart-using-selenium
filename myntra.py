import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import ElementClickInterceptedException


def search_myntra(item):
    global driver
    options = Options()
    service = Service(ChromeDriverManager().install())

    driver = webdriver.Chrome(options=options, service=service)

    driver.get(r'https://www.myntra.com/')

    inp = wait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'input[class="desktop-searchBar"]'))
    )
    time.sleep(3)

    inp.send_keys(item)
    time.sleep(1)
    inp.send_keys(Keys.ENTER)


def add_to_cart():
    global driver
    wait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'div[class="search-searchProductsContainer row-base"]'))
    )
    time.sleep(3)

    items = driver.find_elements(by=By.CSS_SELECTOR, value='li[class="product-base"]')
    items[5].find_element(by=By.TAG_NAME, value='a').click()

    time.sleep(0.5)
    driver.switch_to.window(driver.window_handles[1])
    
    wait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'div[class="pdp-description-container"]'))
    )
    time.sleep(2)

    container_divs_list = driver.find_element(by=By.CSS_SELECTOR, value='div[class="pdp-description-container"]'
                                               ).find_elements(by=By.TAG_NAME, value='div')
        
    for div in container_divs_list:
        if div.text.strip() == "ADD TO BAG":
            div.click()
            break

    time.sleep(2)
    

def remove_from_cart():
    global driver
    driver.get(r'https://www.myntra.com/checkout/cart')

    container = wait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'div[class="item-base-item"]'))
    )
    time.sleep(3)

    try:
        driver.find_element(by=By.CSS_SELECTOR, value='div[class="itemComponents-base-invisibleBackDrop"]').click()
        container.find_element(by=By.CSS_SELECTOR, value='svg[class="itemContainer-base-closeIcon"]').click()

    except ElementClickInterceptedException:
        container.find_element(by=By.CSS_SELECTOR, value='svg[class="itemContainer-base-closeIcon"]').click()

    dialog_box = wait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'div[class="modal-base-container "]'))
    )

    buttons = dialog_box.find_elements(by=By.TAG_NAME, value="button")

    buttons[0].click()
    time.sleep(10)


if __name__ == "__main__":
    item = input("Enter the item need to search: ")
    driver = None

    search_myntra(item)
    add_to_cart()
    remove_from_cart()