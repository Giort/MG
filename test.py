from selenium import webdriver
from selenium.webdriver.chrome.options import Options
ch_options = Options()
#ch_options.add_argument('--headless')
ch_options.page_load_strategy = 'eager'
driver = webdriver.Chrome(options= ch_options)
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
actions = ActionChains(driver)
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import ElementNotVisibleException
from selenium.webdriver.common.keys import Keys
import time
import json
driver.set_window_size(1660, 1000)
driver.implicitly_wait(10)

with open('data.json', 'r') as file:
    data = json.load(file)



# проверка слайдера SOW на главной странице "МГ"
# Скрипт проверяет, сколько участков СП есть у посёлка на странице Каталог участков на сайте МГ
# и сообщает, если их осталось меньше 3
#
# В лог выводится сообщение с количеством посёлков и названия этих посёлков с количеством
# участков СП для каждого из них
# В этом списке выводится сообщение "ERROR" + количество СП, если СП у посёлка меньше 3
#

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



time.sleep(1)
driver.quit()
