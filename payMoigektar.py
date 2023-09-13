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
from selenium.webdriver.support.ui import Select
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

# выбор посёлка и участка
try:
    driver.get("https://pay.moigektar.ru/booking/home/index")
    driver.find_element(by=By.ID, value='select2-project-article-container').click()
    driver.find_element(by=By.CSS_SELECTOR, value='span ul li:nth-child(2)').click()
    time.sleep(1)
    input = wait(driver,10).until(EC.visibility_of_element_located((By.ID, 'select2-homeredirectform-batcharticle-container')))
    input.click()
    batch = wait(driver,10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'span ul li:nth-child(5)')))
    batch.click()
    driver.find_element(by=By.TAG_NAME, value='button').click()
    print('    ОК: страница выбора участка')
except:
    print('ERROR: страница выбора участка')

# # нажать на кнопку на странице оферты
try:
    time.sleep(3)
    actions.send_keys(Keys.PAGE_DOWN).perform()
    btn = wait(driver,10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'button[type="submit"]')))
    time.sleep(3)
    btn.click()
    print('    ОК: страница оферты')
except:
    print('ERROR: страница оферты')

# открыть в новой вкладке сервис бесплатных телефонных номеров
# driver.execute_script("window.open('');")
# time.sleep(1)
# driver.switch_to.window(driver.window_handles[1])
# driver.get("https://sms-activation-service.com/free-numbers/#activity")
# rus = wait(driver,10).until(EC.element_to_be_clickable((By.XPATH, '//div[@class="wrap"]/div[@data-country-code-api="russia"]')))
# rus.click()
# tel = driver.find_element(by=By.XPATH, value='//div[@class="wrap"]/div[@data-country-code-api="russia"]//a[1]')
# tel_num = tel.text
# print(tel_num)
# tel.click()

# вернуться в пэй и ввести номер телефона
try:
# driver.switch_to.window(driver.window_handles[0])
# driver.find_element(by=By.ID, value='phone').send_keys(tel_num)
    driver.find_element(by=By.ID, value='phone').send_keys('+79317065113')
    driver.find_element(by=By.ID, value='sendSms').click()
    # вручную ввести код и ничего не нажимать
    # но если нажать "Отправить", то ничего страшного, просто будет собщение про ошибку на этом этапе
    time.sleep(60)
    driver.find_element(by=By.ID, value='sendResolve').click()
    time.sleep(4)
    driver.find_element(by=By.ID, value='credentialsform-fullname')
    print('    ОК: страница ввода номера телефона')
except:
    print('ERROR: страница ввода номера телефона')

# вернуться на сервис телефонных номеров и ждать СМС с кодом
# driver.switch_to.window(driver.window_handles[1])

# вести регистрационные данные
try:
    driver.find_element(by=By.ID, value='credentialsform-fullname').send_keys(str(data["pay_cred"]["name"]))
    driver.find_element(by=By.ID, value='credentialsform-passport').send_keys(str(data["pay_cred"]["passport"]))
    driver.find_element(by=By.ID, value='credentialsform-email').send_keys(str(data["pay_cred"]["email"]))
    btn = wait(driver,10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'button[type="submit"]')))
    time.sleep(3)
    btn.click()
    print('    ОК: страница ввода персональных данных')
except:
    print('ERROR: страница ввода персональных данных')

# нажать кнопку на странице 7
try:
    time.sleep(3)
    actions.send_keys(Keys.PAGE_DOWN).perform()
    btn = wait(driver,10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'button[type="submit"]')))
    time.sleep(3)
    btn.click()
    print('    ОК: страница подтверждения введённых данных')
except:
    print('ERROR: страница подтверждения введённых данных')

# убедиться, что выполнен переход на страницу оплаты
try:
    price = driver.find_element(by=By.CLASS_NAME, value='payment__header-price-value')
    assert price
    print('    ОК: страница оплаты открылась')
except:
    print('ERROR: страница оплаты')

time.sleep(3)
driver.quit()
