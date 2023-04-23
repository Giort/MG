from selenium import webdriver
from selenium.webdriver.chrome.options import Options
ch_options = Options()
ch_options.add_argument('--headless')
ch_options.page_load_strategy = 'eager'
driver = webdriver.Chrome(options=ch_options)
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait as wait
import time
import json
from selenium.webdriver.common.action_chains import ActionChains
actions = ActionChains(driver)
driver.implicitly_wait(10)
driver.set_window_size(1660, 1000)

with open('data.json', 'r') as file:
    data = json.load(file)
    
# Скрипт заполняет каждую форму корректными данными
#
# В лог выводится сообщение "ОК", если данные были отправлены и отобразилось сообщение об успехе
# В лог выводится сообщение "ERROR", если это сообщение не отобразилось
# В лог выводится сообщение "ERROR", если форма не была найдена по селектору
#


# 1. проверка главной страницы "МГ"
driver.get("https://moigektar.ru/")
# 1.1 проверка формы "Хотите узнать подробнее о проекте?"
try:
    title = driver.find_element(by=By.XPATH, value="//b[text()[contains(.,'Хотите узнать ')]]")
    actions.move_to_element(title).click().perform()
    # сохраняю текущий динамический id формы в переменную для того, чтобы последующие локаторы не были такого вида:
    # //h1/*[text()[contains(.,'Хотите узнать')]]//parent::h1//following-sibling::ul[2]//input[@id='consultationform-phone']
    form_id = driver.find_element(by=By.XPATH, value='//b[text()[contains(.,"Хотите узнать")]]//ancestor::div[2]').get_attribute('id')
    driver.find_element(by=By.XPATH, value="//div[@id='"+ form_id +"']//*[@id='consultationform-name']").send_keys(str(data["test_data_valid"]["name"]))
    driver.find_element(by=By.XPATH, value="//div[@id='"+ form_id +"']//*[@id='consultationform-phone']").send_keys(str(data["test_data_valid"]["phone"]))
    driver.find_element(by=By.XPATH, value="//div[@id='"+ form_id +"']//*[@id='consultationform-email']").send_keys(str(data["test_data_valid"]["email"]))
    driver.find_element(by=By.XPATH, value="//div[@id='"+ form_id +"']//*[text()[contains(.,'Отправить')]]").click()
    try:
        wait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//div[@id='"+ form_id +"']//*[text()[contains(.,'Заявка успешно отправлена')]]")))
        print(" OK: главная 1/4 данные были отправлены")
    except:
        print('ERROR: не отправлены данные в форму "Хотите узнать подробнее о проекте?" на Главной')
except:
    print('ERROR: не могу найти форму "Хотите узнать подробнее о проекте?" на Главной')

# 1.2 проверка формы "Получите каталог посёлков"
try:
    form_id = driver.find_element(by=By.XPATH, value='//b[text()[contains(.,"Получите каталог")]]//ancestor::div[2]').get_attribute('id')
    driver.find_element(by=By.XPATH, value="//div[@id='"+ form_id +"']//*[@id='consultationform-name']").send_keys(str(data["test_data_valid"]["name"]))
    driver.find_element(by=By.XPATH, value="//div[@id='"+ form_id +"']//*[@id='consultationform-phone']").send_keys(str(data["test_data_valid"]["phone"]))
    driver.find_element(by=By.XPATH, value="//div[@id='"+ form_id +"']//*[@id='consultationform-email']").send_keys(str(data["test_data_valid"]["email"]))
    driver.find_element(by=By.XPATH, value="//div[@id='"+ form_id +"']//*[text()[contains(.,'Получить')]]").click()
    try:
        wait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//div[@id='"+ form_id +"']//*[text()[contains(.,'Заявка успешно отправлена')]]")))
        print(" OK: главная 2/4 данные были отправлены")
    except:
        print('ERROR: не отправлены данные в форму "Получите каталог" на Главной')
except:
    print('ERROR: не могу найти форму "Получите каталог" на Главной')

# 1.3 проверка формы "Подпишитесь на рассылку"
try:
    form_id = driver.find_element(by=By.XPATH, value='//b[text()[contains(.,"Подпишитесь на рассылку")]]//ancestor::div[2]').get_attribute('id')
    driver.find_element(by=By.XPATH, value="//div[@id='"+ form_id +"']//*[@id='consultationform-email']").send_keys(str(data["test_data_valid"]["email"]))
    driver.find_element(by=By.XPATH, value="//div[@id='"+ form_id +"']//*[text()[contains(.,'Подписаться')]]").click()
    try:
        wait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//div[@id='"+ form_id +"']//*[text()[contains(.,'Заявка успешно отправлена')]]")))
        print(" OK: главная 3/4 данные были отправлены")
    except:
        print('ERROR: не отправлены данные в форму "Подпишитесь на рассылку" на Главной')
except:
    print('ERROR: не могу найти форму "Подпишитесь на рассылку" на Главной')

