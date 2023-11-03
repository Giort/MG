import chromedriver_binary
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
import time
import json
driver.set_window_size(1660, 1000)
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import ElementNotVisibleException

with open('data.json', 'r') as file:
    data = json.load(file)



driver.get("https://moigektar.ru"+ str(data["mg_loc"]["mg_cur_release"]))


#модалка "Лесная усадьба" в блоке "Лучшие поселки

driver.find_element(by=By.XPATH, value='//*[(contains(@class, "uk-visible@s"))]//*[@uk-toggle="target: #modal-syn39"]//button').click()
driver.find_element(by=By.CSS_SELECTOR, value='#modal-syn39[style="display: block;"] #consultationform-name').send_keys(str(data["test_data_valid"]["name"]))
driver.find_element(by=By.CSS_SELECTOR, value='#modal-syn39[style="display: block;"] #consultationform-phone').send_keys(str(data["test_data_valid"]["phone"]))
driver.find_element(by=By.CSS_SELECTOR, value='#modal-syn39[style="display: block;"] #consultationform-email').send_keys(str(data["test_data_valid"]["email"]))
driver.find_element(by=By.CSS_SELECTOR, value='#modal-syn39[style="display: block;"] button[type="submit"]').click()

wait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[(@id="modal-syn39") and (@style="display: block;")]//*[text()[contains(.,"Заявка отправлена")]]')))
print('   OK: главная, модалка "Лесная усадьба" в блоке "Лучшие поселки')

print('ERROR: не отправлены данные в: главная, модалка "Лесная усадьба" в блоке "Лучшие поселки')
driver.find_element(by=By.XPATH, value='#modal-syn39[style="display: block;"] > div > div > button').click()


time.sleep(2)
driver.quit()
