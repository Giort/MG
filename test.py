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

with open('data.json', 'r') as file:
    data = json.load(file)

#driver.get("https://moigektar.ru/")

# 58. проверка "Бесконечных Знаний"" по наличию заголовка "Бесконечные знания"
driver.get("https://wiki.bug.land/login")
try:
    wait(driver,14).until(EC.visibility_of_element_located((By.XPATH, "//span[text()[contains(.,'Бесконечные')]]")))
    print(' \ / Бесконечные Знания: OK')
except:
    print('ERROR (service_check): не дождался загрузки элемента на "Бесконечных Знаниях"')

time.sleep(3)
driver.quit()
