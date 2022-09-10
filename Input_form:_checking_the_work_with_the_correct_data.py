from selenium import webdriver
from selenium.webdriver.chrome.options import Options
options = Options()
options.add_argument('--headless')
ch_options = Options()
ch_options.add_argument('--headless')
driver = webdriver.Chrome(options= ch_options)
driver.maximize_window()


from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time

# Скрипт заполняет каждую форму корректными данными
# В лог выводится сообщение "ОК" если данные были отправлены и отобразилось сообщение об успехе
# В лог выводится сообщение "ERROR" если это сообщение не отобразилось
# В лог выводится сообщение "ERROR" если элемент не был найден по селектору



# 1. проверка главной страницы "МГ"
# открыть https://moigektar.ru/
driver.get("https://moigektar.ru/")

# 1.1 проверка формы "Хотите узнать подробнее о проекте?"
time.sleep(2)
try:
    driver.find_element(by=By.XPATH, value="//h1/*[text()[contains(.,'Хотите узнать')]]//parent::h1//following-sibling::ul[2]//input[@id='consultationform-name']").send_keys('test')
    driver.find_element(by=By.XPATH, value="//h1/*[text()[contains(.,'Хотите узнать')]]//parent::h1//following-sibling::ul[2]//input[@id='consultationform-phone']").send_keys('9999999999')
    driver.find_element(by=By.XPATH,
                        value="//h1/*[text()[contains(.,'Хотите узнать')]]//parent::h1//following-sibling::ul[2]//input[@id='consultationform-email']").send_keys(
        '1@1.1')
    driver.find_element(by=By.XPATH,
                        value="//h1/*[text()[contains(.,'Хотите узнать')]]//parent::h1//following-sibling::ul[2]//button").click()
    time.sleep(3)
    if driver.find_element(by=By.XPATH,
                        value="//h1/*[text()[contains(.,'Хотите узнать')]]//parent::h1//following-sibling::ul[2]//div[text()[contains(.,'Заявка успешно отправлена')]]").is_displayed():
        print(" OK: 1.1 данные были отправлены")
    else:
        print("ERROR: 1.1 данные не были отправлены")
except NoSuchElementException:
    print("ERROR: 1.1 такого элемента нет в DOM")

# 1.2 проверка формы "Получите каталог посёлков"
try:
    driver.find_element(by=By.XPATH, value="//h1/*[text()[contains(.,'Получите каталог')]]//parent::h1//following-sibling::ul[2]//input[@id='consultationform-name']").send_keys('test')
    driver.find_element(by=By.XPATH, value="//h1/*[text()[contains(.,'Получите каталог')]]//parent::h1//following-sibling::ul[2]//input[@id='consultationform-phone']").send_keys('9999999999')
    driver.find_element(by=By.XPATH,
                        value="//h1/*[text()[contains(.,'Получите каталог')]]//parent::h1//following-sibling::ul[2]//input[@id='consultationform-email']").send_keys(
        '1@1.1')
    driver.find_element(by=By.XPATH,
                        value="//h1/*[text()[contains(.,'Получите каталог')]]//parent::h1//following-sibling::ul[2]//button").click()
    time.sleep(3)
    try:
        if driver.find_element(by=By.XPATH,
                        value="//h1/*[text()[contains(.,'Получите каталог')]]//parent::h1//following-sibling::ul[2]//div[text()[contains(.,'Заявка успешно отправлена')]]").is_displayed():
            print(" OK: 1.2 данные были отправлены")
    except NoSuchElementException:
        print("ERROR: 1.2 данные не были отправлены")
except NoSuchElementException:
    print("ERROR: 1.2 такого элемента нет в DOM")

# 1.3 проверка формы "Подпишитесь на рассылку"
try:
    driver.find_element(by=By.XPATH,
                        value="//h1/*[text()[contains(.,'Подпишитесь на рассылку')]]//parent::h1//following-sibling::ul[2]//input[@id='consultationform-email']").send_keys(
        '1@1.1')
    driver.find_element(by=By.XPATH,
                        value="//h1/*[text()[contains(.,'Подпишитесь на рассылку')]]//parent::h1//following-sibling::ul[2]//button").click()
    time.sleep(3)
    try:
        if driver.find_element(by=By.XPATH,
                        value="//h1/*[text()[contains(.,'Подпишитесь на рассылку')]]//parent::h1//following-sibling::ul[2]//div[text()[contains(.,'Заявка успешно отправлена')]]").is_displayed():
            print(" OK: 1.3 данные были отправлены")
    except NoSuchElementException:
        print("ERROR: 1.3 данные не были отправлены")
except NoSuchElementException:
    print("ERROR: 1.3 такого элемента нет в DOM")

# 1.4 проверка формы "Действуйте! Лучшие участки уже бронируют"
try:
    driver.find_element(by=By.XPATH, value="//h1/*[text()[contains(.,'Действуйте!')]]//parent::h1//following-sibling::ul[2]//input[@id='consultationform-name']").send_keys('test')
    driver.find_element(by=By.XPATH, value="//h1/*[text()[contains(.,'Действуйте!')]]//parent::h1//following-sibling::ul[2]//input[@id='consultationform-phone']").send_keys('9999999999')
    driver.find_element(by=By.XPATH,
                        value="//h1/*[text()[contains(.,'Действуйте!')]]//parent::h1//following-sibling::ul[2]//button").click()
    time.sleep(3)
    try:
        if driver.find_element(by=By.XPATH,
                        value="//h1/*[text()[contains(.,'Действуйте!')]]//parent::h1//following-sibling::ul[2]//div[text()[contains(.,'Заявка успешно отправлена')]]").is_displayed():
            print(" OK: 1.4 данные были отправлены")
    except NoSuchElementException:
        print("ERROR: 1.4 данные не были отправлены")
