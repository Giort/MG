import chromedriver_binary
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
from selenium.webdriver.common.keys import Keys
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

# driver.get("https://moigektar.ru"+ str(data["mg_loc"]["mg_cur_release_2"]))
driver.get("https://moigektar.ru")

# 1. проверка главной страницы "МГ"
print("Главная")

# баннер над хедером и модалка в нём
try:
    driver.find_element(by=By.CSS_SELECTOR, value="div:nth-child(2) .w-banner").click()
    try:
        driver.find_element(by=By.CSS_SELECTOR, value="body > div:last-of-type #consultationform-name").send_keys(str(data["test_data_valid"]["name"]))
        driver.find_element(by=By.CSS_SELECTOR, value="body > div:last-of-type #consultationform-phone").send_keys(str(data["test_data_valid"]["phone"]))
        driver.find_element(by=By.CSS_SELECTOR, value="body > div:last-of-type #consultationform-email").send_keys(str(data["test_data_valid"]["email"]))
        driver.find_element(by=By.CSS_SELECTOR, value="body > div:last-of-type form button").click()
        try:
            wait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//body/div[last()]//*[text()[contains(.,'Заявка отправлена')]]")))
            print("   OK: главная, модалка в баннере над хедером")#
        except:
            print('ERROR: не отправлены данные в: главная, модалка в баннере над хедером')
        driver.find_element(by=By.CSS_SELECTOR, value="body > div:last-of-type > div > div > button").click()
    except:
        print('ERROR: не могу ввести данные в: главная, модалка в баннере над хедером')
except:
    print('ERROR: не могу взаимодействовать: главная, баннер над хедером')

# модалка "Инвестиции" в блоке "Проект «Мой гектар» — это:", секция 5
try:
    driver.find_element(by=By.XPATH, value='//a[@href="#modal-descr-consult"]').click()
    driver.find_element(by=By.CSS_SELECTOR, value="#modal-descr-consult #consultationform-name").send_keys(str(data["test_data_valid"]["name"]))
    driver.find_element(by=By.CSS_SELECTOR, value="#modal-descr-consult #consultationform-phone").send_keys(str(data["test_data_valid"]["phone"]))
    driver.find_element(by=By.CSS_SELECTOR, value="#modal-descr-consult #consultationform-email").send_keys(str(data["test_data_valid"]["email"]))
    driver.find_element(by=By.XPATH, value="//*[@id='modal-descr-consult']//button[text()[contains(.,'Отправить заявку')]]").click()
    try:
        wait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//*[@id='modal-descr-consult']//*[text()[contains(.,'Заявка отправлена')]]")))
        print('   OK: главная, модалка про инвестиции в блоке "МГ - это"')
    except:
        print('ERROR: не отправлены данные в: главная, модалка про инвестиции в блоке "МГ - это"')
    driver.find_element(by=By.XPATH, value="//*[@id='modal-descr-consult']/div/div/*[@uk-close]").click()
except:
    print('ERROR: не могу взаимодействовать: главная, модалка про инвестиции в блоке "МГ - это"')

# модалка "Лесные озера" в блоке "Лучшие поселки"
try:
    driver.find_element(by=By.XPATH, value='//a[@href="#modal-lo"]').click()
    driver.find_element(by=By.CSS_SELECTOR, value="#modal-lo #consultationform-name").send_keys(str(data["test_data_valid"]["name"]))
    driver.find_element(by=By.CSS_SELECTOR, value="#modal-lo #consultationform-phone").send_keys(str(data["test_data_valid"]["phone"]))
    driver.find_element(by=By.CSS_SELECTOR, value="#modal-lo #consultationform-email").send_keys(str(data["test_data_valid"]["email"]))
    driver.find_element(by=By.XPATH, value="//*[@id='modal-lo']//button[text()[contains(.,'Отправить заявку')]]").click()
    try:
        wait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//*[@id='modal-lo']//*[text()[contains(.,'Заявка отправлена')]]")))
        print('   OK: главная, модалка "Лесные озера" в блоке "Лучшие поселки"')
    except:
        print('ERROR: не отправлены данные в: главная, модалка "Лесные озера" в блоке "Лучшие поселки"')
    driver.find_element(by=By.XPATH, value="//*[@id='modal-lo']/div/div/*[@uk-close]").click()
