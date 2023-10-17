import chromedriver_binary
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
count = 0
driver.get("https://syn9.lp.moigektar.ru/")
while count < 3:
    try:
        title = wait(driver, 14).until(EC.presence_of_element_located((By.XPATH, '//div[text()[contains(.,"Генеральный")]]')))
        actions.move_to_element(title).perform()
        driver.find_element(by=By.XPATH, value='//img[@data-src="/img/select/overlay-touch.svg"]').click()
        genplan_elem = wait(driver, 14).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'ymaps.ymaps-2-1-79-inner-panes')))
        if genplan_elem:
            print('   OK: syn_9')
            break
    except:
        count += 1
        if count == 3:
            print('ERROR: генплан на syn_9')
        else:
            driver.refresh()

# syn_24
count = 0
driver.get("https://syn24.lp.moigektar.ru/")
while count < 3:
    try:
        play_btn = wait(driver, 14).until(EC.visibility_of_element_located((By.ID, 'w-select-play')))
        play_btn.click()
        genplan_elem = wait(driver, 14).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'ymaps.ymaps-2-1-79-inner-panes')))
        if genplan_elem:
            print('   OK: syn_24')
            break
    except:
        count += 1
        if count == 3:
            print('ERROR: генплан на syn_24')
        else:
            driver.refresh()

# syn_33
count = 0
driver.get("https://syn33.lp.moigektar.ru/")
while count < 3:
    try:
        play_btn = wait(driver, 14).until(EC.visibility_of_element_located((By.ID, 'w-select-play')))
        play_btn.click()
        genplan_elem = wait(driver, 14).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'ymaps.ymaps-2-1-79-inner-panes')))
        if genplan_elem:
            print('   OK: syn_33')
            break
    except:
        count += 1
        if count == 3:
            print('ERROR: генплан на syn_33')
        else:
            driver.refresh()

# syn_34
count = 0
driver.get("https://syn34.lp.moigektar.ru/")
while count < 3:
    try:
        title = wait(driver, 14).until(EC.presence_of_element_located((By.XPATH, '//div[text()[contains(.,"Генеральный")]]')))
        actions.move_to_element(title).perform()
        driver.find_element(by=By.XPATH, value='//img[@data-src="/img/select/overlay-touch.svg"]').click()
        genplan_elem = wait(driver, 14).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'ymaps.ymaps-2-1-79-inner-panes')))
        if genplan_elem:
            print('   OK: syn_34')
            break
    except:
        count += 1
        if count == 3:
            print('ERROR: генплан на syn_34')
        else:
            driver.refresh()

# syn_37
count = 0
driver.get("https://syn37.lp.moigektar.ru/")
while count < 3:
    try:
        title = wait(driver, 14).until(EC.presence_of_element_located((By.XPATH, '//div[text()[contains(.,"Генеральный")]]')))
        actions.move_to_element(title).perform()
        driver.find_element(by=By.XPATH, value='//img[@data-src="/img/select/overlay-touch.svg"]').click()
        genplan_elem = wait(driver, 14).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'ymaps.ymaps-2-1-79-inner-panes')))
        if genplan_elem:
            print('   OK: syn_37')
            break
    except:
        count += 1
        if count == 3:
            print('ERROR: генплан на syn_37')
        else:
            driver.refresh()

# syn_39
count = 0
driver.get("https://syn39.lp.moigektar.ru/")
while count < 3:
    try:
        title = wait(driver, 14).until(EC.presence_of_element_located((By.XPATH, '//div[text()[contains(.,"Генеральный")]]')))
        actions.move_to_element(title).perform()
        driver.find_element(by=By.XPATH, value='//img[@data-src="/img/select/overlay-touch.svg"]').click()
        genplan_elem = wait(driver, 14).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'ymaps.ymaps-2-1-79-inner-panes')))
        if genplan_elem:
            print('   OK: syn_39')
            break
    except:
        count += 1
        if count == 3:
            print('ERROR: генплан на syn_39')
        else:
            driver.refresh()

