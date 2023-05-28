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
# В лог выводится сообщение "ОК", если: блок SOW присутствует; мод. окно открылось; отобразился 
#   элемент, подтверждающий успешную отправку данных 
# В лог выводится сообщение "ERROR", если: блок SOW не был найден; окно не было открыто; 
#   не был найден подтверждающий элемент 
#

with open('data.json', 'r') as file:
    data = json.load(file)

# проверка слайдера SOW на главной странице "МГ"
driver.get("https://moigektar.ru/")
# проверка, что есть кнопка на карточке участка в блоке "Специальное предложение"
try:
    title = driver.find_element(by=By.XPATH, value="" + str(data["mg_loc"]["mg_main_sow_title"]))
    actions.move_to_element(title).send_keys(Keys.PAGE_DOWN).perform()
    print("   ОК: блок SOW на главной МГ есть")
    btn = wait(driver, 15).until(EC.element_to_be_clickable((By.XPATH, "" + str(data["mg_loc"]["mg_main_sow_btn"]))))
    actions.move_to_element(btn).click().perform()
    time.sleep(3) # пробовал по-разному, но только при явном ожидании драйвер стабильно переключается на окно
    # проверка, что модаль открыта, по тому, есть ли на странице поле ввода этой модали
    try:
        name = wait(driver, 15).until(EC.visibility_of_element_located((By.XPATH, "//div[(contains(@class, 'w-modal-description'))]//input[@id='buybatchform-username']")))
        print('   OK: модаль SOW на главной МГ открылась')
        phone = driver.find_element(by=By.XPATH, value="//div[@class='w-modal-description uk-modal uk-open']//input[@id='buybatchform-userphonenumber']")
        email = driver.find_element(by=By.XPATH, value="//div[@class='w-modal-description uk-modal uk-open']//input[@id='buybatchform-useremail']")
        submitBtn = driver.find_element(by=By.XPATH, value="//div[@class='w-modal-description uk-modal uk-open']//form/div/button[@type='submit']")
        name.send_keys(str(data["test_data_valid"]["name"]))
        phone.send_keys(str(data["test_data_valid"]["phone"]))
        email.send_keys(str(data["test_data_valid"]["email"]))
        try:
            submitBtn.click()
        except:
            submitBtn.click()
        # проверить, что заявка отправлена, по тому, отобразилась ли надпись "Выберите дату визита"
        try:
            successText = wait(driver, 15).until(EC.visibility_of_element_located((By.XPATH, "//div[text()[contains(.,'Выберите дату визита')]]")))
            print('   OK: заявка была отправлена')
            driver.find_element(by=By.XPATH, value="//div[@class='w-modal-description uk-modal uk-open']/div/div/button").click()
        except TimeoutException:
            try:
                failText = wait(driver, 15).until(EC.visibility_of_element_located((By.XPATH, "//div[@class='w-modal-description uk-modal uk-open']//div[text()[contains(.,'Во время отправки заявки возникли сложности')]]")))
                print('ERROR: заявка из SOW на главной МГ не была отправлена и отобразилось сообщение об ошибке отправки')
                driver.find_element(by=By.XPATH, value="//div[@class='w-modal-description uk-modal uk-open']/div/div/button").click()
            except TimeoutException:
                print('ERROR: заявка из SOW на главной МГ не была отправлена')
                driver.find_element(by=By.XPATH, value="//div[@class='w-modal-description uk-modal uk-open']/div/div/button").click()
    except ElementNotVisibleException:
        print("ERROR: модаль из SOW на главной МГ не открылась")
    except TimeoutException:
        print("ERROR: не вижу элемент в модали SOW на главной")
except TimeoutException:
    print("ERROR: не могу найти кнопку, чтобы открыть модаль SOW на главной МГ")
except:
    print("ERROR: что-то не так при проверке работы SOW на главной МГ")


