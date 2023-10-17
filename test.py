from selenium import webdriver

import chromedriver_binary
#from chromedriver_py import binary_path # this will get you the path variable
#
# svc = webdriver.ChromeService(executable_path=binary_path)
# driver = webdriver.Chrome(service=svc)

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
driver.set_window_size(1680, 1000)
driver.implicitly_wait(10)

with open('data.json', 'r') as file:
    data = json.load(file)



#driver.get("https://moigektar.ru/")
#driver.get("https://syn37.lp.moigektar.ru/")


# проверка спецпредложений на син_42
count = 0
driver.get("https://syn42.lp.moigektar.ru/")
while count < 3:
    # проверка, что есть слайдер SOW, по наличию кнопки на карточке
    try:
        btn = wait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[@id='catalogueSpecial']/div/div/div/div[1]//li[1]//button")))
        print("   ОК: блок SOW на странице син_42 есть")
        actions.move_to_element(btn).click(btn).perform()
        time.sleep(3)
        # проверка, что модаль открыта, по тому, есть ли на странице поле ввода этой модали
        try:
            name = driver.find_element(by=By.XPATH, value="//*[@id='buyconcreteform-name']")
            print('   OK: модаль SOW открылась')
            phone = driver.find_element(by=By.XPATH, value="//*[@name='BuyConcreteForm[phone]']")
            email = driver.find_element(by=By.XPATH, value="//*[@id='buyconcreteform-email']")
            submitBtn = driver.find_element(by=By.XPATH, value="//*[@id='buyconcreteform-name']//ancestor::form//*[text()[contains(., 'Отправить заявку')]]")
            name.send_keys(str(data["test_data_valid"]["name"]))
            phone.send_keys(str(data["test_data_valid"]["phone"]))
            email.send_keys(str(data["test_data_valid"]["email"]))
            time.sleep(1)
            submitBtn.click()
            # проверить, что заявка отправлена, по тому, отобразилась ли надпись "Спасибо за заявку"
            successText = wait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//*[@id='buyconcreteform-name']//ancestor::form//*[text()[contains(., 'Заявка отправлена')]]")))
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




time.sleep(5)
driver.quit()
