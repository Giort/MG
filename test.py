from selenium import webdriver
from selenium.webdriver.chrome.options import Options
ch_options = Options()
#ch_options.add_argument('--headless')
ch_options.page_load_strategy = 'eager'
driver = webdriver.Chrome(options= ch_options)
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
actions = ActionChains(driver)
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import ElementNotVisibleException
from selenium.webdriver.common.keys import Keys
import time
import json
driver.set_window_size(1660, 1000)
driver.implicitly_wait(10)

with open('locators.json', 'r') as file:
    locator = json.load(file)


# подсчёт СП на син_39
driver.get("https://syn39.lp.moigektar.ru/")
try:
    title = wait(driver, 14).until(EC.presence_of_element_located((By.XPATH, "//h1[text()[contains(.,'Специальное')]]")))
    ActionChains(driver).move_to_element(title).send_keys(Keys.PAGE_DOWN).perform()
    SO_qty = len(driver.find_elements(by=By.CSS_SELECTOR, value='.w-catalog-projects ul.card-special > li'))
    if SO_qty >= 3:
        print("   OK: количество СП на странице син_39 Лесная усадьба = " + str(SO_qty))
    else:
        print("ERROR: количество СП на странице син_39 Лесная усадьба = " + str(SO_qty))
except:
    print("ERROR: не получилось посчитать СП на странице син_39")



time.sleep(3)
driver.quit()