# проверка слайдера SOW в Каталоге поселков
driver.get("https://moigektar.ru/catalogue")
# проверка, что есть кнопка на карточке участка в блоке "Тотальная распродажа"/"Специальное предложение"
try:
    btn = driver.find_element(by=By.XPATH, value="" + str(data["mg_loc"]["mg_catalog_country_sow_btn"]))
    print("   ОК: блок SOW в каталоге есть")
    actions.move_to_element(btn).click(btn).perform()
    time.sleep(3)
    # проверка, что модаль открыта, по тому, есть ли на странице поле ввода этой модали
    try:
        name = wait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, "//div[@class='w-modal-description uk-modal uk-open']//input[@id='buybatchform-username']")))
        print('   OK: модаль SOW в каталоге открылась')
        phone = driver.find_element(by=By.XPATH, value="//div[@class='w-modal-description uk-modal uk-open']//input[@id='buybatchform-userphonenumber']")
        email = driver.find_element(by=By.XPATH, value="//div[@class='w-modal-description uk-modal uk-open']//input[@id='buybatchform-useremail']")
        submitBtn = driver.find_element(by=By.XPATH, value="//div[@class='w-modal-description uk-modal uk-open']//form/div/button[@type='submit']")
        name.send_keys(str(data["test_data_valid"]["name"]))
        phone.send_keys(str(data["test_data_valid"]["phone"]))
        email.send_keys(str(data["test_data_valid"]["email"]))
        try:
            submitBtn.click()
        except:
            submitBtn.click()
        # проверить, что заявка отправлена, по тому, открылась ли страница благодарности
        time.sleep(10)
        url = driver.current_url
        if url == 'https://moigektar.ru/thanks':
            print('   OK: заявка из SOW в каталоге отправлена, открылась страница благодарности')
        else:
            try:
                failText = wait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//div[@class='w-modal-description uk-modal uk-open']//div[text()[contains(.,'Во время отправки заявки возникли сложности')]]")))
                print('ERROR: заявка из SOW Каталога поселков не была отправлена и отобразилось сообщение об ошибке отправки')
            except TimeoutException:
                print('ERROR: заявка из SOW Каталога поселков не была отправлена')
    except TimeoutException:
        print("ERROR: не вижу элемент в модали SOW Каталога поселков")
    except ElementNotVisibleException:
        print("ERROR:  модаль из SOW Каталога поселков не открылась")
except TimeoutException:
    print("ERROR: не могу найти кнопку, чтобы открыть модаль SOW в Каталоге поселков")
except:
    print("ERROR: что-то не так при проверке работы SOW в Каталоге поселков")


# проверка работы карточек SOW на странице Каталога участков
driver.get("https://moigektar.ru/batches")
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
        try:
            submitBtn.click()
        except:
            submitBtn.click()
        # проверить, что заявка отправлена, по тому, отобразилась ли надпись "Выберите дату визита"
        try:
            successText = wait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//div[text()[contains(.,'Выберите дату визита')]]")))
            print('   OK: заявка была отправлена')
            driver.find_element(by=By.XPATH, value="//div[@class='w-modal-description uk-modal uk-open']/div/div/button").click()
        except TimeoutException:
            try:
                failText = wait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//div[@class='w-modal-description uk-modal uk-open']//div[text()[contains(.,'Во время отправки заявки возникли сложности')]]")))
                print('ERROR: заявка из карточки на странице Каталога участков не была отправлена и отобразилось сообщение об ошибке отправки')
                driver.find_element(by=By.XPATH, value="//div[@class='w-modal-description uk-modal uk-open']/div/div/button").click()
            except TimeoutException:
                print('ERROR: заявка из карточки на странице Каталога участков не была отправлена')
                driver.find_element(by=By.XPATH, value="//div[@class='w-modal-description uk-modal uk-open']/div/div/button").click()
    except ElementNotVisibleException:
        print("ERROR: модаль из карточки на странице Каталога участков не открылась")
    except TimeoutException:
        print("ERROR: не вижу элемент в модали на странице Каталога участков")
except TimeoutException:
    print("ERROR: не могу найти кнопку, чтобы открыть модаль карточки на странице Каталога участков")
except:
    print("ERROR: что-то не так при проверке работы карточки на странице Каталога участков")


# проверка SOW на странице Дачных
driver.get("https://moigektar.ru/batches/country")
# проверка, что есть кнопка на первой карточке участка
try:
    title = wait(driver, 14).until(EC.visibility_of_element_located((By.XPATH, "//h1[text()[contains(.,'Дачные')]]")))
    print("   ОК: блок SOW на странице Дачных есть")
    btn = driver.find_element(by=By.XPATH, value="//ul/li[1]/div//button")
    actions.move_to_element(btn).click().perform()
    time.sleep(3)
    # проверка, что модаль открыта, по тому, есть ли на странице поле ввода этой модали
    try:
        name = wait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//div[@class='w-modal-description uk-modal uk-open']//input[@id='buybatchform-username']")))
        print('   OK: модаль SOW на странице Дачных открылась')
        phone = driver.find_element(by=By.XPATH, value="//div[@class='w-modal-description uk-modal uk-open']//input[@id='buybatchform-userphonenumber']")
        email = driver.find_element(by=By.XPATH, value="//div[@class='w-modal-description uk-modal uk-open']//input[@id='buybatchform-useremail']")
        submitBtn = driver.find_element(by=By.XPATH, value="//div[@class='w-modal-description uk-modal uk-open']//form/div/button[@type='submit']")
        name.send_keys(str(data["test_data_valid"]["name"]))
        phone.send_keys(str(data["test_data_valid"]["phone"]))
        email.send_keys(str(data["test_data_valid"]["email"]))
        try:
            submitBtn.click()
        except:
            submitBtn.click()
        # проверить, что заявка отправлена, по тому, отобразилась ли надпись "Выберите дату визита"
        try:
            successText = wait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//div[text()[contains(.,'Выберите дату визита')]]")))
            print('   OK: заявка была отправлена')
            time.sleep(3)
            driver.find_element(by=By.XPATH, value="//div[@class='w-modal-description uk-modal uk-open']/div/div/button").click()
        except TimeoutException:
            try:
                failText = wait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//div[@class='w-modal-description uk-modal uk-open']//div[text()[contains(.,'Во время отправки заявки возникли сложности')]]")))
                print('ERROR: заявка из SOW на странице Дачных не была отправлена и отобразилось сообщение об ошибке отправки')
                driver.find_element(by=By.XPATH, value="//div[@class='w-modal-description uk-modal uk-open']/div/div/button").click()
            except TimeoutException:
                print('ERROR: заявка из SOW на странице Дачных не была отправлена')
                driver.find_element(by=By.XPATH, value="//div[@class='w-modal-description uk-modal uk-open']/div/div/button").click()
    except ElementNotVisibleException:
        print("ERROR: модаль из SOW на странице Дачных не открылась")
    except TimeoutException:
        print("ERROR: не вижу элемент в модали SOW на странице Дачных")
