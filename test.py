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
        phone = driver.find_element(by=By.XPATH, value="//*[@name='BuyConcreteForm[phone]']")
        email = driver.find_element(by=By.XPATH, value="//*[@id='buyconcreteform-email']")
        submitBtn = driver.find_element(by=By.XPATH, value="//div[@id='modal-select-content']//*[text()[contains(., 'Отправить заявку')]]")
        print('   OK: модаль СП открылась')
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




#time.sleep(5)
driver.quit()

