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

with open('locators.json', 'r') as file:
    locator = json.load(file)


# проверка карточек дачных участков в Каталоге поселков
# проверка, что есть кнопка на карточке участка в блоке "Дачные участки"
driver.get("https://moigektar.ru/catalogue")
try:
    title = wait(driver, 14).until(EC.visibility_of_element_located((By.XPATH, "//h1[text()[contains(., 'Дачные участки')]]")))
    actions.move_to_element(title).send_keys(Keys.PAGE_DOWN).send_keys(Keys.ARROW_DOWN).perform()
    print("   ОК: блок 'Дачные участки' на странице Каталог поселков есть")
    btn = driver.find_element(by=By.XPATH, value="" + str(locator['mg']['mg_catalog_country_country_btn']))
    actions.move_to_element(btn).click().perform()
    time.sleep(3)
    # проверка, что модаль открыта, по тому, есть ли на странице поле ввода этой модали
    try:
        name = wait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, "//div[@class='w-modal-description uk-modal uk-open']//input[@id='buybatchform-username']")))
        print('   OK: модаль из карточки открылась')
        phone = driver.find_element(by=By.XPATH, value="//div[@class='w-modal-description uk-modal uk-open']//input[@id='buybatchform-userphonenumber']")
        email = driver.find_element(by=By.XPATH, value="//div[@class='w-modal-description uk-modal uk-open']//input[@id='buybatchform-useremail']")
        submitBtn = driver.find_element(by=By.XPATH, value="//div[@class='w-modal-description uk-modal uk-open']//button[@type='submit']")
        name.send_keys('test')
        phone.send_keys('9127777777')
        email.send_keys('test@test.test')
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
    except ElementNotVisibleException:
        print('ERROR: модаль карточки блока "Дачные" на странице Каталог поселков не открылась')
    except TimeoutException:
        print('ERROR: не вижу элемент в модали карточки блока "Дачные" на странице Каталог поселков')
except TimeoutException:
    print('ERROR: не могу найти кнопку, чтобы открыть модаль карточки блока "Дачные" на странице Каталог поселков')
except:
    print('ERROR: что-то не так при проверке работы карточки блока "Дачные" на странице Каталог поселков')


time.sleep(3)
driver.quit()