except TimeoutException:
    print("ERROR: не могу найти кнопку, чтобы открыть модаль SOW на странице Дачных")
except:
    print("ERROR: что-то не так при проверке работы SOW на странице Дачных")


# проверка карточек дачных участков в Каталоге поселков
# проверка, что есть кнопка на карточке участка в блоке "Дачные участки"
driver.get("https://moigektar.ru/catalogue")
try:
    title = wait(driver, 14).until(EC.visibility_of_element_located((By.XPATH, "//h1[text()[contains(., 'Дачные участки')]]")))
    actions.move_to_element(title).send_keys(Keys.PAGE_DOWN).send_keys(Keys.ARROW_DOWN).perform()
    print("   ОК: блок 'Дачные участки' на странице Каталог поселков есть")
    btn = driver.find_element(by=By.XPATH, value="" + str(data["mg_loc"]["mg_catalog_country_country_btn"]))
    time.sleep(1)
    actions.move_to_element(btn).click().perform()
    time.sleep(3)
    # проверка, что модаль открыта, по тому, есть ли на странице поле ввода этой модали
    try:
        name = wait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, "//div[@class='w-modal-description uk-modal uk-open']//input[@id='buybatchform-username']")))
        print('   OK: модаль из карточки открылась')
        phone = driver.find_element(by=By.XPATH, value="//div[@class='w-modal-description uk-modal uk-open']//input[@id='buybatchform-userphonenumber']")
        email = driver.find_element(by=By.XPATH, value="//div[@class='w-modal-description uk-modal uk-open']//input[@id='buybatchform-useremail']")
        submitBtn = driver.find_element(by=By.XPATH, value="//div[@class='w-modal-description uk-modal uk-open']//button[@type='submit']")
        name.send_keys(str(data["test_data_valid"]["name"]))
        phone.send_keys(str(data["test_data_valid"]["phone"]))
        email.send_keys(str(data["test_data_valid"]["email"]))
        try:
            submitBtn.click()
        except:
            submitBtn.click()
        # проверить, что заявка отправлена, по тому, открылась ли страница благодарности
        time.sleep(10)
        url = driver.current_url
        if url == 'https://moigektar.ru/thanks':
            print('   OK: заявка из карточки блока "Дачные" на странице Каталог поселков отправлена, открылась страница благодарности')
        else:
            try:
                failText = wait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//div[@class='w-modal-description uk-modal uk-open']//div[text()[contains(.,'Во время отправки заявки возникли сложности')]]")))
                print('ERROR: заявка из карточки блока "Дачные" на странице Каталог поселков не была отправлена и отобразилось сообщение об ошибке отправки')
            except TimeoutException:
                print('ERROR: заявка из карточки блока "Дачные" на странице Каталог поселков не была отправлена')
    except:
        print('ERROR: модаль карточки блока "Дачные" на странице Каталог поселков не открылась')
