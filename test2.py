import time

from seleniumwire import webdriver
from selenium.webdriver.common.by import By


# Настройка драйвера с Selenium Wire
options = {
    'disable_capture': False  # Включаем перехват запросов
}

driver = webdriver.Chrome(seleniumwire_options=options)
driver.set_window_size(1680, 1000)

# Открываем страницу
driver.get('https://moigektar.ru/?__counters=1')

driver.get('https://moigektar.ru/catalogue')
time.sleep(5)
back_button = driver.find_element(By.XPATH, '//*[text()[contains(., "Вернуться на главную")]]')
back_button.click()

text = 'catalog_modal_auth_button_main'

request_found = False
for request in driver.requests:
    if text in request.url:
        print(f"     ОК: при возврате на главную из мод. авторизации в каталоге отправляется цель '{text}'")
        request_found = True
        break

if not request_found:
    print(f"Текст '{text}' не найден в отправленных запросах")


driver.quit()