import time
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
from datetime import datetime


# Засекаем время начала теста
start_time = time.time()

with open('data.json', 'r') as file:
    data = json.load(file)

# Проверяемый урл
MG_BASE_URL = "https://moigektar.ru"
#MG_BASE_URL = "http://moigektar.localhost"


print(f"\n     Проверка отправки целей на МГ на домене {MG_BASE_URL}")


def init_driver():
    """Инициализация драйвера"""
    driver = webdriver.Chrome(
        seleniumwire_options=sw_options,
        options=ch_options)
    return driver

def remove_popup(driver):
    """Удаление попапа посетителей"""
    try:
        popup_w = driver.find_element(by=By.XPATH, value="//div[@id='visitors-popup']")
        driver.execute_script("arguments[0].remove();", popup_w)
    except Exception:
        pass

def auth_user(driver):
    """Авторизация пользователя"""
    try:
        driver.get("https://moigektar.ru/?__counters=1")
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
        return True
    except Exception as e:
        print(f"ERROR: Не удалось авторизоваться - {str(e)}")
        return False

print()
# мод. авторизации в каталоге: отправляется цель, когда модалка показана
def check_catalog_modal_auth_show(tests, max_attempts=3):
    # Словарь для хранения результатов каждого теста
    results = {test['text']: {'success': False, 'attempts': 0} for test in tests}

    for attempt in range(max_attempts):
        driver = None
        try:
            driver = init_driver()

            for test in tests:
                # Если тест уже успешно пройден, пропускаем
                if results[test['text']]['success']:
                    continue

                try:
                    driver.get(test['url'])
                    time.sleep(10)

                    request_found = False
                    for request in driver.requests:
                        if test['goal'] in request.url:
                            results[test['text']]['success'] = True
                            results[test['text']]['attempts'] = attempt + 1
                            request_found = True
                            break

                    if not request_found:
                        results[test['text']]['attempts'] = attempt + 1

                except Exception as e:
                    results[test['text']]['attempts'] = attempt + 1

            all_passed = all(result['success'] for result in results.values())
            if all_passed:
                break

        except Exception as e:
            print(f"Критическая ошибка в попытке {attempt + 1}: {e}")
        finally:
            if driver:
                driver.quit()

            if attempt < max_attempts - 1 and not all(result['success'] for result in results.values()):
                time.sleep(5)

    all_success = True
    for test in tests:
        text = test['text']
        result = results[text]

        if result['success']:
            print(f"     ОК: при открытии {test['text']} отправляется цель '{test['goal']}'")
        else:
            print(f"ERROR: при открытии {test['text']} текст '{test['goal']}' не найден в отправленных запросах")
            all_success = False

    return all_success

# Параметры для check_catalog_modal_auth_show
modal_tests = [
    {
        'url': 'https://moigektar.ru/catalogue/?__counters=1',
        'text': 'каталога без авторизации',
        'goal': 'catalog_v4.authwall_shown'
    },
    {
        'url': 'https://moigektar.ru/batches/59228?__counters=1',
        'text': 'стр. актива без авторизации',
        'goal': 'catalog_v4.authwall_shown'
    }
]

# Запуск
try:
    check_catalog_modal_auth_show(modal_tests)
except Exception as e:
    error_msg = str(e).split('\n')[0]
    print('ERROR: при проверке модалок авторизации — ', error_msg)


# мод. авторизации из хедера: отправляется цель при открытии
def check_header_auth_modal_goal(text, max_attempts=3):

    results = {'success': False, 'attempts': 0}

    for attempt in range(max_attempts):
        driver = None
        try:
            driver = init_driver()
            actions = ActionChains(driver)
            driver.get('https://moigektar.ru/?__counters=1')
            actions.send_keys(Keys.PAGE_DOWN).perform()
            button = driver.find_element(By.XPATH, '(//*[@href="#modal-auth-lk"])[1]')
            button.click()
            time.sleep(5)

            request_found = False
            for request in driver.requests:
                if text in request.url:
                    results['success'] = True
                    results['attempts'] = attempt + 1
                    request_found = True
                    break

            if request_found:
                break

        except Exception as e:
            results['attempts'] = attempt + 1
        finally:
            if driver:
                driver.quit()

            if attempt < max_attempts - 1 and not results['success']:
                time.sleep(5)

    if results['success']:
        print(f"     ОК: при вызове мод. авторизации из навбара отправляется цель '{text}'")
    else:
        print(
            f"ERROR: при вызове мод. авторизации из навбара текст '{text}' не найден в отправленных запросах")

    return results['success']

