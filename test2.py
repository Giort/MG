from time import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
ch_options = Options()
ch_options.add_argument('--headless')
driver = webdriver.Chrome(options= ch_options)
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
actions = ActionChains(driver)
#driver.maximize_window()
driver.set_window_size(1920, 1080)


from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import ElementNotVisibleException
import time




# 11. проверка спецпредложений на vazuza2
driver.get("https://vazuza2.lp.moigektar.ru/")
# 11.1 так как на вазузе нет слайдера СП, буду вызывать карточки СП с Генплана
title = driver.find_element(by=By.XPATH, value="//div[text()[contains(.,'Генеральный')]]")
actions.move_to_element(title).perform()
actions.send_keys(Keys.PAGE_DOWN).perform()
time.sleep(3)
driver.find_element(by=By.XPATH, value='//img[@data-src="/img/vazuza/select/overlay-touch.png"]').click()
print("   ОК: генплан на Вазузе присутствует")
time.sleep(10)
map = driver.find_element(by=By.CLASS_NAME, value='ymaps-2-1-79-events-pane').click()
h = driver.execute_script("document.body.scrollHeight")
print(h)
actions.click()
# 10.2 проверка, что модаль открыта, по тому, есть ли на странице поле ввода этой модали
name = wait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//*[@id='buyconcreteform-name']")))
print('   OK: модаль СП открылась')
phone = driver.find_element(by=By.XPATH, value="//*[@name='BuyConcreteForm[phone]']")
email = driver.find_element(by=By.XPATH, value="//*[@id='buyconcreteform-email']")
time.sleep(1)
submitBtn = driver.find_element(by=By.XPATH, value="//div[@class='concrete-modal uk-modal uk-open']//ul[@class='uk-switcher']//button[@type='submit']")
time.sleep(1)
name.send_keys('test')
time.sleep(1)
phone.send_keys('9127777777')
time.sleep(1)
email.send_keys('test@test.test')
time.sleep(1)
submitBtn.click()
# 10.3 проверить, что заявка отправлена, по тому, отобразилась ли надпись "Спасибо за заявку"
driver.implicitly_wait(10)
successText = wait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[@class='concrete-modal uk-modal uk-open']//div[text()[contains(., 'Заявка отправлена')]]")))
print('   OK: заявка из СП син_53 была отправлена')


time.sleep(5)
driver.quit()
