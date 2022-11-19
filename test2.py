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



# 1. проверка каталога "МГ"
driver.get("https://moigektar.ru/catalogue")
#driver.get("https://app-site-moigektar.stage.bug.land/")

# 1.1 проверка, что есть кнопка на карточке участка в блоке "Тотальная распродажа"
try:
    btn = wait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//*[text()[contains(., 'Специальное предложение')]]//parent::div//div[@uk-slider='sets: true']//li[1]//div/button/span")))
    print("   ОК 1.1: блок СП на странице есть")
except TimeoutException:
    print("ERROR: 1.1 не могу открыть модаль спецпредложений в каталоге МГ")

#time.sleep(10)
driver.quit()
