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

# 8. Проверка раздела "Акции"
# 8.1 Основная страница, Максим - проверяю наличие правильного атрибута lgForm
try:
    driver.get("https://moigektar.ru/actions")
    driver.find_element(by=By.XPATH, value="(//*[text()[contains(.,'Максим')]]/ancestor::div[contains(@id, 'cfw')]//*[@value='mg_action_main_page_max_callback'])[1]")
    print('     ОК: Акции - Основная, форма с Максимом, lgForm')
except Exception as e:
    error_msg = str(e).split('\n')[0]
    print('Ошибка: Акции - Основная, форма с Максимом, lgForm — ', error_msg)

# 8.2 Страница 1 - проверяю наличие правильного атрибута lgForm
try:
    driver.get("https://moigektar.ru/actions/1")
    driver.find_element(by=By.XPATH, value="(//*[text()[contains(.,'Арина')]]/ancestor::div[contains(@id, 'cfw')]//*[@value='mg_action_page_large_family_callback'])[1]")
    print('     ОК: Акции - страница 1, форма с Ариной, lgForm')
except Exception as e:
    error_msg = str(e).split('\n')[0]
    print('Ошибка: Акции - страница 1, форма с Ариной, lgForm — ', error_msg)

# 8.3 Страница 2 - проверяю наличие правильного атрибута lgForm
try:
    driver.get("https://moigektar.ru/actions/2")
    driver.find_element(by=By.XPATH, value="(//*[text()[contains(.,'Максим')]]/ancestor::div[contains(@id, 'cfw')]//*[@value='mg_action_page_svo_callback'])[1]")
    print('     ОК: Акции - страница 2, форма с Максимом, lgForm')
except Exception as e:
    error_msg = str(e).split('\n')[0]
    print('Ошибка: Акции - страница 2, форма с Максимом, lgForm — ', error_msg)

# 8.4 Страница 3 - проверяю наличие правильного атрибута lgForm
try:
    driver.get("https://moigektar.ru/actions/3")
    driver.find_element(by=By.XPATH, value="(//*[text()[contains(.,'Андрей')]]/ancestor::div[contains(@id, 'cfw')]//*[@value='mg_action_page_veteran_callback'])[1]")
    print('     ОК: Акции - страница 3, форма с Андреем, lgForm')
except Exception as e:
    error_msg = str(e).split('\n')[0]
    print('Ошибка: Акции - страница 3, форма с Андреем, lgForm — ', error_msg)

# 8.5 Страница 4 - проверяю наличие правильного атрибута lgForm
try:
    driver.get("https://moigektar.ru/actions/4")
    driver.find_element(by=By.XPATH, value="(//*[text()[contains(.,'София')]]/ancestor::div[contains(@id, 'cfw')]//*[@value='mg_action_page_facilities_callback'])[1]")
    print('     ОК: Акции - страница 4, форма с Софией, lgForm')
except Exception as e:
    error_msg = str(e).split('\n')[0]
    print('Ошибка: Акции - страница 4, форма с Софией, lgForm — ', error_msg)

# 8.6 Страница 5 - проверяю наличие правильного атрибута lgForm
try:
    driver.get("https://moigektar.ru/actions/5")
    driver.find_element(by=By.XPATH, value="(//*[text()[contains(.,'Арина')]]/ancestor::div[contains(@id, 'cfw')]//*[@value='mg_action_page_certificate_friend_callback'])[1]")
    print('     ОК: Акции - страница 5, форма с Ариной, lgForm')
except Exception as e:
    error_msg = str(e).split('\n')[0]
    print('Ошибка: Акции - страница 5, форма с Ариной, lgForm — ', error_msg)

# 8.7 Страница 6 - проверяю наличие правильного атрибута lgForm
try:
    driver.get("https://moigektar.ru/actions/6")
    driver.find_element(by=By.XPATH, value="(//*[text()[contains(.,'Андрей')]]/ancestor::div[contains(@id, 'cfw')]//*[@value='mg_action_page_refugees_callback'])[1]")
    print('     ОК: Акции - страница 6, форма с Андреем, lgForm')
except Exception as e:
    error_msg = str(e).split('\n')[0]
    print('Ошибка: Акции - страница 6, форма с Андреем, lgForm — ', error_msg)

# 8.8 Страница 7 - проверяю наличие правильного атрибута lgForm
try:
    driver.get("https://moigektar.ru/actions/7")
    driver.find_element(by=By.XPATH, value="(//*[text()[contains(.,'Максим')]]/ancestor::div[contains(@id, 'cfw')]//*[@value='mg_action_page_certificate_self_callback'])[1]")
    print('     ОК: Акции - страница 7, форма с Максимом, lgForm')
except Exception as e:
    error_msg = str(e).split('\n')[0]
    print('Ошибка: Акции - страница 7, форма с Максимом, lgForm — ', error_msg)