except NoSuchElementException:
    print("ERROR: 1.4 такого элемента нет в DOM")




# 2. проверка раздела "О проекте"
# 2.1 переход на страницу "О проекте"
driver.get("https://moigektar.ru/about")
time.sleep(2)
try:
    driver.find_element(by=By.XPATH, value="//h1/*[text()[contains(.,'Хотите узнать')]]//parent::h1//following-sibling::ul[2]//input[@id='consultationform-name']").send_keys('test')
    driver.find_element(by=By.XPATH, value="//h1/*[text()[contains(.,'Хотите узнать')]]//parent::h1//following-sibling::ul[2]//input[@id='consultationform-phone']").send_keys('9999999999')
    driver.find_element(by=By.XPATH,
                        value="//h1/*[text()[contains(.,'Хотите узнать')]]//parent::h1//following-sibling::ul[2]//input[@id='consultationform-email']").send_keys(
        '1@1.1')
    driver.find_element(by=By.XPATH,
                        value="//h1/*[text()[contains(.,'Хотите узнать')]]//parent::h1//following-sibling::ul[2]//button").click()
    time.sleep(3)
    try:
        if driver.find_element(by=By.XPATH,
                        value="//h1/*[text()[contains(.,'Хотите узнать')]]//parent::h1//following-sibling::ul[2]//div[text()[contains(.,'Заявка успешно отправлена')]]").is_displayed():
            print(" OK: 2.1 данные были отправлены")
    except NoSuchElementException:
        print("ERROR: 2.1 данные не были отправлены")
except NoSuchElementException:
    print("ERROR: 2.1 такого элемента нет в DOM")

# 2.2 переход на страницу "О проекте - сервисная компания"
driver.get("https://moigektar.ru/about/management")
time.sleep(2)
try:
    driver.find_element(by=By.XPATH, value="//h1/*[text()[contains(.,'Хотите узнать')]]//parent::h1//following-sibling::ul[2]//input[@id='consultationform-name']").send_keys('test')
    driver.find_element(by=By.XPATH, value="//h1/*[text()[contains(.,'Хотите узнать')]]//parent::h1//following-sibling::ul[2]//input[@id='consultationform-phone']").send_keys('9999999999')
    driver.find_element(by=By.XPATH,
                        value="//h1/*[text()[contains(.,'Хотите узнать')]]//parent::h1//following-sibling::ul[2]//input[@id='consultationform-email']").send_keys(
        '1@1.1')
    driver.find_element(by=By.XPATH,
                        value="//h1/*[text()[contains(.,'Хотите узнать')]]//parent::h1//following-sibling::ul[2]//button").click()
    time.sleep(3)
    try:
        if driver.find_element(by=By.XPATH,
                        value="//h1/*[text()[contains(.,'Хотите узнать')]]//parent::h1//following-sibling::ul[2]//div[text()[contains(.,'Заявка успешно отправлена')]]").is_displayed():
            print(" OK: 2.2 данные были отправлены")
    except NoSuchElementException:
        print("ERROR: 2.2 данные не были отправлены")
except NoSuchElementException:
    print("ERROR: 2.2 такого элемента нет в DOM")

# 2.3 переход на страницу "О проекте - личный кабинет"
driver.get("https://moigektar.ru/about/cabinet")
time.sleep(2)
try:
    driver.find_element(by=By.XPATH, value="//h1/*[text()[contains(.,'Хотите узнать')]]//parent::h1//following-sibling::ul[2]//input[@id='consultationform-name']").send_keys('test')
    driver.find_element(by=By.XPATH, value="//h1/*[text()[contains(.,'Хотите узнать')]]//parent::h1//following-sibling::ul[2]//input[@id='consultationform-phone']").send_keys('9999999999')
    driver.find_element(by=By.XPATH,
                        value="//h1/*[text()[contains(.,'Хотите узнать')]]//parent::h1//following-sibling::ul[2]//input[@id='consultationform-email']").send_keys(
        '1@1.1')
    driver.find_element(by=By.XPATH,
                        value="//h1/*[text()[contains(.,'Хотите узнать')]]//parent::h1//following-sibling::ul[2]//button").click()
    time.sleep(3)
    try:
        if driver.find_element(by=By.XPATH,
                        value="//h1/*[text()[contains(.,'Хотите узнать')]]//parent::h1//following-sibling::ul[2]//div[text()[contains(.,'Заявка успешно отправлена')]]").is_displayed():
            print(" OK: 2.3 данные были отправлены")
    except NoSuchElementException:
        print("ERROR: 2.3 данные не были отправлены")
except NoSuchElementException:
    print("ERROR: 2.3 такого элемента нет в DOM")

