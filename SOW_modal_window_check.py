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


# Скрипт открывает окна СП и проверяет, что они открылись
#
# В лог выводится сообщение "ОК", если окно было открыто
# В лог выводится сообщение "ERROR", если окно не было открыто
# В лог выводится сообщение "ERROR" если элемент, открывающий окно, не был найден по селектору


# 1. проверка слайдера СП на главной странице "МГ"
driver.get("https://moigektar.ru/")
# 1.1 проверка, что есть кнопка на карточке участка в блоке "Специальное предложение"
try:
    title = wait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//h1[text()[contains(.,'Специальное')]]")))
    actions.move_to_element(title).send_keys(Keys.PAGE_DOWN).perform()
    print("   ОК: блок СП на главной МГ есть")
    time.sleep(10)
    btn = driver.find_element(by=By.XPATH, value="//div[@id='catalogueSpecial']/div/div/div/div[1]//li[1]//button")
    actions.move_to_element(btn).click().perform()
    # 1.2 проверка, что модаль открыта, по тому, есть ли на странице поле ввода этой модали
    try:
        name = wait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//div[(contains(@class, 'w-modal-description'))]//input[@id='consultationform-name']")))
        print('   OK: модаль СП на главной МГ открылась')
        phone = driver.find_element(by=By.XPATH, value="//div[@class='w-modal-description uk-modal uk-open']//input[@id='consultationform-phone']")
        email = driver.find_element(by=By.XPATH, value="//div[@class='w-modal-description uk-modal uk-open']//input[@id='consultationform-email']")
        submitBtn = driver.find_element(by=By.XPATH, value="//div[@class='w-modal-description uk-modal uk-open']//button[@type='submit']")
        time.sleep(1)
        name.send_keys('test')
        time.sleep(1)
        phone.send_keys('9127777777')
        time.sleep(1)
        email.send_keys('test@test.test')
        time.sleep(1)
        submitBtn.click()
        # 1.3 проверить, что заявка отправлена, по тому, отобразилась ли надпись "Выберите дату визита"
        driver.implicitly_wait(10)
        try:
            successText = wait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[text()[contains(.,'Выберите дату визита')]]")))
            print('   OK: заявка была отправлена')
            time.sleep(3)
            driver.find_element(by=By.XPATH, value="//div[@class='w-modal-description uk-modal uk-open']/div/div/button").click()
        except TimeoutException:
            try:
                failText = wait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[@class='w-modal-description uk-modal uk-open']//div[text()[contains(.,'Во время отправки заявки возникли сложности')]]")))
                print('ERROR: заявка из СП на главной МГ не была отправлена и отобразилось сообщение об ошибке отправки')
                driver.find_element(by=By.XPATH, value="//div[@class='w-modal-description uk-modal uk-open']/div/div/button").click()
            except TimeoutException:
                print('ERROR: заявка из СП на главной МГ не была отправлена')
                driver.find_element(by=By.XPATH, value="//div[@class='w-modal-description uk-modal uk-open']/div/div/button").click()
    except ElementNotVisibleException:
        print("ERROR: модаль из СП на главной МГ не открылась")
except TimeoutException:
    print("ERROR: не могу найти кнопку, чтобы открыть модаль СП на главной МГ")
except:
    print("ERROR: что-то не так при проверке работы СП на главной МГ")


