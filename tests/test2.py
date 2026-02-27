import time
from seleniumwire import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

ch_options = Options()
# ch_options.add_argument('--headless')
ch_options.add_argument("--window-size=1680,1000")
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

# Настройка драйвера с Selenium Wire
# Включаем перехват запросов
sw_options = {'disable_capture': False}
import json


# Засекаем время начала теста
start_time = time.time()

with open('../data/data.json', 'r') as file:
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
        # Удаляем попап посетителей
        popup_visitors = driver.find_element(by=By.XPATH, value="//div[@id='visitors-popup']")
        driver.execute_script("arguments[0].remove();", popup_visitors)
    except Exception:
        pass

    try:
        # Удаляем попап вебинара
        popup_webinar = driver.find_element(by=By.XPATH,
                                            value="//*[contains(@class, 'js-webinar-running-event-modal')]")
        driver.execute_script("arguments[0].remove();", popup_webinar)
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
        print(f" ERROR: Не удалось авторизоваться - {str(e)}")
        return False

print()




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
            f" ERROR: при нажатии на кнопку в 'Выбери уч. в лучшей локации' текст '{text}' не найден в отправленных запросах")

    return results['success']


try:
    check_locations_button_goal('best_location_button')
except Exception as e:
    error_msg = str(e).split('\n')[0]
    print(" ERROR: при нажатии на кнопку в 'Выбери уч. в лучшей локации' — ", error_msg)


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
            print(f" ERROR: при нажатии на {test['button']} текст '{test['goal']}' не найден в отправленных запросах")
            all_success = False

    return all_success

# Параметры для check_catalogue_button_goal
catalogue_button_tests = [
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
    check_catalogue_button_goal(catalogue_button_tests)
except Exception as e:
    error_msg = str(e).split('\n')[0]
    print(' ERROR: при нажатии на кнопки в каталоге — ', error_msg)


# Вычисляем и выводим время выполнения теста
end_time = time.time()
elapsed_time = end_time - start_time
minutes = int(elapsed_time // 60)
seconds = int(elapsed_time % 60)

if minutes > 0:
    print(f'\n     Время выполнения теста: {minutes} мин {seconds} сек ({elapsed_time:.2f} сек)')
else:
    print(f'\n     Время выполнения теста: {seconds} сек ({elapsed_time:.2f} сек)')