# 2.4 переход на страницу "О проекте - партнеры"
driver.get("https://moigektar.ru/about/advantages")
time.sleep(2)
try:
    driver.find_element(by=By.XPATH, value="//h1/*[text()[contains(.,'Хотите узнать')]]//parent::h1//following-sibling::ul[2]//input[@id='consultationform-name']").send_keys('test')
    driver.find_element(by=By.XPATH, value="//h1/*[text()[contains(.,'Хотите узнать')]]//parent::h1//following-sibling::ul[2]//input[@id='consultationform-phone']").send_keys('9999999999')
    driver.find_element(by=By.XPATH,
                        value="//h1/*[text()[contains(.,'Хотите узнать')]]//parent::h1//following-sibling::ul[2]//input[@id='consultationform-email']").send_keys(
        '1@1.1')
    driver.find_element(by=By.XPATH,
                        value="//h1/*[text()[contains(.,'Хотите узнать')]]//parent::h1//following-sibling::ul[2]//button").click()
    time.sleep(3)
    try:
        if driver.find_element(by=By.XPATH,
                        value="//h1/*[text()[contains(.,'Хотите узнать')]]//parent::h1//following-sibling::ul[2]//div[text()[contains(.,'Заявка успешно отправлена')]]").is_displayed():
            print(" OK: 2.4 данные были отправлены")
    except NoSuchElementException:
        print("ERROR: 2.4 данные не были отправлены")
except NoSuchElementException:
    print("ERROR: 2.4 такого элемента нет в DOM")

# 2.5 переход на страницу "О проекте - союз садоводов"
driver.get("https://moigektar.ru/about/union")
time.sleep(2)
try:
    driver.find_element(by=By.XPATH, value="//h1/*[text()[contains(.,'Хотите узнать')]]//parent::h1//following-sibling::ul[2]//input[@id='consultationform-name']").send_keys('test')
    driver.find_element(by=By.XPATH, value="//h1/*[text()[contains(.,'Хотите узнать')]]//parent::h1//following-sibling::ul[2]//input[@id='consultationform-phone']").send_keys('9999999999')
    driver.find_element(by=By.XPATH,
                        value="//h1/*[text()[contains(.,'Хотите узнать')]]//parent::h1//following-sibling::ul[2]//input[@id='consultationform-email']").send_keys(
        '1@1.1')
    driver.find_element(by=By.XPATH,
                        value="//h1/*[text()[contains(.,'Хотите узнать')]]//parent::h1//following-sibling::ul[2]//button").click()
    time.sleep(3)
    try:
        if driver.find_element(by=By.XPATH,
                        value="//h1/*[text()[contains(.,'Хотите узнать')]]//parent::h1//following-sibling::ul[2]//div[text()[contains(.,'Заявка успешно отправлена')]]").is_displayed():
            print(" OK: 2.5 данные были отправлены")
    except NoSuchElementException:
        print("ERROR: 2.5 данные не были отправлены")
except NoSuchElementException:
    print("ERROR: 2.5 такого элемента нет в DOM")

# 2.6 переход на страницу "О проекте - отзывы"
driver.get("https://moigektar.ru/about/reviews")
time.sleep(2)
try:
    driver.find_element(by=By.XPATH, value="//h1/*[text()[contains(.,'Хотите узнать')]]//parent::h1//following-sibling::ul[2]//input[@id='consultationform-name']").send_keys('test')
    driver.find_element(by=By.XPATH, value="//h1/*[text()[contains(.,'Хотите узнать')]]//parent::h1//following-sibling::ul[2]//input[@id='consultationform-phone']").send_keys('9999999999')
    driver.find_element(by=By.XPATH,
                        value="//h1/*[text()[contains(.,'Хотите узнать')]]//parent::h1//following-sibling::ul[2]//input[@id='consultationform-email']").send_keys(
        '1@1.1')
    driver.find_element(by=By.XPATH,
                        value="//h1/*[text()[contains(.,'Хотите узнать')]]//parent::h1//following-sibling::ul[2]//button").click()
    time.sleep(3)
    try:
        if driver.find_element(by=By.XPATH,
                        value="//h1/*[text()[contains(.,'Хотите узнать')]]//parent::h1//following-sibling::ul[2]//div[text()[contains(.,'Заявка успешно отправлена')]]").is_displayed():
            print(" OK: 2.6 данные были отправлены")
    except NoSuchElementException:
        print("ERROR: 2.6 данные не были отправлены")
except NoSuchElementException:
    print("ERROR: 2.6 такого элемента нет в DOM")




# 3 переход на страницу "Каталог поселков"
# 3.1 проверка формы "Хотите узнать подробнее о проекте?"
driver.get("https://moigektar.ru/catalogue")
time.sleep(2)
try:
    driver.find_element(by=By.XPATH, value="//h1/*[text()[contains(.,'Хотите узнать')]]//parent::h1//following-sibling::ul[2]//input[@id='consultationform-name']").send_keys('test')
    driver.find_element(by=By.XPATH, value="//h1/*[text()[contains(.,'Хотите узнать')]]//parent::h1//following-sibling::ul[2]//input[@id='consultationform-phone']").send_keys('9999999999')
    driver.find_element(by=By.XPATH,
                        value="//h1/*[text()[contains(.,'Хотите узнать')]]//parent::h1//following-sibling::ul[2]//input[@id='consultationform-email']").send_keys(
        '1@1.1')
    driver.find_element(by=By.XPATH,
                        value="//h1/*[text()[contains(.,'Хотите узнать')]]//parent::h1//following-sibling::ul[2]//button").click()
    time.sleep(3)
    if driver.find_element(by=By.XPATH,
                        value="//h1/*[text()[contains(.,'Хотите узнать')]]//parent::h1//following-sibling::ul[2]//div[text()[contains(.,'Заявка успешно отправлена')]]").is_displayed():
        print(" OK: 3.1 данные были отправлены")
    else:
        print("ERROR: 3.1 данные не были отправлены")
