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

# модалка 'Оставьте анкету' в 'Вакансии'
try:
    driver.get("https://moigektar.ru/hr")
    driver.find_element(by=By.XPATH, value="//div/div[1]/div/div/div/*[@uk-toggle='target: #modal-main1']").click()
    driver.find_element(by=By.XPATH, value="//*[@id='modal-main1']//*[@id='consultationform-name']").send_keys(str(data["test_data_valid"]["name"]))
    driver.find_element(by=By.XPATH, value="//*[@id='modal-main1']//*[@id='consultationform-phone']").send_keys(str(data["test_data_valid"]["phone"]))
    driver.find_element(by=By.XPATH, value="//*[@id='modal-main1']//*[@id='consultationform-email']").send_keys(str(data["test_data_valid"]["email"]))
    driver.find_element(by=By.XPATH, value="//*[@id='modal-main1']//button[text()[contains(.,'Отправить')]]").click()
    try:
        wait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//*[@id='modal-main1']//*[text()[contains(.,'Заявка успешно отправлена')]]")))
        print("   OK: модалка 'Оставьте анкету' в 'Вакансии'")
        driver.find_element(by=By.XPATH, value="//*[@id='modal-main1']/div/div/*[@uk-close]").click()
    except:
        print("ERROR: не отправлены данные: модалка 'Оставьте анкету' в 'Вакансии'")
except:
    print("ERROR: не могу взаимодействовать: модалка 'Оставьте анкету' в 'Вакансии'")

# проверка вызова этой мод. с первой кнопки "Запишитесь на собеседование"
try:
    btn = driver.find_element(by=By.XPATH, value="//h1[text()[contains(., 'Построй')]]//parent::div//div[@class='uk-text-center@s']//*[@uk-toggle='target: #modal-main1']")
    actions.move_to_element(btn).perform()
    btn.click()
    wait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//*[@id='modal-main1']//*[text()[contains(.,'Заявка успешно отправлена')]]")))
    print("   OK: модалка 'Оставьте анкету' по первой красной кнопке в 'Вакансии'")
    driver.find_element(by=By.XPATH, value="//*[@id='modal-main1']/div/div/*[@uk-close]").click()
except:
    print("ERROR: не могу взаимодействовать: модалка 'Оставьте анкету' по первой красной кнопке в 'Вакансии'")
# проверка вызова этой мод. со второй кнопки "Запишитесь на собеседование"
try:
    driver.find_element(by=By.XPATH, value="//h1[text()[contains(., 'Мы предлагаем')]]//parent::div//div[@class='uk-text-center@s']//*[@uk-toggle='target: #modal-main1']").click()
    wait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//*[@id='modal-main1']//*[text()[contains(.,'Заявка успешно отправлена')]]")))
    print("   OK: модалка 'Оставьте анкету' по второй красной кнопке в 'Вакансии'")
    driver.find_element(by=By.XPATH, value="//*[@id='modal-main1']/div/div/*[@uk-close]").click()
except:
    print("ERROR: не могу взаимодействовать: модалка 'Оставьте анкету' по второй красной кнопке в 'Вакансии'")

time.sleep(3)
driver.quit()
