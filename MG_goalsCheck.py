import time

from exceptiongroup import catch
from selenium.webdriver.support.ui import WebDriverWait as wait
from seleniumwire import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
ch_options = Options()
ch_options.add_argument('--headless')
ch_options.add_argument("--window-size=1680,1000")
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
# Настройка драйвера с Selenium Wire
# Включаем перехват запросов
sw_options = {'disable_capture': False}
import json

with open('data.json', 'r') as file:
    data = json.load(file)

# мод. авторизации из хедера: отправляется цель при открытии и взаимодействии
def check_header_auth_modal_goal(text):
    driver = webdriver.Chrome(
        seleniumwire_options=sw_options,
        options = ch_options)
    driver.get('https://moigektar.ru/?__counters=1')
    button = driver.find_element(By.XPATH, '(//*[@href="#modal-auth-lk"])[1]')
    button.click()
    input = driver.find_element(by=By.XPATH, value='(//*[@id="modal-auth-lk"]//*[@id="consultationform-phone"])[1]')
    input.click()
    time.sleep(5)

    request_found = False
    for request in driver.requests:
        if text in request.url:
            print(f"     ОК: при взаимодействии с мод. авторизации на главной отправляется цель '{text}'")
            request_found = True
            break
    if not request_found:
        print(f"Ошибка: при взаимодействии с мод. авторизации на главной текст '{text}' не найден в отправленных запросах")

    driver.quit()
    return request_found

try:
    check_header_auth_modal_goal('catalog_modal_auth')
except Exception as e:
        error_msg = str(e).split('\n')[0]
        print('Ошибка: при взаимодействии с мод. авторизации на главной — ', error_msg)


# мод. авторизации в каталоге: отправляется цель, если нажали "Вернуться на главную"
def check_catalog_modal_auth_back_to_main_goal(text):
    driver = webdriver.Chrome(
        seleniumwire_options=sw_options,
        options = ch_options)
    # Открываем страницу каталога
    driver.get('https://moigektar.ru/catalogue/?__counters=1')
    back_button = driver.find_element(By.XPATH, '//*[text()[contains(., "Вернуться на главную")]]')
    back_button.click()

    request_found = False
    for request in driver.requests:
        if text in request.url:
            print(f"     ОК: при возврате на главную из мод. авторизации в каталоге отправляется цель '{text}'")
            request_found = True
            break
    if not request_found:
        print(f"Ошибка: при возврате на главную из мод. авторизации в каталоге текст '{text}' не найден в отправленных запросах")

    driver.quit()
    return request_found

try:
    check_catalog_modal_auth_back_to_main_goal('catalog_modal_auth_button_main')
except Exception as e:
        error_msg = str(e).split('\n')[0]
        print('Ошибка: при возврате на главную из мод. авторизации в каталоге — ', error_msg)

# мод. авторизации: отправляется цель, если нажали кнопки соцсетей
def check_catalog_modal_social_media_btn_goal(btn_selector, text, btn):
    driver = webdriver.Chrome(
        seleniumwire_options=sw_options,
        options = ch_options)
    driver.get('https://moigektar.ru')
    driver.find_element(By.XPATH, '(//*[@href="#modal-auth-lk"])[1]').click()
    button = driver.find_element(By.CLASS_NAME, btn_selector)
    button.click()
    time.sleep(5)

    request_found = False
    for request in driver.requests:
        if text in request.url:
            print(f"     ОК: при нажатии в мод. авторизации на кнопку '{btn}' отправляется цель '{text}'")
            request_found = True
            break
    if not request_found:
        print(f"Ошибка: при нажатии в мод. авторизации на кнопку '{btn}' текст '{text}' не найден в отправленных запросах")

    driver.quit()
    return request_found

try:
    check_catalog_modal_social_media_btn_goal(
        btn_selector    =   'js-analytics-vk-auth-button-click',
        text            =   'vk_auth_button_click',
        btn             =   'ВК')
except Exception as e:
        error_msg = str(e).split('\n')[0]
        print("Ошибка: при нажатии в мод. авторизации на кнопку ВК — ", error_msg)

try:
    check_catalog_modal_social_media_btn_goal(
        btn_selector    =   'js-analytics-ya-auth-button-click',
        text            =   'ya_auth_button_click',
        btn             =   'Яндекс')
except Exception as e:
        error_msg = str(e).split('\n')[0]
        print('Ошибка: при нажатии в мод. авторизации на кнопку Яндекс — ', error_msg)

# квиз: отправляется цель, если нажали кнопки вызова квиза
def check_quiz_btn_goal(quiz_btn, goal, place):
    driver = webdriver.Chrome(
        seleniumwire_options=sw_options,
        options = ch_options)
    actions = ActionChains(driver)
    driver.get('https://moigektar.ru')
    btn = driver.find_element(By.XPATH, quiz_btn)
    actions.move_to_element(btn).perform()
    actions.send_keys(Keys.ARROW_DOWN).send_keys(Keys.ARROW_DOWN).perform()
    btn.click()
    time.sleep(5)

    request_found = False
    for request in driver.requests:
        if goal in request.url:
            print(f'     ОК: при нажатии на кнопку квиза "{place}" отправляется цель "{goal}"')
            request_found = True
            break
    if not request_found:
        print(f'Ошибка: при нажатии на кнопку квиза "{place}" текст "{goal}" не найден в отправленных запросах')

    driver.quit()
    return request_found

