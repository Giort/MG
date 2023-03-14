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
driver.set_window_size(1920, 1080)
driver.implicitly_wait(10)


# Скрипт заходит на сайты посёлков, запускает загрузку Виртуального тура
# и проверяет, что элемент на нём прогрузился
#
# В лог выводится сообщение "ОК", если этот элемент загрузился
# В лог выводится сообщение "ERROR", если элемент не загрузился
#


# syn_9
driver.get("https://syn9.lp.moigektar.ru/")
try:
    tour_btn = wait(driver, 14).until(EC.visibility_of_element_located((By.ID, 'w-tour-play')))
    tour_btn.click()
    iframe = driver.find_element(by=By.CLASS_NAME, value="fancybox-iframe")
    driver.switch_to.frame(iframe)
    wait(driver,20).until(EC.visibility_of_element_located((By.XPATH, "//div[(contains(@style, 'z-index: 3056'))][1]")))
    print('   ОК: syn_9')
except:
    print('ERROR: не загрузился виртур на син_9')

# syn_24
driver.get("https://syn24.lp.moigektar.ru/")
try:
    tour_btn = wait(driver, 14).until(EC.visibility_of_element_located((By.ID, 'w-tour-play')))
    tour_btn.click()
    iframe = driver.find_element(by=By.CLASS_NAME, value="fancybox-iframe")
    driver.switch_to.frame(iframe)
    wait(driver,20).until(EC.visibility_of_element_located((By.XPATH, "//div[(contains(@style, 'z-index: 3101'))]")))
    print('   OK: syn_24')
except:
    print('ERROR: не загрузился виртур на син_24')

# syn_33
driver.get("https://syn33.lp.moigektar.ru/")
try:
    tour_btn = wait(driver, 14).until(EC.presence_of_element_located((By.ID, 'w-tour-play')))
    tour_btn.click()
    iframe = driver.find_element(by=By.CLASS_NAME, value="fancybox-iframe")
    driver.switch_to.frame(iframe)
    wait(driver,20).until(EC.visibility_of_element_located((By.XPATH, "//div[(contains(@style, 'z-index: 3101'))]")))
    print('   OK: syn_33')
except:
    print('ERROR: не загрузился виртур на син_33')

# syn_34
driver.get("https://syn34.lp.moigektar.ru/")
try:
    tour_btn = wait(driver, 14).until(EC.presence_of_element_located((By.ID, 'w-tour-play')))
    tour_btn.click()
    iframe = driver.find_element(by=By.CLASS_NAME, value="fancybox-iframe")
    driver.switch_to.frame(iframe)
    wait(driver,20).until(EC.visibility_of_element_located((By.XPATH, "//div[(contains(@style, 'z-index: 3101'))]")))
    print('   OK: syn_34')
except:
    print('ERROR: не загрузился виртур на син_34')

# syn_37
driver.get("https://syn37.lp.moigektar.ru/")
try:
    tour_btn = wait(driver, 14).until(EC.visibility_of_element_located((By.ID, 'w-tour-play')))
    tour_btn.click()
    iframe = driver.find_element(by=By.CLASS_NAME, value="fancybox-iframe")
    driver.switch_to.frame(iframe)
    wait(driver,20).until(EC.visibility_of_element_located((By.XPATH, "//div[(contains(@style, 'z-index: 3101'))]")))
    print('   OK: syn_37')
except:
    print('ERROR: не загрузился виртур на син_37')

# syn_39
driver.get("https://syn39.lp.moigektar.ru/")
try:
    tour_btn = wait(driver, 14).until(EC.visibility_of_element_located((By.ID, 'w-tour-play')))
    tour_btn.click()
    iframe = driver.find_element(by=By.CLASS_NAME, value="fancybox-iframe")
    driver.switch_to.frame(iframe)
    wait(driver,20).until(EC.visibility_of_element_located((By.XPATH, "//div[(contains(@style, 'z-index: 3101'))]")))
    print('   OK: syn_39')
except:
    print('ERROR: не загрузился виртур на син_39')

# syn_42
driver.get("https://syn42.lp.moigektar.ru/")
try:
    tour_btn = wait(driver, 14).until(EC.visibility_of_element_located((By.ID, 'w-tour-play')))
    tour_btn.click()
    iframe = driver.find_element(by=By.CLASS_NAME, value="fancybox-iframe")
    driver.switch_to.frame(iframe)
    wait(driver,20).until(EC.visibility_of_element_located((By.XPATH, "//div[(contains(@style, 'z-index: 3101'))]")))
    print('   OK: syn_42')
except:
    print('ERROR: не загрузился виртур на син_42')

# syn_48
# не получается переместиться к элементам обычным образом - таргет за пределами окна; не разобрался, пока что отложил
driver.get("https://syn48.lp.moigektar.ru/")
try:
    i = 0
    while i < 6:
        actions.send_keys(Keys.PAGE_DOWN).perform()
        i += 1
    time.sleep(1)
    tour_btn = wait(driver, 14).until(EC.visibility_of_element_located((By.ID, 'w-tour-play')))
    actions.move_to_element(tour_btn).pause(1).click(tour_btn).perform()
    iframe = driver.find_element(by=By.CLASS_NAME, value="fancybox-iframe")
    driver.switch_to.frame(iframe)
    wait(driver,20).until(EC.visibility_of_element_located((By.XPATH, "//div[(contains(@style, 'z-index: 3101'))]")))
    print('   OK: syn_48')
