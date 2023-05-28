from selenium import webdriver
from selenium.webdriver.chrome.options import Options
ch_options = Options()
ch_options.add_argument('--headless')
ch_options.page_load_strategy = 'eager'
driver = webdriver.Chrome(options=ch_options)
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait as wait
import json
import time
from selenium.webdriver.common.action_chains import ActionChains
actions = ActionChains(driver)
driver.implicitly_wait(10)
driver.set_window_size(1660, 1000)

with open('data.json', 'r') as file:
    data = json.load(file)

# Скрипт вызывает модальные окна и заполняет корректными данными
#
# В лог выводится сообщение "ОК", если данные были отправлены и отобразилось сообщение об успехе
# В лог выводится сообщение "ERROR", если это сообщение не отобразилось
# В лог выводится сообщение "ERROR", если окно не было открыто или не было найдено
#

driver.get("https://moigektar.ru/")

# 1. проверка главной страницы "МГ"
print("Главная")

# баннер над хедером и модалка в нём
# try:
#     driver.find_element(by=By.CLASS_NAME, value="w-banner").click()
#     print('   OK: баннер над хедером')
#     try:
#         driver.find_element(by=By.CSS_SELECTOR, value="#modal-invest #consultationform-name").send_keys(str(data["test_data_valid"]["name"]))
#         driver.find_element(by=By.CSS_SELECTOR, value="#modal-invest #consultationform-phone").send_keys(str(data["test_data_valid"]["phone"]))
#         driver.find_element(by=By.CSS_SELECTOR, value="#modal-invest #consultationform-email").send_keys(str(data["test_data_valid"]["email"]))
#         driver.find_element(by=By.XPATH, value="//*[@id='modal-invest']//button[text()[contains(.,'Отправить заявку')]]").click()
#         try:
#             wait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//*[@id='modal-invest']//*[text()[contains(.,'Заявка отправлена')]]")))
#             print("   OK: главная, модалка в баннере над хедером")
#             driver.find_element(by=By.XPATH, value="//*[@id='modal-invest']/div/div/*[@uk-close]").click()
#         except:
#             print('ERROR: не отправлены данные в: главная, модалка в баннере над хедером')
#     except:
#         print('ERROR: не могу ввести данные в: главная, модалка в баннере над хедером')
# except:
#     print('ERROR: не могу взаимодействовать: главная, баннер над хедером')

# модалка в блоке "Быстрый старт жизни на земле"
# try:
#     driver.find_element(by=By.XPATH, value="//*[@class='w-change-house']//li[1]//button").click()
#     driver.find_element(by=By.CSS_SELECTOR, value="#modal-meeting-consultation #consultationform-name").send_keys(str(data["test_data_valid"]["name"]))
#     driver.find_element(by=By.CSS_SELECTOR, value="#modal-meeting-consultation #consultationform-phone").send_keys(str(data["test_data_valid"]["phone"]))
#     driver.find_element(by=By.CSS_SELECTOR, value="#modal-meeting-consultation #consultationform-email").send_keys(str(data["test_data_valid"]["email"]))
#     driver.find_element(by=By.XPATH, value="//*[@id='modal-meeting-consultation']//button[text()[contains(.,'Получить консультацию')]]").click()
#     try:
#         wait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//*[@id='modal-meeting-consultation']//*[text()[contains(.,'Заявка отправлена')]]")))
#         print("   OK: главная, модалка в блоке Быстрый старт")
#         driver.find_element(by=By.XPATH, value="//*[@id='modal-meeting-consultation']/div/div/*[@uk-close]").click()
#     except:
#         print('ERROR: не отправлены данные в: главная, модалка в блоке Быстрый старт')
# except:
#     print('ERROR: не могу взаимодействовать: главная, модалка в блоке Быстрый старт')

