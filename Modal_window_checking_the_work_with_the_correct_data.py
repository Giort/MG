from selenium import webdriver
from selenium.webdriver.chrome.options import Options
options = Options()
options.add_argument('--headless')
ch_options = Options()
ch_options.add_argument('--headless')
driver = webdriver.Chrome(options= ch_options)
driver.maximize_window()


from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
wait = WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Скрипт заполняет каждое окно корректными данными
# В лог выводится сообщение "ОК" если данные были отправлены и отобразилось сообщение об успехе
# В лог выводится сообщение "ERROR" если это сообщение не отобразилось
# В лог выводится сообщение "ERROR" если элемент не был найден по селектору



# 1. проверка главной страницы "МГ"
# открыть https://moigektar.ru/
driver.get("https://moigektar.ru/")

# 1.1 проверка окна в блоке "Специальное предложение"
time.sleep(2)
try:
    wait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//h1[text()[contains(.,'Специальное предложение')]]//parent::div//div[1]/div/div[1]/ul/li[1]//button"))).click()
    wait(driver,10).until(EC.element_to_be_clickable((By.XPATH,
                        "//h1[text()[contains(.,'Специальное предложение')]]//ancestor::div[5]//input[@id='consultationform-name']"))).send_keys("test")
    driver.find_element(by=By.XPATH,
                        value="//h1[text()[contains(.,'Специальное предложение')]]//ancestor::div[5]//input[@id='consultationform-phone']").send_keys(
        "9999999999")
    driver.find_element(by=By.XPATH,
                        value="//h1[text()[contains(.,'Специальное предложение')]]//ancestor::div[5]//input[@id='consultationform-email']").send_keys(
        "1@1.1")
    driver.find_element(by=By.XPATH,
                        value="//h1[text()[contains(.,'Специальное предложение')]]//ancestor::div[5]//button[@type='submit']").click()
    time.sleep(3)
    if driver.find_element(by=By.XPATH, value="//h1[text()[contains(.,'Специальное предложение')]]//ancestor::div//div[text()[contains(.,'Заявка успешно отправлена')]]").is_displayed():
        print(" OK: 1.1 заявка отправлена")
    else:
        print("ERROR: 1.1 заявка не отправлена")
    driver.find_element(by=By.XPATH,
                        value="//h1[text()[contains(.,'Специальное предложение')]]//ancestor::div[5]//div[2]/div/button/span[text()[contains(.,'×')]]").click()
except NoSuchElementException:
    print("ERROR: 1.1 такого элемента нет в DOM")












time.sleep(2)
driver.quit()

