from selenium import webdriver
from selenium.webdriver.chrome.options import Options
ch_options = Options()
ch_options.add_argument('--headless')
driver = webdriver.Chrome(options= ch_options)
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementNotVisibleException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
actions = ActionChains(driver)
from selenium.webdriver.common.keys import Keys
import time
#driver.maximize_window()
driver.set_window_size(1920, 1080) # иначе падает тест на 48


# Скрипт заходит на сайты посёлков, запускает загрузку генплана
# и проверяет, что элемент на нём прогрузился
#
# В лог выводится сообщение "ОК", если этот элемент загрузился
# В лог выводится сообщение "ERROR", если элемент не загрузился


# 1. syn_9
driver.get("https://syn9.lp.moigektar.ru/")
try:
    wait(driver, 14).until(EC.presence_of_element_located((By.ID, 'w-select-play')))
    driver.find_element(by=By.ID, value='w-select-play').click()
    wait(driver, 14).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'ymaps.ymaps-2-1-79-inner-panes')))
    print('   OK: syn_9')
except:
    print('ERROR: не загрузился генплан на син_9')

# 2. syn_19
driver.get("https://syn19.lp.moigektar.ru/")
try:
    wait(driver, 14).until(EC.presence_of_element_located((By.ID, 'w-select-play')))
    actions.send_keys(Keys.PAGE_DOWN).send_keys(Keys.PAGE_DOWN).send_keys(Keys.ARROW_DOWN).perform()
    time.sleep(5)
    driver.find_element(by=By.ID, value='w-select-play').click()
    wait(driver, 14).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'ymaps.ymaps-2-1-79-map')))
    print('   OK: syn_19')
except:
    print('ERROR: не загрузился генплан на син_19')

# 3. syn_24
driver.get("https://syn24.lp.moigektar.ru/")
try:
    wait(driver, 14).until(EC.presence_of_element_located((By.ID, 'w-select-play')))
    driver.find_element(by=By.ID, value='w-select-play').click()
    wait(driver, 14).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'ymaps.ymaps-2-1-79-inner-panes')))
    print('   OK: syn_24')
except:
    print('ERROR: не загрузился генплан на син_24')

# 4. syn_33
driver.get("https://syn33.lp.moigektar.ru/")
try:
    wait(driver, 14).until(EC.presence_of_element_located((By.ID, 'w-select-play')))
    driver.find_element(by=By.ID, value='w-select-play').click()
    wait(driver, 14).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'ymaps.ymaps-2-1-79-inner-panes')))
    print('   OK: syn_33')
except:
    print('ERROR: не загрузился генплан на син_33')

# 5. syn_34
driver.get("https://syn34.lp.moigektar.ru/")
try:
    wait(driver, 14).until(EC.presence_of_element_located((By.ID, 'w-select-play')))
    driver.find_element(by=By.ID, value='w-select-play').click()
    wait(driver, 14).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'ymaps.ymaps-2-1-79-inner-panes')))
    print('   OK: syn_34')
except:
    print('ERROR: не загрузился генплан на син_34')

# 6. syn_37
driver.get("https://syn37.lp.moigektar.ru/")
try:
    wait(driver, 14).until(EC.presence_of_element_located((By.ID, 'w-select-play')))
    driver.find_element(by=By.ID, value='w-select-play').click()
    wait(driver, 14).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'ymaps.ymaps-2-1-79-inner-panes')))
    print('   OK: syn_37')
except:
    print('ERROR: не загрузился генплан на син_37')

# 7. syn_39
driver.get("https://syn39.lp.moigektar.ru/")
try:
    wait(driver, 14).until(EC.presence_of_element_located((By.ID, 'w-select-play')))
    driver.find_element(by=By.ID, value='w-select-play').click()
    wait(driver, 14).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'ymaps.ymaps-2-1-79-inner-panes')))
    print('   OK: syn_39')
except:
    print('ERROR: не загрузился генплан на син_39')

# 8. syn_42
driver.get("https://syn42.lp.moigektar.ru/")
try:
    wait(driver, 14).until(EC.presence_of_element_located((By.ID, 'w-select-play')))
    driver.find_element(by=By.ID, value='w-select-play').click()
    wait(driver, 14).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'ymaps.ymaps-2-1-79-inner-panes')))
    print('   OK: syn_42')
except:
    print('ERROR: не загрузился генплан на син_42')

