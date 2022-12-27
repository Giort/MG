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



# 12. проверка спецпредложений на син_84
driver.get("https://syn84.lp.moigektar.ru/")
# 12.1 проверка, что есть слайдер СП, по наличию кнопки на карточке
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
        phone = driver.find_element(by=By.XPATH, value="//*[@name='BuyConcreteForm[phone]']")
        email = driver.find_element(by=By.XPATH, value="//*[@id='buyconcreteform-email']")
        submitBtn = driver.find_element(by=By.XPATH, value="//div[@class='w-modal-description concrete-modal uk-modal uk-open']//*[text()[contains(., 'Отправить заявку')]]")
        print('   OK 11.2: модаль спецпредложений открылась')
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
            print('   OK 11.3: заявка была отправлена')
        except TimeoutException:
            try:
                failText = wait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[@class='w-modal-description concrete-modal uk-modal uk-open']//div[text()[contains(., 'Произошла ошибка')]]")))
                print('ERROR: 11.3: заявка из СП на син_84 не была отправлена и отобразилось сообщение об ошибке отправки')
            except TimeoutException:
                print('ERROR 11.3: заявка из СП на син_84 не была отправлена')
    except ElementNotVisibleException:
        print("ERROR: 12.2 модаль СП на син_84 не открылась")
except TimeoutException:
    print("ERROR: 12.1 не могу найти кнопку, чтобы открыть модаль СП на син_84")
except:
    print("ERROR:  что-то не так при проверке работы СП на син_84")



#time.sleep(5)
driver.quit()