except:
    print('ERROR: не загрузился виртур на син_48')

# syn_53
try:
    driver.get("https://syn53.lp.moigektar.ru/")
    title = driver.find_element(by=By.XPATH, value='//*[text()[contains(., "Виртуальный тур")]]')
    actions.move_to_element(title).send_keys(Keys.PAGE_DOWN).perform()
    time.sleep(1) # без таймслип не работает, драйверВейт и пауза в экшнс не помогают
    btn = driver.find_element(by=By.XPATH, value='//img[@class="w-tour__icon animated-fast"]')
    actions.click(btn).perform()
    iframe = driver.find_element(by=By.CLASS_NAME, value="uk-lightbox-iframe")
    driver.switch_to.frame(iframe)
    wait(driver, 14).until(EC.visibility_of_element_located((By.XPATH, "//div[(contains(@style, 'z-index: 3101'))]")))
    print('   OK: syn_53')
except:
    print('ERROR: не загрузился виртур на син_53')

# syn_67
driver.get("https://syn67.lp.moigektar.ru/")
try:
    tour_btn = wait(driver, 14).until(EC.visibility_of_element_located((By.ID, 'w-tour-play')))
    actions.click(tour_btn).perform()
    iframe = driver.find_element(by=By.CLASS_NAME, value="fancybox-iframe")
    driver.switch_to.frame(iframe)
    wait(driver,20).until(EC.visibility_of_element_located((By.XPATH, "//div[(contains(@style, 'z-index: 3101'))]")))
    print('   OK: syn_67')
except:
    print('ERROR: не загрузился виртур на син_67')

# syn_84
try:
    driver.get("https://syn84.lp.moigektar.ru/")
    title = driver.find_element(by=By.XPATH, value='//*[text()[contains(., "Виртуальный тур")]]')
    actions.move_to_element(title).send_keys(Keys.PAGE_DOWN).perform()
    time.sleep(1)
    btn = driver.find_element(by=By.XPATH, value='//img[@class="w-tour__icon animated-fast"]')
    actions.click(btn).perform()
    iframe = driver.find_element(by=By.CLASS_NAME, value="uk-lightbox-iframe")
    driver.switch_to.frame(iframe)
    wait(driver, 14).until(EC.visibility_of_element_located((By.XPATH, "//div[(contains(@style, 'z-index: 3101'))]")))
    print('   OK: syn_84')
except:
    print('ERROR: не загрузился виртур на син_84')

# syn_85
try:
    driver.get("https://syn85.lp.moigektar.ru/")
    title = driver.find_element(by=By.XPATH, value='//*[text()[contains(., "Виртуальный тур")]]')
    actions.move_to_element(title).send_keys(Keys.PAGE_DOWN).perform()
    time.sleep(1)
    btn = driver.find_element(by=By.XPATH, value='//img[@class="w-tour__icon animated-fast"]')
    actions.click(btn).perform()
    iframe = driver.find_element(by=By.CLASS_NAME, value="uk-lightbox-iframe")
    driver.switch_to.frame(iframe)
    wait(driver, 14).until(EC.visibility_of_element_located((By.XPATH, "//div[(contains(@style, 'z-index: 3101'))]")))
    print('   OK: syn_85')
except:
    print('ERROR: не загрузился виртур на син_85')

# syn_87
try:
    driver.get("https://syn87.lp.moigektar.ru/")
    title = driver.find_element(by=By.XPATH, value='//*[text()[contains(., "Виртуальный тур")]]')
    actions.move_to_element(title).send_keys(Keys.PAGE_DOWN).perform()
    time.sleep(1)
    btn = driver.find_element(by=By.XPATH, value='//div[(contains(@class, "w-tour__icon animated-fast"))]')
    actions.click(btn).perform()
    iframe = driver.find_element(by=By.CLASS_NAME, value="uk-lightbox-iframe")
    driver.switch_to.frame(iframe)
    wait(driver, 22).until(EC.visibility_of_element_located((By.XPATH, "//div[(contains(@style, 'z-index: 230'))]")))
    print('   OK: syn_87')
except:
    print('ERROR: не загрузился виртур на син_87')

# syn_89
try:
    driver.get("https://syn89.lp.moigektar.ru/")
    title = driver.find_element(by=By.XPATH, value='//*[text()[contains(., "Виртуальные туры")]]')
    actions.move_to_element(title).send_keys(Keys.PAGE_DOWN).perform()
    time.sleep(1)
    btn = driver.find_element(by=By.XPATH, value='//img[@class="w-tour__icon animated-fast"]')
    actions.click(btn).perform()
    iframe = driver.find_element(by=By.CLASS_NAME, value="uk-lightbox-iframe")
    driver.switch_to.frame(iframe)
    wait(driver, 14).until(EC.visibility_of_element_located((By.XPATH, "//div[(contains(@style, 'z-index: 3101'))]")))
    print('   OK: syn_89')
except:
    print('ERROR: не загрузился виртур на син_89')




time.sleep(5)
driver.quit()

