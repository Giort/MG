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
driver.set_window_size(1920, 1080)
driver.implicitly_wait(10)

# vazuza2
driver.get("https://vazuza2.lp.moigektar.ru/")
try:
    #wait(driver, 14).until(EC.presence_of_element_located((By.XPATH, '//img[@data-src="/img/vazuza/select/overlay-touch.png"]')))
    title = wait(driver, 14).until(EC.presence_of_element_located((By.XPATH, '//div[text()[contains(.,"Генеральный")]]')))
    actions.move_to_element(title).send_keys(Keys.PAGE_DOWN).perform()
    driver.find_element(by=By.XPATH, value='//img[@data-src="/img/vazuza/select/overlay-touch.png"]').click()
    wait(driver, 14).until(EC.visibility_of_element_located((By.XPATH, '//canvas[4]')))
    print('   OK: vazuza2')
except:
    try:
        #wait(driver, 14).until(EC.presence_of_element_located((By.XPATH, '//img[@data-src="/img/vazuza/select/overlay-touch.png"]')))
        title = wait(driver, 14).until(EC.presence_of_element_located((By.XPATH, '//div[text()[contains(.,"Генеральный")]]')))
        actions.move_to_element(title).send_keys(Keys.PAGE_DOWN).perform()
        driver.find_element(by=By.XPATH, value='//img[@data-src="/img/vazuza/select/overlay-touch.png"]').click()
        wait(driver, 14).until(EC.visibility_of_element_located((By.XPATH, '//canvas[4]')))
        print('   OK: vazuza2')
    except:
        print('ERROR: не загрузился генплан на Вазузе')


time.sleep(1)
driver.quit()
