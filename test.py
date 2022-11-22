from time import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
options = Options()
#options.add_argument('--headless')
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
import time

#   wait(driver,14).until(EC.visibility_of_element_located((By.XPATH, "//span[text()[contains(.,'Генеральный')]]")))


# 50. проверка syn_85 по наличию заголовка "Login"
driver.get("https://syn85.lp.moigektar.ru/")
try:
    wait(driver,14).until(EC.visibility_of_element_located((By.XPATH, "//h2[text()[contains(.,'Генеральный')]]")))
    print('  |  syn_85: OK')
except NoSuchElementException:
    print('ERROR: проблема на син_85')




time.sleep(1)
driver.quit()