except NoSuchElementException:
    print("ERROR: 3.1 такого элемента нет в DOM")



# 4 проверка раздела "Развитие"
# 4.1 переход на страницу "Развитие - развитие поселков"
driver.get("https://moigektar.ru/growth")
time.sleep(2)
try:
    driver.find_element(by=By.XPATH, value="//h1/*[text()[contains(.,'Хотите узнать')]]//parent::h1//following-sibling::ul[2]//input[@id='consultationform-name']").send_keys('test')
    driver.find_element(by=By.XPATH, value="//h1/*[text()[contains(.,'Хотите узнать')]]//parent::h1//following-sibling::ul[2]//input[@id='consultationform-phone']").send_keys('9999999999')
    driver.find_element(by=By.XPATH,
                        value="//h1/*[text()[contains(.,'Хотите узнать')]]//parent::h1//following-sibling::ul[2]//input[@id='consultationform-email']").send_keys(
        '1@1.1')
    driver.find_element(by=By.XPATH,
                        value="//h1/*[text()[contains(.,'Хотите узнать')]]//parent::h1//following-sibling::ul[2]//button").click()
    time.sleep(3)
    if driver.find_element(by=By.XPATH,
                        value="//h1/*[text()[contains(.,'Хотите узнать')]]//parent::h1//following-sibling::ul[2]//div[text()[contains(.,'Заявка успешно отправлена')]]").is_displayed():
        print(" OK: 4.1 данные были отправлены")
    else:
        print("ERROR: 4.1 данные не были отправлены")
except NoSuchElementException:
    print("ERROR: 4.1 такого элемента нет в DOM")

# 4.2 переход на страницу "Развитие - глазами инвестора"
driver.get("https://moigektar.ru/investment")
time.sleep(2)
try:
    driver.find_element(by=By.XPATH, value="//h1/*[text()[contains(.,'Хотите узнать')]]//parent::h1//following-sibling::ul[2]//input[@id='consultationform-name']").send_keys('test')
    driver.find_element(by=By.XPATH, value="//h1/*[text()[contains(.,'Хотите узнать')]]//parent::h1//following-sibling::ul[2]//input[@id='consultationform-phone']").send_keys('9999999999')
    driver.find_element(by=By.XPATH,
                        value="//h1/*[text()[contains(.,'Хотите узнать')]]//parent::h1//following-sibling::ul[2]//input[@id='consultationform-email']").send_keys(
        '1@1.1')
    driver.find_element(by=By.XPATH,
                        value="//h1/*[text()[contains(.,'Хотите узнать')]]//parent::h1//following-sibling::ul[2]//button").click()
    time.sleep(3)
    if driver.find_element(by=By.XPATH,
                        value="//h1/*[text()[contains(.,'Хотите узнать')]]//parent::h1//following-sibling::ul[2]//div[text()[contains(.,'Заявка успешно отправлена')]]").is_displayed():
        print(" OK: 4.2 данные были отправлены")
    else:
        print("ERROR: 4.2 данные не были отправлены")
except NoSuchElementException:
    print("ERROR: 4.2 такого элемента нет в DOM")

# 4.3 переход на страницу "Развитие - капитализация"
driver.get("https://moigektar.ru/investment/capitalization")
time.sleep(2)
try:
    driver.find_element(by=By.XPATH, value="//h1/*[text()[contains(.,'Хотите узнать')]]//parent::h1//following-sibling::ul[2]//input[@id='consultationform-name']").send_keys('test')
    driver.find_element(by=By.XPATH, value="//h1/*[text()[contains(.,'Хотите узнать')]]//parent::h1//following-sibling::ul[2]//input[@id='consultationform-phone']").send_keys('9999999999')
    driver.find_element(by=By.XPATH,
                        value="//h1/*[text()[contains(.,'Хотите узнать')]]//parent::h1//following-sibling::ul[2]//input[@id='consultationform-email']").send_keys(
        '1@1.1')
    driver.find_element(by=By.XPATH,
                        value="//h1/*[text()[contains(.,'Хотите узнать')]]//parent::h1//following-sibling::ul[2]//button").click()
    time.sleep(3)
    if driver.find_element(by=By.XPATH,
                        value="//h1/*[text()[contains(.,'Хотите узнать')]]//parent::h1//following-sibling::ul[2]//div[text()[contains(.,'Заявка успешно отправлена')]]").is_displayed():
        print(" OK: 4.3 данные были отправлены")
    else:
        print("ERROR: 4.3 данные не были отправлены")
except NoSuchElementException:
    print("ERROR: 4.3 такого элемента нет в DOM")

# 4.4 переход на страницу "Развитие - базовая стратегия"
driver.get("https://moigektar.ru/investment/basic")
time.sleep(2)
try:
    driver.find_element(by=By.XPATH, value="//h1/*[text()[contains(.,'Хотите узнать')]]//parent::h1//following-sibling::ul[2]//input[@id='consultationform-name']").send_keys('test')
    driver.find_element(by=By.XPATH, value="//h1/*[text()[contains(.,'Хотите узнать')]]//parent::h1//following-sibling::ul[2]//input[@id='consultationform-phone']").send_keys('9999999999')
    driver.find_element(by=By.XPATH,
                        value="//h1/*[text()[contains(.,'Хотите узнать')]]//parent::h1//following-sibling::ul[2]//input[@id='consultationform-email']").send_keys(
        '1@1.1')
    driver.find_element(by=By.XPATH,
                        value="//h1/*[text()[contains(.,'Хотите узнать')]]//parent::h1//following-sibling::ul[2]//button").click()
    time.sleep(3)
    if driver.find_element(by=By.XPATH,
                        value="//h1/*[text()[contains(.,'Хотите узнать')]]//parent::h1//following-sibling::ul[2]//div[text()[contains(.,'Заявка успешно отправлена')]]").is_displayed():
        print(" OK: 4.4 данные были отправлены")
    else:
        print("ERROR: 4.4 данные не были отправлены")
