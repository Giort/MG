import chromedriver_binary
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


# избавляемся от поп-апа, который перекрывает доступ ко кнопкам
time.sleep(1)
popup_w = driver.find_element(by=By.XPATH, value="//div[@id='visitors-popup']")
driver.execute_script("""
var auth_win = arguments[0];
auth_win.remove();
""", popup_w)

# 1.1 проверка формы "Оставьте заявку", Арина
# проверяю отправку данных через форму
# проверяю наличие правильного атрибута lgForm
try:
    title = driver.find_element(by=By.XPATH, value="/descendant::*[text()[contains(.,'Арина')]][2]")
    # сохраняю текущий динамический id формы в переменную для того, чтобы последующие локаторы не были такого вида:
    # //h1/*[text()[contains(.,'Хотите узнать')]]//parent::h1//following-sibling::ul[2]//input[@id='consultationform-phone']
    form_id = driver.find_element(by=By.XPATH, value="(//*[text()[contains(.,'Арина')]]/ancestor::div[contains(@id, 'cfw')])[1]").get_attribute("id")
    actions.move_to_element(title).perform()
    driver.find_element(by=By.XPATH, value="(//div[@id='"+ form_id +"']//*[@id='consultationform-phone'])[1]").send_keys(str(data["test_data_valid"]["phone"]))
    driver.find_element(by=By.XPATH, value="(//div[@id='"+ form_id +"']//*[text()[contains(.,'Отправить')]])[1]").click()
    try:
        name_input = driver.find_element(by=By.XPATH, value="(//div[@id='"+ form_id +"']//*[@id='consultationform-name'])[2]")
        name_input.click()
    except Exception as e:
        error_msg = str(e).split('\n')[0]
        print("Ошибка: главная, форма с Ариной, отправка через форму — ", error_msg)
    try:
        driver.find_element(by=By.XPATH, value="(//div[@id='"+ form_id +"']//*[@value='mg_main_page_arina_callback'])[2]")
    except Exception as e:
        error_msg = str(e).split('\n')[0]
        print("Ошибка: главная, форма с Ариной, lgForm — ", error_msg)
except Exception as e:
        error_msg = str(e).split('\n')[0]
        print("Ошибка: главная, форма с Ариной — ", error_msg)

# 1.2 проверка формы "Оставьте заявку", Андрей - проверяю наличие правильного атрибута lgForm
try:
    form_id = driver.find_element(by=By.XPATH, value="(//*[text()[contains(.,'Андрей')]]/ancestor::div[contains(@id, 'cfw')]//*[@value='mg_main_page_andrey_callback'])[1]")
except Exception as e:
        error_msg = str(e).split('\n')[0]
        print("Ошибка: главная, форма с Андреем, lgForm — ", error_msg)

# 1.3 проверка формы "Оставьте заявку", София - проверяю наличие правильного атрибута lgForm
try:
    form_id = driver.find_element(by=By.XPATH, value="(//*[text()[contains(.,'София')]]/ancestor::div[contains(@id, 'cfw')]//*[@value='mg_main_page_sofia_callback'])[1]")
except Exception as e:
        error_msg = str(e).split('\n')[0]
        print("Ошибка: главная, форма с Софией, lgForm — ", error_msg)

# 1.4 проверка формы "Оставьте заявку", Максим - проверяю наличие правильного атрибута lgForm
try:
    form_id = driver.find_element(by=By.XPATH, value="(//*[text()[contains(.,'Максим')]]/ancestor::div[contains(@id, 'cfw')]//*[@value='mg_main_page_max_callback'])[1]")
except Exception as e:
        error_msg = str(e).split('\n')[0]
        print("Ошибка: главная, форма с Максимом, lgForm — ", error_msg)

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
        wait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//div[@id='"+ form_id +"']//*[text()[contains(.,'Заявка отправлена')]]")))
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
        wait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//div[@id='"+ form_id +"']//*[text()[contains(.,'Заявка отправлена')]]")))
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
        wait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//div[@id='"+ form_id +"']//*[text()[contains(.,'Заявка отправлена')]]")))
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
        wait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//div[@id='"+ form_id +"']//*[text()[contains(.,'Заявка отправлена')]]")))
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
        wait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//div[@id='"+ form_id +"']//*[text()[contains(.,'Заявка отправлена')]]")))
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
        wait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//div[@id='"+ form_id +"']//*[text()[contains(.,'Заявка отправлена')]]")))
        print(" OK: о проекте 6/6 данные были отправлены")
    except:
        print('ERROR: не отправлены данные в форму "Хотите узнать подробнее о проекте?" в "О проекте" - "Отзывы"')
