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
            print('   OK: модаль SOW на главной МГ открылась')
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


# блок "Проект МГ - это"
# try:
#     assert driver.find_element(by=By.XPATH, value='//*[@id="w-descr"]/div/div[1]//div[@class="w-descr__img"]//ul[@class="uk-slider-items"]').is_displayed()
#     print('   блок "Проект МГ - это": OK')
# except:
#     print('ERROR: проблема с блоком "Проект МГ - это" на главной МГ')


time.sleep(1)
driver.quit()