except NoSuchElementException:
    print("ERROR: 4.4 такого элемента нет в DOM")

# 4.5 переход на страницу "Развитие - предприниматель"
driver.get("https://moigektar.ru/investment/businessman")
time.sleep(2)
try:
    driver.find_element(by=By.XPATH, value="//h1/*[text()[contains(.,'Хотите узнать')]]//parent::h1//following-sibling::ul[2]//input[@id='consultationform-name']").send_keys('test')
    driver.find_element(by=By.XPATH, value="//h1/*[text()[contains(.,'Хотите узнать')]]//parent::h1//following-sibling::ul[2]//input[@id='consultationform-phone']").send_keys('9999999999')
    driver.find_element(by=By.XPATH,
                        value="//h1/*[text()[contains(.,'Хотите узнать')]]//parent::h1//following-sibling::ul[2]//input[@id='consultationform-email']").send_keys(
        '1@1.1')
    driver.find_element(by=By.XPATH,
                        value="//h1/*[text()[contains(.,'Хотите узнать')]]//parent::h1//following-sibling::ul[2]//button").click()
    time.sleep(3)
    if driver.find_element(by=By.XPATH,
                        value="//h1/*[text()[contains(.,'Хотите узнать')]]//parent::h1//following-sibling::ul[2]//div[text()[contains(.,'Заявка успешно отправлена')]]").is_displayed():
        print(" OK: 4.5 данные были отправлены")
    else:
        print("ERROR: 4.5 данные не были отправлены")
except NoSuchElementException:
    print("ERROR: 4.5 такого элемента нет в DOM")

# 4.6 переход на страницу "Развитие - фермер-садовод"
driver.get("https://moigektar.ru/investment/farmer")
time.sleep(2)
try:
    driver.find_element(by=By.XPATH, value="//h1/*[text()[contains(.,'Хотите узнать')]]//parent::h1//following-sibling::ul[2]//input[@id='consultationform-name']").send_keys('test')
    driver.find_element(by=By.XPATH, value="//h1/*[text()[contains(.,'Хотите узнать')]]//parent::h1//following-sibling::ul[2]//input[@id='consultationform-phone']").send_keys('9999999999')
    driver.find_element(by=By.XPATH,
                        value="//h1/*[text()[contains(.,'Хотите узнать')]]//parent::h1//following-sibling::ul[2]//input[@id='consultationform-email']").send_keys(
        '1@1.1')
    driver.find_element(by=By.XPATH,
                        value="//h1/*[text()[contains(.,'Хотите узнать')]]//parent::h1//following-sibling::ul[2]//button").click()
    time.sleep(3)
    if driver.find_element(by=By.XPATH,
                        value="//h1/*[text()[contains(.,'Хотите узнать')]]//parent::h1//following-sibling::ul[2]//div[text()[contains(.,'Заявка успешно отправлена')]]").is_displayed():
        print(" OK: 4.6 данные были отправлены")
    else:
        print("ERROR: 4.6 данные не были отправлены")
except NoSuchElementException:
    print("ERROR: 4.6 такого элемента нет в DOM")

# 4.7 переход на страницу "Развитие - фамильная усадьба"
driver.get("https://moigektar.ru/investment/family")
time.sleep(2)
try:
    driver.find_element(by=By.XPATH, value="//h1/*[text()[contains(.,'Хотите узнать')]]//parent::h1//following-sibling::ul[2]//input[@id='consultationform-name']").send_keys('test')
    driver.find_element(by=By.XPATH, value="//h1/*[text()[contains(.,'Хотите узнать')]]//parent::h1//following-sibling::ul[2]//input[@id='consultationform-phone']").send_keys('9999999999')
    driver.find_element(by=By.XPATH,
                        value="//h1/*[text()[contains(.,'Хотите узнать')]]//parent::h1//following-sibling::ul[2]//input[@id='consultationform-email']").send_keys(
        '1@1.1')
    driver.find_element(by=By.XPATH,
                        value="//h1/*[text()[contains(.,'Хотите узнать')]]//parent::h1//following-sibling::ul[2]//button").click()
    time.sleep(3)
    if driver.find_element(by=By.XPATH,
                        value="//h1/*[text()[contains(.,'Хотите узнать')]]//parent::h1//following-sibling::ul[2]//div[text()[contains(.,'Заявка успешно отправлена')]]").is_displayed():
        print(" OK: 4.7 данные были отправлены")
    else:
        print("ERROR: 4.7 данные не были отправлены")
except NoSuchElementException:
    print("ERROR: 4.7 такого элемента нет в DOM")




