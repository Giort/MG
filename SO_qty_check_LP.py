from selenium import webdriver
from selenium.webdriver.chrome.options import Options
ch_options = Options()
ch_options.add_argument('--headless')
ch_options.page_load_strategy = 'eager'
driver = webdriver.Chrome(options= ch_options)
from selenium.webdriver.common.action_chains import ActionChains
actions = ActionChains(driver)
from selenium.webdriver.common.by import By
import time
from selenium.common.exceptions import ElementNotVisibleException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
driver.set_window_size(1920, 1080)


# Скрипт проверяет, сколько участков СП осталось на сайтах посёлков
#
# В лог выводится сообщение "OK" + количество СП, если СП на странице 3 или больше
# В лог выводится сообщение "ERROR" + количество СП, если СП на странице меньше 3
#
# Прогон теста занимает примерно одну минуту
#

# # 1. подсчёт СП на син_9
# try:
#     driver.get("https://syn9.lp.moigektar.ru/")
#     title = wait(driver, 14).until(EC.presence_of_element_located((By.XPATH, "//div[text()[contains(.,'Специальное')]]")))
#     ActionChains(driver).move_to_element(title).send_keys(Keys.PAGE_DOWN).perform()
#     SO_qty = len(driver.find_elements(by=By.CSS_SELECTOR, value='.w-special-slider-card div div div.slick-slide'))
#     if SO_qty >= 3:
#         print("   OK: количество СП на странице син_9 = " + str(SO_qty))
#     else:
#         print("ERROR: количество СП на странице син_9 = " + str(SO_qty))
# except:
#     print("ERROR: не получилось посчитать СП на странице син_9")


# # 2. подсчёт СП на син_24
# try:
#     driver.get("https://syn24.lp.moigektar.ru/")
#     title = wait(driver, 14).until(EC.presence_of_element_located((By.XPATH, "//div[text()[contains(.,'Специальное')]]")))
#     ActionChains(driver).move_to_element(title).send_keys(Keys.PAGE_DOWN).perform()
#     SO_qty = len(driver.find_elements(by=By.CSS_SELECTOR, value='.w-special-slider-card div div div.slick-slide'))
#     if SO_qty >= 3:
#         print("   OK: количество СП на странице син_24 = " + str(SO_qty))
#     else:
#         print("ERROR: количество СП на странице син_24 = " + str(SO_qty))
# except:
#     print("ERROR: не получилось посчитать СП на странице син_24")


# 3. подсчёт СП на син_33
driver.get("https://syn33.lp.moigektar.ru/")
try:
    title = wait(driver, 14).until(EC.presence_of_element_located((By.XPATH, "//div[text()[contains(.,'Специальное')]]")))
    ActionChains(driver).move_to_element(title).send_keys(Keys.PAGE_DOWN).perform()
    SO_qty = len(driver.find_elements(by=By.CSS_SELECTOR, value='.w-special-slider-card div div div.slick-slide'))
    if SO_qty >= 3:
        print("   OK: количество СП на странице син_33 Лисицыно = " + str(SO_qty))
    else:
        print("ERROR: количество СП на странице син_33 Лисицыно = " + str(SO_qty))
except:
    print("ERROR: не получилось посчитать СП на странице син_33")


# подсчёт СП на син_34
driver.get("https://syn34.lp.moigektar.ru/")
try:
    title = wait(driver, 14).until(EC.presence_of_element_located((By.XPATH, "//h1[text()[contains(.,'Специальное')]]")))
    ActionChains(driver).move_to_element(title).send_keys(Keys.PAGE_DOWN).perform()
    SO_qty = len(driver.find_elements(by=By.CSS_SELECTOR, value='.w-catalog-projects ul.card-special > li'))
    if SO_qty >= 3:
        print("   OK: количество СП на странице син_34 Усадьба в подмосковье = " + str(SO_qty))
    else:
        print("ERROR: количество СП на странице син_34 Усадьба в подмосковье = " + str(SO_qty))
except:
    print("ERROR: не получилось посчитать СП на странице син_34")