# 2. проверка слайдера СП в каталоге "МГ"
driver.get("https://moigektar.ru/catalogue")
# 2.1 проверка, что есть кнопка на карточке участка в блоке "Тотальная распродажа"/"Специальное предложение"
try:
    btn = wait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//*[text()[contains(., 'Специальное предложение')]]//parent::div//div[@uk-slider='sets: true']//li[1]//div/button/span")))
    print("   ОК: блок СП в каталоге есть")
    time.sleep(10)
    actions.move_to_element(btn).click(btn).perform()
    # 2.2 проверка, что модаль открыта, по тому, есть ли на странице поле ввода этой модали
    try:
        name = wait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//div[(contains(@class, 'w-modal-description'))]//input[@id='consultationform-name']")))
        print('   OK: модаль СП в каталоге открылась')
        phone = driver.find_element(by=By.XPATH, value="//div[@class='w-modal-description uk-modal uk-open']//input[@id='consultationform-phone']")
        email = driver.find_element(by=By.XPATH, value="//div[@class='w-modal-description uk-modal uk-open']//input[@id='consultationform-email']")
        submitBtn = driver.find_element(by=By.XPATH, value="//div[@class='w-modal-description uk-modal uk-open']//button[@type='submit']")
        time.sleep(1)
        name.send_keys('test')
        time.sleep(1)
        phone.send_keys('9127777777')
        time.sleep(1)
        email.send_keys('test@test.test')
        time.sleep(1)
        submitBtn.click()
        # 2.3 проверить, что заявка отправлена, по тому, открылась ли страница благодарности
        time.sleep(10)
        url = driver.current_url
        if url == 'https://moigektar.ru/thanks':
            print('   OK: заявка из СП в каталоге отправлена, открылась страница благодарности')
        else:
            try:
                failText = wait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[@class='w-modal-description uk-modal uk-open']//div[text()[contains(.,'Во время отправки заявки возникли сложности')]]")))
                print('ERROR: заявка из СП каталога не была отправлена и отобразилось сообщение об ошибке отправки')
            except TimeoutException:
                print('ERROR: заявка из СП каталога не была отправлена')
    except ElementNotVisibleException:
        print("ERROR:  модаль из СП каталога не открылась")
except TimeoutException:
    print("ERROR: не могу найти кнопку, чтобы открыть модаль СП в каталоге")
except:
    print("ERROR: что-то не так при проверке работы СП в каталоге")


# 3. проверка слайдера дачных участков в каталоге "МГ"
# 3.1 проверка, что есть кнопка на карточке участка в блоке "Дачные участки"
driver.get("https://moigektar.ru/catalogue")
try:
    title = driver.find_element(by=By.XPATH, value="//h1[text()[contains(., 'Дачные участки')]]")
    actions.move_to_element(title).send_keys(Keys.PAGE_DOWN).send_keys(Keys.ARROW_DOWN).perform()
    print("   ОК: блок СП дачные участки на странице есть")
    time.sleep(10)
    btn = driver.find_element(by=By.XPATH, value="//h1[text()[contains(., 'Дачные участки')]]//parent::div//div[1]/div/div//li[1]//button/span")
    actions.move_to_element(btn).click().perform()
    # 3.2 проверка, что модаль открыта, по тому, есть ли на странице поле ввода этой модали
    try:
        name = wait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//div[@class='w-modal-description uk-modal uk-open']//input[@id='consultationform-name']")))
        print('   OK: модаль СП дачных участков открылась')
        phone = driver.find_element(by=By.XPATH, value="//div[@class='w-modal-description uk-modal uk-open']//input[@id='consultationform-phone']")
        email = driver.find_element(by=By.XPATH, value="//div[@class='w-modal-description uk-modal uk-open']//input[@id='consultationform-email']")
        submitBtn = driver.find_element(by=By.XPATH, value="//div[@class='w-modal-description uk-modal uk-open']//button[@type='submit']")
        time.sleep(1)
        name.send_keys('test')
        time.sleep(1)
        phone.send_keys('9127777777')
        time.sleep(1)
        email.send_keys('test@test.test')
        time.sleep(1)
        submitBtn.click()
        # 3.3 проверить, что заявка отправлена, по тому, открылась ли страница благодарности
        time.sleep(10)
        url = driver.current_url
        if url == 'https://moigektar.ru/thanks':
            print('   OK: заявка из СП дачных участков отправлена, открылась страница благодарности')
        else:
            try:
                failText = wait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[@class='w-modal-description uk-modal uk-open']//div[text()[contains(.,'Во время отправки заявки возникли сложности')]]")))
                print('ERROR: заявка из СП дачных участков не была отправлена и отобразилось сообщение об ошибке отправки')
            except TimeoutException:
                print('ERROR: заявка из СП дачных участков не была отправлена')
    except ElementNotVisibleException:
        print("ERROR: модаль СП из дачных участков не открылась")
except TimeoutException:
    print("ERROR: не могу найти кнопку, чтобы открыть модаль СП в дачных участках каталога МГ")
except:
    print("ERROR: что-то не так при проверке работы СП в дачных участках каталога МГ")


