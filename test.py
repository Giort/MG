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
driver.set_window_size(1680, 1000)
driver.implicitly_wait(10)

with open('data.json', 'r') as file:
    data = json.load(file)



#driver.get("https://moigektar.ru/")
#driver.get("https://syn67.lp.moigektar.ru/")

# 59. проверка syn_92 по наличию заголовка "Генеральный"
driver.get("https://syn92.lp.moigektar.ru/")
try:
    wait(driver,14).until(EC.visibility_of_element_located((By.XPATH, "//div[text()[contains(.,'Генеральный')]]")))
    print(' \ / syn_92: OK')
except:
    print('ERROR (service_check): не дождался загрузки элемента на син_92')


time.sleep(6)
driver.quit()