# модалка в блоке "Время вкладывать в землю"
# try:
#     driver.find_element(by=By.XPATH, value="//div[text()[contains(.,'Время вкладывать')]]//parent::div[1]/div/button").click()
#     driver.find_element(by=By.CSS_SELECTOR, value="#modal-save #consultationform-name").send_keys(str(data["test_data_valid"]["name"]))
#     driver.find_element(by=By.CSS_SELECTOR, value="#modal-save #consultationform-phone").send_keys(str(data["test_data_valid"]["phone"]))
#     driver.find_element(by=By.CSS_SELECTOR, value="#modal-save #consultationform-email").send_keys(str(data["test_data_valid"]["email"]))
#     driver.find_element(by=By.XPATH, value="//*[@id='modal-save']//button[text()[contains(.,'Отправить заявку')]]").click()
#     try:
#         wait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//*[@id='modal-save']//*[text()[contains(.,'Заявка отправлена')]]")))
#         print("   OK: главная, модалка в блоке Время вкладывать")
#         driver.find_element(by=By.XPATH, value="//*[@id='modal-save']/div/div/*[@uk-close]").click()
#     except:
#         print('ERROR: не отправлены данные в: главная, модалка в блоке Время вкладывать')
# except:
#     print('ERROR: не могу взаимодействовать: главная, модалка в блоке Время вкладывать')

# модалка в блоке "Почему нам доверяют"
# try:
#     driver.find_element(by=By.XPATH, value="//*[text()[contains(.,'Почему нам доверяют')]]//parent::div//button[@uk-toggle='target: #modal-batch-juridical']").click()
#     driver.find_element(by=By.CSS_SELECTOR, value="#modal-batch-juridical #consultationform-name").send_keys(str(data["test_data_valid"]["name"]))
#     driver.find_element(by=By.CSS_SELECTOR, value="#modal-batch-juridical #consultationform-phone").send_keys(str(data["test_data_valid"]["phone"]))
#     driver.find_element(by=By.CSS_SELECTOR, value="#modal-batch-juridical #consultationform-email").send_keys(str(data["test_data_valid"]["email"]))
#     driver.find_element(by=By.XPATH, value="//*[@id='modal-batch-juridical']//button[text()[contains(.,'Отправить заявку')]]").click()
#     try:
#         wait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//*[@id='modal-batch-juridical']//*[text()[contains(.,'Заявка отправлена')]]")))
#         print("   OK: главная, модалка в блоке Почему нам доверяют")
#         driver.find_element(by=By.XPATH, value="//*[@id='modal-batch-juridical']/div/div/*[@uk-close]").click()
#     except:
#         print('ERROR: не отправлены данные в: главная, модалка в блоке Почему нам доверяют')
# except:
#     print('ERROR: не могу взаимодействовать: главная, модалка в блоке Почему нам доверяют')

# модалка в блоке "Центр правовой поддержки"
# try:
#     driver.find_element(by=By.XPATH, value="//*[@id='cpp']//button").click()
#     driver.find_element(by=By.CSS_SELECTOR, value="#modal-center #consultationform-name").send_keys(str(data["test_data_valid"]["name"]))
#     driver.find_element(by=By.CSS_SELECTOR, value="#modal-center #consultationform-phone").send_keys(str(data["test_data_valid"]["phone"]))
#     driver.find_element(by=By.CSS_SELECTOR, value="#modal-center #consultationform-email").send_keys(str(data["test_data_valid"]["email"]))
#     driver.find_element(by=By.XPATH, value="//*[@id='modal-center']//button[text()[contains(.,'Задать вопрос')]]").click()
#     try:
#         wait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//*[@id='modal-center']//*[text()[contains(.,'Заявка отправлена')]]")))
#         print("   OK: главная, модалка в блоке Центр правовой поддержки")
#         driver.find_element(by=By.XPATH, value="//*[@id='modal-center']/div/div/*[@uk-close]").click()
#     except:
#         print('ERROR: не отправлены данные в: главная, модалка в блоке Центр правовой поддержки')
# except:
#     print('ERROR: не могу взаимодействовать: главная, модалка в блоке Центр правовой поддержки')