# кнопка квиза в хедере
try:
    check_quiz_btn_goal(
        quiz_btn    =  '(//*[contains(@class, "w-navbar")]//a[text()[contains(., "Каталог участков")]])[2]',
        goal        =  'quiz_btn_v2',
        place       =  'в хедере')
except Exception as e:
        error_msg = str(e).split('\n')[0]
        print('Ошибка: при нажатии на кнопку квиза в хедере" — ', error_msg)

# кнопка квиза в "Описании проекта"
try:
    check_quiz_btn_goal(
        quiz_btn    =  '(//*[@id="w-descr"]//a)[2]',
        goal        =  'quiz_btn_v2',
        place       =  'в "Описании проекта"')
except Exception as e:
        error_msg = str(e).split('\n')[0]
        print('Ошибка: при нажатии на кнопку квиза в "Описании проекта" — ', error_msg)

# кнопка квиза в "Успешных примерах"
try:
    check_quiz_btn_goal(
        quiz_btn    =  '(//*[@id="best-example"]//a[text()[contains(., "Каталог участков")]])[1]',
        goal        =  'quiz_btn_v2',
        place       =  'в "Успешных примерах"')
except Exception as e:
        error_msg = str(e).split('\n')[0]
        print('Ошибка: при нажатии на кнопку квиза в "Успешных примерах" — ', error_msg)

# карточки активов: нажали на карточку
def check_batch_card_goal(text):
    driver = webdriver.Chrome(
        seleniumwire_options=sw_options,
        options=ch_options)
    driver.get('https://moigektar.ru/?__counters=1')
    card = driver.find_element(By.XPATH, '(//div[@id="catalogueSpecial"]//li)[1]')
    card.click()
    time.sleep(5)

    request_found = False
    for request in driver.requests:
        if text in request.url:
            print(f"     ОК: при нажатии на карточку актива отправляется цель '{text}'")
            request_found = True
            break
    if not request_found:
        print(
            f"Ошибка: при нажатии на карточку актива текст '{text}' не найден в отправленных запросах")

    driver.quit()
    return request_found

try:
    check_batch_card_goal('catalog_v4.batch_card_click')
except Exception as e:
    error_msg = str(e).split('\n')[0]
    print('Ошибка: при нажатии на карточку актива — ', error_msg)

# карточки активов: нажатия на элементы в карточке
def check_batch_card_button_goal(button_tests):
    driver = webdriver.Chrome(
        seleniumwire_options=sw_options,
        options=ch_options)
    actions = ActionChains(driver)

    try:
        driver.get("https://moigektar.ru")

        #авторизация
        driver.find_element(By.XPATH, '(//*[@href="#modal-auth-lk"])[1]').click()
        time.sleep(2)
        tab = driver.find_element(By.XPATH, '//*[text()="По паролю"]')
        name = driver.find_element(By.XPATH, '//*[@id="authform-login"]')
        password = driver.find_element(By.XPATH, '//*[@id="authform-password"]')
        btn = driver.find_element(By.XPATH, '//*[text()="Войти"]')
        tab.click()
        name.send_keys(str(data["LK_cred"]["login"]))
        password.send_keys(str(data["LK_cred"]["password"]))
        btn.click()
        time.sleep(10)

        # Переход к СП и проверка отправки целей
        driver.get("https://moigektar.ru#catalogueSpecial")
        time.sleep(5)
        for test in button_tests:
            try:
                elem = driver.find_element(By.XPATH, test['loc'])
                elem.click()
                time.sleep(15)

                request_found = False
                for request in driver.requests:
                    if test['goal'] in request.url:
                        print(f"     ОК: при нажатии на {test['place']} отправляется цель '{test['goal']}'")
                        request_found = True
                        break

                if not request_found:
                    print(f"Ошибка: при нажатии на {test['place']} текст '{test['goal']}' не найден")

            except Exception as e:
                error_msg = str(e).split('\n')[0]
                print(f'Ошибка: при нажатии на {test["place"]} — {error_msg}')

    finally:
        driver.quit()

# Параметры для check_batch_card_button_goal
button_tests = [
    {
        'loc': '(//div[@id="catalogueSpecial"]//*[@src="/img/catalog/icons/share-light.svg"])[1]',
        'goal': 'catalog_v4.batch_share',
        'place': 'кнопку "Поделиться" на карточке актива'
    },
    {
        'loc': '(//div[@id="catalogueSpecial"]//*[@src="/img/catalog/icons/pdf.svg"])[1]',
        'goal': 'catalog_v4.batch_presentation_download',
        'place': 'кнопку "pdf" на карточке актива'
    }
]

# Запуск
check_batch_card_button_goal(button_tests)