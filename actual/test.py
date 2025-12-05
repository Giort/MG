import time
from seleniumwire import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

ch_options = Options()
# ch_options.add_argument('--headless')
ch_options.add_argument("--window-size=360,900")
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
        driver.find_element(By.XPATH, '(//*[@href="#modal-auth-lk"])[6]').click()
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


# карточки активов: нажали на карточку
def check_batch_card_goal(text, max_attempts=3):
    # Словарь для хранения результатов
    results = {'success': False, 'attempts': 0}

    for attempt in range(max_attempts):
        driver = None
        try:
            driver = init_driver()
            actions = ActionChains(driver)
            driver.get('https://moigektar.ru/?__counters=1')
            remove_popup(driver)
            card = driver.find_element(By.XPATH, '(//div[@id="catalogueSpecial"]//li)[5]')
            actions.move_to_element(card).perform()
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