# модалка в блоке "Бизнес-планы"
try:
    driver.refresh()
    driver.find_element(by=By.XPATH, value="//*[text()[contains(.,'Бизнес-планы')]]//parent::div/div/div//ul/li[1]//a").click()
    driver.find_element(by=By.CSS_SELECTOR, value="#modal-main #consultationform-name").send_keys(str(data["test_data_valid"]["name"]))
    driver.find_element(by=By.CSS_SELECTOR, value="#modal-main #consultationform-phone").send_keys(str(data["test_data_valid"]["phone"]))
    driver.find_element(by=By.CSS_SELECTOR, value="#modal-main #consultationform-email").send_keys(str(data["test_data_valid"]["email"]))
    driver.find_element(by=By.XPATH, value="//*[@id='modal-main']//button[text()[contains(.,'Отправить заявку')]]").click()
    try:
        wait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//*[@id='modal-main']//*[text()[contains(.,'Заявка отправлена')]]")))
        print("   OK: главная, модалка в блоке Бизнес-планы")
        driver.find_element(by=By.XPATH, value="//*[@id='modal-main']/div/div/*[@uk-close]").click()
    except:
        print('ERROR: не отправлены данные в: главная, модалка в блоке Бизнес-планы')
except:
    print('ERROR: не могу взаимодействовать: главная, модалка в блоке Бизнес-планы')

# модалка в блоке "Приглашаем на встречу"
try:
    driver.find_element(by=By.XPATH, value="//*[@class='w-meeting']//a[text()[contains(.,'Записаться')]]//parent::div/a").click()
    driver.find_element(by=By.CSS_SELECTOR, value="#modal-meeting-meeting #consultationform-name").send_keys(str(data["test_data_valid"]["name"]))
    driver.find_element(by=By.CSS_SELECTOR, value="#modal-meeting-meeting #consultationform-phone").send_keys(str(data["test_data_valid"]["phone"]))
    driver.find_element(by=By.CSS_SELECTOR, value="#modal-meeting-meeting #consultationform-email").send_keys(str(data["test_data_valid"]["email"]))
    driver.find_element(by=By.XPATH, value="//*[@id='modal-meeting-meeting']//button[text()[contains(.,'Отправить заявку')]]").click()
    try:
        wait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//*[@id='modal-meeting-meeting']//*[text()[contains(.,'Заявка отправлена')]]")))
        print("   OK: главная, модалка в блоке Приглашаем на встречу\n")
        driver.find_element(by=By.XPATH, value="//*[@id='modal-meeting-meeting']/div/div/*[@uk-close]").click()
    except:
        print('ERROR: не отправлены данные в: главная, модалка в блоке Приглашаем на встречу\n')
except:
    print('ERROR: не могу взаимодействовать: главная, модалка в блоке Приглашаем на встречу\n')


# Развитие
print("Развитие")

# модалка 'Получить консультацию' в 'Развитие - Развитие поселка'
try:
    driver.get("https://moigektar.ru/growth")
    driver.find_element(by=By.XPATH, value="//*[@uk-toggle='target: #modal-main']").click()
    driver.find_element(by=By.CSS_SELECTOR, value="#modal-main #consultationform-name").send_keys(str(data["test_data_valid"]["name"]))
    driver.find_element(by=By.CSS_SELECTOR, value="#modal-main #consultationform-phone").send_keys(str(data["test_data_valid"]["phone"]))
    driver.find_element(by=By.CSS_SELECTOR, value="#modal-main #consultationform-email").send_keys(str(data["test_data_valid"]["email"]))
    driver.find_element(by=By.XPATH, value="//*[@id='modal-main']//button[text()[contains(.,'Отправить')]]").click()
    try:
        wait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//*[@id='modal-main']//*[text()[contains(.,'Заявка отправлена')]]")))
        print("   OK: модалка 'Получить консультацию' в 'Развитие - Развитие поселка'")
        driver.find_element(by=By.XPATH, value="//*[@id='modal-main']/div/div/*[@uk-close]").click()
    except:
        print("ERROR: не отправлены данные: модалка 'Получить консультацию' в 'Развитие - Развитие поселка'")
except:
    print("ERROR: не могу взаимодействовать: модалка 'Получить консультацию' в 'Развитие - Развитие поселка'")

