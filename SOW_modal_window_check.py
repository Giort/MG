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
import json
driver.set_window_size(1660, 1000)
driver.implicitly_wait(10)

# Скрипт отправляет заявки через мод. окна Спецпредложений
#
# В лог выводится сообщение "ОК", если: найдена кнопка на карточке SOW; отобразился
#   элемент, подтверждающий успешную отправку данных 
# В лог выводится сообщение "ERROR", если: кнопка на карточке SOW не была найдена;
#   не был найден подтверждающий элемент 
#

with open('data.json', 'r') as file:
    data = json.load(file)

# проверка слайдера SOW на главной странице "МГ"
count = 0
driver.get("https://moigektar.ru/")
while count < 3:
    # проверка, что есть кнопка на карточке участка в блоке "Тотальная распродажа"/"Специальное предложение"
    try:
        title = driver.find_element(by=By.XPATH, value="" + str(data["mg_loc"]["mg_main_sow_title"]))
        actions.move_to_element(title).send_keys(Keys.PAGE_DOWN).send_keys(Keys.ARROW_DOWN).perform()
        btn = wait(driver, 15).until(EC.element_to_be_clickable((By.XPATH, "" + str(data["mg_loc"]["mg_main_sow_btn"]))))
        print("   ОК: блок SOW на Главной МГ есть")
        actions.move_to_element(btn).click(btn).perform()
        time.sleep(3)
        # проверка, что модаль открыта, по тому, есть ли на странице поле ввода этой модали
        try:
            name = wait(driver, 15).until(EC.visibility_of_element_located((By.XPATH, "//div[(contains(@class, 'w-modal-description'))]//input[@id='buybatchform-username']")))
            print('   OK: модаль SOW открылась')
            phone = driver.find_element(by=By.XPATH, value="//div[@class='w-modal-description uk-modal uk-open']//input[@id='buybatchform-userphonenumber']")
            email = driver.find_element(by=By.XPATH, value="//div[@class='w-modal-description uk-modal uk-open']//input[@id='buybatchform-useremail']")
            submitBtn = driver.find_element(by=By.XPATH, value="//div[@class='w-modal-description uk-modal uk-open']//form/div/button[@type='submit']")
            name.send_keys(str(data["test_data_valid"]["name"]))
            phone.send_keys(str(data["test_data_valid"]["phone"]))
            email.send_keys(str(data["test_data_valid"]["email"]))
            time.sleep(1)
            submitBtn.click()
            # проверить, что заявка отправлена, по тому, отобразилась ли надпись "Выберите дату визита"
            successText = wait(driver, 15).until(EC.visibility_of_element_located((By.XPATH, "//div[text()[contains(.,'Выберите дату визита')]]")))
            print('   OK: заявка из SOW на главной МГ была отправлена')
            if successText:
                break
        except:
            count += 1
            if count == 3:
                print('ERROR: SOW на Главной МГ: модаль открылась, но заявка не отправлена')
            else:
                driver.refresh()
    except:
        count += 1
        if count == 3:
            print("ERROR: SOW на Главной МГ: не могу нажать кнопку на карточке СП")
        else:
            driver.refresh()


# проверка слайдера SOW в Каталоге поселков
count = 0
driver.get("https://moigektar.ru/catalogue")
while count < 3:
    # проверка, что есть кнопка на карточке участка в блоке "Тотальная распродажа"/"Специальное предложение"
    try:
        btn = driver.find_element(by=By.XPATH, value="" + str(data["mg_loc"]["mg_catalog_country_sow_btn"]))
        print("   ОК: блок SOW в Каталоге поселков есть")
        actions.move_to_element(btn).click(btn).perform()
        time.sleep(3)
        # проверка, что модаль открыта, по тому, есть ли на странице поле ввода этой модали
        try:
            name = wait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, "//div[@class='w-modal-description uk-modal uk-open']//input[@id='buybatchform-username']")))
            print('   OK: модаль SOW открылась')
            phone = driver.find_element(by=By.XPATH, value="//div[@class='w-modal-description uk-modal uk-open']//input[@id='buybatchform-userphonenumber']")
            email = driver.find_element(by=By.XPATH, value="//div[@class='w-modal-description uk-modal uk-open']//input[@id='buybatchform-useremail']")
            submitBtn = driver.find_element(by=By.XPATH, value="//div[@class='w-modal-description uk-modal uk-open']//form/div/button[@type='submit']")
            name.send_keys(str(data["test_data_valid"]["name"]))
            phone.send_keys(str(data["test_data_valid"]["phone"]))
            email.send_keys(str(data["test_data_valid"]["email"]))
            time.sleep(1)
            submitBtn.click()
            # проверить, что заявка отправлена, по тому, открылась ли страница благодарности
            time.sleep(10)
            url = driver.current_url
            if url == 'https://moigektar.ru/thanks':
                print('   OK: заявка из SOW в Каталоге поселков отправлена, открылась страница благодарности')
                break
        except:
            count += 1
            if count == 3:
                print('ERROR: SOW на странице Каталога поселков: модаль открылась, но заявка не отправлена')
            else:
                driver.refresh()
    except:
        count += 1
        if count == 3:
            print("ERROR: SOW на странице Каталога поселков: не могу нажать кнопку на карточке СП")
        else:
            driver.refresh()


# проверка работы карточек SOW на странице Каталога участков
count = 0
driver.get("https://moigektar.ru/batches")