# 4. проверка спецпредложений на син_9
# driver.get("https://syn9.lp.moigektar.ru/")
# # 4.1 проверка, что есть слайдер СП, по наличию кнопки на карточке
# try:
#     btn = wait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//*[@id='price']//div[2]//div[1]/div/div/div/div[2]/div[2]/div[2]/button")))
#     print("   ОК  4.1: блок СП на странице есть")
#     driver.implicitly_wait(10)
#     actions.move_to_element(btn).click(btn).perform()
#     # 4.2 проверка, что модаль открыта, по тому, есть ли на странице поле ввода этой модали
#     try:
#         name = wait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//*[@id='buyconcreteform-name']")))
#         print('   OK  4.2: модаль СП на син_9 открылась')
#     except ElementNotVisibleException:
#         print("ERROR:  4.2 модаль СП на син_9 не открылась")
# except TimeoutException:
#     print("ERROR:  4.1 не могу найти кнопку, чтобы открыть модаль СП на син_9")


# 5. проверка спецпредложений на син_33
driver.get("https://syn33.lp.moigektar.ru/")
# 5.1 проверка, что есть слайдер СП, по наличию кнопки на карточке
try:
    btn = wait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//*[@data-slick-index='0']/div/div/div/div[2]/div[2]/div[2]/button")))
    print("   ОК: блок СП на странице син_33 есть")
    driver.implicitly_wait(10)
    actions.move_to_element(btn).click(btn).perform()
    # 5.2 проверка, что модаль открыта, по тому, есть ли на странице поле ввода этой модали
    try:
        name = wait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//*[@id='buyconcreteform-name']")))
        print('   OK: модаль СП открылась')
        phone = driver.find_element(by=By.XPATH, value="//*[@name='BuyConcreteForm[phone]']")
        email = driver.find_element(by=By.XPATH, value="//*[@id='buyconcreteform-email']")
        submitBtn = driver.find_element(by=By.XPATH, value="//div[@id='modal-select-content']//*[text()[contains(., 'Отправить заявку')]]")
        time.sleep(1)
        name.send_keys('test')
        time.sleep(1)
        phone.send_keys('9127777777')
        time.sleep(1)
        email.send_keys('test@test.test')
        time.sleep(1)
        submitBtn.click()
        # 5.3 проверить, что заявка отправлена, по тому, отобразилась ли надпись "Спасибо за заявку"
        driver.implicitly_wait(10)
        try:
            successText = wait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[@id='modal-select-content']//p[text()[contains(., 'Спасибо за заявку')]]")))
            print('   OK: заявка из СП син_33 была отправлена')
        except TimeoutException:
            try:
                failText = wait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[@id='modal-select-content']//div[text()[contains(., 'Произошла ошибка')]]")))
                print('ERROR: заявка из СП на син_33 не была отправлена и отобразилось сообщение об ошибке отправки')
            except TimeoutException:
                print('ERROR: заявка из СП на син_33 не была отправлена')
    except ElementNotVisibleException:
        print("ERROR: модаль СП на син_33 не открылась")
except TimeoutException:
    print("ERROR: не могу найти кнопку, чтобы открыть модаль СП на син_33")
except:
    print("ERROR: что-то не так при проверке работы СП на син_33")


# 6. проверка спецпредложений на син_34
driver.get("https://syn34.lp.moigektar.ru/")
# 6.1 проверка, что есть слайдер СП, по наличию кнопки на карточке
try:
    btn = wait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//*[@data-slick-index='0']/div/div/div/div[2]/div[2]/div[2]/button")))
    print("   ОК: блок СП на странице син_34 есть")
    driver.implicitly_wait(10)
    actions.move_to_element(btn).click(btn).perform()
    # 6.2 проверка, что модаль открыта, по тому, есть ли на странице поле ввода этой модали
    try:
        name = wait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//*[@id='buyconcreteform-name']")))
        print('   OK: модаль СП открылась')
        phone = driver.find_element(by=By.XPATH, value="//*[@name='BuyConcreteForm[phone]']")
        email = driver.find_element(by=By.XPATH, value="//*[@id='buyconcreteform-email']")
        submitBtn = driver.find_element(by=By.XPATH, value="//div[@id='special-offer-modal']//*[text()[contains(., 'Отправить заявку')]]")
        time.sleep(1)
        name.send_keys('test')
        time.sleep(1)
        phone.send_keys('9127777777')
        time.sleep(1)
        email.send_keys('test@test.test')
        time.sleep(1)
        submitBtn.click()
        # 6.3 проверить, что заявка отправлена, по тому, отобразилась ли надпись "Спасибо за заявку"
        driver.implicitly_wait(10)
        try:
            successText = wait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[@id='special-offer-modal']//p[text()[contains(., 'Спасибо за заявку')]]")))
            print('   OK: заявка из СП син_34 была отправлена')
        except TimeoutException:
            try:
                failText = wait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[@id='special-offer-modal']//div[text()[contains(., 'Произошла ошибка')]]")))
                print('ERROR: заявка из СП на син_34 не была отправлена и отобразилось сообщение об ошибке отправки')
            except TimeoutException:
                print('ERROR: заявка из СП на син_34 не была отправлена')
    except ElementNotVisibleException:
        print("ERROR: модаль СП на син_34 не открылась")