# 5 проверка раздела "Меры поддержки"
# 5.1 переход на страницу "Меры поддержки - государственная поддержка"
driver.get("https://moigektar.ru/documents/gos")
time.sleep(2)
time.sleep(2)
try:
    driver.find_element(by=By.XPATH, value="//h1/*[text()[contains(.,'Хотите узнать')]]//parent::h1//following-sibling::ul[2]//input[@id='consultationform-name']").send_keys('test')
    driver.find_element(by=By.XPATH, value="//h1/*[text()[contains(.,'Хотите узнать')]]//parent::h1//following-sibling::ul[2]//input[@id='consultationform-phone']").send_keys('9999999999')
    driver.find_element(by=By.XPATH,
                        value="//h1/*[text()[contains(.,'Хотите узнать')]]//parent::h1//following-sibling::ul[2]//input[@id='consultationform-email']").send_keys(
        '1@1.1')
    driver.find_element(by=By.XPATH,
                        value="//h1/*[text()[contains(.,'Хотите узнать')]]//parent::h1//following-sibling::ul[2]//button").click()
    time.sleep(3)
    if driver.find_element(by=By.XPATH,
                        value="//h1/*[text()[contains(.,'Хотите узнать')]]//parent::h1//following-sibling::ul[2]//div[text()[contains(.,'Заявка успешно отправлена')]]").is_displayed():
        print(" OK: 5.1 данные были отправлены")
    else:
        print("ERROR: 5.1 данные не были отправлены")
except NoSuchElementException:
    print("ERROR: 5.1 такого элемента нет в DOM")

# 5.2 переход на страницу "Меры поддержки - для владельцев земли"
driver.get("https://moigektar.ru/documents")
time.sleep(2)
try:
    driver.find_element(by=By.XPATH, value="//h1/*[text()[contains(.,'Хотите узнать')]]//parent::h1//following-sibling::ul[2]//input[@id='consultationform-name']").send_keys('test')
    driver.find_element(by=By.XPATH, value="//h1/*[text()[contains(.,'Хотите узнать')]]//parent::h1//following-sibling::ul[2]//input[@id='consultationform-phone']").send_keys('9999999999')
    driver.find_element(by=By.XPATH,
                        value="//h1/*[text()[contains(.,'Хотите узнать')]]//parent::h1//following-sibling::ul[2]//input[@id='consultationform-email']").send_keys(
        '1@1.1')
    driver.find_element(by=By.XPATH,
                        value="//h1/*[text()[contains(.,'Хотите узнать')]]//parent::h1//following-sibling::ul[2]//button").click()
    time.sleep(3)
    if driver.find_element(by=By.XPATH,
                        value="//h1/*[text()[contains(.,'Хотите узнать')]]//parent::h1//following-sibling::ul[2]//div[text()[contains(.,'Заявка успешно отправлена')]]").is_displayed():
        print(" OK: 5.2 данные были отправлены")
    else:
        print("ERROR: 5.2 данные не были отправлены")
except NoSuchElementException:
    print("ERROR: 5.2 такого элемента нет в DOM")

# 5.3 переход на страницу "Меры поддержки - грант Фермер"
driver.get("https://moigektar.ru/documents/farmer")
time.sleep(2)
try:
    driver.find_element(by=By.XPATH, value="//h1/*[text()[contains(.,'Хотите узнать')]]//parent::h1//following-sibling::ul[2]//input[@id='consultationform-name']").send_keys('test')
    driver.find_element(by=By.XPATH, value="//h1/*[text()[contains(.,'Хотите узнать')]]//parent::h1//following-sibling::ul[2]//input[@id='consultationform-phone']").send_keys('9999999999')
    driver.find_element(by=By.XPATH,
                        value="//h1/*[text()[contains(.,'Хотите узнать')]]//parent::h1//following-sibling::ul[2]//input[@id='consultationform-email']").send_keys(
        '1@1.1')
    driver.find_element(by=By.XPATH,
                        value="//h1/*[text()[contains(.,'Хотите узнать')]]//parent::h1//following-sibling::ul[2]//button").click()
    time.sleep(3)
    if driver.find_element(by=By.XPATH,
                        value="//h1/*[text()[contains(.,'Хотите узнать')]]//parent::h1//following-sibling::ul[2]//div[text()[contains(.,'Заявка успешно отправлена')]]").is_displayed():
        print(" OK: 5.3 данные были отправлены")
    else:
        print("ERROR: 5.3 данные не были отправлены")
except NoSuchElementException:
    print("ERROR: 5.3 такого элемента нет в DOM")

# 5.4 переход на страницу "Меры поддержки - Агростартап"
driver.get("https://moigektar.ru/documents/startup")
time.sleep(2)
try:
    driver.find_element(by=By.XPATH, value="//h1/*[text()[contains(.,'Хотите узнать')]]//parent::h1//following-sibling::ul[2]//input[@id='consultationform-name']").send_keys('test')
    driver.find_element(by=By.XPATH, value="//h1/*[text()[contains(.,'Хотите узнать')]]//parent::h1//following-sibling::ul[2]//input[@id='consultationform-phone']").send_keys('9999999999')
    driver.find_element(by=By.XPATH,
                        value="//h1/*[text()[contains(.,'Хотите узнать')]]//parent::h1//following-sibling::ul[2]//input[@id='consultationform-email']").send_keys(
        '1@1.1')
    driver.find_element(by=By.XPATH,
                        value="//h1/*[text()[contains(.,'Хотите узнать')]]//parent::h1//following-sibling::ul[2]//button").click()
    time.sleep(3)
    if driver.find_element(by=By.XPATH,
                        value="//h1/*[text()[contains(.,'Хотите узнать')]]//parent::h1//following-sibling::ul[2]//div[text()[contains(.,'Заявка успешно отправлена')]]").is_displayed():
        print(" OK: 5.4 данные были отправлены")
    else:
        print("ERROR: 5.4 данные не были отправлены")
