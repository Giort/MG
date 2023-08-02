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
driver.set_window_size(1680, 1000)
driver.implicitly_wait(10)

with open('data.json', 'r') as file:
    data = json.load(file)



#driver.get("https://moigektar.ru/")
#driver.get("https://syn99.lp.moigektar.ru/")

# проверка спецпредложений на син_99
count = 0
driver.get("http://syn99.lp.moigektar.ru/")
while count < 3:
    # проверка, что есть слайдер SOW, по наличию кнопки на карточке
    try:
        title = driver.find_element(by=By.XPATH, value="//h1[text()[contains(.,'Специальное')]]")
        ActionChains(driver).move_to_element(title).send_keys(Keys.PAGE_DOWN).perform()
        print("   ОК: блок SOW на странице син_99 есть")
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
            print('   OK: заявка из SOW син_99 была отправлена')
            if successText:
                break
        except:
            count += 1
            if count == 3:
                print('ERROR: SOW на син_99: модаль открылась, но заявка не отправлена')
            else:
                driver.refresh()
    except:
        count += 1
        if count == 3:
            print("ERROR: SOW на син_99: не могу нажать кнопку на карточке СП")
        else:
            driver.refresh()


time.sleep(5)
driver.quit()