except:
    print('ERROR: не могу взаимодействовать: главная, модалка "Лесные озера" в блоке "Лучшие поселки"')

# модалка "Парк Патриот" в блоке "Лучшие поселки"
try:
    driver.find_element(by=By.XPATH, value='//a[@href="#modal-pp"]').click()
    driver.find_element(by=By.CSS_SELECTOR, value="#modal-pp #consultationform-name").send_keys(str(data["test_data_valid"]["name"]))
    driver.find_element(by=By.CSS_SELECTOR, value="#modal-pp #consultationform-phone").send_keys(str(data["test_data_valid"]["phone"]))
    driver.find_element(by=By.CSS_SELECTOR, value="#modal-pp #consultationform-email").send_keys(str(data["test_data_valid"]["email"]))
    driver.find_element(by=By.XPATH, value="//*[@id='modal-pp']//button[text()[contains(.,'Отправить заявку')]]").click()
    try:
        wait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//*[@id='modal-pp']//*[text()[contains(.,'Заявка отправлена')]]")))
        print('   OK: главная, модалка "Парк Патриот" в блоке "Лучшие поселки"')
    except:
        print('ERROR: не отправлены данные в: главная, модалка "Парк Патриот" в блоке "Лучшие поселки"')
    driver.find_element(by=By.XPATH, value="//*[@id='modal-pp']/div/div/*[@uk-close]").click()
except:
    print('ERROR: не могу взаимодействовать: главная, модалка "Парк Патриот" в блоке "Лучшие поселки"')

#модалка "Новая жизнь" в блоке "Лучшие поселки"
try:
    driver.find_element(by=By.XPATH, value='//a[@href="#modal-ng"]').click()
    driver.find_element(by=By.CSS_SELECTOR, value="#modal-ng #consultationform-name").send_keys(str(data["test_data_valid"]["name"]))
    driver.find_element(by=By.CSS_SELECTOR, value="#modal-ng #consultationform-phone").send_keys(str(data["test_data_valid"]["phone"]))
    driver.find_element(by=By.CSS_SELECTOR, value="#modal-ng #consultationform-email").send_keys(str(data["test_data_valid"]["email"]))
    driver.find_element(by=By.XPATH, value="//*[@id='modal-ng']//button[text()[contains(.,'Отправить заявку')]]").click()
    try:
        wait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//*[@id='modal-ng']//*[text()[contains(.,'Заявка отправлена')]]")))
        print('   OK: главная, модалка "Новая жизнь" в блоке "Лучшие поселки"')
    except:
        print('ERROR: не отправлены данные в: главная, модалка "Новая жизнь" в блоке "Лучшие поселки"')
    driver.find_element(by=By.XPATH, value="//*[@id='modal-ng']/div/div/*[@uk-close]").click()
except:
    print('ERROR: не могу взаимодействовать: главная, модалка "Новая жизнь" в блоке "Лучшие поселки"')

#модалка "Усадьба в подмосковье" в блоке "Лучшие поселки"
try:
    driver.find_element(by=By.XPATH, value='//a[@href="#modal-up"]').click()
    driver.find_element(by=By.CSS_SELECTOR, value="#modal-up #consultationform-name").send_keys(str(data["test_data_valid"]["name"]))
    driver.find_element(by=By.CSS_SELECTOR, value="#modal-up #consultationform-phone").send_keys(str(data["test_data_valid"]["phone"]))
    driver.find_element(by=By.CSS_SELECTOR, value="#modal-up #consultationform-email").send_keys(str(data["test_data_valid"]["email"]))
    driver.find_element(by=By.XPATH, value="//*[@id='modal-up']//button[text()[contains(.,'Отправить заявку')]]").click()
    try:
        wait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//*[@id='modal-up']//*[text()[contains(.,'Заявка отправлена')]]")))
        print('   OK: главная, модалка "Усадьба в подмосковье" в блоке "Лучшие поселки"')
    except:
        print('ERROR: не отправлены данные в: главная, модалка "Усадьба в подмосковье" в блоке "Лучшие поселки"')
    driver.find_element(by=By.XPATH, value="//*[@id='modal-up']/div/div/*[@uk-close]").click()
