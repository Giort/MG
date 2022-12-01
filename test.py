from selenium import webdriver
from selenium.webdriver.chrome.options import Options
ch_options = Options()
#ch_options.add_argument('--headless')
driver = webdriver.Chrome(options= ch_options)
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
driver.maximize_window()




# 4.4 переход на страницу "Развитие - базовая стратегия"
driver.get("https://moigektar.ru/investment/basic")
time.sleep(2)
try:
    driver.find_element(by=By.XPATH, value="//h1/*[text()[contains(.,'Хотите узнать')]]//parent::h1//following-sibling::ul[2]//input[@id='consultationform-name']").send_keys('test')
    driver.find_element(by=By.XPATH, value="//h1/*[text()[contains(.,'Хотите узнать')]]//parent::h1//following-sibling::ul[2]//input[@id='consultationform-phone']").send_keys('9127777777')
    driver.find_element(by=By.XPATH,
                        value="//h1/*[text()[contains(.,'Хотите узнать')]]//parent::h1//following-sibling::ul[2]//input[@id='consultationform-email']").send_keys(
        '1@1.1')
    driver.find_element(by=By.XPATH,
                        value="//h1/*[text()[contains(.,'Хотите узнать')]]//parent::h1//following-sibling::ul[2]//button").click()
    time.sleep(3)
    if driver.find_element(by=By.XPATH,
                        value="//h1/*[text()[contains(.,'Хотите узнать')]]//parent::h1//following-sibling::ul[2]//div[text()[contains(.,'Заявка успешно отправлена')]]").is_displayed():
        print('ERROR: не отправлены данные в форму "Хотите узнать подробнее о проекте?" в "Развитие" - "Базовая стратегия"')
    else:
        print("ERROR: 4.4 данные не были отправлены")
except NoSuchElementException:
    print('ERROR: не могу найти форму "Хотите узнать подробнее о проекте?" в "Развитие" - "Базовая стратегия"')

time.sleep(1)
driver.quit()