except:
    print('ERROR: что-то не так при проверке работы карточки блока "Дачные" на странице Каталог поселков')


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
driver.get("https://syn33.lp.moigektar.ru/")
# проверка, что есть слайдер SOW, по наличию кнопки на карточке
try:
    btn = wait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//*[@data-slick-index='0']/div/div/div/div[2]/div[2]/div[2]/button")))
    print("   ОК: блок SOW на странице син_33 есть")
    actions.move_to_element(btn).click(btn).perform()
    # проверка, что модаль открыта, по тому, есть ли на странице поле ввода этой модали
    try:
        name = wait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, "//*[@id='buyconcreteform-name']")))
        print('   OK: модаль SOW открылась')
        phone = driver.find_element(by=By.XPATH, value="//*[@name='BuyConcreteForm[phone]']")
        email = driver.find_element(by=By.XPATH, value="//*[@id='buyconcreteform-email']")
        submitBtn = driver.find_element(by=By.XPATH, value="//div[@id='modal-select-content']//*[text()[contains(., 'Отправить заявку')]]")
        name.send_keys(str(data["test_data_valid"]["name"]))
        phone.send_keys(str(data["test_data_valid"]["phone"]))
        email.send_keys(str(data["test_data_valid"]["email"]))
        try:
            submitBtn.click()
        except:
            submitBtn.click()
        time.sleep(3)
        # проверить, что заявка отправлена, по тому, отобразилась ли надпись "Спасибо за заявку"
        try:
            successText = wait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//div[@id='modal-select-content']//p[text()[contains(., 'Спасибо за заявку')]]")))
            print('   OK: заявка из SOW син_33 была отправлена')
        except TimeoutException:
            try:
                failText = wait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//div[@id='modal-select-content']//div[text()[contains(., 'Произошла ошибка')]]")))
                print('ERROR: заявка из SOW на син_33 не была отправлена и отобразилось сообщение об ошибке отправки')
            except TimeoutException:
                print('ERROR: заявка из SOW на син_33 не была отправлена')
    except ElementNotVisibleException:
        print("ERROR: модаль SOW на син_33 не открылась")
except TimeoutException:
    print("ERROR: не могу найти кнопку, чтобы открыть модаль SOW на син_33")
except:
    print("ERROR: что-то не так при проверке работы SOW на син_33")


# проверка спецпредложений на син_34
driver.get("https://syn34.lp.moigektar.ru/")
# проверка, что есть слайдер SOW, по наличию кнопки на карточке
try:
    btn = wait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//*[@data-slick-index='0']/div/div/div/div[2]/div[2]/div[2]/button")))
    print("   ОК: блок SOW на странице син_34 есть")
    actions.move_to_element(btn).click(btn).perform()
    time.sleep(3)
    # проверка, что модаль открыта, по тому, есть ли на странице поле ввода этой модали
    try:
        name = wait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, "//*[@id='buyconcreteform-name']")))
        print('   OK: модаль SOW открылась')
        phone = driver.find_element(by=By.XPATH, value="//*[@name='BuyConcreteForm[phone]']")
        email = driver.find_element(by=By.XPATH, value="//*[@id='buyconcreteform-email']")
        submitBtn = driver.find_element(by=By.XPATH, value="//div[@id='special-offer-modal']//*[text()[contains(., 'Отправить заявку')]]")
        name.send_keys(str(data["test_data_valid"]["name"]))
        phone.send_keys(str(data["test_data_valid"]["phone"]))
        email.send_keys(str(data["test_data_valid"]["email"]))
        try:
            submitBtn.click()
        except:
            submitBtn.click()
        # проверить, что заявка отправлена, по тому, отобразилась ли надпись "Спасибо за заявку"
        try:
            successText = wait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//div[@id='special-offer-modal']//p[text()[contains(., 'Спасибо за заявку')]]")))
            print('   OK: заявка из SOW син_34 была отправлена')
        except TimeoutException:
            try:
                failText = wait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//div[@id='special-offer-modal']//div[text()[contains(., 'Произошла ошибка')]]")))
                print('ERROR: заявка из SOW на син_34 не была отправлена и отобразилось сообщение об ошибке отправки')
            except TimeoutException:
                print('ERROR: заявка из SOW на син_34 не была отправлена')
    except ElementNotVisibleException:
        print("ERROR: модаль SOW на син_34 не открылась")
except TimeoutException:
    print("ERROR: не могу найти кнопку, чтобы открыть модаль SOW на син_34")
except:
    print("ERROR: что-то не так при проверке работы SOW на син_34")


# проверка спецпредложений на син_37
driver.get("https://syn37.lp.moigektar.ru/")
# проверка, что есть слайдер SOW, по наличию кнопки на карточке
try:
    btn = wait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//*[@data-slick-index='0']/div/div/div/div[2]/div[2]/div[2]/button")))
    print("   ОК: блок SOW на странице син_37 есть")
    actions.move_to_element(btn).click(btn).perform()
    time.sleep(3)
    # проверка, что модаль открыта, по тому, есть ли на странице поле ввода этой модали
    try:
        name = wait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, "//*[@id='buyconcreteform-name']")))
        print('   OK: модаль SOW открылась')
        phone = driver.find_element(by=By.XPATH, value="//*[@name='BuyConcreteForm[phone]']")
        email = driver.find_element(by=By.XPATH, value="//*[@id='buyconcreteform-email']")
        submitBtn = driver.find_element(by=By.XPATH, value="//div[@id='special-offer-modal']//*[text()[contains(., 'Отправить заявку')]]")
        name.send_keys(str(data["test_data_valid"]["name"]))
        phone.send_keys(str(data["test_data_valid"]["phone"]))
        email.send_keys(str(data["test_data_valid"]["email"]))
        try:
            submitBtn.click()
        except:
            submitBtn.click()
        # проверить, что заявка отправлена, по тому, отобразилась ли надпись "Спасибо за заявку"
        try:
            successText = wait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//div[@id='special-offer-modal']//p[text()[contains(., 'Спасибо за заявку')]]")))
            print('   OK: заявка из SOW син_37 была отправлена')
        except TimeoutException:
            try:
                failText = wait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//div[@id='special-offer-modal']//div[text()[contains(., 'Произошла ошибка')]]")))
                print('ERROR: заявка из SOW на син_37 не была отправлена и отобразилось сообщение об ошибке отправки')
            except TimeoutException:
                print('ERROR: заявка из SOW на син_37 не была отправлена')
    except ElementNotVisibleException:
        print("ERROR: модаль SOW на син_37 не открылась")