except NoSuchElementException:
    print("ERROR: 5.4 такого элемента нет в DOM")

# 5.5 переход на страницу "Меры поддержки - грант на семейную ферму"
driver.get("https://moigektar.ru/documents/family")
time.sleep(2)
try:
    driver.find_element(by=By.XPATH, value="//h1/*[text()[contains(.,'Хотите узнать')]]//parent::h1//following-sibling::ul[2]//input[@id='consultationform-name']").send_keys('test')
    driver.find_element(by=By.XPATH, value="//h1/*[text()[contains(.,'Хотите узнать')]]//parent::h1//following-sibling::ul[2]//input[@id='consultationform-phone']").send_keys('9999999999')
    driver.find_element(by=By.XPATH,
                        value="//h1/*[text()[contains(.,'Хотите узнать')]]//parent::h1//following-sibling::ul[2]//input[@id='consultationform-email']").send_keys(
        '1@1.1')
    driver.find_element(by=By.XPATH,
                        value="//h1/*[text()[contains(.,'Хотите узнать')]]//parent::h1//following-sibling::ul[2]//button").click()
    time.sleep(3)
    if driver.find_element(by=By.XPATH,
                        value="//h1/*[text()[contains(.,'Хотите узнать')]]//parent::h1//following-sibling::ul[2]//div[text()[contains(.,'Заявка успешно отправлена')]]").is_displayed():
        print(" OK: 5.5 данные были отправлены")
    else:
        print("ERROR: 5.5 данные не были отправлены")
except NoSuchElementException:
    print("ERROR: 5.5 такого элемента нет в DOM")

# 5.6 переход на страницу "Меры поддержки - сельская ипотека"
driver.get("https://moigektar.ru/documents/ipoteka")
time.sleep(2)
try:
    driver.find_element(by=By.XPATH, value="//h1/*[text()[contains(.,'Хотите узнать')]]//parent::h1//following-sibling::ul[2]//input[@id='consultationform-name']").send_keys('test')
    driver.find_element(by=By.XPATH, value="//h1/*[text()[contains(.,'Хотите узнать')]]//parent::h1//following-sibling::ul[2]//input[@id='consultationform-phone']").send_keys('9999999999')
    driver.find_element(by=By.XPATH,
                        value="//h1/*[text()[contains(.,'Хотите узнать')]]//parent::h1//following-sibling::ul[2]//input[@id='consultationform-email']").send_keys(
        '1@1.1')
    driver.find_element(by=By.XPATH,
                        value="//h1/*[text()[contains(.,'Хотите узнать')]]//parent::h1//following-sibling::ul[2]//button").click()
    time.sleep(3)
    if driver.find_element(by=By.XPATH,
                        value="//h1/*[text()[contains(.,'Хотите узнать')]]//parent::h1//following-sibling::ul[2]//div[text()[contains(.,'Заявка успешно отправлена')]]").is_displayed():
        print(" OK: 5.6 данные были отправлены")
    else:
        print("ERROR: 5.6 данные не были отправлены")
except NoSuchElementException:
    print("ERROR: 5.6 такого элемента нет в DOM")



# 6 проверка раздела "Вопрос-ответ"
# 6.1 переход на страницу "Вопрос-ответ - подробности о проектах"
driver.get("https://moigektar.ru/faq")
time.sleep(2)
try:
    driver.find_element(by=By.XPATH, value="//h1/*[text()[contains(.,'Не нашли')]]//parent::h1//following-sibling::ul[2]//input[@id='consultationform-name']").send_keys('test')
    driver.find_element(by=By.XPATH, value="//h1/*[text()[contains(.,'Не нашли')]]//parent::h1//following-sibling::ul[2]//input[@id='consultationform-phone']").send_keys('9999999999')
    driver.find_element(by=By.XPATH,
                        value="//h1/*[text()[contains(.,'Не нашли')]]//parent::h1//following-sibling::ul[2]//input[@id='consultationform-email']").send_keys(
        '1@1.1')
    driver.find_element(by=By.XPATH,
                        value="//h1/*[text()[contains(.,'Не нашли')]]//parent::h1//following-sibling::ul[2]//button").click()
    time.sleep(3)
    if driver.find_element(by=By.XPATH,
                        value="//h1/*[text()[contains(.,'Не нашли')]]//parent::h1//following-sibling::ul[2]//div[text()[contains(.,'Заявка успешно отправлена')]]").is_displayed():
        print(" OK: 6.1 данные были отправлены")
    else:
        print("ERROR: 6.1 данные не были отправлены")
except NoSuchElementException:
    print("ERROR: 6.1 такого элемента нет в DOM")

