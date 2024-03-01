from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
ch_options = Options()
ch_options.add_argument('--headless')
ch_options.page_load_strategy = 'eager'
service = ChromeService(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=ch_options)
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
actions = ActionChains(driver)
from selenium.webdriver.common.keys import Keys
import time
driver.set_window_size(1600, 1000)
driver.implicitly_wait(10)


# Скрипт заходит на сайты посёлков, запускает загрузку Виртуального тура
# и проверяет, что элемент на нём прогрузился
#
# В лог выводится сообщение "ОК", если этот элемент загрузился
# В лог выводится сообщение "ERROR", если элемент не загрузился
#



# Мой гектар
count = 0
driver.get("https://moigektar.ru/")
while count < 3:
    try:
        title = driver.find_element(by=By.ID, value='w-select-map')
        actions.move_to_element(title).perform()
        time.sleep(1)
        btn = driver.find_element(by=By.XPATH, value='//*[(contains(@class, "w-select__tour-icon"))]')
        actions.click(btn).perform()
        iframe = driver.find_element(by=By.XPATH, value='//iframe[@class="embed-responsive-item"]')
        driver.switch_to.frame(iframe)
        elem = wait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, "//div[(contains(@style, 'z-index: 3099'))]")))
        if elem:
            print('   OK: МГ')
            break
    except:
        count += 1
        if count == 3:
            print('ERROR: не загрузился виртур на МГ')
        else:
            driver.refresh()

# syn_9
count = 0
driver.get("https://syn9.lp.moigektar.ru/")
while count < 3:
    try:
        title = driver.find_element(by=By.ID, value='tour')
        actions.move_to_element(title).perform()
        time.sleep(1)
        btn = driver.find_element(by=By.XPATH, value='//*[(contains(@class, "w-tour__icon animated-fast"))]')
        actions.click(btn).perform()
        iframe = driver.find_element(by=By.CLASS_NAME, value="uk-lightbox-iframe")
        driver.switch_to.frame(iframe)
        elem = wait(driver, 14).until(EC.visibility_of_element_located((By.XPATH, "//div[(contains(@style, 'z-index: 3056'))]")))
        if elem:
            print('   OK: syn_9')
            break
    except:
        count += 1
        if count == 3:
            print('ERROR: не загрузился виртур на син_9')
        else:
            driver.refresh()

# syn_24
# count = 0
# driver.get("https://syn24.lp.moigektar.ru/")
# while count < 3:
#     try:
#         btn = driver.find_element(by=By.ID, value='w-tour-play')
#         actions.move_to_element(btn).perform()
#         actions.click(btn).perform()
#         iframe = driver.find_element(by=By.CLASS_NAME, value="fancybox-iframe")
#         driver.switch_to.frame(iframe)
#         elem = wait(driver, 14).until(EC.visibility_of_element_located((By.XPATH, "//div[(contains(@style, 'z-index: 3101'))]")))
#         if elem:
#             print('   OK: syn_24')
#             break
#     except:
#         count += 1
#         if count == 3:
#             print('ERROR: не загрузился виртур на син_24')
#         else:
#             driver.refresh()

# syn_33
count = 0
driver.get("https://syn33.lp.moigektar.ru/")
while count < 3:
    try:
        title = driver.find_element(by=By.ID, value='tour')
        actions.move_to_element(title).perform()
        time.sleep(1)
        btn = driver.find_element(by=By.XPATH, value='//*[(contains(@class, "w-tour__icon"))]')
        actions.click(btn).perform()
        iframe = driver.find_element(by=By.CLASS_NAME, value="uk-lightbox-iframe")
        driver.switch_to.frame(iframe)
        elem = wait(driver, 14).until(EC.visibility_of_element_located((By.XPATH, "//div[(contains(@style, 'z-index: 3101'))]")))
        if elem:
            print('   OK: syn_33')
            break
    except:
        count += 1
        if count == 3:
            print('ERROR: не загрузился виртур на син_33')
        else:
            driver.refresh()