# syn_42
count = 0
driver.get("https://syn42.lp.moigektar.ru/")
while count < 3:
    try:
        play_btn = wait(driver, 14).until(EC.visibility_of_element_located((By.ID, 'w-select-play')))
        play_btn.click()
        genplan_elem = wait(driver, 14).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'ymaps.ymaps-2-1-79-inner-panes')))
        if genplan_elem:
            print('   OK: syn_42')
            break
    except:
        count += 1
        if count == 3:
            print('ERROR: генплан на syn_42')
        else:
            driver.refresh()

# syn_48
count = 0
driver.get("https://syn48.lp.moigektar.ru/")
while count < 3:
    try:
        title = wait(driver, 14).until(EC.presence_of_element_located((By.XPATH, '//div[text()[contains(.,"Генеральный")]]')))
        actions.move_to_element(title).perform()
        driver.find_element(by=By.XPATH, value='//img[@data-src="/img/select/overlay-touch.svg"]').click()
        genplan_elem = wait(driver, 14).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'ymaps.ymaps-2-1-79-inner-panes')))
        if genplan_elem:
            print('   OK: syn_48')
            break
    except:
        count += 1
        if count == 3:
            print('ERROR: генплан на syn_48')
        else:
            driver.refresh()

# syn_53
count = 0
driver.get("https://syn53.lp.moigektar.ru/")
while count < 3:
    try:
        title = wait(driver, 14).until(EC.presence_of_element_located((By.XPATH, '//div[text()[contains(.,"Генеральный")]]')))
        actions.move_to_element(title).perform()
        driver.find_element(by=By.XPATH, value='//img[@data-src="/img/select/overlay-touch.svg"]').click()
        genplan_elem = wait(driver, 14).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'ymaps.ymaps-2-1-79-inner-panes')))
        if genplan_elem:
            print('   OK: syn_53')
            break
    except:
        count += 1
        if count == 3:
            print('ERROR: генплан на syn_53')
        else:
            driver.refresh()

# vazuza2
try:
    driver.get("https://vazuza2.lp.moigektar.ru/")
    title = wait(driver, 14).until(EC.presence_of_element_located((By.XPATH, '//div[@id="select-b"]/div[1]')))
    actions.move_to_element(title).send_keys(Keys.PAGE_DOWN).perform()
    time.sleep(3)
    driver.find_element(by=By.XPATH, value='//img[@data-src="/img/vazuza/select/overlay-touch.png"]').click()
    wait(driver, 14).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'ymaps.ymaps-2-1-79-inner-panes')))
    print('   OK: vazuza2')
except:
    try:
        driver.refresh()
        title = wait(driver, 14).until(EC.presence_of_element_located((By.XPATH, '//div[@id="select-b"]/div[1]')))
        driver.find_element(by=By.XPATH, value='//img[@data-src="/img/vazuza/select/overlay-touch.png"]').click()
        time.sleep(3)
        wait(driver, 14).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'ymaps.ymaps-2-1-79-inner-panes')))
        print('   OK: vazuza2')
    except:
        print('ERROR: не загрузился генплан на Вазузе')

# syn_67
count = 0
driver.get("https://syn67.lp.moigektar.ru/")
while count < 3:
    try:
        title = wait(driver, 14).until(EC.presence_of_element_located((By.XPATH, '//div[text()[contains(.,"Генеральный")]]')))
        actions.move_to_element(title).perform()
        driver.find_element(by=By.XPATH, value='//img[@data-src="/img/select/overlay-touch.svg"]').click()
        genplan_elem = wait(driver, 14).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'ymaps.ymaps-2-1-79-inner-panes')))
        if genplan_elem:
            print('   OK: syn_67')
            break
    except:
        count += 1
        if count == 3:
            print('ERROR: генплан на syn_67')
        else:
            driver.refresh()