except:
    print('ERROR: не могу взаимодействовать: главная, модалка "Усадьба в подмосковье" в блоке "Лучшие поселки"')

#модалка "Лесная усадьба" в блоке "Поселки в развитии"
try:
    driver.find_element(by=By.XPATH, value='//*[(contains(@class, "uk-visible@s"))]//*[@uk-toggle="target: #modal-syn39"]//button').click()
    driver.find_element(by=By.CSS_SELECTOR, value='#modal-syn39[style="display: block;"] #consultationform-name').send_keys(str(data["test_data_valid"]["name"]))
    driver.find_element(by=By.CSS_SELECTOR, value='#modal-syn39[style="display: block;"] #consultationform-phone').send_keys(str(data["test_data_valid"]["phone"]))
    driver.find_element(by=By.CSS_SELECTOR, value='#modal-syn39[style="display: block;"] #consultationform-email').send_keys(str(data["test_data_valid"]["email"]))
    driver.find_element(by=By.CSS_SELECTOR, value='#modal-syn39[style="display: block;"] button[type="submit"]').click()
    try:
        wait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[(@id="modal-syn39") and (@style="display: block;")]//*[text()[contains(.,"Заявка отправлена")]]')))
        print('   OK: главная, модалка "Лесная усадьба" в блоке "Поселки в развитии"')
    except:
        print('ERROR: не отправлены данные в: главная, модалка "Лесная усадьба" в блоке "Поселки в развитии"')
    driver.find_element(by=By.CSS_SELECTOR, value='#modal-syn39[style="display: block;"] > div > div > button').click()
except:
    print('ERROR: не могу взаимодействовать: главная, модалка "Лесная усадьба" в блоке "Поселки в развитии"')

#модалка в блоке "Посетите усадьбу"
try:
    driver.find_element(by=By.XPATH, value='//div[@class="uk-first-column"]/button[@uk-toggle="target: #modal-stay"]').click()
    driver.find_element(by=By.CSS_SELECTOR, value="#modal-stay #consultationform-name").send_keys(str(data["test_data_valid"]["name"]))
    driver.find_element(by=By.CSS_SELECTOR, value="#modal-stay #consultationform-phone").send_keys(str(data["test_data_valid"]["phone"]))
    driver.find_element(by=By.CSS_SELECTOR, value="#modal-stay #consultationform-email").send_keys(str(data["test_data_valid"]["email"]))
    driver.find_element(by=By.XPATH, value="//*[@id='modal-stay']//button[text()[contains(.,'Отправить заявку')]]").click()
    try:
        wait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//*[@id='modal-stay']//*[text()[contains(.,'Заявка отправлена')]]")))
        print('   OK: главная, модалка в блоке "Посетите усадьбу"')
    except:
        print('ERROR: не отправлены данные в: главная, модалка в блоке "Посетите усадьбу"')
    driver.find_element(by=By.XPATH, value='//*[@id="modal-stay"]//*[(contains(@class,"uk-close"))]').click()
except:
    print('ERROR: не могу взаимодействовать: главная, модалка в блоке "Посетите усадьбу"')

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
    except:
        print('ERROR: не отправлены данные в: главная, модалка в блоке Бизнес-планы')
    driver.find_element(by=By.XPATH, value="//*[@id='modal-main']/div/div/*[@uk-close]").click()
except:
    print('ERROR: не могу взаимодействовать: главная, модалка в блоке Бизнес-планы')