try:
    check_header_auth_modal_goal('catalog_modal_auth')
except Exception as e:
    error_msg = str(e).split('\n')[0]
    print('ERROR: при вызове мод. авторизации из навбара — ', error_msg)


# мод. авторизации в каталоге: отправляется цель, если нажали "Вернуться на главную"
def check_catalog_modal_auth_back_to_main_goal(text, max_attempts=3):
    # Словарь для хранения результатов
    results = {'success': False, 'attempts': 0}

    for attempt in range(max_attempts):
        driver = None
        try:
            driver = init_driver()
            # Открываем страницу каталога
            driver.get('https://moigektar.ru/catalogue/?__counters=1')
            back_button = driver.find_element(By.XPATH, '//*[text()[contains(., "Вернуться на главную")]]')
            time.sleep(1)
            back_button.click()

            request_found = False
            for request in driver.requests:
                if text in request.url:
                    results['success'] = True
                    results['attempts'] = attempt + 1
                    request_found = True
                    break

            if request_found:
                break

        except Exception as e:
            results['attempts'] = attempt + 1
        finally:
            if driver:
                driver.quit()

            if attempt < max_attempts - 1 and not results['success']:
                time.sleep(5)

    if results['success']:
        print(f"     ОК: при возврате на главную из мод. авторизации в каталоге отправляется цель '{text}'")
    else:
        print(
            f"ERROR: при возврате на главную из мод. авторизации в каталоге текст '{text}' не найден в отправленных запросах")

    return results['success']


try:
    check_catalog_modal_auth_back_to_main_goal('catalog_modal_auth_button_main')
except Exception as e:
    error_msg = str(e).split('\n')[0]
    print('ERROR: при возврате на главную из мод. авторизации в каталоге — ', error_msg)


# мод. авторизации: отправляется цель, если нажали кнопки соцсетей
def check_catalog_modal_social_media_btn_goal(tests, max_attempts=3):

    results = {test['btn']: {'success': False, 'attempts': 0} for test in tests}

    for attempt in range(max_attempts):
        driver = None
        try:
            driver = init_driver()
            actions = ActionChains(driver)

            for test in tests:

                if results[test['btn']]['success']:
                    continue

                try:
                    driver.get('https://moigektar.ru/?__counters=1')
                    actions.send_keys(Keys.PAGE_DOWN).perform()
                    driver.find_element(By.XPATH, '(//*[@href="#modal-auth-lk"])[1]').click()
                    button = driver.find_element(By.CLASS_NAME, test['btn_selector'])
                    button.click()
                    time.sleep(5)

                    request_found = False
                    for request in driver.requests:
                        if test['text'] in request.url:
                            results[test['btn']]['success'] = True
                            results[test['btn']]['attempts'] = attempt + 1
                            request_found = True
                            break

                    if not request_found:
                        results[test['btn']]['attempts'] = attempt + 1

                except Exception as e:
                    results[test['btn']]['attempts'] = attempt + 1

            all_passed = all(result['success'] for result in results.values())
            if all_passed:
                break

        except Exception as e:
            print(f"Критическая ошибка в попытке {attempt + 1}: {e}")
        finally:
            if driver:
                driver.quit()

            if attempt < max_attempts - 1 and not all(result['success'] for result in results.values()):
                time.sleep(5)

    all_success = True
    for test in tests:
        btn = test['btn']
        result = results[btn]

        if result['success']:
            print(f"     ОК: при нажатии в мод. авторизации на кнопку '{test['btn']}' отправляется цель '{test['text']}'")
        else:
            print(f"ERROR: при нажатии в мод. авторизации на кнопку '{test['btn']}' текст '{test['text']}' не найден в отправленных запросах")
            all_success = False

    return all_success