# 5. подсчёт СП на син_37
driver.get("https://syn37.lp.moigektar.ru/")
try:
    title = wait(driver, 14).until(EC.presence_of_element_located((By.XPATH, "//div[text()[contains(.,'Специальное')]]")))
    ActionChains(driver).move_to_element(title).send_keys(Keys.PAGE_DOWN).perform()
    SO_qty = len(driver.find_elements(by=By.CSS_SELECTOR, value='.w-special-slider-card div div div.slick-slide'))
    if SO_qty >= 3:
        print("   OK: количество СП на странице син_37 Усадьба на Волге = " + str(SO_qty))
    else:
        print("ERROR: количество СП на странице син_37 Усадьба на Волге = " + str(SO_qty))
except:
    print("ERROR: не получилось посчитать СП на странице син_37")


# подсчёт СП на син_39
driver.get("https://syn39.lp.moigektar.ru/")
try:
    title = wait(driver, 14).until(EC.presence_of_element_located((By.XPATH, "//h1[text()[contains(.,'Специальное')]]")))
    ActionChains(driver).move_to_element(title).send_keys(Keys.PAGE_DOWN).perform()
    SO_qty = len(driver.find_elements(by=By.CSS_SELECTOR, value='.w-catalog-projects ul.card-special > li'))
    if SO_qty >= 3:
        print("   OK: количество СП на странице син_39 Лесная усадьба = " + str(SO_qty))
    else:
        print("ERROR: количество СП на странице син_39 Лесная усадьба = " + str(SO_qty))
except:
    print("ERROR: не получилось посчитать СП на странице син_39")


# 8. подсчёт СП на син_42
# driver.get("https://syn42.lp.moigektar.ru/")
# try:
#     title = wait(driver, 14).until(EC.presence_of_element_located((By.XPATH, "//h2[text()[contains(.,'Специальная')]]")))
#     ActionChains(driver).move_to_element(title).send_keys(Keys.PAGE_DOWN).perform()
#     SO_qty = len(driver.find_elements(by=By.CSS_SELECTOR, value='.w-special-slider-card div div div.slick-slide'))
#     if SO_qty >= 3:
#         print("   OK: количество СП на странице син_42 Усадьба в Завидово = " + str(SO_qty))
#     else:
#         print("ERROR: количество СП на странице син_42 Усадьба в Завидово = " + str(SO_qty))
# except:
#     print("ERROR: не получилось посчитать СП на странице син_42")


# 9. подсчёт СП на син_53
driver.get("https://syn53.lp.moigektar.ru/")
try:
    title = wait(driver, 14).until(EC.presence_of_element_located((By.XPATH, "//h1[text()[contains(.,'Специальное')]]")))
    ActionChains(driver).move_to_element(title).send_keys(Keys.PAGE_DOWN).perform()
    SO_qty = len(driver.find_elements(by=By.CSS_SELECTOR, value='.w-catalog-projects ul.card-special > li'))
    if SO_qty >= 3:
        print("   OK: количество СП на странице син_53 Новая жизнь = " + str(SO_qty))
    else:
        print("ERROR: количество СП на странице син_53 Новая жизнь = " + str(SO_qty))
except:
    print("ERROR: не получилось посчитать СП на странице син_53")


# подсчёт СП на син_67
driver.get("https://syn67.lp.moigektar.ru/")
try:
    title = wait(driver, 14).until(EC.presence_of_element_located((By.XPATH, "//h1[text()[contains(.,'Специальное')]]")))
    ActionChains(driver).move_to_element(title).send_keys(Keys.PAGE_DOWN).perform()
    SO_qty = len(driver.find_elements(by=By.CSS_SELECTOR, value='.w-catalog-projects ul.card-special > li'))
    if SO_qty >= 3:
        print("   OK: количество СП на странице син_67 Мое поместье = " + str(SO_qty))
    else:
        print("ERROR: количество СП на странице син_67 Мое поместье = " + str(SO_qty))
except:
    print("ERROR: не получилось посчитать СП на странице син_67")


