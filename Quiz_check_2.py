import chromedriver_binary
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
ch_options = Options()
ch_options.add_argument('--headless')
ch_options.page_load_strategy = 'eager'
driver = webdriver.Chrome(options= ch_options)
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
actions = ActionChains(driver)
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import json
driver.set_window_size(1660, 1000)
driver.implicitly_wait(10)

with open('data.json', 'r') as file:
    data = json.load(file)



# син_53
count = 0
driver.get("https://syn53.lp.moigektar.ru/")
while count < 3:
    try:
        wait(driver, 30).until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
        driver.find_element(by=By.CSS_SELECTOR, value=".uk-navbar> div > .btn-mquiz").click()
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
        # 3. Выберите необходимые коммуникации
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
        driver.find_element(by=By.ID, value='VuePhoneNumberInput_phone_number').send_keys(str(data["test_data_quiz"]["phone"]))
        driver.find_element(by=By.ID, value='email').send_keys(str(data["test_data_quiz"]["email"]))
        driver.find_element(by=By.CSS_SELECTOR, value='button[type="submit"]').click()
        time.sleep(3)
        success_text =  wait(driver, 15).until(EC.visibility_of_element_located((By.CLASS_NAME, "result__button")))
        if success_text:
            print('   ОК: syn_53 квиз в хедере')
            break
    except:
        count += 1
        if count == 3:
            print('ERROR (quiz_check): квиз в хедере на syn_53')
        else:
            driver.refresh()

# син_56
count = 0
driver.get("https://syn56.lp.moigektar.ru/")
while count < 3:
    try:
        wait(driver, 30).until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
        driver.find_element(by=By.CSS_SELECTOR, value=".uk-navbar> div > .btn-mquiz").click()
        m_iframe = driver.find_element(by=By.XPATH, value="//iframe[@class='marquiz__frame marquiz__frame_open']")
        driver.switch_to.frame(m_iframe)
        driver.find_element(by=By.CLASS_NAME, value="start-page__button").click()
        # 1. Площадь участка
        check1 = wait(driver,15).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'div[data-element-index="0"]')))
        check1.click()
        # 2. Выберите цели использования
        time.sleep(2)
        check2 = wait(driver,15).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'div[data-element-index="0"]')))
        check2.click()
        driver.find_element(by=By.CLASS_NAME, value="quiz-navbar__button_next-text").click()
        # 3. Выберите расположение участка
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
        driver.find_element(by=By.CSS_SELECTOR, value='button[type="submit"]').click()
        time.sleep(3)
        success_text =  wait(driver, 15).until(EC.visibility_of_element_located((By.CLASS_NAME, "result__button")))
        if success_text:
            print('   ОК: syn_56 квиз в хедере')
            break
    except:
        count += 1
        if count == 3:
            print('ERROR (quiz_check): квиз в хедере на syn_56')
        else:
            driver.refresh()

# син_67
count = 0
driver.get("https://syn67.lp.moigektar.ru/")
while count < 3:
    try:
        wait(driver, 30).until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
        driver.find_element(by=By.CSS_SELECTOR, value=".uk-navbar> div > .btn-mquiz").click()
        m_iframe = driver.find_element(by=By.XPATH, value="//iframe[@class='marquiz__frame marquiz__frame_open']")
        driver.switch_to.frame(m_iframe)
        driver.find_element(by=By.CLASS_NAME, value="start-page__button").click()
        # 1. Площадь участка
        time.sleep(2)
        check1 = wait(driver,15).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'div[data-element-index="0"]')))
        check1.click()
        # 2. Выберите цели использования
        time.sleep(2)
        check2 = wait(driver,15).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'div[data-element-index="0"]')))
        check2.click()
        driver.find_element(by=By.CLASS_NAME, value="quiz-navbar__button_next-text").click()
        # 3. Выберите расположение участка
        time.sleep(2)
        check3 = wait(driver,15).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'div[data-element-index="0"]')))
        check3.click()
        driver.find_element(by=By.CLASS_NAME, value="quiz-navbar__button_next-text").click()
        # 4. Бюджет
        time.sleep(2)
        check4 = wait(driver,15).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'div[data-element-index="0"]')))
        check4.click()
        driver.find_element(by=By.CLASS_NAME, value="quiz-navbar__button_next-text").click()
        # 5. Рассматриваете получение гранта?
        time.sleep(2)
        check5 = wait(driver,15).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'div[data-element-index="0"]')))
        check5.click()
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
        driver.find_element(by=By.CSS_SELECTOR, value='button[type="submit"]').click()
        time.sleep(3)
        success_text =  wait(driver, 15).until(EC.visibility_of_element_located((By.CLASS_NAME, "result__button")))
        if success_text:
            print('   ОК: syn_67 квиз в хедере')
            break
    except:
        count += 1
        if count == 3:
            print('ERROR (quiz_check): квиз в хедере на syn_67')
        else:
            driver.refresh()



time.sleep(5)
driver.quit()