# избавляемся от модалки
if count == 0:
    time.sleep(5)
    driver.find_element(by=By.CSS_SELECTOR, value="#modal-auth-batches #consultationform-name").send_keys(str(data["test_data_valid"]["name"]))
    driver.find_element(by=By.CSS_SELECTOR, value="#modal-auth-batches #consultationform-phone").send_keys(str(data["test_data_valid"]["phone"]))
    driver.find_element(by=By.CSS_SELECTOR, value="#modal-auth-batches #consultationform-email").send_keys(str(data["test_data_valid"]["email"]))
    driver.find_element(by=By.XPATH, value="//*[@id='modal-auth-batches']//button[text()[contains(.,'Отправить заявку')]]").click()
    time.sleep(2)

while count < 3:
    # проверка, что есть кнопка на первой карточке участка
    try:
        btn = wait(driver, 15).until(EC.element_to_be_clickable((By.XPATH, "" + str(data["mg_loc"]["mg_catalog_plot_btn"]))))
        print("   ОК: карточки участков на странице Каталога участков есть")
        actions.move_to_element(btn).click().perform()
        time.sleep(3)
        # проверка, что модаль открыта, по тому, есть ли на странице поле ввода этой модали
        try:
            name = wait(driver, 15).until(EC.visibility_of_element_located((By.XPATH, "//div[@class='w-modal-description uk-modal uk-open']//input[@id='buybatchform-username']")))
            print('   OK: модаль актива открылась')
            phone = driver.find_element(by=By.XPATH, value="//div[@class='w-modal-description uk-modal uk-open']//input[@id='buybatchform-userphonenumber']")
            email = driver.find_element(by=By.XPATH, value="//div[@class='w-modal-description uk-modal uk-open']//input[@id='buybatchform-useremail']")
            submitBtn = driver.find_element(by=By.XPATH, value="//div[@class='w-modal-description uk-modal uk-open']//form/div/button[@type='submit']")
            name.send_keys(str(data["test_data_valid"]["name"]))
            phone.send_keys(str(data["test_data_valid"]["phone"]))
            email.send_keys(str(data["test_data_valid"]["email"]))
            time.sleep(1)
            submitBtn.click()
            # проверить, что заявка отправлена, по тому, отобразилась ли надпись "Выберите дату визита"
            successText = wait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//div[text()[contains(.,'Выберите дату визита')]]")))
            print('   OK: заявка была отправлена')
            if successText:
                break
        except:
            count += 1
            if count == 3:
                print('ERROR: SOW на странице Каталога участков: модаль открылась, но заявка не отправлена')
            else:
                driver.refresh()
    except:
        count += 1
        if count == 3:
            print("ERROR: SOW на странице Каталога участков: не могу нажать кнопку на карточке СП")
        else:
            driver.refresh()


# проверка карточек на странице Дачных
count = 0
driver.get("https://moigektar.ru/batches/country")
while count < 3:
    # проверка, что есть кнопка на первой карточке участка
    try:
        title = wait(driver, 14).until(EC.visibility_of_element_located((By.XPATH, "//h1[text()[contains(.,'Дачные')]]")))
        print("   ОК: карточки на странице Дачных есть")
        btn = driver.find_element(by=By.XPATH, value="//ul/li[1]/div//button")
        actions.move_to_element(btn).click().perform()
        time.sleep(3)
        # проверка, что модаль открыта, по тому, есть ли на странице поле ввода этой модали
        try:
            name = wait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//div[@class='w-modal-description uk-modal uk-open']//input[@id='buybatchform-username']")))
            print('   OK: модаль SOW открылась')
            phone = driver.find_element(by=By.XPATH, value="//div[@class='w-modal-description uk-modal uk-open']//input[@id='buybatchform-userphonenumber']")
            email = driver.find_element(by=By.XPATH, value="//div[@class='w-modal-description uk-modal uk-open']//input[@id='buybatchform-useremail']")
            submitBtn = driver.find_element(by=By.XPATH, value="//div[@class='w-modal-description uk-modal uk-open']//form/div/button[@type='submit']")
            name.send_keys(str(data["test_data_valid"]["name"]))
            phone.send_keys(str(data["test_data_valid"]["phone"]))
            email.send_keys(str(data["test_data_valid"]["email"]))
            time.sleep(1)
            submitBtn.click()
            # проверить, что заявка отправлена, по тому, отобразилась ли надпись "Выберите дату визита"
            successText = wait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//div[text()[contains(.,'Выберите дату визита')]]")))
            print('   OK: заявка была отправлена')
            if successText:
                break
        except:
            count += 1
            if count == 3:
                print('ERROR: карточки на странице Дачных: модаль открылась, но заявка не отправлена')
            else:
                driver.refresh()
    except:
        count += 1
        if count == 3:
            print("ERROR: карточки на странице Дачных: не могу нажать кнопку на карточке СП")
        else:
            driver.refresh()


