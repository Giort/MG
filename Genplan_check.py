from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
service = ChromeService(executable_path=ChromeDriverManager().install())
from selenium.webdriver.chrome.options import Options
ch_options = Options()
ch_options.add_argument('--headless')
ch_options.page_load_strategy = 'eager'
driver = webdriver.Chrome(service=service, options= ch_options)
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
import json
#driver.maximize_window()
driver.set_window_size(1920, 1080) # иначе падает тест на 48
driver.implicitly_wait(10)

with open('data.json', 'r') as file:
    data = json.load(file)

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
        driver.find_element(by=By.XPATH, value='//div[(contains(@class, "w-plan__btn"))]').click()
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

# syn_33
count = 0
driver.get("https://syn33.lp.moigektar.ru/")
while count < 3:
    try:
        title = wait(driver, 14).until(EC.presence_of_element_located((By.XPATH, '//div[text()[contains(.,"Генеральный")]]')))
        actions.move_to_element(title).perform()
        driver.find_element(by=By.XPATH, value='(//div[(contains(@class, "w-plan__btn"))])[2]').click()
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
        driver.find_element(by=By.XPATH, value='//div[(contains(@class, "w-plan__btn"))]').click()
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

# syn_39
count = 0
driver.get("https://syn39.lp.moigektar.ru/")
while count < 3:
    try:
        title = wait(driver, 14).until(EC.presence_of_element_located((By.XPATH, '//div[text()[contains(.,"Генеральный")]]')))
        actions.move_to_element(title).perform()
        driver.find_element(by=By.XPATH, value='//div[(contains(@class, "w-plan__btn"))]').click()
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
        title = wait(driver, 14).until(EC.presence_of_element_located((By.XPATH, '//div[text()[contains(.,"Генеральный")]]')))
        actions.move_to_element(title).perform()
        driver.find_element(by=By.XPATH, value='//div[(contains(@class, "w-plan__btn"))]').click()
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

# syn_47
count = 0
driver.get("https://syn47.lp.moigektar.ru/")
while count < 3:
    try:
        block = wait(driver, 14).until(EC.presence_of_element_located((By.ID, 'gen-plan')))
        actions.move_to_element(block).perform()
        driver.find_element(by=By.XPATH, value='//div[(contains(@class, "w-plan__btn"))]').click()
        genplan_elem = wait(driver, 14).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'ymaps.ymaps-2-1-79-inner-panes')))
        if genplan_elem:
            print('   OK: syn_47')
            break
    except:
        count += 1
        if count == 3:
            print('ERROR: генплан на syn_47')
        else:
            driver.refresh()

# syn_48
count = 0
driver.get("https://syn48.lp.moigektar.ru/")
while count < 3:
    try:
        title = wait(driver, 14).until(EC.presence_of_element_located((By.XPATH, '//div[text()[contains(.,"Генеральный")]]')))
        actions.move_to_element(title).perform()
        driver.find_element(by=By.XPATH, value='//div[(contains(@class, "w-plan__btn"))]').click()
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

# syn_52
count = 0
driver.get("https://syn52.lp.moigektar.ru/")
while count < 3:
    try:
        title = wait(driver, 14).until(EC.presence_of_element_located((By.XPATH, '//div[text()[contains(.,"Генеральный")]]')))
        actions.move_to_element(title).perform()
        driver.find_element(by=By.XPATH, value='//div[(contains(@class, "w-plan__btn"))]').click()
        genplan_elem = wait(driver, 14).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'ymaps.ymaps-2-1-79-inner-panes')))
        if genplan_elem:
            print('   OK: syn_52')
            break
    except:
        count += 1
        if count == 3:
            print('ERROR: генплан на syn_52')
        else:
            driver.refresh()

# syn_53
count = 0
driver.get("https://syn53.lp.moigektar.ru/")
while count < 3:
    try:
        title = wait(driver, 14).until(EC.presence_of_element_located((By.XPATH, '//div[text()[contains(.,"Генеральный")]]')))
        actions.move_to_element(title).perform()
        driver.find_element(by=By.XPATH, value='//div[(contains(@class, "w-plan__btn"))]').click()
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

# syn_56
count = 0
driver.get("https://syn56.lp.moigektar.ru/")
while count < 3:
    try:
        title = wait(driver, 14).until(EC.presence_of_element_located((By.XPATH, '//div[text()[contains(.,"Генеральный")]]')))
        actions.move_to_element(title).perform()
        driver.find_element(by=By.XPATH, value='//div[(contains(@class, "w-plan__btn"))]').click()
        genplan_elem = wait(driver, 14).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'ymaps.ymaps-2-1-79-inner-panes')))
        if genplan_elem:
            print('   OK: syn_56')
            break
    except:
        count += 1
        if count == 3:
            print('ERROR: генплан на syn_56')
        else:
            driver.refresh()