# модалка в блоке "Познакомьтесь с проектом"
try:
    driver.find_element(by=By.XPATH, value="//*[@class='w-meeting']/div/div/div/a[text()[contains(.,'Записаться')]]//parent::div/a").click()
    driver.find_element(by=By.CSS_SELECTOR, value="#modal-meeting-meeting #consultationform-name").send_keys(str(data["test_data_valid"]["name"]))
    driver.find_element(by=By.CSS_SELECTOR, value="#modal-meeting-meeting #consultationform-phone").send_keys(str(data["test_data_valid"]["phone"]))
    driver.find_element(by=By.CSS_SELECTOR, value="#modal-meeting-meeting #consultationform-email").send_keys(str(data["test_data_valid"]["email"]))
    driver.find_element(by=By.XPATH, value="//*[@id='modal-meeting-meeting']//button[text()[contains(.,'Отправить заявку')]]").click()
    try:
        wait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//*[@id='modal-meeting-meeting']//*[text()[contains(.,'Заявка отправлена')]]")))
        print("   OK: главная, модалка в блоке Приглашаем на встречу\n")
    except:
        print('ERROR: не отправлены данные в: главная, модалка в блоке Приглашаем на встречу\n')
    driver.find_element(by=By.XPATH, value="//*[@id='modal-meeting-meeting']/div/div/*[@uk-close]").click()
except:
    print('ERROR: не могу взаимодействовать: главная, модалка в блоке Приглашаем на встречу\n')


# Развитие
print("Развитие")

# модалка 'Получить консультацию' в 'Развитие - Развитие поселков'
try:
    driver.get("https://moigektar.ru/growth")
    driver.find_element(by=By.XPATH, value="/descendant::*[@uk-toggle='target: #modal-main'][1]").click()
    driver.find_element(by=By.CSS_SELECTOR, value="#modal-main #consultationform-name").send_keys(str(data["test_data_valid"]["name"]))
    driver.find_element(by=By.CSS_SELECTOR, value="#modal-main #consultationform-phone").send_keys(str(data["test_data_valid"]["phone"]))
    driver.find_element(by=By.CSS_SELECTOR, value="#modal-main #consultationform-email").send_keys(str(data["test_data_valid"]["email"]))
    driver.find_element(by=By.XPATH, value="//*[@id='modal-main']//button[text()[contains(.,'Отправить')]]").click()
    try:
        wait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//*[@id='modal-main']//*[text()[contains(.,'Заявка отправлена')]]")))
        print("   OK: модалка 'Получить консультацию' в 'Развитие - Развитие поселков'")
    except:
        print("ERROR: не отправлены данные: модалка 'Получить консультацию' в 'Развитие - Развитие поселков'")
    driver.find_element(by=By.XPATH, value="//*[@id='modal-main']/div/div/*[@uk-close]").click()
except:
    print("ERROR: не могу взаимодействовать: модалка 'Получить консультацию' в 'Развитие - Развитие поселков'")

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
    except:
        print("ERROR: не отправлены данные: модалка 'Заказать услугу' в 'Развитие - Глазами инвестора'")
    driver.find_element(by=By.XPATH, value="//*[@id='modal-calculation']/div/div/*[@uk-close]").click()
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
    except:
        print("ERROR: не отправлены данные: модалка 'Подобрать участок' в 'Развитие - Глазами инвестора'")
    driver.find_element(by=By.XPATH, value="//*[@id='modal-select']/div/div/*[@uk-close]").click()
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
    except:
        print("ERROR: не отправлены данные: модалка 'Заказать услугу' в 'Развитие - Капитализация'")
    driver.find_element(by=By.XPATH, value="//*[@id='modal-capitalization']/div/div/*[@uk-close]").click()
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
    except:
        print("ERROR: не отправлены данные: модалка 'Заказать услугу' в 'Развитие - Базовая'")
    driver.find_element(by=By.XPATH, value="//*[@id='modal-select']/div/div/*[@uk-close]").click()
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
    except:
        print("ERROR: не отправлены данные: модалка 'Заказать услугу' в 'Развитие - Предприниматель'")
    driver.find_element(by=By.XPATH, value="//*[@id='modal-select']/div/div/*[@uk-close]").click()
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
    except:
        print("ERROR: не отправлены данные: модалка 'Заказать услугу' в 'Развитие - Фермер'")
    driver.find_element(by=By.XPATH, value="//*[@id='modal-select']/div/div/*[@uk-close]").click()
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
    except:
        print("ERROR: не отправлены данные: модалка 'Заказать услугу' в 'Развитие - Фамильная'\n")
    driver.find_element(by=By.XPATH, value="//*[@id='modal-select']/div/div/*[@uk-close]").click()
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
    except:
        print("ERROR: не отправлены данные: модалка 'Заказать услугу' в 'Коллективное строительство ЛЭП'")
    driver.find_element(by=By.XPATH, value="//*[@id='modal-specialist']/div/div/*[@uk-close]").click()
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
    except:
        print("ERROR: не отправлены данные: модалка 'Получить консультацию' в 'Коллективное строительство ЛЭП'\n")
    driver.find_element(by=By.XPATH, value="//*[@id='modal-specialist1']/div/div/*[@uk-close]\n").click()
