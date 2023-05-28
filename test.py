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



# 7 проверка раздела "Вакансии"
# 7.1 переход на страницу "Вакансии"
driver.get("https://moigektar.ru/hr")
try:
    form_id = driver.find_element(by=By.XPATH, value='//b[text()[contains(.,"Оставьте анкету")]]//ancestor::div[2]').get_attribute('id')
    driver.find_element(by=By.XPATH, value="//div[@id='"+ form_id +"']//*[@id='hrform-name']").send_keys(str(data["test_data_valid"]["name"]))
    driver.find_element(by=By.XPATH, value="//div[@id='"+ form_id +"']//*[@id='hrform-phone']").send_keys(str(data["test_data_valid"]["phone"]))
    driver.find_element(by=By.XPATH, value="//div[@id='"+ form_id +"']//*[text()[contains(.,'Отправить')]]").click()
    try:
        wait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//div[@id='"+ form_id +"']//*[text()[contains(.,'Заявка отправлена')]]")))
        print(" OK: данные из вакансий были отправлены")
    except:
        print('ERROR: не отправлены данные в форму "Оставьте анкету" в "Вакансиях"')
except:
    print('ERROR: не могу найти форму "Оставьте анкету" в "Вакансиях"')

# блок "Проект МГ - это"
# try:
#     assert driver.find_element(by=By.XPATH, value='//*[@id="w-descr"]/div/div[1]//div[@class="w-descr__img"]//ul[@class="uk-slider-items"]').is_displayed()
#     print('   блок "Проект МГ - это": OK')
# except:
#     print('ERROR: проблема с блоком "Проект МГ - это" на главной МГ')


time.sleep(1)
driver.quit()