# модалка 'Заказать услугу' на странице 'Развитие - Глазами инвестора'
try:
    driver.get("https://moigektar.ru/investment")
    driver.find_element(by=By.XPATH, value="//*[@uk-toggle='target: #modal-calculation']").click()
    driver.find_element(by=By.CSS_SELECTOR, value="#modal-calculation #consultationform-name").send_keys(str(data["test_data_valid"]["name"]))
    driver.find_element(by=By.CSS_SELECTOR, value="#modal-calculation #consultationform-phone").send_keys(str(data["test_data_valid"]["phone"]))
    driver.find_element(by=By.CSS_SELECTOR, value="#modal-calculation #consultationform-email").send_keys(str(data["test_data_valid"]["email"]))
    driver.find_element(by=By.XPATH, value="//*[@id='modal-calculation']//button[text()[contains(.,'Отправить')]]").click()
    try:
        wait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//*[@id='modal-calculation']//*[text()[contains(.,'Заявка отправлена')]]")))
        print("   OK: модалка 'Заказать услугу' в 'Развитие - Глазами инвестора'")
        driver.find_element(by=By.XPATH, value="//*[@id='modal-calculation']/div/div/*[@uk-close]").click()
    except:
        print("ERROR: не отправлены данные: модалка 'Заказать услугу' в 'Развитие - Глазами инвестора'")
except:
    print("ERROR: не могу взаимодействовать: модалка 'Заказать услугу' в 'Развитие - Глазами инвестора'")

# модалка 'Подобрать участок' на странице 'Развитие - Глазами инвестора'
try:
    driver.find_element(by=By.XPATH, value="//*[@uk-toggle='target: #modal-select']").click()
    driver.find_element(by=By.CSS_SELECTOR, value="#modal-select #consultationform-name").send_keys(str(data["test_data_valid"]["name"]))
    driver.find_element(by=By.CSS_SELECTOR, value="#modal-select #consultationform-phone").send_keys(str(data["test_data_valid"]["phone"]))
    driver.find_element(by=By.CSS_SELECTOR, value="#modal-select #consultationform-email").send_keys(str(data["test_data_valid"]["email"]))
    driver.find_element(by=By.XPATH, value="//*[@id='modal-select']//button[text()[contains(.,'Подобрать')]]").click()
    try:
        wait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//*[@id='modal-select']//*[text()[contains(.,'Заявка отправлена')]]")))
        print("   OK: модалка 'Подобрать участок' в 'Развитие - Глазами инвестора'")
        driver.find_element(by=By.XPATH, value="//*[@id='modal-select']/div/div/*[@uk-close]").click()
    except:
        print("ERROR: не отправлены данные: модалка 'Подобрать участок' в 'Развитие - Глазами инвестора'")
except:
    print("ERROR: не могу взаимодействовать: модалка 'Подобрать участок' в 'Развитие - Глазами инвестора'")

# модалка 'Заказать услугу' в 'Развитие - Капитализация'
try:
    driver.get("https://moigektar.ru/investment/capitalization")
    driver.find_element(by=By.XPATH, value="//*[@uk-toggle='target: #modal-capitalization']").click()
    driver.find_element(by=By.CSS_SELECTOR, value="#modal-capitalization #consultationform-name").send_keys(str(data["test_data_valid"]["name"]))
    driver.find_element(by=By.CSS_SELECTOR, value="#modal-capitalization #consultationform-phone").send_keys(str(data["test_data_valid"]["phone"]))
    driver.find_element(by=By.CSS_SELECTOR, value="#modal-capitalization #consultationform-email").send_keys(str(data["test_data_valid"]["email"]))
    driver.find_element(by=By.XPATH, value="//*[@id='modal-capitalization']//button[text()[contains(.,'Заказать')]]").click()
    try:
        wait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//*[@id='modal-capitalization']//*[text()[contains(.,'Заявка отправлена')]]")))
        print("   OK: модалка 'Заказать услугу' в 'Развитие - Капитализация'")
        driver.find_element(by=By.XPATH, value="//*[@id='modal-capitalization']/div/div/*[@uk-close]").click()
    except:
        print("ERROR: не отправлены данные: модалка 'Заказать услугу' в 'Развитие - Капитализация'")
except:
    print("ERROR: не могу взаимодействовать: модалка 'Заказать услугу' в 'Развитие - Капитализация'")