# Параметры для check_catalog_modal_social_media_btn_goal
social_tests = [
    {
        'btn_selector': 'js-analytics-vk-auth-button-click',
        'text': 'vk_auth_button_click',
        'btn': 'ВК'
    },
    {
        'btn_selector': 'js-analytics-ya-auth-button-click',
        'text': 'ya_auth_button_click',
        'btn': 'Яндекс'
    }
]

# Запуск
try:
    check_catalog_modal_social_media_btn_goal(social_tests)
except Exception as e:
    error_msg = str(e).split('\n')[0]
    print('ERROR: при проверке кнопок соцсетей в модалке авторизации — ', error_msg)


# квиз: отправляется цель, если нажали кнопки вызова квиза
def check_quiz_btn_goal(tests, max_attempts=3):

    results = {test['place']: {'success': False, 'attempts': 0} for test in tests}

    for attempt in range(max_attempts):
        driver = None
        try:
            driver = init_driver()
            actions = ActionChains(driver)

            for test in tests:

                if results[test['place']]['success']:
                    continue

                try:
                    driver.get('https://moigektar.ru/?__counters=1')
                    btn = driver.find_element(By.XPATH, test['quiz_btn'])
                    actions.move_to_element(btn).perform()
                    actions.send_keys(Keys.ARROW_DOWN).send_keys(Keys.ARROW_DOWN).perform()
                    btn.click()
                    time.sleep(10)

                    request_found = False
                    for request in driver.requests:
                        if test['goal'] in request.url:
                            results[test['place']]['success'] = True
                            results[test['place']]['attempts'] = attempt + 1
                            request_found = True
                            break

                    if not request_found:
                        results[test['place']]['attempts'] = attempt + 1

                except Exception as e:
                    results[test['place']]['attempts'] = attempt + 1

            all_passed = all(result['success'] for result in results.values())
            if all_passed:
                break

        except Exception as e:
            print(f"Критическая ошибка в попытке {attempt + 1}: {e}")
        finally:
            if driver:
                driver.quit()

            if attempt < max_attempts - 1 and not all(result['success'] for result in results.values()):
                time.sleep(5)

    all_success = True
    for test in tests:
        place = test['place']
        result = results[place]

        if result['success']:
            print(f'     ОК: при нажатии на кнопку квиза {test["place"]} отправляется цель "{test["goal"]}"')
        else:
            print(f'ERROR: при нажатии на кнопку квиза {test["place"]} текст "{test["goal"]}" не найден в отправленных запросах')
            all_success = False

    return all_success

# Параметры для check_quiz_btn_goal
quiz_tests = [
    {
        'quiz_btn': '(//*[contains(@class, "w-navbar")]//a[text()[contains(., "Каталог участков")]])[2]',
        'goal': 'quiz_btn_v2',
        'place': 'в хедере'
    },
    {
        'quiz_btn': '(//*[@id="w-descr"]//a)[3]',
        'goal': 'quiz_btn_v2',
        'place': 'в "Описании проекта"'
    },
    {
        'quiz_btn': '(//*[@id="best-example"]//a[text()[contains(., "Каталог участков")]])[1]',
        'goal': 'quiz_btn_v2',
        'place': 'в "Успешных примерах"'
    }
]

# Запуск
try:
    check_quiz_btn_goal(quiz_tests)
except Exception as e:
    error_msg = str(e).split('\n')[0]
    print('ERROR: при проверке кнопок квиза — ', error_msg)


# карточки активов: нажали на карточку
def check_batch_card_goal(text, max_attempts=3):
    # Словарь для хранения результатов
    results = {'success': False, 'attempts': 0}

    for attempt in range(max_attempts):
        driver = None
        try:
            driver = init_driver()
            driver.get('https://moigektar.ru/?__counters=1')
            card = driver.find_element(By.XPATH, '(//div[@id="catalogueSpecial"]//li)[4]')
            card.click()
            time.sleep(10)

            request_found = False
            for request in driver.requests:
                if text in request.url:
                    results['success'] = True
                    results['attempts'] = attempt + 1
                    request_found = True
                    break

            if request_found:
                break

        except Exception as e:
            results['attempts'] = attempt + 1
        finally:
            if driver:
                driver.quit()

            if attempt < max_attempts - 1 and not results['success']:
                time.sleep(5)

    if results['success']:
        print(f"     ОК: при нажатии на карточку актива отправляется цель '{text}'")
    else:
        print(f"ERROR: при нажатии на карточку актива текст '{text}' не найден в отправленных запросах")

    return results['success']