# проверка карточек дачных участков в Каталоге поселков
count = 0
driver.get("https://moigektar.ru/catalogue")
while count < 3:
    # проверка, что есть кнопка на карточке участка в блоке "Дачные поселки"
    try:
        title = wait(driver, 14).until(EC.visibility_of_element_located((By.XPATH, "//h1[text()[contains(., 'Дачные участки')]]")))
        actions.move_to_element(title).send_keys(Keys.PAGE_DOWN).send_keys(Keys.ARROW_DOWN).perform()
        btn = driver.find_element(by=By.XPATH, value="" + str(data["mg_loc"]["mg_catalog_country_country_btn"]))
        print("   ОК: блок Дачных в Каталоге поселков есть")
        actions.move_to_element(btn).click(btn).perform()
        time.sleep(3)
        # проверка, что модаль открыта, по тому, есть ли на странице поле ввода этой модали
        try:
            name = wait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, "//div[@class='w-modal-description uk-modal uk-open']//input[@id='buybatchform-username']")))
            print('   OK: модаль SOW открылась')
            phone = driver.find_element(by=By.XPATH, value="//div[@class='w-modal-description uk-modal uk-open']//input[@id='buybatchform-userphonenumber']")
            email = driver.find_element(by=By.XPATH, value="//div[@class='w-modal-description uk-modal uk-open']//input[@id='buybatchform-useremail']")
            submitBtn = driver.find_element(by=By.XPATH, value="//div[@class='w-modal-description uk-modal uk-open']//form/div/button[@type='submit']")
            name.send_keys(str(data["test_data_valid"]["name"]))
            phone.send_keys(str(data["test_data_valid"]["phone"]))
            email.send_keys(str(data["test_data_valid"]["email"]))
            time.sleep(1)
            submitBtn.click()
            # проверить, что заявка отправлена, по тому, открылась ли страница благодарности
            time.sleep(10)
            url = driver.current_url
            if url == 'https://moigektar.ru/thanks':
                print('   OK: заявка из Дачных в Каталоге поселков отправлена, открылась страница благодарности')
                break
        except:
            count += 1
            if count == 3:
                print('ERROR: Дачные на странице Каталога поселков: модаль открылась, но заявка не отправлена')
            else:
                driver.refresh()
    except:
        count += 1
        if count == 3:
            print("ERROR: Дачные на странице Каталога поселков: не могу нажать кнопку на карточке СП")
        else:
            driver.refresh()


# 4. проверка спецпредложений на син_9
# driver.get("https://syn9.lp.moigektar.ru/")
# # 4.1 проверка, что есть слайдер SOW, по наличию кнопки на карточке
# try:
#     btn = wait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//*[@id='price']//div[2]//div[1]/div/div/div/div[2]/div[2]/div[2]/button")))
#     print("   ОК  4.1: блок SOW на странице есть")
#     driver.implicitly_wait(10)
#     actions.move_to_element(btn).click(btn).perform()
#     # 4.2 проверка, что модаль открыта, по тому, есть ли на странице поле ввода этой модали
#     try:
#         name = wait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//*[@id='buyconcreteform-name']")))
#         print('   OK  4.2: модаль SOW на син_9 открылась')
#     except ElementNotVisibleException:
#         print("ERROR:  4.2 модаль SOW на син_9 не открылась")
# except TimeoutException:
#     print("ERROR:  4.1 не могу найти кнопку, чтобы открыть модаль SOW на син_9")


# проверка спецпредложений на син_33
count = 0
driver.get("https://syn33.lp.moigektar.ru/")
while count < 3:
    # проверка, что есть слайдер SOW, по наличию кнопки на карточке
    try:
        btn = wait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//*[@data-slick-index='0']/div/div/div/div[2]/div[2]/div[2]/button")))
        print("   ОК: блок SOW на странице син_33 есть")
        actions.move_to_element(btn).click(btn).perform()
        time.sleep(3)
        # проверка, что модаль открыта, по тому, есть ли на странице поле ввода этой модали
        try:
            name = driver.find_element(by=By.XPATH, value="//*[@id='buyconcreteform-name']")
            print('   OK: модаль SOW открылась')
            phone = driver.find_element(by=By.XPATH, value="//*[@name='BuyConcreteForm[phone]']")
            email = driver.find_element(by=By.XPATH, value="//*[@id='buyconcreteform-email']")
            submitBtn = driver.find_element(by=By.XPATH, value="//div[@id='modal-select-content']//*[text()[contains(., 'Отправить заявку')]]")
            name.send_keys(str(data["test_data_valid"]["name"]))
            phone.send_keys(str(data["test_data_valid"]["phone"]))
            email.send_keys(str(data["test_data_valid"]["email"]))
            time.sleep(1)
            submitBtn.click()
            # проверить, что заявка отправлена, по тому, отобразилась ли надпись "Спасибо за заявку"
            successText = wait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//div[@id='modal-select-content']//p[text()[contains(., 'Спасибо за заявку')]]")))
            print('   OK: заявка из SOW син_33 была отправлена')
            if successText:
                break
        except:
            count += 1
            if count == 3:
                print('ERROR: SOW на син_33: модаль открылась, но заявка не отправлена')
            else:
                driver.refresh()
    except:
        count += 1
        if count == 3:
            print("ERROR: SOW на син_33: не могу нажать кнопку на карточке СП")
        else:
            driver.refresh()