# модалка 'Заказать услугу' в 'Развитие - Базовая'
try:
    driver.get("https://moigektar.ru/investment/basic")
    driver.find_element(by=By.XPATH, value="//*[@uk-toggle='target: #modal-select']").click()
    driver.find_element(by=By.CSS_SELECTOR, value="#modal-select #consultationform-name").send_keys(str(data["test_data_valid"]["name"]))
    driver.find_element(by=By.CSS_SELECTOR, value="#modal-select #consultationform-phone").send_keys(str(data["test_data_valid"]["phone"]))
    driver.find_element(by=By.CSS_SELECTOR, value="#modal-select #consultationform-email").send_keys(str(data["test_data_valid"]["email"]))
    driver.find_element(by=By.XPATH, value="//*[@id='modal-select']//button[text()[contains(.,'Заказать')]]").click()
    try:
        wait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//*[@id='modal-select']//*[text()[contains(.,'Заявка отправлена')]]")))
        print("   OK: модалка 'Заказать услугу' в 'Развитие - Базовая'")
        driver.find_element(by=By.XPATH, value="//*[@id='modal-select']/div/div/*[@uk-close]").click()
    except:
        print("ERROR: не отправлены данные: модалка 'Заказать услугу' в 'Развитие - Базовая'")
except:
    print("ERROR: не могу взаимодействовать: модалка 'Заказать услугу' в 'Развитие - Базовая'")

# модалка 'Заказать услугу' в 'Развитие - Предприниматель'
try:
    driver.get("https://moigektar.ru/investment/businessman")
    driver.find_element(by=By.XPATH, value="//*[@uk-toggle='target: #modal-select']").click()
    driver.find_element(by=By.CSS_SELECTOR, value="#modal-select #consultationform-name").send_keys(str(data["test_data_valid"]["name"]))
    driver.find_element(by=By.CSS_SELECTOR, value="#modal-select #consultationform-phone").send_keys(str(data["test_data_valid"]["phone"]))
    driver.find_element(by=By.CSS_SELECTOR, value="#modal-select #consultationform-email").send_keys(str(data["test_data_valid"]["email"]))
    driver.find_element(by=By.XPATH, value="//*[@id='modal-select']//button[text()[contains(.,'Задать')]]").click()
    try:
        wait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//*[@id='modal-select']//*[text()[contains(.,'Заявка отправлена')]]")))
        print("   OK: модалка 'Заказать услугу' в 'Развитие - Предприниматель'")
        driver.find_element(by=By.XPATH, value="//*[@id='modal-select']/div/div/*[@uk-close]").click()
    except:
        print("ERROR: не отправлены данные: модалка 'Заказать услугу' в 'Развитие - Предприниматель'")
except:
    print("ERROR: не могу взаимодействовать: модалка 'Заказать услугу' в 'Развитие - Предприниматель'")

# модалка 'Заказать услугу' в 'Развитие - Фермер'
try:
    driver.get("https://moigektar.ru/investment/farmer")
    driver.find_element(by=By.XPATH, value="//*[@uk-toggle='target: #modal-select']").click()
    driver.find_element(by=By.CSS_SELECTOR, value="#modal-select #consultationform-name").send_keys(str(data["test_data_valid"]["name"]))
    driver.find_element(by=By.CSS_SELECTOR, value="#modal-select #consultationform-phone").send_keys(str(data["test_data_valid"]["phone"]))
    driver.find_element(by=By.CSS_SELECTOR, value="#modal-select #consultationform-email").send_keys(str(data["test_data_valid"]["email"]))
    driver.find_element(by=By.XPATH, value="//*[@id='modal-select']//button[text()[contains(.,'Получить')]]").click()
    try:
        wait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//*[@id='modal-select']//*[text()[contains(.,'Заявка отправлена')]]")))
        print("   OK: модалка 'Заказать услугу' в 'Развитие - Фермер'")
        driver.find_element(by=By.XPATH, value="//*[@id='modal-select']/div/div/*[@uk-close]").click()
    except:
        print("ERROR: не отправлены данные: модалка 'Заказать услугу' в 'Развитие - Фермер'")
except:
    print("ERROR: не могу взаимодействовать: модалка 'Заказать услугу' в 'Развитие - Фермер'")

