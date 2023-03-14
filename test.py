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



# 7 проверка раздела "Вакансии"

# 7.1 переход на страницу "Вакансии"
driver.get("https://moigektar.ru/hr")
try:
    driver.find_element(by=By.XPATH, value="//h1/*[text()[contains(.,'Оставьте анкету')]]//parent::h1//following-sibling::ul[2]//input[@id='hrform-name']").send_keys('test')
    driver.find_element(by=By.XPATH, value="//h1/*[text()[contains(.,'Оставьте анкету')]]//parent::h1//following-sibling::ul[2]//input[@id='hrform-phone']").send_keys('9127777777')
    driver.find_element(by=By.XPATH,
                        value="//h1/*[text()[contains(.,'Оставьте анкету')]]//parent::h1//following-sibling::ul[2]/li[1]//button").click()
    try:
        wait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//h1/*[text()[contains(.,'Оставьте анкету')]]//parent::h1//following-sibling::ul[2]//div[text()[contains(.,'Заявка успешно отправлена')]]")))
        print(" OK: данные из вакансий были отправлены")
    except:
        print('ERROR: не отправлены данные в форму "Оставьте анкету" в "Вакансиях"')
except:
    print('ERROR: не могу найти форму "Оставьте анкету" в "Вакансиях"')

time.sleep(5)
driver.quit()