# проверка спецпредложений на син_34
count = 0
driver.get("https://syn34.lp.moigektar.ru/")
while count < 3:
    # проверка, что есть слайдер SOW, по наличию кнопки на карточке
    try:
        title = driver.find_element(by=By.XPATH, value="//h1[text()[contains(.,'Специальное')]]")
        ActionChains(driver).move_to_element(title).send_keys(Keys.PAGE_DOWN).perform()
        print("   ОК: блок SOW на странице син_34 есть")
        btn = driver.find_element(by=By.XPATH, value="//div[@id='catalogueSpecial']/div/div/div/div[1]//li[1]//button")
        actions.move_to_element(btn).click(btn).perform()
        time.sleep(3)
        # проверка, что модаль открыта, по тому, есть ли на странице поле ввода этой модали
        try:
            name = driver.find_element(by=By.XPATH, value="//*[@id='buyconcreteform-name']")
            print('   OK: модаль SOW открылась')
            phone = driver.find_element(by=By.XPATH, value="//*[@name='BuyConcreteForm[phone]']")
            email = driver.find_element(by=By.XPATH, value="//*[@id='buyconcreteform-email']")
            submitBtn = driver.find_element(by=By.XPATH, value="//div[@class='w-modal-description concrete-modal uk-modal uk-open']//*[text()[contains(., 'Отправить заявку')]]")
            name.send_keys(str(data["test_data_valid"]["name"]))
            phone.send_keys(str(data["test_data_valid"]["phone"]))
            email.send_keys(str(data["test_data_valid"]["email"]))
            time.sleep(1)
            submitBtn.click()
            # проверить, что заявка отправлена, по тому, отобразилась ли надпись "Спасибо за заявку"
            successText = wait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//div[@class='w-modal-description concrete-modal uk-modal uk-open']//div[text()[contains(., 'Заявка отправлена')]]")))
            print('   OK: заявка из SOW син_34 была отправлена')
            if successText:
                break
        except:
            count += 1
            if count == 3:
                print('ERROR: SOW на син_34: модаль открылась, но заявка не отправлена')
            else:
                driver.refresh()
    except:
        count += 1
        if count == 3:
            print("ERROR: SOW на син_34: не могу нажать кнопку на карточке СП")
        else:
            driver.refresh()


# проверка спецпредложений на син_37
count = 0
driver.get("https://syn37.lp.moigektar.ru/")
while count < 3:
    # проверка, что есть слайдер SOW, по наличию кнопки на карточке
    try:
        btn = wait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//*[@data-slick-index='0']/div/div/div/div[2]/div[2]/div[2]/button")))
        print("   ОК: блок SOW на странице син_37 есть")
        actions.move_to_element(btn).click(btn).perform()
        time.sleep(3)
        # проверка, что модаль открыта, по тому, есть ли на странице поле ввода этой модали
        try:
            name = driver.find_element(by=By.XPATH, value="//*[@id='buyconcreteform-name']")
            print('   OK: модаль SOW открылась')
            phone = driver.find_element(by=By.XPATH, value="//*[@name='BuyConcreteForm[phone]']")
            email = driver.find_element(by=By.XPATH, value="//*[@id='buyconcreteform-email']")
            submitBtn = driver.find_element(by=By.XPATH, value="//div[@id='special-offer-modal']//*[text()[contains(., 'Отправить заявку')]]")
            name.send_keys(str(data["test_data_valid"]["name"]))
            phone.send_keys(str(data["test_data_valid"]["phone"]))
            email.send_keys(str(data["test_data_valid"]["email"]))
            time.sleep(1)
            submitBtn.click()
            # проверить, что заявка отправлена, по тому, отобразилась ли надпись "Спасибо за заявку"
            successText = wait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//div[@id='special-offer-modal']//p[text()[contains(., 'Спасибо за заявку')]]")))
            print('   OK: заявка из SOW син_37 была отправлена')
            if successText:
                break
        except:
            count += 1
            if count == 3:
                print('ERROR: SOW на син_37: модаль открылась, но заявка не отправлена')
            else:
                driver.refresh()
    except:
        count += 1
        if count == 3:
            print("ERROR: SOW на син_37: не могу нажать кнопку на карточке СП")
        else:
            driver.refresh()


# проверка спецпредложений на син_39
count = 0
driver.get("https://syn39.lp.moigektar.ru/")
while count < 3:
    # проверка, что есть слайдер SOW, по наличию кнопки на карточке
    try:
        title = driver.find_element(by=By.XPATH, value="//h1[text()[contains(.,'Специальное')]]")
        ActionChains(driver).move_to_element(title).send_keys(Keys.PAGE_DOWN).perform()
        print("   ОК: блок SOW на странице син_39 есть")
        btn = driver.find_element(by=By.XPATH, value="//div[@id='catalogueSpecial']/div/div/div/div[1]//li[1]//button")
        actions.move_to_element(btn).click(btn).perform()
        time.sleep(3)
        # проверка, что модаль открыта, по тому, есть ли на странице поле ввода этой модали
        try:
            name = driver.find_element(by=By.XPATH, value="//*[@id='buyconcreteform-name']")
            print('   OK: модаль SOW открылась')
            phone = driver.find_element(by=By.XPATH, value="//*[@name='BuyConcreteForm[phone]']")
            email = driver.find_element(by=By.XPATH, value="//*[@id='buyconcreteform-email']")
            submitBtn = driver.find_element(by=By.XPATH, value="//div[@class='w-modal-description concrete-modal uk-modal uk-open']//*[text()[contains(., 'Отправить заявку')]]")
            name.send_keys(str(data["test_data_valid"]["name"]))
            phone.send_keys(str(data["test_data_valid"]["phone"]))
            email.send_keys(str(data["test_data_valid"]["email"]))
            time.sleep(1)
            submitBtn.click()
            # проверить, что заявка отправлена, по тому, отобразилась ли надпись "Спасибо за заявку"
            successText = wait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//div[@class='w-modal-description concrete-modal uk-modal uk-open']//div[text()[contains(., 'Заявка отправлена')]]")))
            print('   OK: заявка из SOW син_39 была отправлена')
            if successText:
                break
        except:
            count += 1
            if count == 3:
                print('ERROR: SOW на син_39: модаль открылась, но заявка не отправлена')
            else:
                driver.refresh()
    except:
        count += 1
        if count == 3:
            print("ERROR: SOW на син_39: не могу нажать кнопку на карточке СП")
        else:
            driver.refresh()