# модалка 'Заказать услугу' в 'Развитие - Фамильная'
try:
    driver.get("https://moigektar.ru/investment/family")
    driver.find_element(by=By.XPATH, value="//*[@uk-toggle='target: #modal-select']").click()
    driver.find_element(by=By.CSS_SELECTOR, value="#modal-select #consultationform-name").send_keys(str(data["test_data_valid"]["name"]))
    driver.find_element(by=By.CSS_SELECTOR, value="#modal-select #consultationform-phone").send_keys(str(data["test_data_valid"]["phone"]))
    driver.find_element(by=By.CSS_SELECTOR, value="#modal-select #consultationform-email").send_keys(str(data["test_data_valid"]["email"]))
    driver.find_element(by=By.XPATH, value="//*[@id='modal-select']//button[text()[contains(.,'Получить')]]").click()
    try:
        wait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//*[@id='modal-select']//*[text()[contains(.,'Заявка отправлена')]]")))
        print("   OK: модалка 'Заказать услугу' в 'Развитие - Фамильная'\n")
        driver.find_element(by=By.XPATH, value="//*[@id='modal-select']/div/div/*[@uk-close]").click()
    except:
        print("ERROR: не отправлены данные: модалка 'Заказать услугу' в 'Развитие - Фамильная'\n")
except:
    print("ERROR: не могу взаимодействовать: модалка 'Заказать услугу' в 'Развитие - Фамильная'\n")


# Услуги - 'Коллективное строительство ЛЭП'
print('Услуги')

# модалка 'Заказать услугу' в 'Коллективное строительство ЛЭП'
try:
    driver.get("https://moigektar.ru/services/kollektivnoe-stroitelstvo-liniy-elektroperedach")
    driver.find_element(by=By.XPATH, value="//div[@class]/*[@uk-toggle='target: #modal-specialist']").click()
    driver.find_element(by=By.CSS_SELECTOR, value="#modal-specialist #consultationform-name").send_keys(str(data["test_data_valid"]["name"]))
    driver.find_element(by=By.CSS_SELECTOR, value="#modal-specialist #consultationform-phone").send_keys(str(data["test_data_valid"]["phone"]))
    driver.find_element(by=By.CSS_SELECTOR, value="#modal-specialist #consultationform-email").send_keys(str(data["test_data_valid"]["email"]))
    driver.find_element(by=By.XPATH, value="//*[@id='modal-specialist']//button[text()[contains(.,'Заказать')]]").click()
    try:
        wait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//*[@id='modal-specialist']//*[text()[contains(.,'Заявка отправлена')]]")))
        print("   OK: модалка 'Заказать услугу' в 'Коллективное строительство ЛЭП'")
        driver.find_element(by=By.XPATH, value="//*[@id='modal-specialist']/div/div/*[@uk-close]").click()
    except:
        print("ERROR: не отправлены данные: модалка 'Заказать услугу' в 'Коллективное строительство ЛЭП'")
except:
    print("ERROR: не могу взаимодействовать: модалка 'Заказать услугу' в 'Коллективное строительство ЛЭП'")

# модалка 'Получить консультацию' в 'Коллективное строительство ЛЭП'
try:
    driver.find_element(by=By.XPATH, value="//div[@class]/*[@uk-toggle='target: #modal-specialist1']").click()
    driver.find_element(by=By.CSS_SELECTOR, value="#modal-specialist1 #consultationform-name").send_keys(str(data["test_data_valid"]["name"]))
    driver.find_element(by=By.CSS_SELECTOR, value="#modal-specialist1 #consultationform-phone").send_keys(str(data["test_data_valid"]["phone"]))
    driver.find_element(by=By.CSS_SELECTOR, value="#modal-specialist1 #consultationform-email").send_keys(str(data["test_data_valid"]["email"]))
    driver.find_element(by=By.XPATH, value="//*[@id='modal-specialist1']//button[text()[contains(.,'Отправить')]]").click()
    try:
        wait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//*[@id='modal-specialist1']//*[text()[contains(.,'Заявка отправлена')]]")))
        print("   OK: модалка 'Получить консультацию' в 'Коллективное строительство ЛЭП'\n")
        driver.find_element(by=By.XPATH, value="//*[@id='modal-specialist1']/div/div/*[@uk-close]\n").click()
    except:
        print("ERROR: не отправлены данные: модалка 'Получить консультацию' в 'Коллективное строительство ЛЭП'\n")