except:
    print('ERROR: не могу найти форму "Хотите узнать подробнее о проекте?" в "О проекте" - "Отзывы"')


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
        wait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//div[@id='"+ form_id +"']//*[text()[contains(.,'Заявка отправлена')]]")))
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
        wait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//div[@id='"+ form_id +"']//*[text()[contains(.,'Заявка отправлена')]]")))
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
        wait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//div[@id='"+ form_id +"']//*[text()[contains(.,'Заявка отправлена')]]")))
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
        wait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//div[@id='"+ form_id +"']//*[text()[contains(.,'Заявка отправлена')]]")))
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
        wait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//div[@id='"+ form_id +"']//*[text()[contains(.,'Заявка отправлена')]]")))
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
        wait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//div[@id='"+ form_id +"']//*[text()[contains(.,'Заявка отправлена')]]")))
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
        wait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//div[@id='"+ form_id +"']//*[text()[contains(.,'Заявка отправлена')]]")))
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
        wait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//div[@id='"+ form_id +"']//*[text()[contains(.,'Заявка отправлена')]]")))
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
        wait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//div[@id='"+ form_id +"']//*[text()[contains(.,'Заявка отправлена')]]")))
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
        wait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//div[@id='"+ form_id +"']//*[text()[contains(.,'Заявка отправлена')]]")))
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
        wait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//div[@id='"+ form_id +"']//*[text()[contains(.,'Заявка отправлена')]]")))
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
        wait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//div[@id='"+ form_id +"']//*[text()[contains(.,'Заявка отправлена')]]")))
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
        wait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//div[@id='"+ form_id +"']//*[text()[contains(.,'Заявка отправлена')]]")))
        print(" OK: меры поддержки 6/6 данные были отправлены")
    except:
        print('ERROR: не отправлены данные в форму "Хотите узнать подробнее о господдержке?" в "Меры поддержки" - "Сельская ипотека"')
except:
    print('ERROR: не могу найти форму "Хотите узнать подробнее о господдержке?" в "Меры поддержки" - "Сельская ипотека"')


# 6 проверка раздела "Вопрос-ответ"
# 6.1 переход на страницу "Вопрос-ответ - подробности о проектах"
driver.get("https://moigektar.ru/faq")
try:
    form_id = driver.find_element(by=By.XPATH, value='//b[text()[contains(.,"Оставьте ")]]//ancestor::div[5]').get_attribute('id')
    try:
        driver.find_element(by=By.XPATH, value="//div[@id='"+ form_id +"']//*[@id='consultationform-name']").send_keys(str(data["test_data_valid"]["name"]))
        driver.find_element(by=By.XPATH, value="//div[@id='"+ form_id +"']//*[@id='consultationform-phone']").send_keys(str(data["test_data_valid"]["phone"]))
        driver.find_element(by=By.XPATH, value="//div[@id='"+ form_id +"']//*[text()[contains(.,'Отправить')]]").click()
        wait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//div[@id='"+ form_id +"']//*[text()[contains(.,'Заявка отправлена')]]")))
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
    name = wait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[@id='"+ form_id +"']//*[@id='hrform-name']")))
    name.send_keys(str(data["test_data_valid"]["name"]))
    driver.find_element(by=By.XPATH, value="//div[@id='"+ form_id +"']//*[@id='hrform-phone']").send_keys(str(data["test_data_valid"]["phone"]))
    driver.find_element(by=By.XPATH, value="//div[@id='"+ form_id +"']//*[text()[contains(.,'Отправить')]]").click()
    try:
        wait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//div[@id='"+ form_id +"']//*[text()[contains(.,'Заявка отправлена')]]")))
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
        wait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//div[@id='"+ form_id +"']//*[text()[contains(.,'Заявка отправлена')]]")))
        print(" OK: данные из контактов были отправлены")
    except:
        print('ERROR: не отправлены данные в форму "Хотите задать вопрос специалисту?" в "Контактах"')
except:
    print('ERROR: не могу найти форму "Хотите задать вопрос специалисту?" в "Контактах"')


#time.sleep(8)
driver.quit()

