from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
ch_options = Options()

ch_options.add_argument('--headless')
ch_options.page_load_strategy = 'eager'
driver = webdriver.Chrome(service = Service(ChromeDriverManager().install()), options = ch_options)
ch_options.page_load_strategy = 'eager'
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
actions = ActionChains(driver)
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import ElementNotVisibleException
from selenium.webdriver.common.keys import Keys
import time
import json
driver.set_window_size(1600, 1000)
driver.implicitly_wait(10)


# Засекаем время начала теста
start_time = time.time()

with open('../data/data.json', 'r') as file:
    data = json.load(file)

print(f"\n     Проверка генерации КП \n")

# логин
driver.get("https://moigektar.ru/catalogue")

tab = driver.find_element(by=By.XPATH, value='(//*[text()="По паролю"])[2]')
name = driver.find_element(by=By.XPATH, value='(//*[@id="authform-login"])[2]')
password = driver.find_element(by=By.XPATH, value='(//*[@id="authform-password"])[2]')
btn = driver.find_element(by=By.XPATH, value='(//*[text()="Войти"])[2]')

tab.click()
name.send_keys(str(data["LK_cred"]["login"]))
password.send_keys(str(data["LK_cred"]["password"]))
btn.click()
time.sleep(10)

# сделать выборку по не самым популярным фильтрам (чтобы не было КП из кеша), нажать на кнопку "пдф",
# на странице КП дождаться отображения иконки "Смотреть КП"
driver.get("https://moigektar.ru/catalogue?clusterIds%5B%5D=88")
time.sleep(2)
actions.send_keys(Keys.PAGE_DOWN).send_keys(Keys.ARROW_DOWN).send_keys(Keys.ARROW_DOWN).send_keys(Keys.ARROW_DOWN).perform()
time.sleep(2)
btn = driver.find_element(by=By.XPATH, value='(//*[(contains(@class, "js-card-special-icon-click-download"))])[1]')
btn.click()
window_after = driver.window_handles[1]
driver.switch_to.window(window_after)

count_kp = 1
while count_kp < 21:
    try:
        kp = driver.current_url
        look_btn = wait(driver,60).until(EC.visibility_of_element_located((By.XPATH, '//*[@title="Посмотреть"]')))
        if look_btn:
            print('     OK: КП сгенерировано. Попытка номер ' + str(count_kp))
            break
    except:
        count_kp += 1
        if count_kp == 21:
            print('ERROR: на странице генерации КП нет кнопки "Посмотреть"')
            break
        else:
            driver.refresh()



time.sleep(3)
driver.quit()


# Вычисляем и выводим время выполнения теста
end_time = time.time()
elapsed_time = end_time - start_time
minutes = int(elapsed_time // 60)
seconds = int(elapsed_time % 60)

if minutes > 0:
    print(f'\n     Время выполнения теста: {minutes} мин {seconds} сек ({elapsed_time:.2f} сек)')
else:
    print(f'\n     Время выполнения теста: {seconds} сек ({elapsed_time:.2f} сек)')
