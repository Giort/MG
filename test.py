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
        submitBtn = driver.find_element(by=By.XPATH, value="//div[@class='w-modal-description uk-modal uk-open']//form/div/button[@type='submit']")
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



time.sleep(5)
driver.quit()

