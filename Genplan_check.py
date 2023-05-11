from selenium import webdriver
from selenium.webdriver.chrome.options import Options
ch_options = Options()
ch_options.add_argument('--headless')
ch_options.page_load_strategy = 'eager'
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
driver.implicitly_wait(10)


# Скрипт заходит на сайты посёлков, запускает загрузку генплана
# и проверяет, что элемент на нём прогрузился
#
# В лог выводится сообщение "ОК", если этот элемент загрузился
# В лог выводится сообщение "ERROR", если элемент не загрузился
#


# syn_9
try:
    driver.get("https://syn9.lp.moigektar.ru/")
    play_btn = wait(driver, 14).until(EC.visibility_of_element_located((By.ID, 'w-select-play')))
    play_btn.click()
    wait(driver, 14).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'ymaps.ymaps-2-1-79-inner-panes')))
    print('   OK: syn_9')
except:
    print('ERROR: не загрузился генплан на син_9')

# syn_24
try:
    driver.get("https://syn24.lp.moigektar.ru/")
    play_btn = wait(driver, 14).until(EC.visibility_of_element_located((By.ID, 'w-select-play')))
    play_btn.click()
    wait(driver, 14).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'ymaps.ymaps-2-1-79-inner-panes')))
    print('   OK: syn_24')
except:
    try:
        driver.refresh()
        play_btn = wait(driver, 14).until(EC.visibility_of_element_located((By.ID, 'w-select-play')))
        play_btn.click()
        wait(driver, 14).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'ymaps.ymaps-2-1-79-inner-panes')))
        print('   OK: syn_24')
    except:
        print('ERROR: не загрузился генплан на син_24')

# syn_33
try:
    driver.get("https://syn33.lp.moigektar.ru/")
    play_btn = wait(driver, 14).until(EC.visibility_of_element_located((By.ID, 'w-select-play')))
    play_btn.click()
    wait(driver, 14).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'ymaps.ymaps-2-1-79-inner-panes')))
    print('   OK: syn_33')
except:
    print('ERROR: не загрузился генплан на син_33')

# syn_34
try:
    driver.get("https://syn34.lp.moigektar.ru/")
    play_btn = wait(driver, 14).until(EC.visibility_of_element_located((By.ID, 'w-select-play')))
    play_btn.click()
    wait(driver, 14).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'ymaps.ymaps-2-1-79-inner-panes')))
    print('   OK: syn_34')
except:
    print('ERROR: не загрузился генплан на син_34')

# syn_37
try:
    driver.get("https://syn37.lp.moigektar.ru/")
    play_btn = wait(driver, 14).until(EC.visibility_of_element_located((By.ID, 'w-select-play')))
    play_btn.click()
    wait(driver, 14).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'ymaps.ymaps-2-1-79-inner-panes')))
    print('   OK: syn_37')
except:
    print('ERROR: не загрузился генплан на син_37')

# syn_39
try:
    driver.get("https://syn39.lp.moigektar.ru/")
    title = wait(driver, 14).until(EC.presence_of_element_located((By.XPATH, '//div[text()[contains(.,"Генеральный")]]')))
    actions.move_to_element(title).perform()
    driver.find_element(by=By.XPATH, value='//img[@data-src="/img/select/overlay-touch.svg"]').click()
    wait(driver, 14).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'ymaps.ymaps-2-1-79-inner-panes')))
    print('   OK: syn_39')
except:
    print('ERROR: не загрузился генплан на син_39')

# syn_42
try:
    driver.get("https://syn42.lp.moigektar.ru/")
    play_btn = wait(driver, 14).until(EC.visibility_of_element_located((By.ID, 'w-select-play')))
    play_btn.click()
    wait(driver, 14).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'ymaps.ymaps-2-1-79-inner-panes')))
    print('   OK: syn_42')
except:
    print('ERROR: не загрузился генплан на син_42')

# syn_48
try:
    driver.get("https://syn48.lp.moigektar.ru/")
    play_btn = wait(driver, 14).until(EC.visibility_of_element_located((By.CLASS_NAME, 'w-select-icon')))
    actions.send_keys(Keys.PAGE_DOWN).send_keys(Keys.PAGE_DOWN).perform()
    time.sleep(5)
    play_btn.click()
    wait(driver, 14).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'ymaps.ymaps-2-1-79-inner-panes')))
    print('   OK: syn_48')
except:
    print('ERROR: не загрузился генплан на син_48')

