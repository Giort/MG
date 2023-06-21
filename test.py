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

# syn_34
try:
    driver.get("https://syn34.lp.moigektar.ru/")
    title = wait(driver, 14).until(EC.presence_of_element_located((By.XPATH, '//div[text()[contains(.,"Генеральный")]]')))
    actions.move_to_element(title).perform()
    driver.find_element(by=By.XPATH, value='//img[@data-src="/img/select/overlay-touch.svg"]').click()
    wait(driver, 14).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'ymaps.ymaps-2-1-79-inner-panes')))
    print('   OK: syn_34')
except:
    print('ERROR: не загрузился генплан на син_34')


time.sleep(1)
driver.quit()