try:
    check_batch_card_goal('catalog_v4.batch_card_click')
except Exception as e:
    error_msg = str(e).split('\n')[0]
    print('ERROR: при нажатии на карточку актива — ', error_msg)


# карточки активов: нажатия на элементы в карточке, если пользователь авторизован
def check_batch_card_button_goal(button_tests, max_attempts=3):

    results = {test['place']: {'success': False, 'attempts': 0} for test in button_tests}

    for attempt in range(max_attempts):
        driver = None
        try:
            driver = init_driver()
            actions = ActionChains(driver)
            driver.get("https://moigektar.ru/?__counters=1")

            if not auth_user(driver):
                if attempt < max_attempts - 1:
                    time.sleep(5)
                continue

            time.sleep(5)

            for test in button_tests:
                if results[test['place']]['success']:
                    continue

                try:
                    elem = driver.find_element(By.XPATH, test['loc'])
                    actions.move_to_element(elem).perform()
                    actions.send_keys(Keys.ARROW_DOWN).perform()
                    elem.click()
                    time.sleep(15)

                    request_found = False
                    for request in driver.requests:
                        if test['goal'] in request.url:
                            results[test['place']]['success'] = True
                            results[test['place']]['attempts'] = attempt + 1
                            request_found = True
                            break

                    if not request_found:
                        results[test['place']]['attempts'] = attempt + 1

                except Exception as e:
                    results[test['place']]['attempts'] = attempt + 1

            all_passed = all(result['success'] for result in results.values())
            if all_passed:
                break

        except Exception as e:
            print(f"Критическая ошибка в попытке {attempt + 1}: {e}")

        finally:
            if driver:
                driver.quit()

            if attempt < max_attempts - 1 and not all(result['success'] for result in results.values()):
                time.sleep(5)

    all_success = True
    for test in button_tests:
        place = test['place']
        result = results[place]

        if result['success']:
            print(f"     OK: при нажатии на {test['place']} отправляется цель '{test['goal']}'")
        else:
            print(f" ERROR: при нажатии на {test['place']} текст '{test['goal']}' не найден в отправленных запросах")
            all_success = False

    return all_success


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
try:
    check_batch_card_button_goal(button_tests)
except Exception as e:
    error_msg = str(e).split('\n')[0]
    print('ERROR: при нажатиях на кнопки в карточках активов — ', error_msg)


# карточки активов: нажатия на элементы в карточке, если пользователь НЕ авторизован
def check_batch_card_button_goal_unauth(button_tests, max_attempts=3):
    # Словарь для хранения результатов каждой кнопки
    results = {test['place']: {'success': False, 'attempts': 0} for test in button_tests}

    for attempt in range(max_attempts):
        driver = None
        try:
            driver = init_driver()
            actions = ActionChains(driver)
            driver.get("https://moigektar.ru/?__counters=1")
            time.sleep(5)

            for test in button_tests:
                # Если тест уже успешно пройден, пропускаем
                if results[test['place']]['success']:
                    continue

                try:
                    elem = driver.find_element(By.XPATH, test['loc'])
                    actions.move_to_element(elem).perform()
                    actions.send_keys(Keys.ARROW_DOWN).perform()
                    elem.click()
                    time.sleep(15)

                    request_found = False
                    for request in driver.requests:
                        if test['goal'] in request.url:
                            results[test['place']]['success'] = True
                            results[test['place']]['attempts'] = attempt + 1
                            request_found = True
                            break

                    if not request_found:
                        results[test['place']]['attempts'] = attempt + 1

                except Exception as e:
                    results[test['place']]['attempts'] = attempt + 1

            # Проверяем, все ли тесты прошли успешно
            all_passed = all(result['success'] for result in results.values())
            if all_passed:
                break

        except Exception as e:
            print(f"Критическая ошибка в попытке {attempt + 1}: {e}")
        finally:
            if driver:
                driver.quit()

            if attempt < max_attempts - 1 and not all(result['success'] for result in results.values()):
                time.sleep(5)

    # Выводим итоговые результаты после всех попыток
    all_success = True
    for test in button_tests:
        place = test['place']
        result = results[place]

        if result['success']:
            print(f"     ОК: у неавт. юзера при нажатии на {test['place']} отправляется цель '{test['goal']}'")
        else:
            print(f"ERROR: у неавт. юзера при нажатии на {test['place']} текст '{test['goal']}' не найден")
            all_success = False

    return all_success