# проверка спецпредложений на син_42
count = 0
driver.get("https://syn42.lp.moigektar.ru/")
while count < 3:
    # проверка, что есть слайдер SOW, по наличию кнопки на карточке
    try:
        btn = wait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//*[@data-slick-index='0']/div/div/div/div[2]/div[2]/div[2]/button")))
        print("   ОК: блок SOW на странице син_42 есть")
        actions.move_to_element(btn).click(btn).perform()
        time.sleep(3)
        # проверка, что модаль открыта, по тому, есть ли на странице поле ввода этой модали
        try:
            name = driver.find_element(by=By.XPATH, value="//*[@id='buyconcreteform-name']")
            print('   OK: модаль SOW открылась')
            phone = driver.find_element(by=By.XPATH, value="//*[@name='BuyConcreteForm[phone]']")
            email = driver.find_element(by=By.XPATH, value="//*[@id='buyconcreteform-email']")
            submitBtn = driver.find_element(by=By.XPATH, value="//div[@class='w-modal-price']//*[text()[contains(., 'Отправить заявку')]]")
            name.send_keys(str(data["test_data_valid"]["name"]))
            phone.send_keys(str(data["test_data_valid"]["phone"]))
            email.send_keys(str(data["test_data_valid"]["email"]))
            time.sleep(1)
            submitBtn.click()
            # проверить, что заявка отправлена, по тому, отобразилась ли надпись "Спасибо за заявку"
            successText = wait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//div[@class='w-modal-price']//p[text()[contains(., 'Спасибо за заявку')]]")))
            print('   OK: заявка из SOW син_42 была отправлена')
            if successText:
                break
        except:
            count += 1
            if count == 3:
                print('ERROR: SOW на син_42: модаль открылась, но заявка не отправлена')
            else:
                driver.refresh()
    except:
        count += 1
        if count == 3:
            print("ERROR: SOW на син_42: не могу нажать кнопку на карточке СП")
        else:
            driver.refresh()


# проверка спецпредложений на син_53
count = 0
driver.get("https://syn53.lp.moigektar.ru/")
while count < 3:
    # проверка, что есть слайдер SOW, по наличию кнопки на карточке
    try:
        title = driver.find_element(by=By.XPATH, value="//h1[text()[contains(.,'Специальное')]]")
        ActionChains(driver).move_to_element(title).send_keys(Keys.PAGE_DOWN).perform()
        print("   ОК: блок SOW на странице син_53 есть")
        btn = driver.find_element(by=By.XPATH, value="//div[@id='catalogueSpecial']/div/div/div/div[1]//li[1]//button")
        actions.move_to_element(btn).click(btn).perform()
        time.sleep(3)
        # проверка, что модаль открыта, по тому, есть ли на странице поле ввода этой модали
        try:
            name = driver.find_element(by=By.XPATH, value="//*[@id='buyconcreteform-name']")
            print('   OK: модаль SOW открылась')
            phone = driver.find_element(by=By.XPATH, value="//*[@name='BuyConcreteForm[phone]']")
            email = driver.find_element(by=By.XPATH, value="//*[@id='buyconcreteform-email']")
            submitBtn = driver.find_element(by=By.XPATH, value="//div[@class='w-modal-description concrete-modal uk-modal uk-open']//*[text()[contains(., 'Отправить заявку')]]")
            name.send_keys(str(data["test_data_valid"]["name"]))
            phone.send_keys(str(data["test_data_valid"]["phone"]))
            email.send_keys(str(data["test_data_valid"]["email"]))
            time.sleep(1)
            submitBtn.click()
            # проверить, что заявка отправлена, по тому, отобразилась ли надпись "Спасибо за заявку"
            successText = wait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//div[@class='w-modal-description concrete-modal uk-modal uk-open']//div[text()[contains(., 'Заявка отправлена')]]")))
            print('   OK: заявка из SOW син_53 была отправлена')
            if successText:
                break
        except:
            count += 1
            if count == 3:
                print('ERROR: SOW на син_53: модаль открылась, но заявка не отправлена')
            else:
                driver.refresh()
    except:
        count += 1
        if count == 3:
            print("ERROR: SOW на син_53: не могу нажать кнопку на карточке СП")
        else:
            driver.refresh()


