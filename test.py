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
driver.set_window_size(1680, 1000)
driver.implicitly_wait(10)

with open('data.json', 'r') as file:
    data = json.load(file)



#driver.get("https://moigektar.ru/")
driver.get("https://syn39.lp.moigektar.ru/")

# модалка "Получить консультацию" в блоке "Зона интенсивного развития"
try:
    time.sleep(2)
    btn = driver.find_element(by=By.XPATH, value='//button[@uk-toggle="target: #modal-zir"]')
    actions.move_to_element(btn).perform()
    btn.click()
    name = wait(driver, 14).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="modal-zir"]//*[@id="consultationform-name"]')))
    name.send_keys(str(data["test_data_valid"]["name"]))
    driver.find_element(by=By.XPATH, value='//*[@id="modal-zir"]//*[@id="consultationform-phone"]').send_keys(str(data["test_data_valid"]["phone"]))
    driver.find_element(by=By.XPATH, value='//*[@id="modal-zir"]//*[@id="consultationform-email"]').send_keys(str(data["test_data_valid"]["email"]))
    driver.find_element(by=By.XPATH, value='//*[@id="modal-zir"]//*[@type="submit"]').click()
    wait(driver, 14).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="modal-zir"]//*[text()[contains(., "Заявка отправлена")]]')))
    driver.find_element(by=By.XPATH, value='//*[@id="modal-zir"]/div/div/div[1]/button').click()
    print('   OK: syn_39 модалка в блоке "Зона интенсивного развития"')
except:
    print('ERROR: что-то не так с модалкой в блоке "Зона интенсивного развития" на син_39')


time.sleep(6)
driver.quit()
