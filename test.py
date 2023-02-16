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


# 15. syn_87
driver.get("https://mt.lp.moigektar.ru/")
try:
    wait(driver, 14).until(EC.presence_of_element_located((By.XPATH, '//div[@class="js-select-map"]')))
    title = driver.find_element(by=By.XPATH, value="//div[text()[contains(.,'Генеральный')]]")
    actions.move_to_element(title).perform()
    time.sleep(3)
    driver.find_element(by=By.XPATH, value='//img[@data-src="/img/select/overlay-touch.svg"]').click()
    wait(driver, 14).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'ymaps.ymaps-2-1-79-inner-panes')))
    print('   OK: syn_87')
except:
    print('ERROR: не загрузился генплан на син_87')







time.sleep(5)
driver.quit()