except TimeoutException:
    print("ERROR: не могу найти кнопку, чтобы открыть модаль СП на син_34")
except:
    print("ERROR: что-то не так при проверке работы СП на син_34")


# 7. проверка спецпредложений на син_37
driver.get("https://syn37.lp.moigektar.ru/")
# 7.1 проверка, что есть слайдер СП, по наличию кнопки на карточке
try:
    btn = wait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//*[@data-slick-index='0']/div/div/div/div[2]/div[2]/div[2]/button")))
    print("   ОК: блок СП на странице син_37 есть")
    driver.implicitly_wait(10)
    actions.move_to_element(btn).click(btn).perform()
    # 6.2 проверка, что модаль открыта, по тому, есть ли на странице поле ввода этой модали
    try:
        name = wait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//*[@id='buyconcreteform-name']")))
        print('   OK: модаль СП открылась')
        phone = driver.find_element(by=By.XPATH, value="//*[@name='BuyConcreteForm[phone]']")
        email = driver.find_element(by=By.XPATH, value="//*[@id='buyconcreteform-email']")
        submitBtn = driver.find_element(by=By.XPATH, value="//div[@id='special-offer-modal']//*[text()[contains(., 'Отправить заявку')]]")
        time.sleep(1)
        name.send_keys('test')
        time.sleep(1)
        phone.send_keys('9127777777')
        time.sleep(1)
        email.send_keys('test@test.test')
        time.sleep(1)
        submitBtn.click()
        # 6.3 проверить, что заявка отправлена, по тому, отобразилась ли надпись "Спасибо за заявку"
        driver.implicitly_wait(10)
        try:
            successText = wait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[@id='special-offer-modal']//p[text()[contains(., 'Спасибо за заявку')]]")))
            print('   OK: заявка из СП син_37 была отправлена')
        except TimeoutException:
            try:
                failText = wait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[@id='special-offer-modal']//div[text()[contains(., 'Произошла ошибка')]]")))
                print('ERROR: заявка из СП на син_37 не была отправлена и отобразилось сообщение об ошибке отправки')
            except TimeoutException:
                print('ERROR: заявка из СП на син_37 не была отправлена')
    except ElementNotVisibleException:
        print("ERROR: модаль СП на син_37 не открылась")
except TimeoutException:
    print("ERROR: не могу найти кнопку, чтобы открыть модаль СП на син_37")
except:
    print("ERROR: что-то не так при проверке работы СП на син_37")


# 8. проверка спецпредложений на син_39
driver.get("https://syn39.lp.moigektar.ru/")
# 8.1 проверка, что есть слайдер СП, по наличию кнопки на карточке
try:
    btn = wait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//*[@data-slick-index='0']/div/div/div/div[2]/div[2]/div[2]/button")))
    print("   ОК: блок СП на странице син_39 есть")
    driver.implicitly_wait(10)
    actions.move_to_element(btn).click(btn).perform()
    # 8.2 проверка, что модаль открыта, по тому, есть ли на странице поле ввода этой модали
    try:
        name = wait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//*[@id='buyconcreteform-name']")))
        print('   OK: модаль СП открылась')
        phone = driver.find_element(by=By.XPATH, value="//*[@name='BuyConcreteForm[phone]']")
        email = driver.find_element(by=By.XPATH, value="//*[@id='buyconcreteform-email']")
        submitBtn = driver.find_element(by=By.XPATH, value="//div[@class='w-modal-price']//*[text()[contains(., 'Отправить заявку')]]")
        time.sleep(1)
        name.send_keys('test')
        time.sleep(1)
        phone.send_keys('9127777777')
        time.sleep(1)
        email.send_keys('test@test.test')
        time.sleep(1)
        submitBtn.click()
        # 6.3 проверить, что заявка отправлена, по тому, отобразилась ли надпись "Спасибо за заявку"
        driver.implicitly_wait(10)
        try:
            successText = wait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[@class='w-modal-price']//p[text()[contains(., 'Спасибо за заявку')]]")))
            print('   OK: заявка из СП син_39 была отправлена')
        except TimeoutException:
            try:
                failText = wait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[@class='w-modal-price']//div[text()[contains(., 'Произошла ошибка')]]")))
                print('ERROR: заявка из СП на син_39 не была отправлена и отобразилось сообщение об ошибке отправки')
            except TimeoutException:
                print('ERROR: заявка из СП на син_39 не была отправлена')
    except ElementNotVisibleException:
        print("ERROR: модаль СП на син_39 не открылась")