# 10. подсчёт СП на син_84
driver.get("https://syn84.lp.moigektar.ru/")
try:
    title = wait(driver, 14).until(EC.presence_of_element_located((By.XPATH, "//h1[text()[contains(.,'Специальное')]]")))
    ActionChains(driver).move_to_element(title).send_keys(Keys.PAGE_DOWN).perform()
    SO_qty = len(driver.find_elements(by=By.CSS_SELECTOR, value='.w-catalog-projects ul.card-special > li'))
    if SO_qty >= 3:
        print("   OK: количество СП на странице син_84 Малая родина = " + str(SO_qty))
    else:
        print("ERROR: количество СП на странице син_84 Малая родина = " + str(SO_qty))
except:
    print("ERROR: не получилось посчитать СП на странице син_84")


# 11. подсчёт СП на син_85
driver.get("https://syn85.lp.moigektar.ru/")
try:
    title = wait(driver, 14).until(EC.presence_of_element_located((By.XPATH, "//h1[text()[contains(.,'Специальное')]]")))
    ActionChains(driver).move_to_element(title).send_keys(Keys.PAGE_DOWN).perform()
    SO_qty = len(driver.find_elements(by=By.CSS_SELECTOR, value='.w-catalog-projects ul.card-special > li'))
    if SO_qty >= 3:
        print("   OK: количество СП на странице син_85 Междуречье = " + str(SO_qty))
    else:
        print("ERROR: количество СП на странице син_85 Междуречье = " + str(SO_qty))
except:
    print("ERROR: не получилось посчитать СП на странице син_85")


# 12. подсчёт СП на син_87
driver.get("https://syn87.lp.moigektar.ru/")
try:
    title = wait(driver, 14).until(EC.presence_of_element_located((By.XPATH, "//h1[text()[contains(.,'Специальное')]]")))
    ActionChains(driver).move_to_element(title).send_keys(Keys.PAGE_DOWN).perform()
    SO_qty = len(driver.find_elements(by=By.CSS_SELECTOR, value='.w-catalog-projects ul.card-special > li'))
    if SO_qty >= 3:
        print("   OK: количество СП на странице син_87 Москва Тверская = " + str(SO_qty))
    else:
        print("ERROR: количество СП на странице син_87 Москва Тверская = " + str(SO_qty))
except:
    print("ERROR: не получилось посчитать СП на странице син_87")


# 13. подсчёт СП на син_89
driver.get("https://syn89.lp.moigektar.ru/")
try:
    title = wait(driver, 14).until(EC.presence_of_element_located((By.XPATH, "//h1[text()[contains(.,'Специальное')]]")))
    ActionChains(driver).move_to_element(title).send_keys(Keys.PAGE_DOWN).perform()
    SO_qty = len(driver.find_elements(by=By.CSS_SELECTOR, value='.w-catalog-projects ul.card-special > li'))
    if SO_qty >= 3:
        print("   OK: количество СП на странице син_89 Долина озёр = " + str(SO_qty))
    else:
        print("ERROR: количество СП на странице син_89 Долина озёр = " + str(SO_qty))
except:
    print("ERROR: не получилось посчитать СП на странице син_89")

# 14. подсчёт СП на син_92
driver.get("http://syn92.lp.moigektar.ru/")
try:
    title = wait(driver, 14).until(EC.presence_of_element_located((By.XPATH, "//h1[text()[contains(.,'Специальное')]]")))
    ActionChains(driver).move_to_element(title).send_keys(Keys.PAGE_DOWN).perform()
    SO_qty = len(driver.find_elements(by=By.CSS_SELECTOR, value='.w-catalog-projects ul.card-special > li'))
    if SO_qty >= 3:
        print("   OK: количество СП на странице син_92 Долина озёр = " + str(SO_qty))
    else:
        print("ERROR: количество СП на странице син_92 Долина озёр = " + str(SO_qty))
except:
    print("ERROR: не получилось посчитать СП на странице син_92")

time.sleep(1)
driver.quit()
