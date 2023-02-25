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






driver.get("https://moigektar.ru/")

try:
    wait(driver,14).until(EC.visibility_of_element_located((By.XPATH, "//h1[text()[contains(.,'Гектар под ваши')]]")))
    print('   блок "Гектар под ваши цели": OK')
except:
    print('ERROR: проблема с блоком "Гектар под ваши цели" на главной МГ')

try:
    wait(driver,14).until(EC.visibility_of_element_located((By.XPATH, "//h1[text()[contains(.,'Лучшее время')]]")))
    print('   блок "Лучшее время для покупки": OK')
except:
    print('ERROR: проблема с блоком "Лучшее время для покупки" на главной МГ')

try:
    title = wait(driver,14).until(EC.visibility_of_element_located((By.XPATH, "//h1[text()[contains(.,'Специальное предложение')]]")))
    print('   блок "Специальное предложение": OK')
    try:
        actions.move_to_element(title).send_keys(Keys.PAGE_DOWN).perform()
        wait(driver,14).until(EC.visibility_of_element_located((By.XPATH, "//*[text()[contains(., 'Специальное предложение')]]//parent::div//div[@uk-slider='sets: true']//li[1]//div/button/span")))
        print('   карточки в СП на главной: OK')
    except:
        print('ERROR: проблема с карточками СП на главной МГ')
except (TimeoutException, NoSuchElementException, ElementNotVisibleException):
    print('ERROR: проблема с блоком "Специальное предложение" на главной МГ')

try:
    l_title = wait(driver,14).until(EC.visibility_of_element_located((By.XPATH, "//h1[text()[contains(.,'Лучшие поселки')]]")))
    print('   блок "Лучшие поселки": OK')
    try:
        actions.move_to_element(l_title).send_keys(Keys.PAGE_DOWN).perform()
        wait(driver,14).until(EC.visibility_of_element_located((By.XPATH, "//*[@id='catalogue']//div[1]/div/div[1]//li[1]//button")))
        print('   карточки в Лучших посёлках на главной: OK')
    except:
        print('ERROR: проблема с карточками Лучшие посёлки на главной МГ')
except:
    print('ERROR: проблема с блоком "Лучшие поселки проекта" на главной МГ')



time.sleep(5)
driver.quit()

