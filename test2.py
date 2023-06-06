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




# син_84
try:
    driver.get("https://syn84.lp.moigektar.ru/")
    wait(driver, 30).until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
    driver.find_element(by=By.CSS_SELECTOR, value=".uk-navbar> div > .btn-mquiz").click()
    time.sleep(3)
    m_iframe = driver.find_element(by=By.XPATH, value="//iframe[@class='marquiz__frame marquiz__frame_open']")
    driver.switch_to.frame(m_iframe)
    driver.find_element(by=By.CLASS_NAME, value="start-page__button").click()
    # 1. Выберите цели использования
    time.sleep(2)
    check1 = wait(driver,15).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'div[data-element-index="0"]')))
    check1.click()
    driver.find_element(by=By.CLASS_NAME, value="quiz-navbar__button_next-text").click()
    # 2. Выберите расположение участка
    time.sleep(2)
    check2 = wait(driver,15).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'div[data-element-index="0"]')))
    check2.click()
    driver.find_element(by=By.CLASS_NAME, value="quiz-navbar__button_next-text").click()
    # 3. Выберите необходимые коммункиации
    time.sleep(2)
    check3 = wait(driver,15).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'div[data-element-index="0"]')))
    check3.click()
    driver.find_element(by=By.CLASS_NAME, value="quiz-navbar__button_next-text").click()
    # 4. Бюджет
    time.sleep(2)
    check4 = wait(driver,15).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'div[data-element-index="0"]')))
    check4.click()
    driver.find_element(by=By.CLASS_NAME, value="quiz-navbar__button_next-text").click()
    # 5. Когда планируете начать строительство?
    time.sleep(2)
    check5 = wait(driver,15).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'div[data-element-index="0"]')))
    check5.click()
    # заполнить поля ввода
    time.sleep(2)
    name = wait(driver,15).until(EC.element_to_be_clickable((By.ID, 'name')))
    name.send_keys(str(data["test_data_quiz"]["name"]))
    driver.find_element(by=By.ID, value='VuePhoneNumberInput_country_selector').click()
    driver.find_element(by=By.XPATH, value='//div[text()[contains(., "United States")]]').click()
    driver.find_element(by=By.ID, value='VuePhoneNumberInput_phone_number').send_keys(str(data["test_data_quiz"]["phone"]))
    driver.find_element(by=By.ID, value='email').send_keys(str(data["test_data_quiz"]["email"]))
    driver.find_element(by=By.CSS_SELECTOR, value='form > button[type="submit"]').click()
    time.sleep(3)
    assert driver.find_element(by=By.CLASS_NAME, value='result__btn-text').is_displayed()
    print('   OK: syn_84 квиз в хедере')
except:
    print('ERROR: квиз в хедере на syn_84')

time.sleep(2)
driver.quit()
