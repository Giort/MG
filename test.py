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

driver.get("https://syn53.lp.moigektar.ru/")

# модалка "Обратная связь" в блоке "Новая жизнь - это"
try:
    time.sleep(2)
    driver.refresh()
    btn_1 = wait(driver, 14).until(EC.element_to_be_clickable((By.XPATH, "//*[text()[contains(., 'Показать еще')]]")))
    actions.move_to_element(btn_1).perform()
    btn_1.click()
    actions.send_keys(Keys.PAGE_DOWN).send_keys(Keys.PAGE_DOWN).perform()
    btn_2 = wait(driver, 14).until(EC.element_to_be_clickable((By.XPATH, "//div[@class='uk-visible@m uk-width-1-1']/*[text()[contains(., 'Узнать подробности')]]")))
    btn_2.click()
    name = wait(driver, 14).until(EC.element_to_be_clickable((By.XPATH, '//*[@class="uk-modal w-modal-callback uk-open"]//*[@id="consultationform-name"]')))
    name.send_keys(str(data["test_data_valid"]["name"]))
    driver.find_element(by=By.XPATH, value='//*[@class="uk-modal w-modal-callback uk-open"]//*[@id="consultationform-phone"]').send_keys(str(data["test_data_valid"]["phone"]))
    driver.find_element(by=By.XPATH, value='//*[@class="uk-modal w-modal-callback uk-open"]//*[@id="consultationform-email"]').send_keys(str(data["test_data_valid"]["email"]))
    driver.find_element(by=By.XPATH, value='//*[@class="uk-modal w-modal-callback uk-open"]//*[@type="submit"]').click()
    wait(driver, 14).until(EC.visibility_of_element_located((By.XPATH, '//*[@class="uk-modal w-modal-callback uk-open"]//*[text()[contains(., "Заявка отправлена")]]')))
    driver.find_element(by=By.XPATH, value='//*[@class="uk-modal w-modal-callback uk-open"]/div/div/div/button').click()
    print('   OK: syn_53 модалка в блоке "НЖ - это"')
except:
    print('ERROR: что-то не так с модалкой в блоке "НЖ - это" на син_53')

time.sleep(3)
driver.quit()