except TimeoutException:
    print("ERROR: не могу найти кнопку, чтобы открыть модаль SOW на син_37")
except:
    print("ERROR: что-то не так при проверке работы SOW на син_37")


# проверка спецпредложений на син_39
driver.get("https://syn39.lp.moigektar.ru/")
# проверка, что есть слайдер SOW, по наличию кнопки на карточке
try:
    title = wait(driver, 14).until(EC.presence_of_element_located((By.XPATH, "//h1[text()[contains(.,'Специальное')]]")))
    ActionChains(driver).move_to_element(title).send_keys(Keys.PAGE_DOWN).perform()
    print("   ОК: блок SOW на странице син_39 есть")
    time.sleep(3)
    btn = driver.find_element(by=By.XPATH, value="//div[@id='catalogueSpecial']/div/div/div/div[1]//li[1]//button")
    actions.move_to_element(btn).click(btn).perform()
    time.sleep(3)
    # проверка, что модаль открыта, по тому, есть ли на странице поле ввода этой модали
    try:
        name = wait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//*[@id='buyconcreteform-name']")))
        print('   OK: модаль SOW открылась')
        phone = driver.find_element(by=By.XPATH, value="//*[@name='BuyConcreteForm[phone]']")
        email = driver.find_element(by=By.XPATH, value="//*[@id='buyconcreteform-email']")
        submitBtn = driver.find_element(by=By.XPATH, value="//div[@class='w-modal-description concrete-modal uk-modal uk-open']//*[text()[contains(., 'Отправить заявку')]]")
        name.send_keys(str(data["test_data_valid"]["name"]))
        phone.send_keys(str(data["test_data_valid"]["phone"]))
        email.send_keys(str(data["test_data_valid"]["email"]))
        try:
            submitBtn.click()
        except:
            submitBtn.click()
        # проверить, что заявка отправлена, по тому, отобразилась ли надпись "Спасибо за заявку"
        driver.implicitly_wait(10)
        try:
            successText = wait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[@class='w-modal-description concrete-modal uk-modal uk-open']//div[text()[contains(., 'Заявка отправлена')]]")))
            print('   OK: заявка из SOW на син_39 была отправлена')
        except TimeoutException:
            try:
                failText = wait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[@class='w-modal-price']//div[text()[contains(., 'Произошла ошибка')]]")))
                print('ERROR: заявка из SOW на син_39 не была отправлена и отобразилось сообщение об ошибке отправки')
            except TimeoutException:
                print('ERROR: заявка из SOW на син_39 не была отправлена')
    except ElementNotVisibleException:
        print("ERROR: модаль SOW на син_39 не открылась")
except TimeoutException:
    print("ERROR: не могу найти кнопку, чтобы открыть модаль SOW на син_39")
except:
    print("ERROR: что-то не так при проверке работы SOW на син_39")


# # проверка спецпредложений на син_42
# driver.get("https://syn42.lp.moigektar.ru/")
# # проверка, что есть слайдер SOW, по наличию кнопки на карточке
# try:
#     btn = wait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//*[@data-slick-index='0']/div/div/div/div[2]/div[2]/div[2]/button")))
#     print("   ОК: блок SOW на странице син_42 есть")
#     actions.move_to_element(btn).click(btn).perform()
#     time.sleep(3)
#     # проверка, что модаль открыта, по тому, есть ли на странице поле ввода этой модали
#     try:
#         name = wait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, "//*[@id='buyconcreteform-name']")))
#         print('   OK: модаль SOW открылась')
#         phone = driver.find_element(by=By.XPATH, value="//*[@name='BuyConcreteForm[phone]']")
#         email = driver.find_element(by=By.XPATH, value="//*[@id='buyconcreteform-email']")
#         submitBtn = driver.find_element(by=By.XPATH, value="//div[@class='w-modal-price']//*[text()[contains(., 'Отправить заявку')]]")
#         name.send_keys(str(data["test_data_valid"]["name"]))
#         phone.send_keys(str(data["test_data_valid"]["phone"]))
#         email.send_keys(str(data["test_data_valid"]["email"]))
#         time.sleep(2)
#         submitBtn.click()
#         # проверить, что заявка отправлена, по тому, отобразилась ли надпись "Спасибо за заявку"
#         try:
#             successText = wait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//div[@class='w-modal-price']//p[text()[contains(., 'Спасибо за заявку')]]")))
#             print('   OK: заявка из SOW син_42 была отправлена')
#         except TimeoutException:
#             try:
#                 failText = wait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//div[@class='w-modal-price']//div[text()[contains(., 'Произошла ошибка')]]")))
#                 print('ERROR: заявка из SOW на син_42 не была отправлена и отобразилось сообщение об ошибке отправки')
#             except TimeoutException:
#                 print('ERROR: заявка из SOW на син_42 не была отправлена')
#     except ElementNotVisibleException:
#         print("ERROR: модаль SOW на син_42 не открылась")
# except TimeoutException:
#     print("ERROR: не могу найти кнопку, чтобы открыть модаль SOW на син_42")
# except:
#     print("ERROR: что-то не так при проверке работы SOW на син_42")


