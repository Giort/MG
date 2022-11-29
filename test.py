from time import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
ch_options = Options()
#ch_options.add_argument('--headless')
driver = webdriver.Chrome(options= ch_options)
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
actions = ActionChains(driver)
driver.maximize_window()
wait = WebDriverWait


from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import ElementNotVisibleException
from selenium.webdriver.common.keys import Keys
import time


# 2. Каталог
driver.get('https://moigektar.ru/catalogue')
try:
    wait(driver,14).until(EC.presence_of_element_located((By.XPATH, "h1[text()[contains(.,'Лучшие поселки')]]")))
    print('   блок "Лучшие поселки": OK')
except TimeoutException:
    print('ERROR: проблема с блоком "Лучшие поселки"')
except NoSuchElementException:
    print('ERROR')

time.sleep(1)
driver.quit()