except TimeoutException:
    print("ERROR: не могу найти кнопку, чтобы открыть модаль СП на син_39")
except:
    print("ERROR: что-то не так при проверке работы СП на син_39")


# 9. проверка спецпредложений на син_42
driver.get("https://syn42.lp.moigektar.ru/")
# 9.1 проверка, что есть слайдер СП, по наличию кнопки на карточке
try:
    btn = wait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//*[@data-slick-index='0']/div/div/div/div[2]/div[2]/div[2]/button")))
    print("   ОК: блок СП на странице син_42 есть")
    driver.implicitly_wait(10)
    actions.move_to_element(btn).click(btn).perform()
    # 9.2 проверка, что модаль открыта, по тому, есть ли на странице поле ввода этой модали
    try:
        name = wait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//*[@id='buyconcreteform-name']")))
        print('   OK: модаль СП открылась')
        phone = driver.find_element(by=By.XPATH, value="//*[@name='BuyConcreteForm[phone]']")
        email = driver.find_element(by=By.XPATH, value="//*[@id='buyconcreteform-email']")
        submitBtn = driver.find_element(by=By.XPATH, value="//div[@class='w-modal-price']//*[text()[contains(., 'Отправить заявку')]]")
        time.sleep(1)
        name.send_keys('test')
        time.sleep(1)
        phone.send_keys('9127777777')
        time.sleep(1)
        email.send_keys('test@test.test')
        time.sleep(1)
        submitBtn.click()
        # 6.3 проверить, что заявка отправлена, по тому, отобразилась ли надпись "Спасибо за заявку"
        driver.implicitly_wait(10)
        try:
            successText = wait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[@class='w-modal-price']//p[text()[contains(., 'Спасибо за заявку')]]")))
            print('   OK: заявка из СП син_42 была отправлена')
        except TimeoutException:
            try:
                failText = wait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[@class='w-modal-price']//div[text()[contains(., 'Произошла ошибка')]]")))
                print('ERROR: заявка из СП на син_42 не была отправлена и отобразилось сообщение об ошибке отправки')
            except TimeoutException:
                print('ERROR: заявка из СП на син_42 не была отправлена')
    except ElementNotVisibleException:
        print("ERROR: модаль СП на син_42 не открылась")
except TimeoutException:
    print("ERROR: не могу найти кнопку, чтобы открыть модаль СП на син_42")
except:
    print("ERROR: что-то не так при проверке работы СП на син_42")


