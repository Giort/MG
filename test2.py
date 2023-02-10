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



# 1. проверка слайдера СП на главной странице "МГ"
driver.get("https://moigektar.ru/")
wait(driver,14).until(EC.visibility_of_element_located((By.XPATH, "//*[@id='eapps-vk-feed-6543b37b-15d1-4951-a888-a92bd0bddd8b']/div/div/div[1]/div/div[1]/div/div/div[2]/div/div[1]/div/div")))

#time.sleep(10)
driver.quit()