# 9. syn_48
driver.get("https://syn48.lp.moigektar.ru/")
try:
    wait(driver, 14).until(EC.presence_of_element_located((By.CLASS_NAME, 'w-select-icon')))
    actions.send_keys(Keys.PAGE_DOWN).send_keys(Keys.PAGE_DOWN).perform()
    time.sleep(5)
    driver.find_element(by=By.CLASS_NAME, value='w-select-icon').click()
    wait(driver, 14).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'ymaps.ymaps-2-1-79-inner-panes')))
    print('   OK: syn_48')
except:
    print('ERROR: не загрузился генплан на син_48')

# 10. syn_53
driver.get("https://syn53.lp.moigektar.ru/")
try:
    wait(driver, 14).until(EC.presence_of_element_located((By.XPATH, '//div[@class="js-select-map"]')))
    title = driver.find_element(by=By.XPATH, value="//div[text()[contains(.,'Генеральный')]]")
    actions.move_to_element(title).perform()
    time.sleep(3)
    driver.find_element(by=By.XPATH, value='//img[@data-src="/img/select/overlay-touch.svg"]').click()
    wait(driver, 14).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'ymaps.ymaps-2-1-79-inner-panes')))
    print('   OK: syn_53')
except:
    print('ERROR: не загрузился генплан на син_53')

# 11. syn_67
driver.get("https://syn67.lp.moigektar.ru/")
try:
    wait(driver, 14).until(EC.presence_of_element_located((By.ID, 'w-select-play')))
    driver.find_element(by=By.ID, value='w-select-play').click()
    wait(driver, 14).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'ymaps.ymaps-2-1-79-inner-panes')))
    print('   OK: syn_67')
except:
    print('ERROR: не загрузился генплан на син_67')

# 12. syn_84
driver.get("https://syn84.lp.moigektar.ru/")
try:
    wait(driver, 14).until(EC.presence_of_element_located((By.XPATH, '//div[@class="js-select-map"]')))
    title = driver.find_element(by=By.XPATH, value="//div[text()[contains(.,'Генеральный')]]")
    actions.move_to_element(title).perform()
    time.sleep(3)
    driver.find_element(by=By.XPATH, value='//img[@data-src="/img/select/overlay-touch.svg"]').click()
    wait(driver, 14).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'ymaps.ymaps-2-1-79-inner-panes')))
    print('   OK: syn_84')
except:
    print('ERROR: не загрузился генплан на син_84')

# 13. syn_85
driver.get("https://syn85.lp.moigektar.ru/")
try:
    wait(driver, 14).until(EC.presence_of_element_located((By.XPATH, '//div[@class="js-select-map"]')))
    title = driver.find_element(by=By.XPATH, value="//div[text()[contains(.,'Генеральный')]]")
    actions.move_to_element(title).perform()
    time.sleep(3)
    driver.find_element(by=By.XPATH, value='//img[@data-src="/img/select/overlay-touch.svg"]').click()
    wait(driver, 14).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'ymaps.ymaps-2-1-79-inner-panes')))
    print('   OK: syn_85')
except:
    print('ERROR: не загрузился генплан на син_85')

# 14. syn_89
driver.get("https://syn89.lp.moigektar.ru/")
try:
    wait(driver, 14).until(EC.presence_of_element_located((By.XPATH, '//div[@class="js-select-map"]')))
    title = driver.find_element(by=By.XPATH, value="//div[text()[contains(.,'Генеральный')]]")
    actions.move_to_element(title).perform()
    time.sleep(3)
    driver.find_element(by=By.XPATH, value='//img[@data-src="/img/select/overlay-touch.svg"]').click()
    wait(driver, 14).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'ymaps.ymaps-2-1-79-inner-panes')))
    print('   OK: syn_89')
except:
    print('ERROR: не загрузился генплан на син_89')

# 15. syn_87
driver.get("https://mt.lp.moigektar.ru/")
try:
    wait(driver, 14).until(EC.presence_of_element_located((By.XPATH, '//div[@class="js-select-map"]')))
    title = driver.find_element(by=By.XPATH, value="//div[text()[contains(.,'Генеральный')]]")
    actions.move_to_element(title).perform()
    time.sleep(3)
    driver.find_element(by=By.XPATH, value='//img[@data-src="/img/select/overlay-touch.svg"]').click()
    wait(driver, 14).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'ymaps.ymaps-2-1-79-inner-panes')))
    print('   OK: syn_87')
except:
    print('ERROR: не загрузился генплан на син_87')


time.sleep(5)
driver.quit()

