import time

from exceptiongroup import catch
from selenium.webdriver.support.ui import WebDriverWait as wait
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
from datetime import datetime

with open('../data.json', 'r') as file:
    data = json.load(file)


# Главная, блок "Выбери участок в лучшей локации", нажали кнопку "Смотреть участки"
def check_locations_button_goal(text):
    driver = webdriver.Chrome(
        seleniumwire_options=sw_options,
        options=ch_options)
    actions = ActionChains(driver)
    driver.get('https://moigektar.ru/?__counters=1')

    try:
        popup_w = driver.find_element(by=By.XPATH, value="//div[@id='visitors-popup']")
        driver.execute_script("arguments[0].remove();", popup_w)
    except:
        print("Popup not found")

    title = driver.find_element(By.XPATH, '//*[text()[contains(., "Выбери участок")]]')
    actions.move_to_element(title).perform()
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_%f')
    driver.save_screenshot(f'screenshot_{timestamp}.png')
    actions.send_keys(Keys.PAGE_DOWN).perform()
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_%f')
    driver.save_screenshot(f'screenshot_{timestamp}.png')
    button = driver.find_element(By.XPATH, '(//*[text()[contains(., "Смотреть участки")]])[1]')
    button.click()
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_%f')
    driver.save_screenshot(f'screenshot_{timestamp}.png')
    time.sleep(5)

    request_found = False
    for request in driver.requests:
        if text in request.url:
            print(f"     ОК: при нажатии на кнопку в 'Выбери уч. в лучшей локации' отправляется цель '{text}'")
            request_found = True
            break
    if not request_found:
        print(
            f"ERROR: при нажатии на кнопку в 'Выбери уч. в лучшей локации' текст '{text}' не найден в отправленных запросах")

    driver.quit()
    return request_found

try:
    check_locations_button_goal('best_location_button')
except Exception as e:
    error_msg = str(e).split('\n')[0]
    print("ERROR: при нажатии на кнопку в 'Выбери уч. в лучшей локации' — ", error_msg)


