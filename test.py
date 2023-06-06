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



# проверка слайдера SOW на главной странице "МГ"
# Скрипт проверяет, сколько участков СП есть у посёлка на странице Каталог участков на сайте МГ
# и сообщает, если их осталось меньше 3
#
# В лог выводится сообщение с количеством посёлков и названия этих посёлков с количеством
# участков СП для каждого из них
# В этом списке выводится сообщение "ERROR" + количество СП, если СП у посёлка меньше 3
#

# syn_84
try:
    driver.get("https://syn84.lp.moigektar.ru/")
    title = driver.find_element(by=By.XPATH, value='//*[text()[contains(., "Виртуальный тур")]]')
    actions.move_to_element(title).send_keys(Keys.PAGE_DOWN).perform()
    time.sleep(6)
    btn = driver.find_element(by=By.XPATH, value='//img[@class="w-tour__icon animated-fast"]')
    actions.click(btn).perform()
    iframe = driver.find_element(by=By.CLASS_NAME, value="uk-lightbox-iframe")
    driver.switch_to.frame(iframe)
    wait(driver, 14).until(EC.visibility_of_element_located((By.XPATH, "//div[(contains(@style, 'z-index: 204'))]")))
    print('   OK: syn_84')
except:
    print('ERROR: не загрузился виртур на син_84')


time.sleep(1)
driver.quit()