except:
    print("ERROR: не могу взаимодействовать: модалка 'Получить консультацию' в 'Коллективное строительство ЛЭП'\n")


# Бизнес-планы
print("Бизнес-планы")

# модалка 'Получить консультацию' в 'Бизнес-планы' на первой карточке
try:
    driver.get("https://moigektar.ru/business-plans")
    btn = wait(driver, 14).until(EC.element_to_be_clickable((By.XPATH, "//div[@data-key='1']//*[@uk-toggle='target: #modal-main']")))
    btn.click()
    driver.find_element(by=By.CSS_SELECTOR, value="#modal-main #consultationform-name").send_keys(str(data["test_data_valid"]["name"]))
    driver.find_element(by=By.CSS_SELECTOR, value="#modal-main #consultationform-phone").send_keys(str(data["test_data_valid"]["phone"]))
    driver.find_element(by=By.CSS_SELECTOR, value="#modal-main #consultationform-email").send_keys(str(data["test_data_valid"]["email"]))
    driver.find_element(by=By.XPATH, value="//*[@id='modal-main']//button[text()[contains(.,'Отправить')]]").click()
    try:
        wait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//*[@id='modal-main']//*[text()[contains(.,'Заявка отправлена')]]")))
        print("   OK: модалка 'Получить консультацию' в 'Бизнес-планы'\n")
    except:
        print("ERROR: не отправлены данные: модалка 'Получить консультацию' в 'Бизнес-планы'\n")
    driver.find_element(by=By.XPATH, value="//*[@id='modal-main']/div/div/*[@uk-close]").click()
except:
    print("ERROR: не могу взаимодействовать: модалка 'Получить консультацию' в 'Бизнес-планы'\n")

# Вакансии
print("Вакансии")

# модалка 'Оставьте анкету' в 'Вакансии'
try:
    driver.get("https://moigektar.ru/hr")
    btn = wait(driver, 14).until(EC.element_to_be_clickable((By.XPATH, "/descendant::*[@uk-toggle='target: #modal-main1'][1]")))
    btn.click()
    driver.find_element(by=By.CSS_SELECTOR, value="#modal-main1 #consultationform-name").send_keys(str(data["test_data_valid"]["name"]))
    driver.find_element(by=By.CSS_SELECTOR, value="#modal-main1 #consultationform-phone").send_keys(str(data["test_data_valid"]["phone"]))
    driver.find_element(by=By.CSS_SELECTOR, value="#modal-main1 #consultationform-email").send_keys(str(data["test_data_valid"]["email"]))
    driver.find_element(by=By.XPATH, value="//*[@id='modal-main1']//button[text()[contains(.,'Отправить')]]").click()
    try:
        wait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//*[@id='modal-main1']//*[text()[contains(.,'Заявка отправлена')]]")))
        print("   OK: модалка 'Оставьте анкету' в 'Вакансии'")
    except:
        print("ERROR: не отправлены данные: модалка 'Оставьте анкету' в 'Вакансии'")
    driver.find_element(by=By.XPATH, value="//*[@id='modal-main1']/div/div/*[@uk-close]").click()
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

