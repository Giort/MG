from time import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
options = Options()
options.add_argument('--headless')
ch_options = Options()
ch_options.add_argument('--headless')
driver = webdriver.Chrome(options= ch_options)
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
driver.maximize_window()


from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time



# 28. проверка syn_13 по видимости заголовка "Выберите поселок"
driver.get("https://syn13.lp.moigektar.ru/")
time.sleep(3)
block28=driver.find_element(by=By.XPATH, value="//p[text()[contains(.,'Выберите поселок')]]")
if block28.is_displayed():
    print(' 28 syn_13: OK')




time.sleep(2)
driver.quit()