# syn_34
count = 0
driver.get("https://syn34.lp.moigektar.ru/")
while count < 3:
    try:
        title = driver.find_element(by=By.ID, value='tour')
        actions.move_to_element(title).perform()
        time.sleep(1)
        btn = driver.find_element(by=By.XPATH, value='//*[(contains(@class, "w-tour__icon animated-fast"))]')
        actions.click(btn).perform()
        iframe = driver.find_element(by=By.CLASS_NAME, value="uk-lightbox-iframe")
        driver.switch_to.frame(iframe)
        elem = wait(driver, 14).until(EC.visibility_of_element_located((By.XPATH, "//div[(contains(@style, 'z-index: 219'))]")))
        if elem:
            print('   OK: syn_34')
            break
    except:
        count += 1
        if count == 3:
            print('ERROR: не загрузился виртур на син_34')
        else:
            driver.refresh()

# syn_39
count = 0
driver.get("https://syn39.lp.moigektar.ru/")
while count < 3:
    try:
        title = driver.find_element(by=By.XPATH, value='//div[text()[contains(., "Виртуальный тур")]]')
        actions.move_to_element(title).send_keys(Keys.PAGE_DOWN).perform()
        time.sleep(1)
        btn = driver.find_element(by=By.XPATH, value='//*[(contains(@class, "w-tour__icon animated-fast"))]')
        actions.click(btn).perform()
        iframe = driver.find_element(by=By.CLASS_NAME, value="uk-lightbox-iframe")
        driver.switch_to.frame(iframe)
        elem = wait(driver, 14).until(EC.visibility_of_element_located((By.XPATH, "//div[(contains(@style, 'z-index: 267'))]")))
        if elem:
            print('   OK: syn_39')
            break
    except:
        count += 1
        if count == 3:
            print('ERROR: не загрузился виртур на син_39')
        else:
            driver.refresh()

# syn_42
count = 0
driver.get("https://syn42.lp.moigektar.ru/")
while count < 3:
    try:
        title = driver.find_element(by=By.XPATH, value='//div[text()[contains(., "Виртуальный тур")]]')
        actions.move_to_element(title).send_keys(Keys.PAGE_DOWN).perform()
        time.sleep(1)
        btn = driver.find_element(by=By.XPATH, value='//*[(contains(@class, "w-tour__icon animated-fast"))]')
        actions.click(btn).perform()
        iframe = driver.find_element(by=By.CLASS_NAME, value="uk-lightbox-iframe")
        driver.switch_to.frame(iframe)
        elem = wait(driver, 14).until(EC.visibility_of_element_located((By.XPATH, "//div[(contains(@style, 'z-index: 3101'))]")))
        if elem:
            print('   OK: syn_42')
            break
    except:
        count += 1
        if count == 3:
            print('ERROR: не загрузился виртур на син_42')
        else:
            driver.refresh()

# syn_48
count = 0
driver.get("https://syn48.lp.moigektar.ru/")
while count < 3:
    try:
        title = driver.find_element(by=By.ID, value='tour')
        actions.move_to_element(title).perform()
        time.sleep(1)
        btn = driver.find_element(by=By.XPATH, value='//*[(contains(@class, "w-tour__icon animated-fast"))]')
        actions.click(btn).perform()
        iframe = driver.find_element(by=By.CLASS_NAME, value="uk-lightbox-iframe")
        driver.switch_to.frame(iframe)
        elem = wait(driver, 14).until(EC.visibility_of_element_located((By.XPATH, "//div[(contains(@style, 'z-index: 330'))]")))
        if elem:
            print('   OK: syn_48')
            break
    except:
        count += 1
        if count == 3:
            print('ERROR: не загрузился виртур на син_48')
        else:
            driver.refresh()

# syn_52
count = 0
driver.get("https://syn52.lp.moigektar.ru/")
while count < 3:
    try:
        title = driver.find_element(by=By.ID, value='tour')
        actions.move_to_element(title).perform()
        time.sleep(1)
        btn = driver.find_element(by=By.XPATH, value='//*[(contains(@class, "w-tour__icon"))]')
        actions.click(btn).perform()
        iframe = driver.find_element(by=By.CLASS_NAME, value="uk-lightbox-iframe")
        driver.switch_to.frame(iframe)
        elem = wait(driver, 14).until(EC.visibility_of_element_located((By.XPATH, "//div[(contains(@style, 'z-index: 245'))]")))
        if elem:
            print('   OK: syn_52')
            break
    except:
        count += 1
        if count == 3:
            print('ERROR: не загрузился виртур на син_52')
        else:
            driver.refresh()