# проверка спецпредложений на син_53
driver.get("https://syn53.lp.moigektar.ru/")
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
        try:
            submitBtn.click()
        except:
            submitBtn.click()
        # проверить, что заявка отправлена, по тому, отобразилась ли надпись "Спасибо за заявку"
        try:
            successText = wait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//div[@class='w-modal-description concrete-modal uk-modal uk-open']//div[text()[contains(., 'Заявка отправлена')]]")))
            print('   OK: заявка из SOW син_53 была отправлена')
        except TimeoutException:
            try:
                failText = wait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//div[@class='w-modal-price']//div[text()[contains(., 'Произошла ошибка')]]")))
                print('ERROR: заявка из SOW на син_53 не была отправлена и отобразилось сообщение об ошибке отправки')
            except TimeoutException:
                print('ERROR: заявка из SOW на син_53 не была отправлена')
    except ElementNotVisibleException:
        print("ERROR: модаль SOW на син_53 не открылась")
except TimeoutException:
    print("ERROR: не могу найти кнопку, чтобы открыть модаль SOW на син_53")
except:
    print("ERROR: что-то не так при проверке работы SOW на син_53")


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
driver.get("https://syn67.lp.moigektar.ru/")
# проверка, что есть слайдер SOW, по наличию кнопки на карточке
try:
    title = wait(driver, 14).until(EC.presence_of_element_located((By.XPATH, "//h1[text()[contains(.,'Специальное')]]")))
    ActionChains(driver).move_to_element(title).send_keys(Keys.PAGE_DOWN).perform()
    print("   ОК: блок SOW на странице син_67 есть")
    time.sleep(3)
    btn = driver.find_element(by=By.XPATH, value="//div[@id='catalogueSpecial']/div/div/div/div[1]//li[1]//button")
    actions.move_to_element(btn).click(btn).perform()
    time.sleep(3)
    # проверка, что модаль открыта, по тому, есть ли на странице поле ввода этой модали
    try:
        name = wait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//*[@id='buyconcreteform-name']")))
        print('   OK: модаль SOW открылась')
        phone = driver.find_element(by=By.XPATH, value="//*[@name='BuyConcreteForm[phone]']")
        email = driver.find_element(by=By.XPATH, value="//*[@id='buyconcreteform-email']")
        submitBtn = driver.find_element(by=By.XPATH, value="//div[@class='w-modal-description concrete-modal uk-modal uk-open']//*[text()[contains(., 'Отправить заявку')]]")
        name.send_keys(str(data["test_data_valid"]["name"]))
        phone.send_keys(str(data["test_data_valid"]["phone"]))
        email.send_keys(str(data["test_data_valid"]["email"]))
        try:
            submitBtn.click()
        except:
            submitBtn.click()
        # проверить, что заявка отправлена, по тому, отобразилась ли надпись "Спасибо за заявку"
        driver.implicitly_wait(10)
        try:
            successText = wait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[@class='w-modal-description concrete-modal uk-modal uk-open']//div[text()[contains(., 'Заявка отправлена')]]")))
            print('   OK: заявка из SOW на син_67 была отправлена')
        except TimeoutException:
            try:
                failText = wait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[@class='w-modal-price']//div[text()[contains(., 'Произошла ошибка')]]")))
                print('ERROR: заявка из SOW на син_67 не была отправлена и отобразилось сообщение об ошибке отправки')
            except TimeoutException:
                print('ERROR: заявка из SOW на син_67 не была отправлена')
    except ElementNotVisibleException:
        print("ERROR: модаль SOW на син_67 не открылась")
except TimeoutException:
    print("ERROR: не могу найти кнопку, чтобы открыть модаль SOW на син_67")
except:
    print("ERROR: что-то не так при проверке работы SOW на син_67")