# # 11. проверка спецпредложений на vazuza2
# driver.get("https://vazuza2.lp.moigektar.ru/")
# # 11.1 так как на вазузе нет слайдера SOW, буду вызывать карточки SOW с Генплана // так и не смог добиться чтобы работало
# # в хедлесс нажимает не туда, а в обычном режиме работает, как задумано
# try:
#     title = driver.find_element(by=By.XPATH, value="//div[text()[contains(.,'Генеральный')]]")
#     actions.move_to_element(title).perform()
#     actions.send_keys(Keys.PAGE_DOWN).perform()
#     time.sleep(3)
#     driver.find_element(by=By.XPATH, value='//img[@data-src="/img/vazuza/select/overlay-touch.png"]').click()
#     print("   ОК: генплан на Вазузе присутствует")
#     time.sleep(14)
#     # клик в центр общего большого элемента. После этого станет возможно нажимать непосредственно на точки на плане
#     driver.find_element(by=By.CLASS_NAME, value='ymaps-2-1-79-events-pane').click()
#     time.sleep(4)
#     # в хедлесс клик в эту область попадает на шар, поэтому надо сместиться
#     actions.send_keys(Keys.ARROW_UP).perform()
#     actions.click()
#     # 11.2 проверка, что модаль открыта, по тому, есть ли на странице поле ввода этой модали
#     try:
#         name = wait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//*[@id='buyconcreteform-name']")))
#         print('   OK: модаль SOW открылась')
#         phone = driver.find_element(by=By.XPATH, value="//*[@name='BuyConcreteForm[phone]']")
#         email = driver.find_element(by=By.XPATH, value="//*[@id='buyconcreteform-email']")
#         time.sleep(1)
#         submitBtn = driver.find_element(by=By.XPATH, value="//div[@class='concrete-modal uk-modal uk-open']//ul[@class='uk-switcher']//button[@type='submit']")
#         time.sleep(1)
#         name.send_keys(str(data["test_data_valid"]["name"]))
#         time.sleep(1)
#         phone.send_keys(str(data["test_data_valid"]["phone"]))
#         time.sleep(1)
#         email.send_keys(str(data["test_data_valid"]["email"]))
#         time.sleep(2)
#         submitBtn.click()
#         # 11.3 проверить, что заявка отправлена, по тому, отобразилась ли надпись "Спасибо за заявку"
#         driver.implicitly_wait(10)
#         try:
#             successText = wait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[@class='concrete-modal uk-modal uk-open']//div[text()[contains(., 'Заявка отправлена')]]")))
#             print('   OK: заявка из SOW на Вазузе была отправлена')
#         except TimeoutException:
#             try:
#                 failText = wait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[@class='concrete-modal uk-modal uk-open']//div[text()[contains(., 'Произошла ошибка')]]")))
#                 print('ERROR: заявка из SOW на Вазузе не была отправлена и отобразилось сообщение об ошибке отправки')
#             except TimeoutException:
#                 print('ERROR: заявка из SOW на Вазузе не была отправлена')
#     except ElementNotVisibleException:
#         print("ERROR: модаль SOW на Вазузе не открылась")
# except TimeoutException:
#     print("ERROR: не могу найти кнопку, чтобы открыть модаль SOW на Вазузе")
# except:
#     print("ERROR: что-то не так при проверке работы SOW на Вазузе")


# проверка спецпредложений на син_67
# count = 0
# driver.get("https://syn67.lp.moigektar.ru/")
# while count < 3:
#     # проверка, что есть слайдер SOW, по наличию кнопки на карточке
#     try:
#         title = driver.find_element(by=By.XPATH, value="//h1[text()[contains(.,'Специальное')]]")
#         ActionChains(driver).move_to_element(title).send_keys(Keys.PAGE_DOWN).perform()
#         print("   ОК: блок SOW на странице син_67 есть")
#         btn = driver.find_element(by=By.XPATH, value="//div[@id='catalogueSpecial']/div/div/div/div[1]//li[1]//button")
#         actions.move_to_element(btn).click(btn).perform()
#         time.sleep(3)
#         # проверка, что модаль открыта, по тому, есть ли на странице поле ввода этой модали
#         try:
#             name = driver.find_element(by=By.XPATH, value="//*[@id='buyconcreteform-name']")
#             print('   OK: модаль SOW открылась')
#             phone = driver.find_element(by=By.XPATH, value="//*[@name='BuyConcreteForm[phone]']")
#             email = driver.find_element(by=By.XPATH, value="//*[@id='buyconcreteform-email']")
#             submitBtn = driver.find_element(by=By.XPATH, value="//div[@class='w-modal-description concrete-modal uk-modal uk-open']//*[text()[contains(., 'Отправить заявку')]]")
#             name.send_keys(str(data["test_data_valid"]["name"]))
#             phone.send_keys(str(data["test_data_valid"]["phone"]))
#             email.send_keys(str(data["test_data_valid"]["email"]))
#             time.sleep(1)
#             submitBtn.click()
#             # проверить, что заявка отправлена, по тому, отобразилась ли надпись "Спасибо за заявку"
#             successText = wait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//div[@class='w-modal-description concrete-modal uk-modal uk-open']//div[text()[contains(., 'Заявка отправлена')]]")))
#             print('   OK: заявка из SOW син_67 была отправлена')
#             if successText:
#                 break
#         except:
#             count += 1
#             if count == 3:
#                 print('ERROR: SOW на син_67: модаль открылась, но заявка не отправлена')
#             else:
#                 driver.refresh()
#     except:
#         count += 1
#         if count == 3:
#             print("ERROR: SOW на син_67: не могу нажать кнопку на карточке СП")
#         else:
#             driver.refresh()


