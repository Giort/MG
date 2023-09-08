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



driver.get("https://moigektar.ru/")
#driver.get("https://syn39.lp.moigektar.ru/")


# модалка в блоке "Сохраните свои сбережения"
try:
    title = driver.find_element(by=By.XPATH, value='//h1[text()[contains(.,"Сохраните свои")]]')
    actions.move_to_element(title).perform()
    actions.send_keys(Keys.PAGE_DOWN).perform()
    driver.find_element(by=By.XPATH, value='//button[@uk-toggle="target: #modal-save"]').click()
    driver.find_element(by=By.CSS_SELECTOR, value="#modal-save #consultationform-name").send_keys(str(data["test_data_valid"]["name"]))
    driver.find_element(by=By.CSS_SELECTOR, value="#modal-save #consultationform-phone").send_keys(str(data["test_data_valid"]["phone"]))
    driver.find_element(by=By.CSS_SELECTOR, value="#modal-save #consultationform-email").send_keys(str(data["test_data_valid"]["email"]))
    driver.find_element(by=By.XPATH, value="//*[@id='modal-save']//button[text()[contains(.,'Отправить заявку')]]").click()
    try:
        wait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//*[@id='modal-save']//*[text()[contains(.,'Заявка отправлена')]]")))
        print('   OK: главная, модалка в блоке "Сохраните свои сбережения"')
    except:
        print('ERROR: не отправлены данные в: главная, модалка в блоке "Сохраните свои сбережения"')
    driver.find_element(by=By.XPATH, value='//*[@id="modal-save"]/div/div/*[(contains(@class,"uk-close"))]').click()
except:
    print('ERROR: не могу взаимодействовать: главная, модалка в блоке "Сохраните свои сбережения"')


time.sleep(5)
driver.quit()