# 6.2 переход на страницу "Вопрос-ответ - о развитии участка"
driver.get("https://moigektar.ru/faq/growth")
time.sleep(2)
try:
    driver.find_element(by=By.XPATH, value="//h1/*[text()[contains(.,'Не нашли')]]//parent::h1//following-sibling::ul[2]//input[@id='consultationform-name']").send_keys('test')
    driver.find_element(by=By.XPATH, value="//h1/*[text()[contains(.,'Не нашли')]]//parent::h1//following-sibling::ul[2]//input[@id='consultationform-phone']").send_keys('9999999999')
    driver.find_element(by=By.XPATH,
                        value="//h1/*[text()[contains(.,'Не нашли')]]//parent::h1//following-sibling::ul[2]//input[@id='consultationform-email']").send_keys(
        '1@1.1')
    driver.find_element(by=By.XPATH,
                        value="//h1/*[text()[contains(.,'Не нашли')]]//parent::h1//following-sibling::ul[2]//button").click()
    time.sleep(3)
    if driver.find_element(by=By.XPATH,
                        value="//h1/*[text()[contains(.,'Не нашли')]]//parent::h1//following-sibling::ul[2]//div[text()[contains(.,'Заявка успешно отправлена')]]").is_displayed():
        print(" OK: 6.2 данные были отправлены")
    else:
        print("ERROR: 6.2 данные не были отправлены")
except NoSuchElementException:
    print("ERROR: 6.2 такого элемента нет в DOM")

# 6.3 переход на страницу "Вопрос-ответ - стоимость земли"
driver.get("https://moigektar.ru/faq/cost")
time.sleep(2)
try:
    driver.find_element(by=By.XPATH, value="//h1/*[text()[contains(.,'Не нашли')]]//parent::h1//following-sibling::ul[2]//input[@id='consultationform-name']").send_keys('test')
    driver.find_element(by=By.XPATH, value="//h1/*[text()[contains(.,'Не нашли')]]//parent::h1//following-sibling::ul[2]//input[@id='consultationform-phone']").send_keys('9999999999')
    driver.find_element(by=By.XPATH,
                        value="//h1/*[text()[contains(.,'Не нашли')]]//parent::h1//following-sibling::ul[2]//input[@id='consultationform-email']").send_keys(
        '1@1.1')
    driver.find_element(by=By.XPATH,
                        value="//h1/*[text()[contains(.,'Не нашли')]]//parent::h1//following-sibling::ul[2]//button").click()
    time.sleep(3)
    if driver.find_element(by=By.XPATH,
                        value="//h1/*[text()[contains(.,'Не нашли')]]//parent::h1//following-sibling::ul[2]//div[text()[contains(.,'Заявка успешно отправлена')]]").is_displayed():
        print(" OK: 6.3 данные были отправлены")
    else:
        print("ERROR: 6.3 данные не были отправлены")
except NoSuchElementException:
    print("ERROR: 6.3 такого элемента нет в DOM")

# 6.4 переход на страницу "Вопрос-ответ - оформление земли"
driver.get("https://moigektar.ru/faq/own")
time.sleep(2)
try:
    driver.find_element(by=By.XPATH, value="//h1/*[text()[contains(.,'Не нашли')]]//parent::h1//following-sibling::ul[2]//input[@id='consultationform-name']").send_keys('test')
    driver.find_element(by=By.XPATH, value="//h1/*[text()[contains(.,'Не нашли')]]//parent::h1//following-sibling::ul[2]//input[@id='consultationform-phone']").send_keys('9999999999')
    driver.find_element(by=By.XPATH,
                        value="//h1/*[text()[contains(.,'Не нашли')]]//parent::h1//following-sibling::ul[2]//input[@id='consultationform-email']").send_keys(
        '1@1.1')
    driver.find_element(by=By.XPATH,
                        value="//h1/*[text()[contains(.,'Не нашли')]]//parent::h1//following-sibling::ul[2]//button").click()
    time.sleep(3)
    if driver.find_element(by=By.XPATH,
                        value="//h1/*[text()[contains(.,'Не нашли')]]//parent::h1//following-sibling::ul[2]//div[text()[contains(.,'Заявка успешно отправлена')]]").is_displayed():
        print(" OK: 6.4 данные были отправлены")
    else:
        print("ERROR: 6.4 данные не были отправлены")
except NoSuchElementException:
    print("ERROR: 6.4 такого элемента нет в DOM")




# 7 проверка раздела "Контакты"
# 7.1 переход на страницу "Контакты"
driver.get("https://moigektar.ru/contacts")
time.sleep(2)
try:
    driver.find_element(by=By.XPATH, value="//h1/*[text()[contains(.,'Хотите задать')]]//parent::h1//following-sibling::ul[2]//input[@id='consultationform-name']").send_keys('test')
    driver.find_element(by=By.XPATH, value="//h1/*[text()[contains(.,'Хотите задать')]]//parent::h1//following-sibling::ul[2]//input[@id='consultationform-phone']").send_keys('9999999999')
    driver.find_element(by=By.XPATH,
                        value="//h1/*[text()[contains(.,'Хотите задать')]]//parent::h1//following-sibling::ul[2]//input[@id='consultationform-email']").send_keys(
        '1@1.1')
    driver.find_element(by=By.XPATH,
                        value="//h1/*[text()[contains(.,'Хотите задать')]]//parent::h1//following-sibling::ul[2]//button").click()
    time.sleep(3)
    if driver.find_element(by=By.XPATH,
                        value="//h1/*[text()[contains(.,'Хотите задать')]]//parent::h1//following-sibling::ul[2]//div[text()[contains(.,'Заявка успешно отправлена')]]").is_displayed():
        print(" OK: 7.1 данные были отправлены")
    else:
        print("ERROR: 7.1 данные не были отправлены")
except NoSuchElementException:
    print("ERROR: 7.1 такого элемента нет в DOM")


#time.sleep(10)
driver.quit()