# проверка спецпредложений на син_84
driver.get("https://syn84.lp.moigektar.ru/")
# проверка, что есть слайдер SOW, по наличию кнопки на карточке
try:
    title = wait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//h1[text()[contains(.,'Специальное')]]")))
    ActionChains(driver).move_to_element(title).send_keys(Keys.PAGE_DOWN).perform()
    print("   ОК: блок SOW на странице син_84 есть")
    btn = driver.find_element(by=By.XPATH, value="//div[@id='catalogueSpecial']/div/div/div/div[1]//li[1]//button")
    actions.move_to_element(btn).click(btn).perform()
    time.sleep(3)
    # проверка, что модаль открыта, по тому, есть ли на странице поле ввода этой модали
    try:
        name = wait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, "//*[@id='buyconcreteform-name']")))
        print('   OK: модаль SOW открылась')
        phone = driver.find_element(by=By.XPATH, value="//*[@name='BuyConcreteForm[phone]']")
        email = driver.find_element(by=By.XPATH, value="//*[@id='buyconcreteform-email']")
        submitBtn = driver.find_element(by=By.XPATH, value="//div[@class='w-modal-description concrete-modal uk-modal uk-open']//*[text()[contains(., 'Отправить заявку')]]")
        name.send_keys(str(data["test_data_valid"]["name"]))
        phone.send_keys(str(data["test_data_valid"]["phone"]))
        email.send_keys(str(data["test_data_valid"]["email"]))
        try:
            submitBtn.click()
        except:
            submitBtn.click()
        # проверить, что заявка отправлена, по тому, отобразилась ли надпись "Спасибо за заявку"
        try:
            successText = wait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//div[@class='w-modal-description concrete-modal uk-modal uk-open']//div[text()[contains(., 'Заявка отправлена')]]")))
            print('   OK: заявка была отправлена')
        except TimeoutException:
            try:
                failText = wait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//div[@class='w-modal-description concrete-modal uk-modal uk-open']//div[text()[contains(., 'Произошла ошибка')]]")))
                print('ERROR: заявка из SOW на син_84 не была отправлена и отобразилось сообщение об ошибке отправки')
            except TimeoutException:
                print('ERROR: заявка из SOW на син_84 не была отправлена')
    except ElementNotVisibleException:
        print("ERROR: модаль SOW на син_84 не открылась")
except TimeoutException:
    print("ERROR: не могу найти кнопку, чтобы открыть модаль SOW на син_84")
except:
    print("ERROR: что-то не так при проверке работы SOW на син_84")


# проверка спецпредложений на син_85
driver.get("https://syn85.lp.moigektar.ru/")
# проверка, что есть слайдер SOW, по наличию кнопки на карточке
try:
    title = wait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//h1[text()[contains(.,'Специальное')]]")))
    ActionChains(driver).move_to_element(title).send_keys(Keys.PAGE_DOWN).perform()
    print("   ОК: блок SOW на странице син_85 есть")
    btn = driver.find_element(by=By.XPATH, value="//div[@id='catalogueSpecial']/div/div/div/div[1]//li[1]//button")
    actions.move_to_element(btn).click(btn).perform()
    time.sleep(3)
    # проверка, что модаль открыта, по тому, есть ли на странице поле ввода этой модали
    try:
        name = wait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, "//*[@id='buyconcreteform-name']")))
        print('   OK: модаль SOW открылась')
        phone = driver.find_element(by=By.XPATH, value="//*[@name='BuyConcreteForm[phone]']")
        email = driver.find_element(by=By.XPATH, value="//*[@id='buyconcreteform-email']")
        submitBtn = driver.find_element(by=By.XPATH, value="//div[@class='w-modal-description concrete-modal uk-modal uk-open']//*[text()[contains(., 'Отправить заявку')]]")
        name.send_keys(str(data["test_data_valid"]["name"]))
        phone.send_keys(str(data["test_data_valid"]["phone"]))
        email.send_keys(str(data["test_data_valid"]["email"]))
        try:
            submitBtn.click()
        except:
            submitBtn.click()
        # проверить, что заявка отправлена, по тому, отобразилась ли надпись "Спасибо за заявку"
        try:
            successText = wait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//div[@class='w-modal-description concrete-modal uk-modal uk-open']//div[text()[contains(., 'Заявка отправлена')]]")))
            print('   OK: заявка из SOW син_85 была отправлена')
        except TimeoutException:
            try:
                failText = wait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//div[@class='w-modal-price']//div[text()[contains(., 'Произошла ошибка')]]")))
                print('ERROR: заявка из SOW на син_85 не была отправлена и отобразилось сообщение об ошибке отправки')
            except TimeoutException:
                print('ERROR: заявка из SOW на син_85 не была отправлена')
    except ElementNotVisibleException:
        print("ERROR: модаль SOW на син_85 не открылась")
except TimeoutException:
    print("ERROR: не могу найти кнопку, чтобы открыть модаль SOW на син_85")
except:
    print("ERROR: что-то не так при проверке работы SOW на син_85")