# 1.4 проверка формы "Действуйте! Лучшие участки уже бронируют"
try:
    form_id = driver.find_element(by=By.XPATH, value='//b[text()[contains(.,"Действуйте!")]]//ancestor::div[2]').get_attribute('id')
    driver.find_element(by=By.XPATH, value="//div[@id='"+ form_id +"']//*[@id='consultationform-name']").send_keys(str(data["test_data_valid"]["name"]))
    driver.find_element(by=By.XPATH, value="//div[@id='"+ form_id +"']//*[@id='consultationform-phone']").send_keys(str(data["test_data_valid"]["phone"]))
    driver.find_element(by=By.XPATH, value="//div[@id='"+ form_id +"']//*[text()[contains(.,'Узнать')]]").click()
    try:
        wait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//div[@id='"+ form_id +"']//*[text()[contains(.,'Заявка успешно отправлена')]]")))
        print(" OK: главная 4/4 данные были отправлены")
    except:
        print('ERROR: не отправлены данные в форму "Действуйте" на Главной')
except:
    print('ERROR: не могу найти форму "Действуйте" на Главной')


# 2. проверка раздела "О проекте"
# 2.1 переход на страницу "О проекте"
driver.get("https://moigektar.ru/about")
try:
    form_id = driver.find_element(by=By.XPATH, value='//b[text()[contains(.,"Хотите узнать")]]//ancestor::div[2]').get_attribute('id')
    driver.find_element(by=By.XPATH, value="//div[@id='"+ form_id +"']//*[@id='consultationform-name']").send_keys(str(data["test_data_valid"]["name"]))
    driver.find_element(by=By.XPATH, value="//div[@id='"+ form_id +"']//*[@id='consultationform-phone']").send_keys(str(data["test_data_valid"]["phone"]))
    driver.find_element(by=By.XPATH, value="//div[@id='"+ form_id +"']//*[@id='consultationform-email']").send_keys(str(data["test_data_valid"]["email"]))
    driver.find_element(by=By.XPATH, value="//div[@id='"+ form_id +"']//*[text()[contains(.,'Отправить')]]").click()
    try:
        wait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//div[@id='"+ form_id +"']//*[text()[contains(.,'Заявка успешно отправлена')]]")))
        print(" OK: о проекте 1/6 данные были отправлены")
    except:
        print('ERROR: не отправлены данные в форму "Хотите узнать подробнее о проекте?" в "О проекте"')
except:
    print('ERROR: не могу найти форму "Хотите узнать подробнее о проекте?" в "О проекте"')

# 2.2 переход на страницу "О проекте - сервисная компания"
driver.get("https://moigektar.ru/about/management")
try:
    form_id = driver.find_element(by=By.XPATH, value='//b[text()[contains(.,"Хотите узнать")]]//ancestor::div[2]').get_attribute('id')
    driver.find_element(by=By.XPATH, value="//div[@id='"+ form_id +"']//*[@id='consultationform-name']").send_keys(str(data["test_data_valid"]["name"]))
    driver.find_element(by=By.XPATH, value="//div[@id='"+ form_id +"']//*[@id='consultationform-phone']").send_keys(str(data["test_data_valid"]["phone"]))
    driver.find_element(by=By.XPATH, value="//div[@id='"+ form_id +"']//*[@id='consultationform-email']").send_keys(str(data["test_data_valid"]["email"]))
    driver.find_element(by=By.XPATH, value="//div[@id='"+ form_id +"']//*[text()[contains(.,'Отправить')]]").click()
    try:
        wait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//div[@id='"+ form_id +"']//*[text()[contains(.,'Заявка успешно отправлена')]]")))
        print(" OK: о проекте 2/6 данные были отправлены")
    except:
        print('ERROR: не отправлены данные в форму "Хотите узнать подробнее о проекте?" в "О проекте" - "Сервисная компания"')
except:
    print('ERROR: не могу найти форму "Хотите узнать подробнее о проекте?" в "О проекте" - "Сервисная компания"')

# 2.3 переход на страницу "О проекте - личный кабинет"
driver.get("https://moigektar.ru/about/cabinet")
try:
    form_id = driver.find_element(by=By.XPATH, value='//b[text()[contains(.,"Хотите узнать")]]//ancestor::div[2]').get_attribute('id')
    driver.find_element(by=By.XPATH, value="//div[@id='"+ form_id +"']//*[@id='consultationform-name']").send_keys(str(data["test_data_valid"]["name"]))
    driver.find_element(by=By.XPATH, value="//div[@id='"+ form_id +"']//*[@id='consultationform-phone']").send_keys(str(data["test_data_valid"]["phone"]))
    driver.find_element(by=By.XPATH, value="//div[@id='"+ form_id +"']//*[@id='consultationform-email']").send_keys(str(data["test_data_valid"]["email"]))
    driver.find_element(by=By.XPATH, value="//div[@id='"+ form_id +"']//*[text()[contains(.,'Отправить')]]").click()
    try:
        wait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//div[@id='"+ form_id +"']//*[text()[contains(.,'Заявка успешно отправлена')]]")))
        print(" OK: о проекте 3/6 данные были отправлены")
    except:
        print('ERROR: не отправлены данные в форму "Хотите узнать подробнее о проекте?" в "О проекте" - "Личный кабинет"')