except:
    print("ERROR: не могу взаимодействовать: модалка 'Получить консультацию' в 'Коллективное строительство ЛЭП'\n")


# Бизнес-планы
print("Бизнес-планы")

# модалка 'Получить консультацию' в 'Бизнес-планы' на первой карточке
try:
    driver.get("https://moigektar.ru/business-plans")
    driver.find_element(by=By.XPATH, value="//div[@data-key='1']//*[@uk-toggle='target: #modal-main']").click()
    driver.find_element(by=By.CSS_SELECTOR, value="#modal-main #consultationform-name").send_keys(str(data["test_data_valid"]["name"]))
    driver.find_element(by=By.CSS_SELECTOR, value="#modal-main #consultationform-phone").send_keys(str(data["test_data_valid"]["phone"]))
    driver.find_element(by=By.CSS_SELECTOR, value="#modal-main #consultationform-email").send_keys(str(data["test_data_valid"]["email"]))
    driver.find_element(by=By.XPATH, value="//*[@id='modal-main']//button[text()[contains(.,'Отправить')]]").click()
    try:
        wait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//*[@id='modal-main']//*[text()[contains(.,'Заявка отправлена')]]")))
        print("   OK: модалка 'Получить консультацию' в 'Бизнес-планы'\n")
        driver.find_element(by=By.XPATH, value="//*[@id='modal-main']/div/div/*[@uk-close]").click()
    except:
        print("ERROR: не отправлены данные: модалка 'Получить консультацию' в 'Бизнес-планы'\n")
except:
    print("ERROR: не могу взаимодействовать: модалка 'Получить консультацию' в 'Бизнес-планы'\n")

# Вакансии
print("Вакансии")

# модалка 'Оставьте анкету' в 'Вакансии'
try:
    driver.get("https://moigektar.ru/hr")
    driver.find_element(by=By.XPATH, value="//div/div[1]/div/div/div/*[@uk-toggle='target: #modal-main1']").click()
    driver.find_element(by=By.CSS_SELECTOR, value="#modal-main1 #consultationform-name").send_keys(str(data["test_data_valid"]["name"]))
    driver.find_element(by=By.CSS_SELECTOR, value="#modal-main1 #consultationform-phone").send_keys(str(data["test_data_valid"]["phone"]))
    driver.find_element(by=By.CSS_SELECTOR, value="#modal-main1 #consultationform-email").send_keys(str(data["test_data_valid"]["email"]))
    driver.find_element(by=By.XPATH, value="//*[@id='modal-main1']//button[text()[contains(.,'Отправить')]]").click()
    try:
        wait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//*[@id='modal-main1']//*[text()[contains(.,'Заявка отправлена')]]")))
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
    wait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//*[@id='modal-main1']//*[text()[contains(.,'Заявка отправлена')]]")))
    print("   OK: модалка 'Оставьте анкету' по первой красной кнопке в 'Вакансии'")
    driver.find_element(by=By.XPATH, value="//*[@id='modal-main1']/div/div/*[@uk-close]").click()
except:
    print("ERROR: не могу взаимодействовать: модалка 'Оставьте анкету' по первой красной кнопке в 'Вакансии'")
# проверка вызова этой мод. со второй кнопки "Запишитесь на собеседование"
try:
    driver.find_element(by=By.XPATH, value="//h1[text()[contains(., 'Мы предлагаем')]]//parent::div//div[@class='uk-text-center@s']//*[@uk-toggle='target: #modal-main1']").click()
    wait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//*[@id='modal-main1']//*[text()[contains(.,'Заявка отправлена')]]")))
    print("   OK: модалка 'Оставьте анкету' по второй красной кнопке в 'Вакансии'")
    driver.find_element(by=By.XPATH, value="//*[@id='modal-main1']/div/div/*[@uk-close]").click()
except:
    print("ERROR: не могу взаимодействовать: модалка 'Оставьте анкету' по второй красной кнопке в 'Вакансии'")


#time.sleep(8)
driver.quit()

