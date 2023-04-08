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


driver.get("https://syn85.lp.moigektar.ru/")


# модалка в хедере
try:
    time.sleep(2)
    btn = wait(driver, 14).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "nav > div > div > .btn-mquiz")))
    btn.click()
    name = wait(driver, 14).until(EC.element_to_be_clickable((By.XPATH, '//*[@class="uk-modal w-modal-callback uk-open"]//*[@id="callbackform-name"]')))
    name.send_keys('test')
    driver.find_element(by=By.XPATH, value='//*[@class="uk-modal w-modal-callback uk-open"]//*[@id="callbackform-phone"]').send_keys('9127777777')
    driver.find_element(by=By.XPATH, value='//*[@class="uk-modal w-modal-callback uk-open"]//*[@type="submit"]').click()
    wait(driver, 14).until(EC.visibility_of_element_located((By.XPATH, '//*[@class="uk-modal w-modal-callback uk-open"]//*[text()[contains(., "Заявка отправлена")]]')))
    driver.find_element(by=By.XPATH, value='//*[@class="uk-modal w-modal-callback uk-open"]/div/div/div/button').click()
    print('   OK: syn_85 модалка в хедере]')
except:
    print('ERROR: что-то не так с модалкой в хедере на син_85')





time.sleep(3)
driver.quit()