except:
    print('ERROR: не могу найти форму "Хотите узнать подробнее о проекте?" в "О проекте" - "Личный кабинет"')

# 2.4 переход на страницу "О проекте - партнеры"
driver.get("https://moigektar.ru/about/advantages")
try:
    form_id = driver.find_element(by=By.XPATH, value='//b[text()[contains(.,"Хотите узнать")]]//ancestor::div[2]').get_attribute('id')
    driver.find_element(by=By.XPATH, value="//div[@id='"+ form_id +"']//*[@id='consultationform-name']").send_keys(str(data["test_data_valid"]["name"]))
    driver.find_element(by=By.XPATH, value="//div[@id='"+ form_id +"']//*[@id='consultationform-phone']").send_keys(str(data["test_data_valid"]["phone"]))
    driver.find_element(by=By.XPATH, value="//div[@id='"+ form_id +"']//*[@id='consultationform-email']").send_keys(str(data["test_data_valid"]["email"]))
    driver.find_element(by=By.XPATH, value="//div[@id='"+ form_id +"']//*[text()[contains(.,'Отправить')]]").click()
    try:
        wait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//div[@id='"+ form_id +"']//*[text()[contains(.,'Заявка успешно отправлена')]]")))
        print(" OK: о проекте 4/6 данные были отправлены")
    except:
        print('ERROR: не отправлены данные в форму "Хотите узнать подробнее о проекте?" в "О проекте" - "Партнеры"')
except:
    print('ERROR: не могу найти форму "Хотите узнать подробнее о проекте?" в "О проекте" - "Партнеры"')

# 2.5 переход на страницу "О проекте - союз садоводов"
driver.get("https://moigektar.ru/about/union")
try:
    form_id = driver.find_element(by=By.XPATH, value='//b[text()[contains(.,"Хотите узнать")]]//ancestor::div[2]').get_attribute('id')
    driver.find_element(by=By.XPATH, value="//div[@id='"+ form_id +"']//*[@id='consultationform-name']").send_keys(str(data["test_data_valid"]["name"]))
    driver.find_element(by=By.XPATH, value="//div[@id='"+ form_id +"']//*[@id='consultationform-phone']").send_keys(str(data["test_data_valid"]["phone"]))
    driver.find_element(by=By.XPATH, value="//div[@id='"+ form_id +"']//*[@id='consultationform-email']").send_keys(str(data["test_data_valid"]["email"]))
    driver.find_element(by=By.XPATH, value="//div[@id='"+ form_id +"']//*[text()[contains(.,'Отправить')]]").click()
    try:
        wait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//div[@id='"+ form_id +"']//*[text()[contains(.,'Заявка успешно отправлена')]]")))
        print(" OK: о проекте 5/6 данные были отправлены")
    except:
        print('ERROR: не отправлены данные в форму "Хотите узнать подробнее о проекте?" в "О проекте" - "Союз садоводов"')
except:
    print('ERROR: не могу найти форму "Хотите узнать подробнее о проекте?" в "О проекте" - "Союз садоводов"')

# 2.6 переход на страницу "О проекте - отзывы"
driver.get("https://moigektar.ru/about/reviews")
try:
    form_id = driver.find_element(by=By.XPATH, value='//b[text()[contains(.,"Хотите узнать")]]//ancestor::div[2]').get_attribute('id')
    driver.find_element(by=By.XPATH, value="//div[@id='"+ form_id +"']//*[@id='consultationform-name']").send_keys(str(data["test_data_valid"]["name"]))
    driver.find_element(by=By.XPATH, value="//div[@id='"+ form_id +"']//*[@id='consultationform-phone']").send_keys(str(data["test_data_valid"]["phone"]))
    driver.find_element(by=By.XPATH, value="//div[@id='"+ form_id +"']//*[@id='consultationform-email']").send_keys(str(data["test_data_valid"]["email"]))
    driver.find_element(by=By.XPATH, value="//div[@id='"+ form_id +"']//*[text()[contains(.,'Отправить')]]").click()
    try:
        wait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//div[@id='"+ form_id +"']//*[text()[contains(.,'Заявка успешно отправлена')]]")))
        print(" OK: о проекте 6/6 данные были отправлены")
    except:
        print('ERROR: не отправлены данные в форму "Хотите узнать подробнее о проекте?" в "О проекте" - "Отзывы"')
except:
    print('ERROR: не могу найти форму "Хотите узнать подробнее о проекте?" в "О проекте" - "Отзывы"')


