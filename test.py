from selenium import webdriver
from selenium.webdriver.chrome.options import Options
ch_options = Options()
ch_options.add_argument('--headless')
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
#driver.maximize_window()
driver.set_window_size(1920, 1080)



# 32. проверка syn_17 по видимости заголовка "Виртуальные туры"
driver.get("https://syn107.lp.moigektar.ru/")
try:
    wait(driver,14).until(EC.visibility_of_element_located((By.XPATH, "//span[text()[contains(.,'Виртуальные')]]")))
    print(' \ / syn_17: OK')
except NoSuchElementException:
    print('ERROR: проблема на син_17')
except TimeoutException:
    print('ERROR: не дождался загрузки элемента на син_17')




time.sleep(5)
driver.quit()

