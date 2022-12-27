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
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import ElementNotVisibleException
import time



# 1. проверка каталога "МГ"
driver.get("https://moigektar.ru/catalogue")
try:
    title = wait(driver,14).until(EC.visibility_of_element_located((By.XPATH, "//h1[text()[contains(., 'Дачные участки')]]")))
    print('   блок "Дачные участки": OK')
    try:
        actions.move_to_element(title).send_keys(Keys.PAGE_DOWN).send_keys(Keys.ARROW_DOWN).perform()
        wait(driver,14).until(EC.visibility_of_element_located((By.XPATH, "//h1[text()[contains(., 'Дачные участки')]]//parent::div//div[1]/div/div//li[1]//button/span")))
        print('   карточки в "Дачных участках": OK')
    except:
        print('ERROR: проблема с карточками в "Дачных участках"')
except (TimeoutException, NoSuchElementException, ElementNotVisibleException):
    print('ERROR: проблема с блоком "Дачные участки"')

#time.sleep(10)
driver.quit()