# проверка страницы "Каталог поселков"
# переход на страницу "Каталог поселков"
driver.get("https://moigektar.ru/catalogue")
try:
    form_id = driver.find_element(by=By.XPATH, value='//b[text()[contains(.,"Хотите узнать")]]//ancestor::div[2]').get_attribute('id')
    driver.find_element(by=By.XPATH, value="//div[@id='"+ form_id +"']//*[@id='consultationform-name']").send_keys(str(data["test_data_valid"]["name"]))
    driver.find_element(by=By.XPATH, value="//div[@id='"+ form_id +"']//*[@id='consultationform-phone']").send_keys(str(data["test_data_valid"]["phone"]))
    driver.find_element(by=By.XPATH, value="//div[@id='"+ form_id +"']//*[@id='consultationform-email']").send_keys(str(data["test_data_valid"]["email"]))
    driver.find_element(by=By.XPATH, value="//div[@id='"+ form_id +"']//*[text()[contains(.,'Отправить')]]").click()
    time.sleep(8)
    url = driver.current_url
    if url == 'https://moigektar.ru/thanks':
        print(' OK: заявка из каталога отправлена, открылась страница благодарности')
    else:
        print('ERROR: не отправлены данные в форму "Хотите узнать подробнее о проекте?" в Каталоге')
except NoSuchElementException:
    print('ERROR: не могу найти форму "Хотите узнать подробнее о проекте?" в Каталоге')


# 4 проверка раздела "Развитие"
# 4.1 переход на страницу "Развитие - развитие поселков"
driver.get("https://moigektar.ru/growth")
try:
    form_id = driver.find_element(by=By.XPATH, value='//b[text()[contains(.,"Хотите узнать")]]//ancestor::div[2]').get_attribute('id')
    driver.find_element(by=By.XPATH, value="//div[@id='"+ form_id +"']//*[@id='consultationform-name']").send_keys(str(data["test_data_valid"]["name"]))
    driver.find_element(by=By.XPATH, value="//div[@id='"+ form_id +"']//*[@id='consultationform-phone']").send_keys(str(data["test_data_valid"]["phone"]))
    driver.find_element(by=By.XPATH, value="//div[@id='"+ form_id +"']//*[@id='consultationform-email']").send_keys(str(data["test_data_valid"]["email"]))
    driver.find_element(by=By.XPATH, value="//div[@id='"+ form_id +"']//*[text()[contains(.,'Отправить')]]").click()
    try:
        wait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//div[@id='"+ form_id +"']//*[text()[contains(.,'Заявка успешно отправлена')]]")))
        print(" OK: развитие 1/7 данные были отправлены")
    except:
        print('ERROR: не отправлены данные в форму "Хотите узнать подробнее об услугах и развитии?" в "Развитие" - "Развитие поселков"')
except:
    print('ERROR: не могу найти форму "Хотите узнать подробнее о проекте?" в "Развитие" - "Развитие поселков"')

# 4.2 переход на страницу "Развитие - глазами инвестора"
driver.get("https://moigektar.ru/investment")
try:
    form_id = driver.find_element(by=By.XPATH, value='//b[text()[contains(.,"Хотите узнать")]]//ancestor::div[2]').get_attribute('id')
    driver.find_element(by=By.XPATH, value="//div[@id='"+ form_id +"']//*[@id='consultationform-name']").send_keys(str(data["test_data_valid"]["name"]))
    driver.find_element(by=By.XPATH, value="//div[@id='"+ form_id +"']//*[@id='consultationform-phone']").send_keys(str(data["test_data_valid"]["phone"]))
    driver.find_element(by=By.XPATH, value="//div[@id='"+ form_id +"']//*[@id='consultationform-email']").send_keys(str(data["test_data_valid"]["email"]))
    driver.find_element(by=By.XPATH, value="//div[@id='"+ form_id +"']//*[text()[contains(.,'Отправить')]]").click()
    try:
        wait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//div[@id='"+ form_id +"']//*[text()[contains(.,'Заявка успешно отправлена')]]")))
        print(" OK: развитие 2/7 данные были отправлены")
    except:
        print('ERROR: не отправлены данные в форму "Хотите узнать подробнее о проекте?" в "Развитие" - "Глазами инвестора"')
except:
    print('ERROR: не могу найти форму "Хотите узнать подробнее о проекте?" в "Развитие" - "Глазами инвестора"')

# 4.3 переход на страницу "Развитие - капитализация"
driver.get("https://moigektar.ru/investment/capitalization")
try:
    form_id = driver.find_element(by=By.XPATH, value='//b[text()[contains(.,"Хотите узнать")]]//ancestor::div[2]').get_attribute('id')
    driver.find_element(by=By.XPATH, value="//div[@id='"+ form_id +"']//*[@id='consultationform-name']").send_keys(str(data["test_data_valid"]["name"]))
    driver.find_element(by=By.XPATH, value="//div[@id='"+ form_id +"']//*[@id='consultationform-phone']").send_keys(str(data["test_data_valid"]["phone"]))
    driver.find_element(by=By.XPATH, value="//div[@id='"+ form_id +"']//*[@id='consultationform-email']").send_keys(str(data["test_data_valid"]["email"]))
    driver.find_element(by=By.XPATH, value="//div[@id='"+ form_id +"']//*[text()[contains(.,'Отправить')]]").click()
    try:
        wait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//div[@id='"+ form_id +"']//*[text()[contains(.,'Заявка успешно отправлена')]]")))
        print(" OK: развитие 3/7 данные были отправлены")
    except:
        print('ERROR: не отправлены данные в форму "Хотите узнать подробнее о проекте?" в "Развитие" - "Капитализация"')
