import time

from exceptiongroup import catch
from selenium.webdriver.support.ui import WebDriverWait as wait
from seleniumwire import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException
ch_options = Options()
#ch_options.add_argument('--headless')
ch_options.add_argument("--window-size=1680,1000")
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
# Настройка драйвера с Selenium Wire
# Включаем перехват запросов
sw_options = {'disable_capture': False}
import json
from selenium.webdriver.common.action_chains import ActionChains
from tenacity import retry, stop_after_attempt, retry_if_exception, retry_if_exception_type, wait_fixed
driver = webdriver.Chrome(options=ch_options)
actions = ActionChains(driver)

with open('data.json', 'r') as file:
    data = json.load(file)



# карточки активов: нажали на карточку
def check_batch_card_goal(text):
    driver = webdriver.Chrome(
        seleniumwire_options=sw_options,
        options=ch_options)
    actions = ActionChains(driver)
    driver.get('https://moigektar.ru/?__counters=1')

    # избавляемся от поп-апа, который перекрывает доступ к карточкам
    try:
        popup_w = driver.find_element(by=By.XPATH, value="//div[@id='visitors-popup']")
        driver.execute_script("""
        var auth_win = arguments[0];
        auth_win.remove();
        """, popup_w)
    except:
        print("Popup not found")

    card = driver.find_element(By.XPATH, '(//div[@id="catalogueSpecial"]//li)[4]')
    time.sleep(1500)
    actions.move_to_element(card).perform()
    card.click()
    time.sleep(1500)

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

