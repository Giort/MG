import time

from exceptiongroup import catch
from selenium.webdriver.support.ui import WebDriverWait as wait
from seleniumwire import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException
ch_options = Options()
#ch_options.add_argument('--headless')
ch_options.add_argument("--window-size=1680,1000")
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
# Настройка драйвера с Selenium Wire
# Включаем перехват запросов
sw_options = {'disable_capture': False}
import json
from selenium.webdriver.common.action_chains import ActionChains
from tenacity import retry, stop_after_attempt, retry_if_exception, retry_if_exception_type, wait_fixed
driver = webdriver.Chrome(options=ch_options)
actions = ActionChains(driver)

with open('data.json', 'r') as file:
    data = json.load(file)

# 2. Проверка каталога
# 2.1 каталог, проверка формы "Оставьте заявку", Арина - проверяю наличие правильного атрибута lgForm
try:
    driver.get("https://moigektar.ru/catalogue-no-auth")
    actions.send_keys(Keys.PAGE_DOWN).send_keys(Keys.PAGE_DOWN).perform()
    time.sleep(2)
    actions.send_keys(Keys.PAGE_DOWN).send_keys(Keys.ARROW_DOWN).perform()
    time.sleep(2)
    actions.send_keys(Keys.PAGE_DOWN).send_keys(Keys.ARROW_DOWN).perform()
    time.sleep(2)
    actions.send_keys(Keys.PAGE_DOWN).send_keys(Keys.ARROW_DOWN).perform()
    time.sleep(2)
    actions.send_keys(Keys.PAGE_DOWN).send_keys(Keys.ARROW_DOWN).perform()
    time.sleep(2)
    actions.send_keys(Keys.PAGE_DOWN).send_keys(Keys.ARROW_DOWN).perform()
    time.sleep(2)
    driver.find_element(by=By.XPATH, value="(//*[text()[contains(.,'Арина')]]/ancestor::div[contains(@id, 'cfw')]//*[@value='mg_catalog_arina_callback'])[1]")
    print("     ОК: каталог, форма с Ариной, lgForm")
except Exception as e:
    error_msg = str(e).split('\n')[0]
    print("Ошибка: каталог, форма с Ариной, lgForm — ", error_msg)