except:
    print('ERROR: не могу найти форму "Хотите узнать подробнее о проекте?" в "Развитие" - "Капитализация"')

# 4.4 переход на страницу "Развитие - базовая стратегия"
driver.get("https://moigektar.ru/investment/basic")
try:
    form_id = driver.find_element(by=By.XPATH, value='//b[text()[contains(.,"Хотите узнать")]]//ancestor::div[2]').get_attribute('id')
    driver.find_element(by=By.XPATH, value="//div[@id='"+ form_id +"']//*[@id='consultationform-name']").send_keys(str(data["test_data_valid"]["name"]))
    driver.find_element(by=By.XPATH, value="//div[@id='"+ form_id +"']//*[@id='consultationform-phone']").send_keys(str(data["test_data_valid"]["phone"]))
    driver.find_element(by=By.XPATH, value="//div[@id='"+ form_id +"']//*[@id='consultationform-email']").send_keys(str(data["test_data_valid"]["email"]))
    driver.find_element(by=By.XPATH, value="//div[@id='"+ form_id +"']//*[text()[contains(.,'Отправить')]]").click()
    try:
        wait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//div[@id='"+ form_id +"']//*[text()[contains(.,'Заявка успешно отправлена')]]")))
        print(" OK: развитие 4/7 данные были отправлены")
    except:
        print('ERROR: не отправлены данные в форму "Хотите узнать подробнее о проекте?" в "Развитие" - "Базовая стратегия"')
except:
    print('ERROR: не могу найти форму "Хотите узнать подробнее о проекте?" в "Развитие" - "Базовая стратегия"')

# 4.5 переход на страницу "Развитие - предприниматель"
driver.get("https://moigektar.ru/investment/businessman")
try:
    form_id = driver.find_element(by=By.XPATH, value='//b[text()[contains(.,"Хотите узнать")]]//ancestor::div[2]').get_attribute('id')
    driver.find_element(by=By.XPATH, value="//div[@id='"+ form_id +"']//*[@id='consultationform-name']").send_keys(str(data["test_data_valid"]["name"]))
    driver.find_element(by=By.XPATH, value="//div[@id='"+ form_id +"']//*[@id='consultationform-phone']").send_keys(str(data["test_data_valid"]["phone"]))
    driver.find_element(by=By.XPATH, value="//div[@id='"+ form_id +"']//*[@id='consultationform-email']").send_keys(str(data["test_data_valid"]["email"]))
    driver.find_element(by=By.XPATH, value="//div[@id='"+ form_id +"']//*[text()[contains(.,'Отправить')]]").click()
    try:
        wait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//div[@id='"+ form_id +"']//*[text()[contains(.,'Заявка успешно отправлена')]]")))
        print(" OK: развитие 5/7 данные были отправлены")
    except:
        print('ERROR: не отправлены данные в форму "Хотите узнать подробнее о проекте?" в "Развитие" - "Предприниматель"')
except:
    print('ERROR: не могу найти форму "Хотите узнать подробнее о проекте?" в "Развитие" - "Предприниматель"')

# 4.6 переход на страницу "Развитие - фермер-садовод"
driver.get("https://moigektar.ru/investment/farmer")
try:
    form_id = driver.find_element(by=By.XPATH, value='//b[text()[contains(.,"Хотите узнать")]]//ancestor::div[2]').get_attribute('id')
    driver.find_element(by=By.XPATH, value="//div[@id='"+ form_id +"']//*[@id='consultationform-name']").send_keys(str(data["test_data_valid"]["name"]))
    driver.find_element(by=By.XPATH, value="//div[@id='"+ form_id +"']//*[@id='consultationform-phone']").send_keys(str(data["test_data_valid"]["phone"]))
    driver.find_element(by=By.XPATH, value="//div[@id='"+ form_id +"']//*[@id='consultationform-email']").send_keys(str(data["test_data_valid"]["email"]))
    driver.find_element(by=By.XPATH, value="//div[@id='"+ form_id +"']//*[text()[contains(.,'Отправить')]]").click()
    try:
        wait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//div[@id='"+ form_id +"']//*[text()[contains(.,'Заявка успешно отправлена')]]")))
        print(" OK: развитие 6/7 данные были отправлены")
    except:
        print('ERROR: не отправлены данные в форму "Хотите узнать подробнее о проекте?" в "Развитие" - "Фермер-садовод"')
