from selenium import webdriver
from selenium.webdriver.chrome.options import Options
options = Options()
#options.add_argument('--headless')
ch_options = Options()
#ch_options.add_argument('--headless')
driver = webdriver.Chrome(options= ch_options)
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
driver.maximize_window()


from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time



# открыть https://moigektar.ru/
driver.get("https://moigektar.ru/")


try:
    driver.find_element(by=By.XPATH, value="//h1/*[text()[contains(.,'Хотите узнать')]]//parent::h1//following-sibling::ul[2]/li/form/div/div//input[@id='consultationform-name']").send_keys('test')
    driver.find_element(by=By.XPATH, value="//h1/*[text()[contains(.,'Хотите узнать')]]//parent::h1//following-sibling::ul[2]/li/form/div/div//input[@id='consultationform-phone']").send_keys('9999999999')
    driver.find_element(by=By.XPATH,
                        value="//h1/*[text()[contains(.,'Хотите узнать')]]//parent::h1//following-sibling::ul[2]//input[@id='consultationform-email']").send_keys(
        '1@1.1')
    driver.find_element(by=By.XPATH,
                        value="//h1/*[text()[contains(.,'Хотите узнать')]]//parent::h1//following-sibling::ul[2]//button").click()
    time.sleep(3)
    if driver.find_element(by=By.XPATH,
                        value="//h1/*[text()[contains(.,'Хотите узнать')]]//parent::h1//following-sibling::ul[2]//div[text()[contains(.,'Заявка успешно отправлена')]]").is_displayed():
        print(" OK: 1.1 данные были отправлены")
    else:
        print("ERROR: 1.1 данные не были отправлены")
except NoSuchElementException:
    print("ERROR: Такого элемента нет в DOM")


# 1. проверка главной страницы "МГ"
# 1.1 проверка формы "Хотите узнать подробнее о проекте?"

# Прямой селектор!!! - //h1/*[text()[contains(.,'Хотите узнать')]]
#
# time.sleep(1)
# if driver.find_element(by=By.XPATH, value="//h1/*[text()[contains(.,'Хотите узнать')]]//parent::div").is_displayed():
#     print('OK')

time.sleep(10)
driver.quit()