# vazuza2
count = 0
driver.get("https://vazuza2.lp.moigektar.ru/")
while count < 3:
    try:
        title = wait(driver, 14).until(EC.presence_of_element_located((By.XPATH, '//div[@id="plan"]/div/div/div/div/div[text()[contains(.,"Генеральный")]]')))
        actions.move_to_element(title).perform()
        driver.find_element(by=By.XPATH, value='//div[(contains(@class, "w-plan__video-btn"))]').click()
        genplan_elem = wait(driver, 14).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'ymaps.ymaps-2-1-79-inner-panes')))
        if genplan_elem:
            print('   OK: Вазуза')
            break
    except:
        count += 1
        if count == 3:
            print('ERROR: генплан на Вазузе')
        else:
            driver.refresh()

# syn_67
count = 0
driver.get("https://syn67.lp.moigektar.ru/")
while count < 3:
    try:
        title = wait(driver, 14).until(EC.presence_of_element_located((By.XPATH, '//div[text()[contains(.,"Генеральный")]]')))
        actions.move_to_element(title).perform()
        driver.find_element(by=By.XPATH, value='//div[(contains(@class, "w-plan__btn"))]').click()
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

# syn_73
count = 0
driver.get("https://syn73.lp.moigektar.ru/")
while count < 3:
    try:
        title = wait(driver, 14).until(EC.presence_of_element_located((By.XPATH, '//div[text()[contains(.,"Генеральный")]]')))
        actions.move_to_element(title).perform()
        driver.find_element(by=By.XPATH, value='//div[(contains(@class, "w-plan__btn"))]').click()
        genplan_elem = wait(driver, 14).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'ymaps.ymaps-2-1-79-inner-panes')))
        if genplan_elem:
            print('   OK: syn_73')
            break
    except:
        count += 1
        if count == 3:
            print('ERROR: генплан на syn_73')
        else:
            driver.refresh()

# syn_84
count = 0
driver.get("https://syn84.lp.moigektar.ru/")
while count < 3:
    try:
        title = wait(driver, 14).until(EC.presence_of_element_located((By.XPATH, '//div[text()[contains(.,"Генеральный")]]')))
        actions.move_to_element(title).perform()
        driver.find_element(by=By.XPATH, value='//div[(contains(@class, "w-plan__btn"))]').click()
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
        driver.find_element(by=By.XPATH, value='//div[(contains(@class, "w-plan__btn"))]').click()
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
        driver.find_element(by=By.XPATH, value='//div[(contains(@class, "w-plan__btn"))]').click()
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
        driver.find_element(by=By.XPATH, value='//div[(contains(@class, "w-plan__video-btn"))]').click()
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
        driver.find_element(by=By.XPATH, value='//div[(contains(@class, "w-plan__btn"))]').click()
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

# syn_95
count = 0
driver.get("https://syn95.lp.moigektar.ru/")
while count < 3:
    try:
        title = wait(driver, 14).until(EC.presence_of_element_located((By.XPATH, '//div[text()[contains(.,"Генеральный")]]')))
        actions.move_to_element(title).perform()
        driver.find_element(by=By.XPATH, value='//div[(contains(@class, "w-plan__btn"))]').click()
        genplan_elem = wait(driver, 14).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'ymaps.ymaps-2-1-79-inner-panes')))
        if genplan_elem:
            print('   OK: syn_95')
            break
    except:
        count += 1
        if count == 3:
            print('ERROR: генплан на syn_95')
        else:
            driver.refresh()

# syn_99
count = 0
driver.get("https://syn99.lp.moigektar.ru/")
while count < 3:
    try:
        title = wait(driver, 14).until(EC.presence_of_element_located((By.XPATH, '//div[text()[contains(.,"Генеральный")]]')))
        actions.move_to_element(title).perform()
        driver.find_element(by=By.XPATH, value='//div[(contains(@class, "w-plan__btn"))]').click()
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

# syn_111
driver.get("https://syn111.lp.moigektar.ru/")
login = driver.find_element(by=By.ID, value='loginconfig-username')
password = driver.find_element(by=By.ID, value='loginconfig-password')
submit = driver.find_element(by=By.CSS_SELECTOR, value='div button')
login.send_keys(str(data["111_cred"]["login"]))
password.send_keys(str(data["111_cred"]["password"]))
submit.click()
time.sleep(2)
count = 0
while count < 3:
    try:
        title = wait(driver, 14).until(EC.presence_of_element_located((By.XPATH, '//div[text()[contains(.,"Генеральный")]]')))
        actions.move_to_element(title).perform()
        driver.find_element(by=By.XPATH, value='//div[(contains(@class, "w-plan__btn"))]').click()
        genplan_elem = wait(driver, 14).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'ymaps.ymaps-2-1-79-inner-panes')))
        if genplan_elem:
            print('   OK: syn_111')
            break
    except:
        count += 1
        if count == 3:
            print('ERROR: генплан на syn_111')
        else:
            driver.refresh()

time.sleep(5)
driver.quit()