except:
    print('ERROR: не могу найти форму "Хотите узнать подробнее о проекте?" в "Развитие" - "Фермер-садовод"')

# 4.7 переход на страницу "Развитие - фамильная усадьба"
driver.get("https://moigektar.ru/investment/family")
try:
    form_id = driver.find_element(by=By.XPATH, value='//b[text()[contains(.,"Хотите узнать")]]//ancestor::div[2]').get_attribute('id')
    driver.find_element(by=By.XPATH, value="//div[@id='"+ form_id +"']//*[@id='consultationform-name']").send_keys(str(data["test_data_valid"]["name"]))
    driver.find_element(by=By.XPATH, value="//div[@id='"+ form_id +"']//*[@id='consultationform-phone']").send_keys(str(data["test_data_valid"]["phone"]))
    driver.find_element(by=By.XPATH, value="//div[@id='"+ form_id +"']//*[@id='consultationform-email']").send_keys(str(data["test_data_valid"]["email"]))
    driver.find_element(by=By.XPATH, value="//div[@id='"+ form_id +"']//*[text()[contains(.,'Отправить')]]").click()
    try:
        wait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//div[@id='"+ form_id +"']//*[text()[contains(.,'Заявка успешно отправлена')]]")))
        print(" OK: развитие 7/7 данные были отправлены")
    except:
        print('ERROR: не отправлены данные в форму "Хотите узнать подробнее о проекте?" в "Развитие" - "Фамильная усадьба"')
except:
    print('ERROR: не могу найти форму "Хотите узнать подробнее о проекте?" в "Развитие" - "Фамильная усадьба"')


# 5 проверка раздела "Меры поддержки"
# 5.1 переход на страницу "Меры поддержки - государственная поддержка"
driver.get("https://moigektar.ru/documents/gos")
try:
    form_id = driver.find_element(by=By.XPATH, value='//b[text()[contains(.,"Хотите узнать")]]//ancestor::div[2]').get_attribute('id')
    driver.find_element(by=By.XPATH, value="//div[@id='"+ form_id +"']//*[@id='consultationform-name']").send_keys(str(data["test_data_valid"]["name"]))
    driver.find_element(by=By.XPATH, value="//div[@id='"+ form_id +"']//*[@id='consultationform-phone']").send_keys(str(data["test_data_valid"]["phone"]))
    driver.find_element(by=By.XPATH, value="//div[@id='"+ form_id +"']//*[@id='consultationform-email']").send_keys(str(data["test_data_valid"]["email"]))
    driver.find_element(by=By.XPATH, value="//div[@id='"+ form_id +"']//*[text()[contains(.,'Отправить')]]").click()
    try:
        wait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//div[@id='"+ form_id +"']//*[text()[contains(.,'Заявка успешно отправлена')]]")))
        print(" OK: меры поддержки 1/6 данные были отправлены")
    except:
        print('ERROR: не отправлены данные в форму "Хотите узнать подробнее о господдержке?" в "Меры поддержки" - "Государственная поддержка"')
except:
    print('ERROR: не могу найти форму "Хотите узнать подробнее о господдержке?" в "Меры поддержки" - "Государственная поддержка"')

# 5.2 переход на страницу "Меры поддержки - для владельцев земли"
driver.get("https://moigektar.ru/documents")
try:
    form_id = driver.find_element(by=By.XPATH, value='//b[text()[contains(.,"Хотите узнать")]]//ancestor::div[2]').get_attribute('id')
    driver.find_element(by=By.XPATH, value="//div[@id='"+ form_id +"']//*[@id='consultationform-name']").send_keys(str(data["test_data_valid"]["name"]))
    driver.find_element(by=By.XPATH, value="//div[@id='"+ form_id +"']//*[@id='consultationform-phone']").send_keys(str(data["test_data_valid"]["phone"]))
    driver.find_element(by=By.XPATH, value="//div[@id='"+ form_id +"']//*[@id='consultationform-email']").send_keys(str(data["test_data_valid"]["email"]))
    driver.find_element(by=By.XPATH, value="//div[@id='"+ form_id +"']//*[text()[contains(.,'Отправить')]]").click()
    try:
        wait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//div[@id='"+ form_id +"']//*[text()[contains(.,'Заявка успешно отправлена')]]")))
        print(" OK: меры поддержки 2/6 данные были отправлены")
    except:
        print('ERROR: не отправлены данные в форму "Хотите узнать подробнее о господдержке?" в "Меры поддержки" - "Для владельцев земли"')
except:
    print('ERROR: не могу найти форму "Хотите узнать подробнее о господдержке?" в "Меры поддержки" - "Для владельцев земли"')