# syn_84
count = 0
driver.get("https://syn84.lp.moigektar.ru/")
while count < 3:
    try:
        title = wait(driver, 14).until(EC.presence_of_element_located((By.XPATH, '//div[text()[contains(.,"Генеральный")]]')))
        actions.move_to_element(title).perform()
        driver.find_element(by=By.XPATH, value='//img[@data-src="/img/select/overlay-touch.svg"]').click()
        genplan_elem = wait(driver, 14).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'ymaps.ymaps-2-1-79-inner-panes')))
        if genplan_elem:
            print('   OK: syn_84')
            break
    except:
        count += 1
        if count == 3:
            print('ERROR: генплан на syn_84')
        else:
            driver.refresh()

# syn_85
count = 0
driver.get("https://syn85.lp.moigektar.ru/")
while count < 3:
    try:
        title = wait(driver, 14).until(EC.presence_of_element_located((By.XPATH, '//div[text()[contains(.,"Генеральный")]]')))
        actions.move_to_element(title).perform()
        driver.find_element(by=By.XPATH, value='//img[@data-src="/img/select/overlay-touch.svg"]').click()
        genplan_elem = wait(driver, 14).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'ymaps.ymaps-2-1-79-inner-panes')))
        if genplan_elem:
            print('   OK: syn_85')
            break
    except:
        count += 1
        if count == 3:
            print('ERROR: генплан на syn_85')
        else:
            driver.refresh()

# syn_87
count = 0
driver.get("https://syn87.lp.moigektar.ru/")
while count < 3:
    try:
        title = wait(driver, 14).until(EC.presence_of_element_located((By.XPATH, '//div[text()[contains(.,"Генеральный")]]')))
        actions.move_to_element(title).perform()
        driver.find_element(by=By.XPATH, value='//img[@data-src="/img/select/overlay-touch.svg"]').click()
        genplan_elem = wait(driver, 14).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'ymaps.ymaps-2-1-79-inner-panes')))
        if genplan_elem:
            print('   OK: syn_87')
            break
    except:
        count += 1
        if count == 3:
            print('ERROR: генплан на syn_87')
        else:
            driver.refresh()

# syn_89
count = 0
driver.get("https://syn89.lp.moigektar.ru/")
while count < 3:
    try:
        title = wait(driver, 14).until(EC.presence_of_element_located((By.XPATH, '//div[text()[contains(.,"Генеральный")]]')))
        actions.move_to_element(title).perform()
        driver.find_element(by=By.XPATH, value='//img[@data-src="/img/select/overlay-touch.svg"]').click()
        genplan_elem = wait(driver, 14).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'ymaps.ymaps-2-1-79-inner-panes')))
        if genplan_elem:
            print('   OK: syn_89')
            break
    except:
        count += 1
        if count == 3:
            print('ERROR: генплан на syn_89')
        else:
            driver.refresh()

# syn_92
count = 0
driver.get("https://syn92.lp.moigektar.ru/")
while count < 3:
    try:
        title = wait(driver, 14).until(EC.presence_of_element_located((By.XPATH, '//div[text()[contains(.,"Генеральный")]]')))
        actions.move_to_element(title).perform()
        driver.find_element(by=By.XPATH, value='//img[@data-src="/img/select/overlay-touch.svg"]').click()
        genplan_elem = wait(driver, 14).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'ymaps.ymaps-2-1-79-inner-panes')))
        if genplan_elem:
            print('   OK: syn_92')
            break
    except:
        count += 1
        if count == 3:
            print('ERROR: генплан на syn_92')
        else:
            driver.refresh()

# syn_99
count = 0
driver.get("https://syn99.lp.moigektar.ru/")
while count < 3:
    try:
        title = wait(driver, 14).until(EC.presence_of_element_located((By.XPATH, '//div[text()[contains(.,"Генеральный")]]')))
        actions.move_to_element(title).perform()
        driver.find_element(by=By.XPATH, value='//img[@data-src="/img/select/overlay-touch.svg"]').click()
        genplan_elem = wait(driver, 14).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'ymaps.ymaps-2-1-79-inner-panes')))
        if genplan_elem:
            print('   OK: syn_99')
            break
    except:
        count += 1
        if count == 3:
            print('ERROR: генплан на syn_99')
        else:
            driver.refresh()


time.sleep(5)
driver.quit()