# syn_53
count = 0
driver.get("https://syn53.lp.moigektar.ru/")
while count < 3:
    try:
        title = driver.find_element(by=By.XPATH, value='//*[@id="tour"]')
        actions.move_to_element(title).perform()
        time.sleep(1)
        btn = driver.find_element(by=By.XPATH, value='//*[(contains(@class, "w-tour__icon animated-fast"))]')
        actions.click(btn).perform()
        iframe = driver.find_element(by=By.CLASS_NAME, value="uk-lightbox-iframe")
        driver.switch_to.frame(iframe)
        elem = wait(driver, 14).until(EC.visibility_of_element_located((By.XPATH, "//div[(contains(@style, 'z-index: 306'))]")))
        if elem:
            print('   OK: syn_53')
            break
    except:
        count += 1
        if count == 3:
            print('ERROR: не загрузился виртур на син_53')
        else:
            driver.refresh()

# syn_56
count = 0
driver.get("https://syn56.lp.moigektar.ru/")
while count < 3:
    try:
        title = driver.find_element(by=By.ID, value='tour')
        actions.move_to_element(title).perform()
        time.sleep(1)
        btn = driver.find_element(by=By.XPATH, value='//*[(contains(@class, "w-tour__icon animated-fast"))]')
        actions.click(btn).perform()
        iframe = driver.find_element(by=By.CLASS_NAME, value="uk-lightbox-iframe")
        driver.switch_to.frame(iframe)
        elem = wait(driver, 14).until(EC.visibility_of_element_located((By.XPATH, "//div[(contains(@style, 'z-index: 3101'))]")))
        if elem:
            print('   OK: syn_56')
            break
    except:
        count += 1
        if count == 3:
            print('ERROR: не загрузился виртур на син_56')
        else:
            driver.refresh()

# syn_67
count = 0
driver.get("https://syn67.lp.moigektar.ru/")
while count < 3:
    try:
        title = driver.find_element(by=By.ID, value='tour')
        actions.move_to_element(title).perform()
        time.sleep(1)
        btn = driver.find_element(by=By.XPATH, value='//*[(contains(@class, "w-tour__icon animated-fast"))]')
        actions.click(btn).perform()
        iframe = driver.find_element(by=By.CLASS_NAME, value="uk-lightbox-iframe")
        driver.switch_to.frame(iframe)
        elem = wait(driver, 14).until(EC.visibility_of_element_located((By.XPATH, "//div[(contains(@style, 'z-index: 3101'))]")))
        if elem:
            print('   OK: syn_67')
            break
    except:
        count += 1
        if count == 3:
            print('ERROR: не загрузился виртур на син_67')
        else:
            driver.refresh()

# syn_84
count = 0
driver.get("https://syn84.lp.moigektar.ru/")
while count < 3:
    try:
        title = driver.find_element(by=By.ID, value='tour')
        actions.move_to_element(title).perform()
        time.sleep(3)
        btn = driver.find_element(by=By.XPATH, value='//*[(contains(@class, "w-tour__icon animated-fast"))]')
        actions.click(btn).perform()
        iframe = driver.find_element(by=By.CLASS_NAME, value="uk-lightbox-iframe")
        driver.switch_to.frame(iframe)
        elem = wait(driver, 14).until(EC.visibility_of_element_located((By.XPATH, "//div[(contains(@style, 'z-index: 182'))]")))
        if elem:
            print('   OK: syn_84')
            break
    except:
        count += 1
        if count == 3:
            print('ERROR: не загрузился виртур на син_84')
        else:
            driver.refresh()

# syn_85
count = 0
driver.get("https://syn85.lp.moigektar.ru/")
while count < 3:
    try:
        title = driver.find_element(by=By.ID, value='tour')
        actions.move_to_element(title).perform()
        time.sleep(1)
        btn = driver.find_element(by=By.XPATH, value='//*[(contains(@class, "w-tour__icon animated-fast"))]')
        actions.click(btn).perform()
        iframe = driver.find_element(by=By.CLASS_NAME, value="uk-lightbox-iframe")
        driver.switch_to.frame(iframe)
        elem = wait(driver, 14).until(EC.visibility_of_element_located((By.XPATH, "//div[(contains(@style, 'z-index: 3101'))]")))
        if elem:
            print('   OK: syn_85')
            break
    except:
        count += 1
        if count == 3:
            print('ERROR: не загрузился виртур на син_85')
        else:
            driver.refresh()