# Параметры для check_batch_card_button_goal_unauth
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
try:
    check_batch_card_button_goal_unauth(button_tests)
except Exception as e:
    error_msg = str(e).split('\n')[0]
    print('ERROR: при нажатиях на кнопки в карточках активов — ', error_msg)


# Главная, блок "Отзывы о проекте", нажали кнопку "Посмотреть больше"
def check_news_button_goal(text, max_attempts=3):
    # Словарь для хранения результатов
    results = {'success': False, 'attempts': 0}

    for attempt in range(max_attempts):
        driver = None
        try:
            driver = init_driver()
            actions = ActionChains(driver)
            driver.get('https://moigektar.ru/?__counters=1')

            remove_popup(driver)

            title = driver.find_element(By.XPATH, '(//*[text()[contains(., "Отзывы о проекте")]])[2]')
            actions.move_to_element(title).perform()
            actions.send_keys(Keys.PAGE_DOWN).send_keys(Keys.PAGE_DOWN).perform()
            button = driver.find_element(By.XPATH, '//div/*[@href="/about/reviews"]')
            button.click()
            time.sleep(5)

            request_found = False
            for request in driver.requests:
                if text in request.url:
                    results['success'] = True
                    results['attempts'] = attempt + 1
                    request_found = True
                    break

            if request_found:
                break

        except Exception as e:
            results['attempts'] = attempt + 1
        finally:
            if driver:
                driver.quit()

            if attempt < max_attempts - 1 and not results['success']:
                time.sleep(5)

    # Выводим итоговый результат после всех попыток
    if results['success']:
        print(f"     ОК: при нажатии на кнопку в 'Отзывах' отправляется цель '{text}'")
    else:
        print(f"ERROR: при нажатии на кнопку в 'Отзывах' текст '{text}' не найден в отправленных запросах")

    return results['success']


try:
    check_news_button_goal('main_reviews_button')
except Exception as e:
    error_msg = str(e).split('\n')[0]
    print("ERROR: при нажатии на кнопку в 'Отзывах' — ", error_msg)


# Главная, блок "Выбери участок в лучшей локации", нажали кнопку "Смотреть участки"
def check_locations_button_goal(text, max_attempts=3):
    # Словарь для хранения результатов
    results = {'success': False, 'attempts': 0}

    for attempt in range(max_attempts):
        driver = None
        try:
            driver = init_driver()
            actions = ActionChains(driver)
            driver.get('https://moigektar.ru/?__counters=1')

            remove_popup(driver)

            title = driver.find_element(By.XPATH, '//*[text()[contains(., "Выбери участок")]]')
            actions.move_to_element(title).perform()
            time.sleep(5)
            actions.send_keys(Keys.PAGE_DOWN).perform()
            time.sleep(5)
            actions.send_keys(Keys.PAGE_DOWN).perform()
            time.sleep(5)
            button = driver.find_element(By.XPATH, '(//*[text()[contains(., "Смотреть участки")]])[1]')
            button.click()
            time.sleep(5)

            request_found = False
            for request in driver.requests:
                if text in request.url:
                    results['success'] = True
                    results['attempts'] = attempt + 1
                    request_found = True
                    break

            if request_found:
                break

        except Exception as e:
            results['attempts'] = attempt + 1
        finally:
            if driver:
                driver.quit()

            if attempt < max_attempts - 1 and not results['success']:
                time.sleep(5)

    # Выводим итоговый результат после всех попыток
    if results['success']:
        print(f"     ОК: при нажатии на кнопку в 'Выбери уч. в лучшей локации' отправляется цель '{text}'")
    else:
        print(
            f"ERROR: при нажатии на кнопку в 'Выбери уч. в лучшей локации' текст '{text}' не найден в отправленных запросах")

    return results['success']