# 5.3 переход на страницу "Меры поддержки - грант Фермер"
driver.get("https://moigektar.ru/documents/farmer")
try:
    form_id = driver.find_element(by=By.XPATH, value='//b[text()[contains(.,"Хотите узнать")]]//ancestor::div[2]').get_attribute('id')
    driver.find_element(by=By.XPATH, value="//div[@id='"+ form_id +"']//*[@id='consultationform-name']").send_keys(str(data["test_data_valid"]["name"]))
    driver.find_element(by=By.XPATH, value="//div[@id='"+ form_id +"']//*[@id='consultationform-phone']").send_keys(str(data["test_data_valid"]["phone"]))
    driver.find_element(by=By.XPATH, value="//div[@id='"+ form_id +"']//*[@id='consultationform-email']").send_keys(str(data["test_data_valid"]["email"]))
    driver.find_element(by=By.XPATH, value="//div[@id='"+ form_id +"']//*[text()[contains(.,'Отправить')]]").click()
    try:
        wait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//div[@id='"+ form_id +"']//*[text()[contains(.,'Заявка успешно отправлена')]]")))
        print(" OK: меры поддержки 3/6 данные были отправлены")
    except:
        print('ERROR: не отправлены данные в форму "Хотите узнать подробнее о господдержке?" в "Меры поддержки" - "Грант "Фермер"')
except:
    print('ERROR: не могу найти форму "Хотите узнать подробнее о господдержке?" в "Меры поддержки" - "Грант "Фермер"')

# 5.4 переход на страницу "Меры поддержки - Агростартап"
driver.get("https://moigektar.ru/documents/startup")
try:
    form_id = driver.find_element(by=By.XPATH, value='//b[text()[contains(.,"Хотите узнать")]]//ancestor::div[2]').get_attribute('id')
    driver.find_element(by=By.XPATH, value="//div[@id='"+ form_id +"']//*[@id='consultationform-name']").send_keys(str(data["test_data_valid"]["name"]))
    driver.find_element(by=By.XPATH, value="//div[@id='"+ form_id +"']//*[@id='consultationform-phone']").send_keys(str(data["test_data_valid"]["phone"]))
    driver.find_element(by=By.XPATH, value="//div[@id='"+ form_id +"']//*[@id='consultationform-email']").send_keys(str(data["test_data_valid"]["email"]))
    driver.find_element(by=By.XPATH, value="//div[@id='"+ form_id +"']//*[text()[contains(.,'Отправить')]]").click()
    try:
        wait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//div[@id='"+ form_id +"']//*[text()[contains(.,'Заявка успешно отправлена')]]")))
        print(" OK: меры поддержки 4/6 данные были отправлены")
    except:
        print('ERROR: не отправлены данные в форму "Хотите узнать подробнее о господдержке?" в "Меры поддержки" - "Агростартап"')
except:
    print('ERROR: не могу найти форму "Хотите узнать подробнее о господдержке?" в "Меры поддержки" - "Агростартап"')

# 5.5 переход на страницу "Меры поддержки - грант на семейную ферму"
driver.get("https://moigektar.ru/documents/family")
try:
    form_id = driver.find_element(by=By.XPATH, value='//b[text()[contains(.,"Хотите узнать")]]//ancestor::div[2]').get_attribute('id')
    driver.find_element(by=By.XPATH, value="//div[@id='"+ form_id +"']//*[@id='consultationform-name']").send_keys(str(data["test_data_valid"]["name"]))
    driver.find_element(by=By.XPATH, value="//div[@id='"+ form_id +"']//*[@id='consultationform-phone']").send_keys(str(data["test_data_valid"]["phone"]))
    driver.find_element(by=By.XPATH, value="//div[@id='"+ form_id +"']//*[@id='consultationform-email']").send_keys(str(data["test_data_valid"]["email"]))
    driver.find_element(by=By.XPATH, value="//div[@id='"+ form_id +"']//*[text()[contains(.,'Отправить')]]").click()
    try:
        wait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//div[@id='"+ form_id +"']//*[text()[contains(.,'Заявка успешно отправлена')]]")))
        print(" OK: меры поддержки 5/6 данные были отправлены")
    except:
        print('ERROR: не отправлены данные в форму "Хотите узнать подробнее о господдержке?" в "Меры поддержки" - "Грант на семейную ферму"')
except:
    print('ERROR: не могу найти форму "Хотите узнать подробнее о господдержке?" в "Меры поддержки" - "Грант на семейную ферму"')

# 5.6 переход на страницу "Меры поддержки - сельская ипотека"
driver.get("https://moigektar.ru/documents/ipoteka")
try:
    form_id = driver.find_element(by=By.XPATH, value='//b[text()[contains(.,"Хотите узнать")]]//ancestor::div[2]').get_attribute('id')
    driver.find_element(by=By.XPATH, value="//div[@id='"+ form_id +"']//*[@id='consultationform-name']").send_keys(str(data["test_data_valid"]["name"]))
    driver.find_element(by=By.XPATH, value="//div[@id='"+ form_id +"']//*[@id='consultationform-phone']").send_keys(str(data["test_data_valid"]["phone"]))
    driver.find_element(by=By.XPATH, value="//div[@id='"+ form_id +"']//*[@id='consultationform-email']").send_keys(str(data["test_data_valid"]["email"]))
    driver.find_element(by=By.XPATH, value="//div[@id='"+ form_id +"']//*[text()[contains(.,'Отправить')]]").click()
    try:
        wait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//div[@id='"+ form_id +"']//*[text()[contains(.,'Заявка успешно отправлена')]]")))
        print(" OK: меры поддержки 6/6 данные были отправлены")
    except:
        print('ERROR: не отправлены данные в форму "Хотите узнать подробнее о господдержке?" в "Меры поддержки" - "Сельская ипотека"')