# 10. проверка спецпредложений на син_53
driver.get("https://syn53.lp.moigektar.ru/")
# 10.1 проверка, что есть слайдер СП, по наличию кнопки на карточке
try:
    btn = wait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//*[@data-slick-index='0']/div/div/div/div[2]/div[2]/div[2]/button")))
    print("   ОК: блок СП на странице син_53 есть")
    driver.implicitly_wait(10)
    actions.move_to_element(btn).click(btn).perform()
    # 10.2 проверка, что модаль открыта, по тому, есть ли на странице поле ввода этой модали
    try:
        name = wait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//*[@id='buyconcreteform-name']")))
        print('   OK: модаль СП открылась')
        phone = driver.find_element(by=By.XPATH, value="//*[@name='BuyConcreteForm[phone]']")
        email = driver.find_element(by=By.XPATH, value="//*[@id='buyconcreteform-email']")
        submitBtn = driver.find_element(by=By.XPATH, value="//div[@class='w-modal-price']//*[text()[contains(., 'Отправить заявку')]]")
        time.sleep(1)
        name.send_keys('test')
        time.sleep(1)
        phone.send_keys('9127777777')
        time.sleep(1)
        email.send_keys('test@test.test')
        time.sleep(1)
        submitBtn.click()
        # 10.3 проверить, что заявка отправлена, по тому, отобразилась ли надпись "Спасибо за заявку"
        driver.implicitly_wait(10)
        try:
            successText = wait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[@class='w-modal-price']//p[text()[contains(., 'Спасибо за заявку')]]")))
            print('   OK: заявка из СП син_53 была отправлена')
        except TimeoutException:
            try:
                failText = wait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[@class='w-modal-price']//div[text()[contains(., 'Произошла ошибка')]]")))
                print('ERROR: заявка из СП на син_53 не была отправлена и отобразилось сообщение об ошибке отправки')
            except TimeoutException:
                print('ERROR: заявка из СП на син_53 не была отправлена')
    except ElementNotVisibleException:
        print("ERROR: модаль СП на син_53 не открылась")
except TimeoutException:
    print("ERROR: не могу найти кнопку, чтобы открыть модаль СП на син_53")
except:
    print("ERROR: что-то не так при проверке работы СП на син_53")


# 11. проверка спецпредложений на син_85
# ============================== не проверено, так как сейчас нет участков СП на 85-м
driver.get("https://syn85.lp.moigektar.ru/")
# 11.1 проверка, что есть слайдер СП, по наличию кнопки на карточке
try:
    title = wait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//h1[text()[contains(.,'Специальное')]]")))
    ActionChains(driver).move_to_element(title).send_keys(Keys.PAGE_DOWN).perform()
    print("   ОК: блок СП на странице син_85 есть")
    time.sleep(5)
    btn = driver.find_element(by=By.XPATH, value="//div[@id='catalogueSpecial']/div/div/div/div[1]//li[1]//button")
    actions.move_to_element(btn).click(btn).perform()
    # 11.2 проверка, что модаль открыта, по тому, есть ли на странице поле ввода этой модали
    try:
        name = wait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//*[@id='buyconcreteform-name']")))
        print('   OK: модаль СП открылась')
        phone = driver.find_element(by=By.XPATH, value="//*[@name='BuyConcreteForm[phone]']")
        email = driver.find_element(by=By.XPATH, value="//*[@id='buyconcreteform-email']")
        submitBtn = driver.find_element(by=By.XPATH, value="//div[@class='w-modal-description concrete-modal uk-modal uk-open']//*[text()[contains(., 'Отправить заявку')]]")
        time.sleep(1)
        name.send_keys('test')
        time.sleep(1)
        phone.send_keys('9127777777')
        time.sleep(1)
        email.send_keys('test@test.test')
        time.sleep(1)
        submitBtn.click()
        # 11.3 проверить, что заявка отправлена, по тому, отобразилась ли надпись "Спасибо за заявку"
        driver.implicitly_wait(10)
        try:
            successText = wait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[@class='w-modal-description concrete-modal uk-modal uk-open']//div[text()[contains(., 'Заявка отправлена')]]")))
            print('   OK: заявка из СП син_85 была отправлена')
        except TimeoutException:
            try:
                failText = wait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[@class='w-modal-price']//div[text()[contains(., 'Произошла ошибка')]]")))
                print('ERROR: заявка из СП на син_85 не была отправлена и отобразилось сообщение об ошибке отправки')
            except TimeoutException:
                print('ERROR: заявка из СП на син_85 не была отправлена')
    except ElementNotVisibleException:
        print("ERROR: модаль СП на син_85 не открылась")
except TimeoutException:
    print("ERROR: не могу найти кнопку, чтобы открыть модаль СП на син_85")
except:
    print("ERROR: что-то не так при проверке работы СП на син_85")


