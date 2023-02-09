from selenium import webdriver
from selenium.webdriver.chrome.options import Options
ch_options = Options()
#ch_options.add_argument('--headless')
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
#driver.maximize_window()
driver.set_window_size(1920, 1080)


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
        name = wait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//div[@class='w-modal-description uk-modal uk-open']//input[@id='buybatchform-username']")))
        print('   OK: модаль СП на главной МГ открылась')
        phone = driver.find_element(by=By.XPATH, value="//div[@class='w-modal-description uk-modal uk-open']//input[@id='buybatchform-usernumber']")
        email = driver.find_element(by=By.XPATH, value="//div[@class='w-modal-description uk-modal uk-open']//input[@id='buybatchform-useremail']")
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
        print("ERROR: не вижу элемент в модали СП на главной")
except TimeoutException:
    print("ERROR: не могу найти кнопку, чтобы открыть модаль СП на главной МГ")
except:
    print("ERROR: что-то не так при проверке работы СП на главной МГ")


time.sleep(5)
driver.quit()