# syn_87
count = 0
driver.get("https://syn87.lp.moigektar.ru/")
while count < 3:
    try:
        title = driver.find_element(by=By.ID, value='tour')
        actions.move_to_element(title).perform()
        time.sleep(1)
        btn = driver.find_element(by=By.XPATH, value='//*[(contains(@class, "w-tour__icon animated-fast"))]')
        actions.click(btn).perform()
        iframe = driver.find_element(by=By.CLASS_NAME, value="uk-lightbox-iframe")
        driver.switch_to.frame(iframe)
        elem = wait(driver, 14).until(EC.visibility_of_element_located((By.XPATH, "//div[(contains(@style, 'z-index: 230'))]")))
        if elem:
            print('   OK: syn_87')
            break
    except:
        count += 1
        if count == 3:
            print('ERROR: не загрузился виртур на син_87')
        else:
            driver.refresh()

# syn_89
count = 0
driver.get("https://syn89.lp.moigektar.ru/")
while count < 3:
    try:
        title = driver.find_element(by=By.ID, value='tour')
        actions.move_to_element(title).perform()
        time.sleep(1)
        btn = driver.find_element(by=By.XPATH, value='//*[(contains(@class, "w-tour__icon animated-fast"))]')
        actions.click(btn).perform()
        iframe = driver.find_element(by=By.CLASS_NAME, value="uk-lightbox-iframe")
        driver.switch_to.frame(iframe)
        elem = wait(driver, 14).until(EC.visibility_of_element_located((By.XPATH, "//div[(contains(@style, 'z-index: 3101'))]")))
        if elem:
            print('   OK: syn_89')
            break
    except:
        count += 1
        if count == 3:
            print('ERROR: не загрузился виртур на син_89')
        else:
            driver.refresh()

# syn_92
count = 0
driver.get("https://syn92.lp.moigektar.ru/")
while count < 3:
    try:
        title = driver.find_element(by=By.ID, value='tour')
        actions.move_to_element(title).perform()
        time.sleep(1)
        btn = driver.find_element(by=By.XPATH, value='//*[(contains(@class, "w-tour__icon animated-fast"))]')
        actions.click(btn).perform()
        iframe = driver.find_element(by=By.CLASS_NAME, value="uk-lightbox-iframe")
        driver.switch_to.frame(iframe)
        elem = wait(driver, 14).until(EC.visibility_of_element_located((By.XPATH, "//div[(contains(@style, 'z-index: 189'))]")))
        if elem:
            print('   OK: syn_92')
            break
    except:
        count += 1
        if count == 3:
            print('ERROR: не загрузился виртур на син_92')
        else:
            driver.refresh()

# syn_95
count = 0
driver.get("https://syn95.lp.moigektar.ru/")
while count < 3:
    try:
        title = driver.find_element(by=By.ID, value='tour')
        actions.move_to_element(title).perform()
        time.sleep(1)
        btn = driver.find_element(by=By.XPATH, value='//*[(contains(@class, "w-tour__icon-btn"))]')
        actions.click(btn).perform()
        iframe = driver.find_element(by=By.CLASS_NAME, value="uk-lightbox-iframe")
        driver.switch_to.frame(iframe)
        elem = wait(driver, 14).until(EC.visibility_of_element_located((By.XPATH, "//div[(contains(@style, 'z-index: 227'))]")))
        if elem:
            print('   OK: syn_95')
            break
    except:
        count += 1
        if count == 3:
            print('ERROR: не загрузился виртур на син_95')
        else:
            driver.refresh()

# syn_99
count = 0
driver.get("https://syn99.lp.moigektar.ru/")
while count < 3:
    try:
        title = driver.find_element(by=By.ID, value='tour')
        actions.move_to_element(title).perform()
        time.sleep(1)
        btn = driver.find_element(by=By.XPATH, value='//*[(contains(@class, "w-tour__icon"))]')
        actions.click(btn).perform()
        iframe = driver.find_element(by=By.CLASS_NAME, value="uk-lightbox-iframe")
        driver.switch_to.frame(iframe)
        elem = wait(driver, 14).until(EC.visibility_of_element_located((By.XPATH, "//div[(contains(@style, 'z-index: 201'))]")))
        if elem:
            print('   OK: syn_99')
            break
    except:
        count += 1
        if count == 3:
            print('ERROR: не загрузился виртур на син_99')
        else:
            driver.refresh()

time.sleep(5)
driver.quit()

