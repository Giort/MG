from selenium import webdriver
from selenium.webdriver.chrome.options import Options
ch_options = Options()
ch_options.add_argument('--headless')
driver = webdriver.Chrome(options= ch_options)
driver.maximize_window()


from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementNotVisibleException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
wait = WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
actions = ActionChains(driver)
import time


# Скрипт открывает окна СП и проверяет, что они открылись
# В лог выводится сообщение "ОК" если окно было открыто
# В лог выводится сообщение "ERROR", если окно не было открыто
# В лог выводится сообщение "ERROR" если элемент, открывающий окно, не был найден по селектору



# 1. проверка слайдера СП на главной странице "МГ"
driver.get("https://moigektar.ru/")
# 1.1 проверка, что есть кнопка на карточке участка в блоке "Специальное предложение"
try:
    title = wait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//h1[text()[contains(.,'Специальное')]]")))
    actions.move_to_element(title).send_keys(Keys.PAGE_DOWN).perform()
    print("   ОК  1.1: блок СП на странице есть")
    time.sleep(10)
    btn = driver.find_element(by=By.XPATH, value="//div[@id='catalogueSpecial']/div/div/div/div[1]//li[1]//button")
    actions.move_to_element(btn).click().perform()
    # 1.2 проверка, что модаль открыта, по тому, есть ли на странице поле ввода этой модали
    try:
        name = wait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//div[@class='w-modal-description uk-modal uk-open']//input[@id='consultationform-name']")))
        print('   OK  1.2: модаль спецпредложений открылась')
    except ElementNotVisibleException:
        print("ERROR:  1.2 модаль СП из блока СП на главной не открылась")
except TimeoutException:
    print("ERROR:  1.1 не могу найти кнопку, чтобы открыть модаль СП на главной МГ")


# 2. проверка слайдера СП в каталоге "МГ"
driver.get("https://moigektar.ru/catalogue")
# 2.1 проверка, что есть кнопка на карточке участка в блоке "Тотальная распродажа"
try:
    btn = wait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//*[text()[contains(., 'Специальное предложение')]]//parent::div//div[@uk-slider='sets: true']//li[1]//div/button/span")))
    print("   ОК  2.1: блок СП на странице есть")
    time.sleep(10)
    actions.move_to_element(btn).click(btn).perform()
    # 2.2 проверка, что модаль открыта, по тому, есть ли на странице поле ввода этой модали
    try:
        name = wait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//div[@class='w-modal-description uk-modal uk-open']//input[@id='consultationform-name']")))
        print('   OK  2.2: модаль спецпредложений открылась')
        closeBtn = driver.find_element(by=By.XPATH, value="//div[@class='w-modal-description uk-modal uk-open']/div/div/button")
        closeBtn.click()
    except ElementNotVisibleException:
        print("ERROR:  2.2 модаль спецпредложений из СП каталога не открылась")
except TimeoutException:
    print("ERROR:  2.1 не могу найти кнопку, чтобы открыть модаль СП в блоке СП каталога МГ")


# 3. проверка слайдера дачных участков в каталоге "МГ"
# 3.1 проверка, что есть кнопка на карточке участка в блоке "Дачные участки"
try:
    btn = wait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//h1[text()[contains(., 'Дачные участки')]]//parent::div//div[1]/div/div//li[1]//button/span")))
    print("   ОК  3.1: блок СП дачные участки на странице есть")
    driver.implicitly_wait(10)
    actions.move_to_element(btn).click(btn).perform()
    # 3.2 проверка, что модаль открыта, по тому, есть ли на странице поле ввода этой модали
    try:
        name = wait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//div[@class='w-modal-description uk-modal uk-open']//input[@id='consultationform-name']")))
        print('   OK  3.2: модаль спецпредложений открылась')
        closeBtn = driver.find_element(by=By.XPATH, value="//div[@class='w-modal-description uk-modal uk-open']/div/div/button")
        closeBtn.click()
    except ElementNotVisibleException:
        print("ERROR:  3.2 модаль СП из дачных участков не открылась")
except TimeoutException:
    print("ERROR:  3.1 не могу найти кнопку, чтобы открыть модаль СП в дачных участках каталога МГ")


# 4. проверка спецпредложений на син_9
driver.get("https://syn9.lp.moigektar.ru/")
# 4.1 проверка, что есть слайдер СП, по наличию кнопки на карточке
try:
    btn = wait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//*[@id='price']//div[2]//div[1]/div/div/div/div[2]/div[2]/div[2]/button")))
    print("   ОК  4.1: блок СП на странице есть")
    driver.implicitly_wait(10)
    actions.move_to_element(btn).click(btn).perform()
    # 4.2 проверка, что модаль открыта, по тому, есть ли на странице поле ввода этой модали
    try:
        name = wait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//*[@id='buyconcreteform-name']")))
        print('   OK  4.2: модаль СП на син_9 открылась')
    except ElementNotVisibleException:
        print("ERROR:  4.2 модаль СП на син_9 не открылась")
