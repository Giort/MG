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






# 7. подсчёт СП на син_39
try:
    driver.get("https://syn39.lp.moigektar.ru/")
    title = wait(driver, 14).until(EC.presence_of_element_located((By.XPATH, "//h2[text()[contains(.,'Специальная')]]")))
    ActionChains(driver).move_to_element(title).send_keys(Keys.PAGE_DOWN).perform()
    SO_qty = len(driver.find_elements(by=By.CSS_SELECTOR, value='.w-special-slider-card div div div.slick-slide'))
    if SO_qty >= 3:
        print("   OK: количество СП на син_39 Лесная усадьба = " + str(SO_qty))
    else:
        print("ERROR: количество СП на син_39 Лесная усадьба = " + str(SO_qty))
except:
    print("ERROR: не получилось посчитать СП на син_39")


time.sleep(2)
driver.quit()

