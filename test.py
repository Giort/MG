from selenium import webdriver
from selenium.webdriver.chrome.options import Options
ch_options = Options()
ch_options.add_argument('--headless')
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
driver.set_window_size(1440, 800)


# 11. проверка спецпредложений на vazuza2
# не работает в хэдлесс, работает в обычном. Пока что не удалось разобраться, отложил
driver.get("https://vazuza2.lp.moigektar.ru/")
# 11.1 так как на вазузе нет слайдера СП, буду вызывать карточки СП с Генплана
title = driver.find_element(by=By.XPATH, value="//div[text()[contains(.,'Генеральный')]]")
actions.move_to_element(title).perform()
actions.send_keys(Keys.PAGE_DOWN).perform()
time.sleep(3)
# запуск генплана
driver.find_element(by=By.XPATH, value='//img[@data-src="/img/vazuza/select/overlay-touch.png"]').click()
print("   ОК: генплан на Вазузе присутствует")
time.sleep(14)
driver.save_screenshot("111.png")
# клик в центр общего большого элемента
driver.find_element(by=By.CLASS_NAME, value='ymaps-2-1-79-events-pane').click()
time.sleep(4)
driver.save_screenshot("222.png")
# сдвинуть курсор вверх
driver.execute_script("window.scrollBy(0, 20);")
time.sleep(4)
driver.save_screenshot("333.png")
# нажать
actions.click()
time.sleep(4)
driver.save_screenshot("444.png")

# 11.2 проверка, что модаль открыта, по тому, есть ли на странице поле ввода этой модали
#name = wait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//*[@id='buyconcreteform-name']")))
name = driver.find_element(by=By.XPATH, value="//*[@id='buyconcreteform-name']")
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

# 11.3 проверить, что заявка отправлена, по тому, отобразилась ли надпись "Спасибо за заявку"
driver.implicitly_wait(10)
try:
    successText = wait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[@class='concrete-modal uk-modal uk-open']//div[text()[contains(., 'Заявка отправлена')]]")))
    print('   OK: заявка из СП на Вазузе была отправлена')
except TimeoutException:
    try:
        failText = wait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[@class='concrete-modal uk-modal uk-open']//div[text()[contains(., 'Произошла ошибка')]]")))
        print('ERROR: заявка из СП на Вазузе не была отправлена и отобразилось сообщение об ошибке отправки')
    except TimeoutException:
        print('ERROR: заявка из СП на Вазузе не была отправлена')



time.sleep(5)
driver.quit()