except:
    print('ERROR: не могу найти форму "Хотите узнать подробнее о господдержке?" в "Меры поддержки" - "Сельская ипотека"')


# 6 проверка раздела "Вопрос-ответ"
# 6.1 переход на страницу "Вопрос-ответ - подробности о проектах"
driver.get("https://moigektar.ru/faq")
try:
    form_id = driver.find_element(by=By.XPATH, value='//b[text()[contains(.,"Не нашли")]]//ancestor::div[2]').get_attribute('id')
    driver.find_element(by=By.XPATH, value="//div[@id='"+ form_id +"']//*[@id='consultationform-name']").send_keys(str(data["test_data_valid"]["name"]))
    driver.find_element(by=By.XPATH, value="//div[@id='"+ form_id +"']//*[@id='consultationform-phone']").send_keys(str(data["test_data_valid"]["phone"]))
    driver.find_element(by=By.XPATH, value="//div[@id='"+ form_id +"']//*[@id='consultationform-email']").send_keys(str(data["test_data_valid"]["email"]))
    driver.find_element(by=By.XPATH, value="//div[@id='"+ form_id +"']//*[text()[contains(.,'Отправить')]]").click()
    try:
        wait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//div[@id='"+ form_id +"']//*[text()[contains(.,'Заявка успешно отправлена')]]")))
        print(" OK: данные из вопросов были отправлены")
    except:
        print('ERROR: не отправлены данные в форму "Не нашли ответа на свой вопрос?" в "Вопрос-ответ"')
except:
    print('ERROR: не могу найти форму "Не нашли ответа на свой вопрос?" в "Вопрос-ответ"')


# 7 проверка раздела "Вакансии"
# 7.1 переход на страницу "Вакансии"
driver.get("https://moigektar.ru/hr")
try:
    form_id = driver.find_element(by=By.XPATH, value='//b[text()[contains(.,"Оставьте анкету")]]//ancestor::div[2]').get_attribute('id')
    driver.find_element(by=By.XPATH, value="//div[@id='"+ form_id +"']//*[@id='hrform-name']").send_keys(str(data["test_data_valid"]["name"]))
    driver.find_element(by=By.XPATH, value="//div[@id='"+ form_id +"']//*[@id='hrform-phone']").send_keys(str(data["test_data_valid"]["phone"]))
    driver.find_element(by=By.XPATH, value="//div[@id='"+ form_id +"']//*[text()[contains(.,'Отправить')]]").click()
    try:
        wait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//div[@id='"+ form_id +"']//*[text()[contains(.,'Заявка успешно отправлена')]]")))
        print(" OK: данные из вакансий были отправлены")
    except:
        print('ERROR: не отправлены данные в форму "Оставьте анкету" в "Вакансиях"')
except:
    print('ERROR: не могу найти форму "Оставьте анкету" в "Вакансиях"')


# 8 проверка раздела "Контакты"
# 8.1 переход на страницу "Контакты"
driver.get("https://moigektar.ru/contacts")
try:
    form_id = driver.find_element(by=By.XPATH, value='//b[text()[contains(.,"Хотите задать")]]//ancestor::div[2]').get_attribute('id')
    driver.find_element(by=By.XPATH, value="//div[@id='"+ form_id +"']//*[@id='consultationform-name']").send_keys(str(data["test_data_valid"]["name"]))
    driver.find_element(by=By.XPATH, value="//div[@id='"+ form_id +"']//*[@id='consultationform-phone']").send_keys(str(data["test_data_valid"]["phone"]))
    driver.find_element(by=By.XPATH, value="//div[@id='"+ form_id +"']//*[@id='consultationform-email']").send_keys(str(data["test_data_valid"]["email"]))
    driver.find_element(by=By.XPATH, value="//div[@id='"+ form_id +"']//*[text()[contains(.,'Отправить')]]").click()
    try:
        wait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//div[@id='"+ form_id +"']//*[text()[contains(.,'Заявка успешно отправлена')]]")))
        print(" OK: данные из контактов были отправлены")
    except:
        print('ERROR: не отправлены данные в форму "Хотите задать вопрос специалисту?" в "Контактах"')
except:
    print('ERROR: не могу найти форму "Хотите задать вопрос специалисту?" в "Контактах"')


#time.sleep(8)
driver.quit()

