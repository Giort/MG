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
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import ElementNotVisibleException
import time



# 1. проверка "МГ" по видимости заголовка "Специальное преложение" на главной
driver.get("https://moigektar.ru/")
try:
    wait(driver,14).until(EC.presence_of_element_located((By.XPATH, "//h1[text()[contains(.,'Гектар под ваши цели')]]")))
    print('  |  МГ: OK')
except NoSuchElementException:
    print('ERROR: проблема на МГ')


# 2. проверка ЛК по видимости баннера, который отображается при первом входе в ЛК
driver.get("https://cabinet.moigektar.ru/security/login")
try:
    btn=wait(driver,14).until(EC.presence_of_element_located((By.XPATH, "//a[text()[contains(.,'Попробовать прямо сейчас!')]]")))
    actions.move_to_element(btn).click(btn).perform()
    wait(driver,14).until(EC.presence_of_element_located((By.XPATH, "//img[@src='/img/polls-banner.jpg']")))
    print('  |  ЛК: ОК')
except NoSuchElementException:
    print('ERROR: проблема на ЛК')

# 3. проверка syn_9 по видимости заголовка "Генеральный"
driver.get("https://syn9.lp.moigektar.ru/")
try:
    wait(driver,14).until(EC.presence_of_element_located((By.XPATH, "//span[text()[contains(.,'Генеральный')]]")))
    print(' / \ syn_9: OK')
except NoSuchElementException:
    print('ERROR: проблема на син_9')




time.sleep(5)
driver.quit()