# syn_53
try:
    driver.get("https://syn53.lp.moigektar.ru/")
    title = wait(driver, 14).until(EC.presence_of_element_located((By.XPATH, '//div[text()[contains(.,"Генеральный")]]')))
    actions.move_to_element(title).perform()
    driver.find_element(by=By.XPATH, value='//img[@data-src="/img/select/overlay-touch.svg"]').click()
    wait(driver, 14).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'ymaps.ymaps-2-1-79-inner-panes')))
    print('   OK: syn_53')
except:
    print('ERROR: не загрузился генплан на син_53')

# vazuza2
try:
    driver.get("https://vazuza2.lp.moigektar.ru/")
    title = wait(driver, 14).until(EC.presence_of_element_located((By.XPATH, '//div[text()[contains(.,"Генеральный")]]')))
    actions.move_to_element(title).send_keys(Keys.PAGE_DOWN).perform()
    driver.find_element(by=By.XPATH, value='//img[@data-src="/img/vazuza/select/overlay-touch.png"]').click()
    wait(driver, 14).until(EC.visibility_of_element_located((By.XPATH, '//canvas[4]')))
    print('   OK: vazuza2')
except:
    try:
        driver.refresh()
        title = wait(driver, 14).until(EC.presence_of_element_located((By.XPATH, '//div[text()[contains(.,"Генеральный")]]')))
        driver.find_element(by=By.XPATH, value='//img[@data-src="/img/vazuza/select/overlay-touch.png"]').click()
        wait(driver, 14).until(EC.visibility_of_element_located((By.XPATH, '//canvas[4]')))
        print('   OK: vazuza2')
    except:
        print('ERROR: не загрузился генплан на Вазузе')

# syn_67
try:
    driver.get("https://syn67.lp.moigektar.ru/")
    title = wait(driver, 14).until(EC.presence_of_element_located((By.XPATH, '//div[text()[contains(.,"Генеральный")]]')))
    actions.move_to_element(title).perform()
    driver.find_element(by=By.XPATH, value='//img[@data-src="/img/select/overlay-touch.svg"]').click()
    wait(driver, 14).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'ymaps.ymaps-2-1-79-inner-panes')))
    print('   OK: syn_67')
except:
    print('ERROR: не загрузился генплан на син_67')

# syn_84
try:
    driver.get("https://syn84.lp.moigektar.ru/")
    title = driver.find_element(by=By.XPATH, value="//div[text()[contains(.,'Генеральный')]]")
    actions.move_to_element(title).perform()
    time.sleep(3)
    driver.find_element(by=By.XPATH, value='//img[@data-src="/img/select/overlay-touch.svg"]').click()
    wait(driver, 14).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'ymaps.ymaps-2-1-79-inner-panes')))
    print('   OK: syn_84')
except:
    print('ERROR: не загрузился генплан на син_84')

# syn_85
try:
    driver.get("https://syn85.lp.moigektar.ru/")
    title = driver.find_element(by=By.XPATH, value="//div[text()[contains(.,'Генеральный')]]")
    actions.move_to_element(title).perform()
    time.sleep(3)
    driver.find_element(by=By.XPATH, value='//img[@data-src="/img/select/overlay-touch.svg"]').click()
    wait(driver, 14).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'ymaps.ymaps-2-1-79-inner-panes')))
    print('   OK: syn_85')
except:
    print('ERROR: не загрузился генплан на син_85')

# syn_87
try:
    driver.get("https://mt.lp.moigektar.ru/")
    title = driver.find_element(by=By.XPATH, value="//div[text()[contains(.,'Генеральный')]]")
    actions.move_to_element(title).perform()
    time.sleep(3)
    driver.find_element(by=By.XPATH, value='//img[@data-src="/img/select/overlay-touch.svg"]').click()
    wait(driver, 14).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'ymaps.ymaps-2-1-79-inner-panes')))
    print('   OK: syn_87')
except:
    print('ERROR: не загрузился генплан на син_87')

# syn_89
try:
    driver.get("https://syn89.lp.moigektar.ru/")
    title = driver.find_element(by=By.XPATH, value="//div[text()[contains(.,'Генеральный')]]")
    actions.move_to_element(title).perform()
    time.sleep(3)
    driver.find_element(by=By.XPATH, value='//img[@data-src="/img/select/overlay-touch.svg"]').click()
    wait(driver, 14).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'ymaps.ymaps-2-1-79-inner-panes')))
    print('   OK: syn_89')
except:
    print('ERROR: не загрузился генплан на син_89')


time.sleep(5)
driver.quit()