# проверка спецпредложений на син_87
driver.get("https://syn87.lp.moigektar.ru/")
# проверка, что есть слайдер SOW, по наличию кнопки на карточке
try:
    title = wait(driver, 14).until(EC.presence_of_element_located((By.XPATH, "//h1[text()[contains(.,'Специальное')]]")))
    ActionChains(driver).move_to_element(title).send_keys(Keys.PAGE_DOWN).perform()
    print("   ОК: блок SOW на странице син_87 есть")
    time.sleep(3)
    btn = driver.find_element(by=By.XPATH, value="//div[@id='catalogueSpecial']/div/div/div/div[1]//li[1]//button")
    actions.move_to_element(btn).click(btn).perform()
    time.sleep(3)
    # проверка, что модаль открыта, по тому, есть ли на странице поле ввода этой модали
    try:
        name = wait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//*[@id='buyconcreteform-name']")))
        print('   OK: модаль SOW открылась')
        phone = driver.find_element(by=By.XPATH, value="//*[@name='BuyConcreteForm[phone]']")
        email = driver.find_element(by=By.XPATH, value="//*[@id='buyconcreteform-email']")
        submitBtn = driver.find_element(by=By.XPATH, value="//div[@class='w-modal-description concrete-modal uk-modal uk-open']//*[text()[contains(., 'Отправить заявку')]]")
        name.send_keys(str(data["test_data_valid"]["name"]))
        phone.send_keys(str(data["test_data_valid"]["phone"]))
        email.send_keys(str(data["test_data_valid"]["email"]))
        try:
            submitBtn.click()
        except:
            submitBtn.click()
        # проверить, что заявка отправлена, по тому, отобразилась ли надпись "Спасибо за заявку"
        driver.implicitly_wait(10)
        try:
            successText = wait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[@class='w-modal-description concrete-modal uk-modal uk-open']//div[text()[contains(., 'Заявка отправлена')]]")))
            print('   OK: заявка из SOW на син_87 была отправлена')
        except TimeoutException:
            try:
                failText = wait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[@class='w-modal-price']//div[text()[contains(., 'Произошла ошибка')]]")))
                print('ERROR: заявка из SOW на син_87 не была отправлена и отобразилось сообщение об ошибке отправки')
            except TimeoutException:
                print('ERROR: заявка из SOW на син_87 не была отправлена')
    except ElementNotVisibleException:
        print("ERROR: модаль SOW на син_87 не открылась")
except TimeoutException:
    print("ERROR: не могу найти кнопку, чтобы открыть модаль SOW на син_87")
except:
    print("ERROR: что-то не так при проверке работы SOW на син_87")


# проверка спецпредложений на син_89
driver.get("https://syn89.lp.moigektar.ru/")
# проверка, что есть слайдер SOW, по наличию кнопки на карточке
try:
    title = wait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//h1[text()[contains(.,'Специальное')]]")))
    ActionChains(driver).move_to_element(title).send_keys(Keys.PAGE_DOWN).perform()
    print("   ОК: блок SOW на странице син_89 есть")
    btn = driver.find_element(by=By.XPATH, value="//div[@id='catalogueSpecial']/div/div/div/div[1]//li[1]//button")
    actions.move_to_element(btn).click(btn).perform()
    time.sleep(3)
    # проверка, что модаль открыта, по тому, есть ли на странице поле ввода этой модали
    try:
        name = wait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, "//*[@id='buyconcreteform-name']")))
        print('   OK: модаль SOW открылась')
        phone = driver.find_element(by=By.XPATH, value="//*[@name='BuyConcreteForm[phone]']")
        email = driver.find_element(by=By.XPATH, value="//*[@id='buyconcreteform-email']")
        submitBtn = driver.find_element(by=By.XPATH, value="//div[@class='w-modal-description concrete-modal uk-modal uk-open']//*[text()[contains(., 'Отправить заявку')]]")
        name.send_keys(str(data["test_data_valid"]["name"]))
        phone.send_keys(str(data["test_data_valid"]["phone"]))
        email.send_keys(str(data["test_data_valid"]["email"]))
        try:
            submitBtn.click()
        except:
            submitBtn.click()
        # проверить, что заявка отправлена, по тому, отобразилась ли надпись "Спасибо за заявку"
        try:
            successText = wait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//div[@class='w-modal-description concrete-modal uk-modal uk-open']//div[text()[contains(., 'Заявка отправлена')]]")))
            print('   OK: заявка из SOW син_89 была отправлена')
        except TimeoutException:
            try:
                failText = wait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//div[@class='w-modal-price']//div[text()[contains(., 'Произошла ошибка')]]")))
                print('ERROR: заявка из SOW на син_89 не была отправлена и отобразилось сообщение об ошибке отправки')
            except TimeoutException:
                print('ERROR: заявка из SOW на син_89 не была отправлена')
    except ElementNotVisibleException:
        print("ERROR: модаль SOW на син_89 не открылась")
except TimeoutException:
    print("ERROR: не могу найти кнопку, чтобы открыть модаль SOW на син_89")
except:
    print("ERROR: что-то не так при проверке работы SOW на син_89")



time.sleep(1)
driver.quit()