# проверка спецпредложений на син_84
count = 0
driver.get("https://syn84.lp.moigektar.ru/")
while count < 3:
    # проверка, что есть слайдер SOW, по наличию кнопки на карточке
    try:
        title = driver.find_element(by=By.XPATH, value="//h1[text()[contains(.,'Специальное')]]")
        ActionChains(driver).move_to_element(title).send_keys(Keys.PAGE_DOWN).perform()
        print("   ОК: блок SOW на странице син_84 есть")
        btn = driver.find_element(by=By.XPATH, value="//div[@id='catalogueSpecial']/div/div/div/div[1]//li[1]//button")
        actions.move_to_element(btn).click(btn).perform()
        time.sleep(3)
        # проверка, что модаль открыта, по тому, есть ли на странице поле ввода этой модали
        try:
            name = driver.find_element(by=By.XPATH, value="//*[@id='buyconcreteform-name']")
            print('   OK: модаль SOW открылась')
            phone = driver.find_element(by=By.XPATH, value="//*[@name='BuyConcreteForm[phone]']")
            email = driver.find_element(by=By.XPATH, value="//*[@id='buyconcreteform-email']")
            submitBtn = driver.find_element(by=By.XPATH, value="//div[@class='w-modal-description concrete-modal uk-modal uk-open']//*[text()[contains(., 'Отправить заявку')]]")
            name.send_keys(str(data["test_data_valid"]["name"]))
            phone.send_keys(str(data["test_data_valid"]["phone"]))
            email.send_keys(str(data["test_data_valid"]["email"]))
            time.sleep(1)
            submitBtn.click()
            # проверить, что заявка отправлена, по тому, отобразилась ли надпись "Спасибо за заявку"
            successText = wait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//div[@class='w-modal-description concrete-modal uk-modal uk-open']//div[text()[contains(., 'Заявка отправлена')]]")))
            print('   OK: заявка из SOW син_84 была отправлена')
            if successText:
                break
        except:
            count += 1
            if count == 3:
                print('ERROR: SOW на син_84: модаль открылась, но заявка не отправлена')
            else:
                driver.refresh()
    except:
        count += 1
        if count == 3:
            print("ERROR: SOW на син_84: не могу нажать кнопку на карточке СП")
        else:
            driver.refresh()


# проверка спецпредложений на син_85
count = 0
driver.get("https://syn85.lp.moigektar.ru/")
while count < 3:
    # проверка, что есть слайдер SOW, по наличию кнопки на карточке
    try:
        title = driver.find_element(by=By.XPATH, value="//h1[text()[contains(.,'Специальное')]]")
        ActionChains(driver).move_to_element(title).send_keys(Keys.PAGE_DOWN).perform()
        print("   ОК: блок SOW на странице син_85 есть")
        btn = driver.find_element(by=By.XPATH, value="//div[@id='catalogueSpecial']/div/div/div/div[1]//li[1]//button")
        actions.move_to_element(btn).click(btn).perform()
        time.sleep(3)
        # проверка, что модаль открыта, по тому, есть ли на странице поле ввода этой модали
        try:
            name = driver.find_element(by=By.XPATH, value="//*[@id='buyconcreteform-name']")
            print('   OK: модаль SOW открылась')
            phone = driver.find_element(by=By.XPATH, value="//*[@name='BuyConcreteForm[phone]']")
            email = driver.find_element(by=By.XPATH, value="//*[@id='buyconcreteform-email']")
            submitBtn = driver.find_element(by=By.XPATH, value="//div[@class='w-modal-description concrete-modal uk-modal uk-open']//*[text()[contains(., 'Отправить заявку')]]")
            name.send_keys(str(data["test_data_valid"]["name"]))
            phone.send_keys(str(data["test_data_valid"]["phone"]))
            email.send_keys(str(data["test_data_valid"]["email"]))
            time.sleep(1)
            submitBtn.click()
            # проверить, что заявка отправлена, по тому, отобразилась ли надпись "Спасибо за заявку"
            successText = wait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//div[@class='w-modal-description concrete-modal uk-modal uk-open']//div[text()[contains(., 'Заявка отправлена')]]")))
            print('   OK: заявка из SOW син_85 была отправлена')
            if successText:
                break
        except:
            count += 1
            if count == 3:
                print('ERROR: SOW на син_85: модаль открылась, но заявка не отправлена')
            else:
                driver.refresh()
    except:
        count += 1
        if count == 3:
            print("ERROR: SOW на син_85: не могу нажать кнопку на карточке СП")
        else:
            driver.refresh()


# проверка спецпредложений на син_87
count = 0
driver.get("https://syn87.lp.moigektar.ru/")
while count < 3:
    # проверка, что есть слайдер SOW, по наличию кнопки на карточке
    try:
        title = driver.find_element(by=By.XPATH, value="//h1[text()[contains(.,'Специальное')]]")
        ActionChains(driver).move_to_element(title).send_keys(Keys.PAGE_DOWN).perform()
        print("   ОК: блок SOW на странице син_87 есть")
        btn = driver.find_element(by=By.XPATH, value="//div[@id='catalogueSpecial']/div/div/div/div[1]//li[1]//button")
        actions.move_to_element(btn).click(btn).perform()
        time.sleep(3)
        # проверка, что модаль открыта, по тому, есть ли на странице поле ввода этой модали
        try:
            name = driver.find_element(by=By.XPATH, value="//*[@id='buyconcreteform-name']")
            print('   OK: модаль SOW открылась')
            phone = driver.find_element(by=By.XPATH, value="//*[@name='BuyConcreteForm[phone]']")
            email = driver.find_element(by=By.XPATH, value="//*[@id='buyconcreteform-email']")
            submitBtn = driver.find_element(by=By.XPATH, value="//div[@class='w-modal-description concrete-modal uk-modal uk-open']//*[text()[contains(., 'Отправить заявку')]]")
            name.send_keys(str(data["test_data_valid"]["name"]))
            phone.send_keys(str(data["test_data_valid"]["phone"]))
            email.send_keys(str(data["test_data_valid"]["email"]))
            time.sleep(1)
            submitBtn.click()
            # проверить, что заявка отправлена, по тому, отобразилась ли надпись "Спасибо за заявку"
            successText = wait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//div[@class='w-modal-description concrete-modal uk-modal uk-open']//div[text()[contains(., 'Заявка отправлена')]]")))
            print('   OK: заявка из SOW син_87 была отправлена')
            if successText:
                break
        except:
            count += 1
            if count == 3:
                print('ERROR: SOW на син_87: модаль открылась, но заявка не отправлена')
            else:
                driver.refresh()
    except:
        count += 1
        if count == 3:
            print("ERROR: SOW на син_87: не могу нажать кнопку на карточке СП")
        else:
            driver.refresh()