try:
    check_locations_button_goal('best_location_button')
except Exception as e:
    error_msg = str(e).split('\n')[0]
    print("ERROR: при нажатии на кнопку в 'Выбери уч. в лучшей локации' — ", error_msg)


# каталог: нажатия на кнопки
def check_catalogue_button_goal(button_tests, max_attempts=3):
    # Словарь для хранения результатов каждой кнопки
    results = {test['button']: {'success': False, 'attempts': 0} for test in button_tests}

    for attempt in range(max_attempts):
        driver = None
        try:
            driver = init_driver()
            actions = ActionChains(driver)

            for test in button_tests:
                # Если тест уже успешно пройден, пропускаем
                if results[test['button']]['success']:
                    continue

                try:
                    driver.get("https://moigektar.ru/catalogue-no-auth/?__counters=1")
                    time.sleep(5)
                    if not test['goal'] == "catalog_v4.filter_button_click":
                        actions.send_keys(Keys.PAGE_DOWN).perform()
                    elem = driver.find_element(By.XPATH, test['loc'])
                    if test['goal'] == "catalog_v4.list_view_toggle":
                        button = driver.find_element(By.XPATH, '(//*[text()[contains(., "На карте")]])[1]')
                        button.click()
                        time.sleep(5)
                    elem.click()
                    time.sleep(15)

                    request_found = False
                    for request in driver.requests:
                        if test['goal'] in request.url:
                            results[test['button']]['success'] = True
                            results[test['button']]['attempts'] = attempt + 1
                            request_found = True
                            break

                    if not request_found:
                        results[test['button']]['attempts'] = attempt + 1

                except Exception as e:
                    results[test['button']]['attempts'] = attempt + 1

            # Проверяем, все ли тесты прошли успешно
            all_passed = all(result['success'] for result in results.values())
            if all_passed:
                break

        except Exception as e:
            print(f"Критическая ошибка в попытке {attempt + 1}: {e}")
        finally:
            if driver:
                driver.quit()

            if attempt < max_attempts - 1 and not all(result['success'] for result in results.values()):
                time.sleep(5)

    all_success = True
    for test in button_tests:
        button = test['button']
        result = results[button]

        if result['success']:
            print(f"     ОК: при нажатии на {test['button']} отправляется цель '{test['goal']}'")
        else:
            print(f"ERROR: при нажатии на {test['button']} текст '{test['goal']}' не найден в отправленных запросах")
            all_success = False

    return all_success

# Параметры для check_catalogue_button_goal
button_tests = [
    {
        'loc': '(//*[text()[contains(., "На карте")]])[1]',
        'goal': 'catalog_v4.map_view_toggle',
        'button': 'кнопку "Карта"'
    },
    {
        'loc': '(//*[text()[contains(., "Плиткой")]])[1]',
        'goal': 'catalog_v4.list_view_toggle',
        'button': 'кнопку "Плитка"'
    },
    {
        'loc': '(//*[text()[contains(., "Туристический")]])[1]',
        'goal': 'filter_interaction.business_toggle',
        'button': 'кнопку "Туристический бизнес"'
    },
    {
        'loc': '(//*[text()[contains(., "Фильтр")]])[1]',
        'goal': 'catalog_v4.filter_button_click',
        'button': 'кнопку "Фильтр"'
    }
]

# Запуск
try:
    check_catalogue_button_goal(button_tests)
except Exception as e:
    error_msg = str(e).split('\n')[0]
    print('ERROR: при нажатии на кнопки в каталоге — ', error_msg)


# Вычисляем и выводим время выполнения теста
end_time = time.time()
elapsed_time = end_time - start_time
minutes = int(elapsed_time // 60)
seconds = int(elapsed_time % 60)

if minutes > 0:
    print(f'\nВремя выполнения теста: {minutes} мин {seconds} сек ({elapsed_time:.2f} сек)')
else:
    print(f'\nВремя выполнения теста: {seconds} сек ({elapsed_time:.2f} сек)')