# 12. проверка спецпредложений на син_84
driver.get("https://syn84.lp.moigektar.ru/")
# 12.1 проверка, что есть слайдер СП, по наличию кнопки на карточке
try:
    title = wait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//h1[text()[contains(.,'Специальное')]]")))
    ActionChains(driver).move_to_element(title).send_keys(Keys.PAGE_DOWN).perform()
    print("   ОК: блок СП на странице син_84 есть")
    time.sleep(5)
    btn = driver.find_element(by=By.XPATH, value="//div[@id='catalogueSpecial']/div/div/div/div[1]//li[1]//button")
    actions.move_to_element(btn).click(btn).perform()
    # 12.2 проверка, что модаль открыта, по тому, есть ли на странице поле ввода этой модали
    try:
        name = wait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//*[@id='buyconcreteform-name']")))
        print('   OK: модаль СП открылась')
        phone = driver.find_element(by=By.XPATH, value="//*[@name='BuyConcreteForm[phone]']")
        email = driver.find_element(by=By.XPATH, value="//*[@id='buyconcreteform-email']")
        submitBtn = driver.find_element(by=By.XPATH, value="//div[@class='w-modal-description concrete-modal uk-modal uk-open']//*[text()[contains(., 'Отправить заявку')]]")
        time.sleep(1)
        name.send_keys('test')
        time.sleep(1)
        phone.send_keys('9127777777')
        time.sleep(1)
        email.send_keys('test@test.test')
        time.sleep(1)
        submitBtn.click()
        # 12.3 проверить, что заявка отправлена, по тому, отобразилась ли надпись "Спасибо за заявку"
        driver.implicitly_wait(10)
        try:
            successText = wait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[@class='w-modal-description concrete-modal uk-modal uk-open']//div[text()[contains(., 'Заявка отправлена')]]")))
            print('   OK: заявка была отправлена')
        except TimeoutException:
            try:
                failText = wait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[@class='w-modal-description concrete-modal uk-modal uk-open']//div[text()[contains(., 'Произошла ошибка')]]")))
                print('ERROR: заявка из СП на син_84 не была отправлена и отобразилось сообщение об ошибке отправки')
            except TimeoutException:
                print('ERROR: заявка из СП на син_84 не была отправлена')
    except ElementNotVisibleException:
        print("ERROR: модаль СП на син_84 не открылась")
except TimeoutException:
    print("ERROR: не могу найти кнопку, чтобы открыть модаль СП на син_84")
except:
    print("ERROR: что-то не так при проверке работы СП на син_84")


# # 13. проверка спецпредложений на син_24
# # ============= сейчас на 24 нет ни одного участка СП
# driver.get("https://syn24.lp.moigektar.ru/")
# # 13.1 проверка, что есть слайдер СП, по наличию кнопки на карточке
# try:
#     btn = wait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//*[@data-slick-index='0']/div/div/div/div[2]/div[2]/div[2]/button")))
#     print("   ОК: блок СП на странице син_24 есть")
#     driver.implicitly_wait(10)
#     actions.move_to_element(btn).click(btn).perform()
#     # 13.2 проверка, что модаль открыта, по тому, есть ли на странице поле ввода этой модали
#     try:
#         name = wait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//*[@id='consultationform-name']")))
#         print('   OK: модаль СП на син_24 открылась')
#     except ElementNotVisibleException:
#         print("ERROR: модаль СП на син_24 не открылась")
# except TimeoutException:
#     print("ERROR: не могу найти кнопку, чтобы открыть модаль СП на син_24")


# # 14. проверка спецпредложений на син_89
# # ================= пока что нет виджета СП на 89-м
# driver.get("https://syn89.lp.moigektar.ru/")
# # 14.1 проверка, что есть слайдер СП, по наличию кнопки на карточке
# try:
#     title = wait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//h1[text()[contains(.,'Специальное')]]")))
#     ActionChains(driver).move_to_element(title).send_keys(Keys.PAGE_DOWN).perform()
#     print("   ОК: блок СП на странице син_89 есть")
#     time.sleep(5)
#     btn = driver.find_element(by=By.XPATH, value="//div[@id='catalogueSpecial']/div/div/div/div[1]//li[1]//button")
#     actions.move_to_element(btn).click(btn).perform()
#     # 14.2 проверка, что модаль открыта, по тому, есть ли на странице поле ввода этой модали
#     try:
#         name = wait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//*[@id='buyconcreteform-name']")))
#         print('   OK: модаль СП на син_89 открылась')
#     except ElementNotVisibleException:
#         print("ERROR: модаль СП на син_89 не открылась")
# except TimeoutException:
#     print("ERROR: не могу найти кнопку, чтобы открыть модаль СП на син_89")

time.sleep(1)
driver.quit()

