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
#driver.maximize_window()
driver.set_window_size(1920, 1080)


# 1. проверка слайдера СП на главной странице "МГ"
driver.get("https://moigektar.ru/")

try:
    title_n = driver.find_element(by=By.XPATH, value="//h1[text()[contains(.,'на новости проекта')]]")
    print('   блок "Подпишитесь на новости проекта": OK')
    try:
        actions.move_to_element(title_n).send_keys(Keys.PAGE_DOWN).perform()
        wait(driver,14).until(EC.visibility_of_element_located((By.XPATH, "//*[@data-app='eapps-vk-feed']/div/div/div[1]/div/div[1]/div/div")))
        print('   блок "Подпишитесь на новости проекта": OK, новости ВК отображаются')
    except:
        print('ERROR: проблема с новостями ВК на главной МГ')
except:
    print('ERROR: проблема с блоком "Подпишитесь на новости проекта" на главной МГ')



time.sleep(5)
driver.quit()