except TimeoutException:
    print("ERROR:  4.1 не могу найти кнопку, чтобы открыть модаль СП на син_9")


# 5. проверка спецпредложений на син_33
driver.get("https://syn33.lp.moigektar.ru/")
# 5.1 проверка, что есть слайдер СП, по наличию кнопки на карточке
try:
    btn = wait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//*[@data-slick-index='0']/div/div/div/div[2]/div[2]/div[2]/button")))
    print("   ОК  5.1: блок СП на странице есть")
    driver.implicitly_wait(10)
    actions.move_to_element(btn).click(btn).perform()
    # 5.2 проверка, что модаль открыта, по тому, есть ли на странице поле ввода этой модали
    try:
        name = wait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//*[@id='buyconcreteform-name']")))
        print('   OK  5.2: модаль СП на син_33 открылась')
    except ElementNotVisibleException:
        print("ERROR:  5.2 модаль СП на син_33 не открылась")
except TimeoutException:
    print("ERROR:  5.1 не могу найти кнопку, чтобы открыть модаль СП на син_33")


# 6. проверка спецпредложений на син_34
driver.get("https://syn34.lp.moigektar.ru/")
# 6.1 проверка, что есть слайдер СП, по наличию кнопки на карточке
try:
    btn = wait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//*[@data-slick-index='0']/div/div/div/div[2]/div[2]/div[2]/button")))
    print("   ОК  6.1: блок СП на странице есть")
    driver.implicitly_wait(10)
    actions.move_to_element(btn).click(btn).perform()
    # 6.2 проверка, что модаль открыта, по тому, есть ли на странице поле ввода этой модали
    try:
        name = wait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//*[@id='buyconcreteform-name']")))
        print('   OK  6.2: модаль СП на син_34 открылась')
    except ElementNotVisibleException:
        print("ERROR:  6.2 модаль СП на син_34 не открылась")
except TimeoutException:
    print("ERROR:  6.1 не могу найти кнопку, чтобы открыть модаль СП на син_34")


# 7. проверка спецпредложений на син_37
driver.get("https://syn37.lp.moigektar.ru/")
# 7.1 проверка, что есть слайдер СП, по наличию кнопки на карточке
try:
    btn = wait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//*[@data-slick-index='0']/div/div/div/div[2]/div[2]/div[2]/button")))
    print("   ОК  7.1: блок СП на странице есть")
    driver.implicitly_wait(10)
    actions.move_to_element(btn).click(btn).perform()
    # 7.2 проверка, что модаль открыта, по тому, есть ли на странице поле ввода этой модали
    try:
        name = wait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//*[@id='buyconcreteform-name']")))
        print('   OK  7.2: модаль СП на син_37 открылась')
    except ElementNotVisibleException:
        print("ERROR:  7.2 модаль СП на син_37 не открылась")
except TimeoutException:
    print("ERROR:  7.1 не могу найти кнопку, чтобы открыть модаль СП на син_37")


# 8. проверка спецпредложений на син_39
driver.get("https://syn39.lp.moigektar.ru/")
# 8.1 проверка, что есть слайдер СП, по наличию кнопки на карточке
try:
    btn = wait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//*[@data-slick-index='0']/div/div/div/div[2]/div[2]/div[2]/button")))
    print("   ОК  8.1: блок СП на странице есть")
    driver.implicitly_wait(10)
    actions.move_to_element(btn).click(btn).perform()
    # 8.2 проверка, что модаль открыта, по тому, есть ли на странице поле ввода этой модали
    try:
        name = wait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//*[@id='buyconcreteform-name']")))
        print('   OK  8.2: модаль СП на син_39 открылась')
    except ElementNotVisibleException:
        print("ERROR:  8.2 модаль СП на син_39 не открылась")
except TimeoutException:
    print("ERROR:  8.1 не могу найти кнопку, чтобы открыть модаль СП на син_39")


# 9. проверка спецпредложений на син_42
driver.get("https://syn42.lp.moigektar.ru/")
# 9.1 проверка, что есть слайдер СП, по наличию кнопки на карточке
try:
    btn = wait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//*[@data-slick-index='0']/div/div/div/div[2]/div[2]/div[2]/button")))
    print("   ОК  9.1: блок СП на странице есть")
    driver.implicitly_wait(10)
    actions.move_to_element(btn).click(btn).perform()
    # 9.2 проверка, что модаль открыта, по тому, есть ли на странице поле ввода этой модали
    try:
        name = wait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//*[@id='buyconcreteform-name']")))
        print('   OK  9.2: модаль СП на син_42 открылась')
    except ElementNotVisibleException:
        print("ERROR:  9.2 модаль СП на син_42 не открылась")
