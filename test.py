from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
ch_options = Options()
#ch_options.add_argument('--headless')
ch_options.page_load_strategy = 'eager'
driver = webdriver.Chrome(service = Service(ChromeDriverManager().install()), options = ch_options)
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
driver.set_window_size(1680, 1000)
driver.implicitly_wait(10)

with open('data.json', 'r') as file:
    data = json.load(file)



#driver.get("https://moigektar.ru")
#driver.get("https://syn73.lp.moigektar.ru/")

# 1. проверка главной страницы "МГ"
driver.get("http://moigektar.ru")

# избавляемся от поп-апа, который перекрывает доступ ко кнопкам
time.sleep(1)
popup_w = driver.find_element(by=By.XPATH, value="//div[@id='visitors-popup']")
driver.execute_script("""
var auth_win = arguments[0];
auth_win.remove();
""", popup_w)

# 1.4 проверка формы "Оставьте заявку", Максим - проверяю наличие правильного атрибута lgForm
try:
    form_id = driver.find_element(by=By.XPATH, value="(//*[text()[contains(.,'Максим')]]/ancestor::div[contains(@id, 'cfw')]//*[@value='mg_main_page_max_callback'])[1]")
except Exception as e:
        error_msg = str(e).split('\n')[0]
        print("Ошибка: главная, форма с Максимом, lgForm — ", error_msg)


time.sleep(5)
driver.quit()
