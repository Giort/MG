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

driver.implicitly_wait(10)


# form_id = driver.find_element(by=By.XPATH, value='//b[text()[contains(.,"Подпишитесь на рассылку")]]//ancestor::div[2]').get_attribute('id')
# //div[@id='"+ form_id +"']


# проверка СП на странице СП
driver.get("https://moigektar.ru/batches")
# проверка, что есть кнопка на первой карточке участка
try:
    title = driver.find_element(by=By.XPATH, value='//h1[text()[contains(.,"Специальное")]]')
    actions.move_to_element(title).send_keys(Keys.PAGE_DOWN).perform()
    print("   ОК: блок СП на странице СП есть")
    btn = wait(driver, 15).until(EC.element_to_be_clickable((By.XPATH, "//*[@class='w-catalog-projects']//li[1]/div/div[2]/div[3]/button")))
    actions.move_to_element(btn).click().perform()
    time.sleep(3)
    # проверка, что модаль открыта, по тому, есть ли на странице поле ввода этой модали
    try:
        name = wait(driver, 15).until(EC.visibility_of_element_located((By.XPATH, "//div[@class='w-modal-description uk-modal uk-open']//input[@id='buybatchform-username']")))
        print('   OK: модаль СП на странице СП открылась')
        phone = driver.find_element(by=By.XPATH, value="//div[@class='w-modal-description uk-modal uk-open']//input[@id='buybatchform-userphonenumber']")
        email = driver.find_element(by=By.XPATH, value="//div[@class='w-modal-description uk-modal uk-open']//input[@id='buybatchform-useremail']")
        submitBtn = driver.find_element(by=By.XPATH, value="//div[@class='w-modal-description uk-modal uk-open']//form/div/button[@type='submit']")
        name.send_keys('test')
        phone.send_keys('9127777777')
        email.send_keys('test@test.test')
        submitBtn.click()
        # проверить, что заявка отправлена, по тому, отобразилась ли надпись "Выберите дату визита"
        try:
            successText = wait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//div[text()[contains(.,'Выберите дату визита')]]")))
            print('   OK: заявка была отправлена')
            driver.find_element(by=By.XPATH, value="//div[@class='w-modal-description uk-modal uk-open']/div/div/button").click()
        except TimeoutException:
            try:
                failText = wait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//div[@class='w-modal-description uk-modal uk-open']//div[text()[contains(.,'Во время отправки заявки возникли сложности')]]")))
                print('ERROR: заявка из СП на странице СП не была отправлена и отобразилось сообщение об ошибке отправки')
                driver.find_element(by=By.XPATH, value="//div[@class='w-modal-description uk-modal uk-open']/div/div/button").click()
            except TimeoutException:
                print('ERROR: заявка из СП на странице СП не была отправлена')
                driver.find_element(by=By.XPATH, value="//div[@class='w-modal-description uk-modal uk-open']/div/div/button").click()
    except ElementNotVisibleException:
        print("ERROR: модаль из СП на странице СП не открылась")
    except TimeoutException:
        print("ERROR: не вижу элемент в модали СП на странице СП")
except TimeoutException:
    print("ERROR: не могу найти кнопку, чтобы открыть модаль СП на странице СП")
except:
    print("ERROR: что-то не так при проверке работы СП на странице СП")


time.sleep(1)
driver.quit()