except TimeoutException:
    print("ERROR:  9.1 не могу найти кнопку, чтобы открыть модаль СП на син_42")
    

# 10. проверка спецпредложений на син_53
driver.get("https://syn53.lp.moigektar.ru/")
# 10.1 проверка, что есть слайдер СП, по наличию кнопки на карточке
try:
    btn = wait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//*[@data-slick-index='0']/div/div/div/div[2]/div[2]/div[2]/button")))
    print("   ОК 10.1: блок СП на странице есть")
    driver.implicitly_wait(10)
    actions.move_to_element(btn).click(btn).perform()
    # 10.2 проверка, что модаль открыта, по тому, есть ли на странице поле ввода этой модали
    try:
        name = wait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//*[@id='buyconcreteform-name']")))
        print('   OK 10.2: модаль СП на син_53 открылась')
    except ElementNotVisibleException:
        print("ERROR: 10.2 модаль СП на син_53 не открылась")
except TimeoutException:
    print("ERROR: 10.1 не могу найти кнопку, чтобы открыть модаль СП на син_53")


# 11. проверка спецпредложений на син_85
driver.get("https://syn85.lp.moigektar.ru/")
# 11.1 проверка, что есть слайдер СП, по наличию кнопки на карточке
try:
    title = wait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//h1[text()[contains(.,'Специальное')]]")))
    ActionChains(driver).move_to_element(title).send_keys(Keys.PAGE_DOWN).perform()
    print("   ОК 11.1: блок СП на странице есть")
    time.sleep(5)
    btn = driver.find_element(by=By.XPATH, value="//div[@id='catalogueSpecial']/div/div/div/div[1]//li[1]//button")
    actions.move_to_element(btn).click(btn).perform()
    # 11.2 проверка, что модаль открыта, по тому, есть ли на странице поле ввода этой модали
    try:
        name = wait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//*[@id='buyconcreteform-name']")))
        print('   OK 11.2: модаль СП на син_85 открылась')
    except ElementNotVisibleException:
        print("ERROR: 11.2 модаль СП на син_85 не открылась")
except TimeoutException:
    print("ERROR: 11.1 не могу найти кнопку, чтобы открыть модаль СП на син_85")

# 12. проверка спецпредложений на син_84
driver.get("https://syn84.lp.moigektar.ru/")
# 11.1 проверка, что есть слайдер СП, по наличию кнопки на карточке
try:
    title = wait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//h1[text()[contains(.,'Специальное')]]")))
    ActionChains(driver).move_to_element(title).send_keys(Keys.PAGE_DOWN).perform()
    print("   ОК 12.1: блок СП на странице есть")
    time.sleep(5)
    btn = driver.find_element(by=By.XPATH, value="//div[@id='catalogueSpecial']/div/div/div/div[1]//li[1]//button")
    actions.move_to_element(btn).click(btn).perform()
    # 12.2 проверка, что модаль открыта, по тому, есть ли на странице поле ввода этой модали
    try:
        name = wait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//*[@id='buyconcreteform-name']")))
        print('   OK 12.2: модаль СП на син_84 открылась')
    except ElementNotVisibleException:
        print("ERROR: 12.2 модаль СП на син_84 не открылась")
except TimeoutException:
    print("ERROR: 12.1 не могу найти кнопку, чтобы открыть модаль СП на син_84")

# 13. проверка спецпредложений на син_24
driver.get("https://syn24.lp.moigektar.ru/")
# 13.1 проверка, что есть слайдер СП, по наличию кнопки на карточке
try:
    btn = wait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//*[@data-slick-index='0']/div/div/div/div[2]/div[2]/div[2]/button")))
    print("   ОК 13.1: блок СП на странице есть")
    driver.implicitly_wait(10)
    actions.move_to_element(btn).click(btn).perform()
    # 13.2 проверка, что модаль открыта, по тому, есть ли на странице поле ввода этой модали
    try:
        name = wait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//*[@id='consultationform-name']")))
        print('   OK 13.2: модаль СП на син_24 открылась')
    except ElementNotVisibleException:
        print("ERROR: 13.2 модаль СП на син_24 не открылась")
except TimeoutException:
    print("ERROR: 13.1 не могу найти кнопку, чтобы открыть модаль СП на син_24")

time.sleep(1)
driver.quit()

