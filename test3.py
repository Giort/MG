from time import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
options = Options()
#options.add_argument('--headless')
ch_options = Options()
#ch_options.add_argument('--headless')
driver = webdriver.Chrome(options= ch_options)
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
actions = ActionChains(driver)
driver.maximize_window()
wait = WebDriverWait


from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time



driver.get("https://moigektar.ru/")

time.sleep(2)

try:
    driver.find_element(by=By.XPATH,
                        value="//h1/*[text()[contains(.,'Подпишитесь на рассылку')]]//parent::h1//following-sibling::ul[2]//input[@id='consultationform-email']").send_keys(
        '1@1.1')
    btn = driver.find_element(by=By.XPATH,
                        value="//h1/*[text()[contains(.,'Подпишитесь на рассылку')]]//parent::h1//following-sibling::ul[2]//button").click()

    time.sleep(3)
    try:
        if driver.find_element(by=By.XPATH,
                        value="//h1/*[text()[contains(.,'Подпишитесь на рассылку')]]//parent::h1//following-sibling::ul[2]//div[text()[contains(.,'Заявка успешно отправлена')]]").is_displayed():
            print(" OK: 1.3 данные были отправлены")
    except NoSuchElementException:
        print("ERROR: 1.3 данные не были отправлены")
except NoSuchElementException:
    print("ERROR: 1.3 такого элемента нет в DOM")




time.sleep(10)
#driver.quit()
