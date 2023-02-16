from time import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
ch_options = Options()
ch_options.add_argument('--headless')
driver = webdriver.Chrome(options= ch_options)
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
actions = ActionChains(driver)
driver.maximize_window()


from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import ElementNotVisibleException
import time




# 2. проверка ЛК по видимости баннера, который отображается при первом входе в ЛК
driver.get("https://cabinet.moigektar.ru/security/login")
try:
    btn=wait(driver,14).until(EC.presence_of_element_located((By.XPATH, "//a[text()[contains(.,'Попробовать прямо сейчас!')]]")))
    actions.move_to_element(btn).click().perform()
    wait(driver,14).until(EC.presence_of_element_located((By.XPATH, "//img[@src='/img/polls-banner.jpg']")))
    print('  |  ЛК: ОК')
except:
    print('ERROR (service_check): не дождался загрузки элемента на ЛК')


#time.sleep(10)
driver.quit()