# проверка спецпредложений на син_89
count = 0
driver.get("https://syn89.lp.moigektar.ru/")
while count < 3:
    # проверка, что есть слайдер SOW, по наличию кнопки на карточке
    try:
        title = driver.find_element(by=By.XPATH, value="//h1[text()[contains(.,'Специальное')]]")
        ActionChains(driver).move_to_element(title).send_keys(Keys.PAGE_DOWN).perform()
        print("   ОК: блок SOW на странице син_89 есть")
        btn = driver.find_element(by=By.XPATH, value="//div[@id='catalogueSpecial']/div/div/div/div[1]//li[1]//button")
        actions.move_to_element(btn).click(btn).perform()
        time.sleep(3)
        # проверка, что модаль открыта, по тому, есть ли на странице поле ввода этой модали
        try:
            name = driver.find_element(by=By.XPATH, value="//*[@id='buyconcreteform-name']")
            print('   OK: модаль SOW открылась')
            phone = driver.find_element(by=By.XPATH, value="//*[@name='BuyConcreteForm[phone]']")
            email = driver.find_element(by=By.XPATH, value="//*[@id='buyconcreteform-email']")
            submitBtn = driver.find_element(by=By.XPATH, value="//div[@class='w-modal-description concrete-modal uk-modal uk-open']//*[text()[contains(., 'Отправить заявку')]]")
            name.send_keys(str(data["test_data_valid"]["name"]))
            phone.send_keys(str(data["test_data_valid"]["phone"]))
            email.send_keys(str(data["test_data_valid"]["email"]))
            time.sleep(1)
            submitBtn.click()
            # проверить, что заявка отправлена, по тому, отобразилась ли надпись "Спасибо за заявку"
            successText = wait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//div[@class='w-modal-description concrete-modal uk-modal uk-open']//div[text()[contains(., 'Заявка отправлена')]]")))
            print('   OK: заявка из SOW син_89 была отправлена')
            if successText:
                break
        except:
            count += 1
            if count == 3:
                print('ERROR: SOW на син_89: модаль открылась, но заявка не отправлена')
            else:
                driver.refresh()
    except:
        count += 1
        if count == 3:
            print("ERROR: SOW на син_89: не могу нажать кнопку на карточке СП")
        else:
            driver.refresh()

# проверка спецпредложений на син_92
count = 0
driver.get("http://syn92.lp.moigektar.ru/")
while count < 3:
    # проверка, что есть слайдер SOW, по наличию кнопки на карточке
    try:
        title = driver.find_element(by=By.XPATH, value="//h1[text()[contains(.,'Специальное')]]")
        ActionChains(driver).move_to_element(title).send_keys(Keys.PAGE_DOWN).perform()
        print("   ОК: блок SOW на странице син_92 есть")
        btn = driver.find_element(by=By.XPATH, value="//div[@id='catalogueSpecial']/div/div/div/div[1]//li[1]//button")
        actions.move_to_element(btn).click(btn).perform()
        time.sleep(3)
        # проверка, что модаль открыта, по тому, есть ли на странице поле ввода этой модали
        try:
            name = driver.find_element(by=By.XPATH, value="//*[@id='buyconcreteform-name']")
            print('   OK: модаль SOW открылась')
            phone = driver.find_element(by=By.XPATH, value="//*[@name='BuyConcreteForm[phone]']")
            email = driver.find_element(by=By.XPATH, value="//*[@id='buyconcreteform-email']")
            submitBtn = driver.find_element(by=By.XPATH, value="//div[@class='w-modal-description concrete-modal uk-modal uk-open']//*[text()[contains(., 'Отправить заявку')]]")
            name.send_keys(str(data["test_data_valid"]["name"]))
            phone.send_keys(str(data["test_data_valid"]["phone"]))
            email.send_keys(str(data["test_data_valid"]["email"]))
            time.sleep(1)
            submitBtn.click()
            # проверить, что заявка отправлена, по тому, отобразилась ли надпись "Спасибо за заявку"
            successText = wait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//div[@class='w-modal-description concrete-modal uk-modal uk-open']//div[text()[contains(., 'Заявка отправлена')]]")))
            print('   OK: заявка из SOW син_92 была отправлена')
            if successText:
                break
        except:
            count += 1
            if count == 3:
                print('ERROR: SOW на син_92: модаль открылась, но заявка не отправлена')
            else:
                driver.refresh()
    except:
        count += 1
        if count == 3:
            print("ERROR: SOW на син_92: не могу нажать кнопку на карточке СП")
        else:
            driver.refresh()


time.sleep(1)
driver.quit()

