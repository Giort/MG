from selenium import webdriver
from selenium.webdriver.chrome.options import Options
ch_options = Options()
#ch_options.add_argument('--headless')
ch_options.page_load_strategy = 'eager'
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
import json
driver.set_window_size(1920, 1080)
driver.implicitly_wait(10)


# syn_67
try:
    driver.get("https://syn67.lp.moigektar.ru/")
    title = driver.find_element(by=By.XPATH, value='//*[text()[contains(., "Виртуальный тур")]]')
    actions.move_to_element(title).send_keys(Keys.PAGE_DOWN).perform()
    time.sleep(1) # без таймслип не работает, драйверВейт и пауза в экшнс не помогают
    btn = driver.find_element(by=By.XPATH, value='//div[(contains(@class, "w-tour__icon animated-fast"))]/img')
    actions.click(btn).perform()
    iframe = driver.find_element(by=By.CLASS_NAME, value="uk-lightbox-iframe")
    driver.switch_to.frame(iframe)
    wait(driver, 14).until(EC.visibility_of_element_located((By.XPATH, "//div[(contains(@style, 'z-index: 3101'))]")))
    print('   OK: syn_67')
except:
    print('ERROR: не загрузился виртур на син_67')



# # syn_67
# try:
#     driver.get("https://syn67.lp.moigektar.ru/")
#     tour_btn = wait(driver, 14).until(EC.visibility_of_element_located((By.ID, 'w-tour-play')))
#     actions.click(tour_btn).perform()
#     iframe = driver.find_element(by=By.CLASS_NAME, value="fancybox-iframe")
#     driver.switch_to.frame(iframe)
#     wait(driver,20).until(EC.visibility_of_element_located((By.XPATH, "//div[(contains(@style, 'z-index: 3101'))]")))
#     print('   OK: syn_67')
# except:
#     print('ERROR: не загрузился виртур на син_67')


time.sleep(1)
driver.quit()
