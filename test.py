from selenium import webdriver
from selenium.webdriver.chrome.options import Options
ch_options = Options()
#ch_options.add_argument('--headless')
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


# 1. Главная
driver.get("https://moigektar.ru/")
print('Главная')

try:
    title = wait(driver,14).until(EC.visibility_of_element_located((By.XPATH, "//h1[text()[contains(.,'Специальное предложение')]]")))
    print('   блок "Специальное предложение": OK')
    try:
        actions.move_to_element(title).send_keys(Keys.PAGE_DOWN).perform()
        wait(driver,14).until(EC.visibility_of_element_located((By.XPATH, "//*[text()[contains(., 'Специальное предложение')]]//parent::div//div[@uk-slider='sets: true']//li[1]//div/button/span")))
        print('   карточки в СП: OK')
    except:
        print('ERROR: проблема с карточками СП на главной МГ')
except (TimeoutException, NoSuchElementException, ElementNotVisibleException):
    print('ERROR: проблема с блоком "Специальное предложение" на главной МГ')


time.sleep(5)
driver.quit()

