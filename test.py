from selenium import webdriver
from selenium.webdriver.chrome.options import Options
ch_options = Options()
ch_options.add_argument('--headless')
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
#driver.maximize_window()
driver.set_window_size(1920, 1080)

driver.implicitly_wait(10)


# form_id = driver.find_element(by=By.XPATH, value='//b[text()[contains(.,"Подпишитесь на рассылку")]]//ancestor::div[2]').get_attribute('id')
# //div[@id='"+ form_id +"']


# 2.2 переход на страницу "О проекте - сервисная компания"
driver.get("https://moigektar.ru/about/management")
try:
    form_id = driver.find_element(by=By.XPATH, value='//b[text()[contains(.,"Подпишитесь на рассылку")]]//ancestor::div[2]').get_attribute('id')
    driver.find_element(by=By.XPATH, value="//h1/*[text()[contains(.,'Хотите узнать')]]//parent::h1//following-sibling::ul[2]//input[@id='consultationform-name']").send_keys('test')
    driver.find_element(by=By.XPATH, value="//h1/*[text()[contains(.,'Хотите узнать')]]//parent::h1//following-sibling::ul[2]//input[@id='consultationform-phone']").send_keys('9127777777')
    driver.find_element(by=By.XPATH,
                        value="//h1/*[text()[contains(.,'Хотите узнать')]]//parent::h1//following-sibling::ul[2]//input[@id='consultationform-email']").send_keys(
        '1@1.1')
    driver.find_element(by=By.XPATH,
                        value="//h1/*[text()[contains(.,'Хотите узнать')]]//parent::h1//following-sibling::ul[2]//button[text()[contains(.,'Отправить')]]").click()
    try:
        wait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//h1/*[text()[contains(.,'Хотите узнать')]]//parent::h1//following-sibling::ul[2]//div[text()[contains(.,'Заявка успешно отправлена')]]")))
        print(" OK: о проекте 2/6 данные были отправлены")
    except:
        print('ERROR: не отправлены данные в форму "Хотите узнать подробнее о проекте?" в "О проекте" - "Сервисная компания"')
except:
    print('ERROR: не могу найти форму "Хотите узнать подробнее о проекте?" в "О проекте" - "Сервисная компания"')


time.sleep(1)
driver.quit()
