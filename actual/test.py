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

with open('../data.json', 'r') as file:
    data = json.load(file)



#driver.get("https://moigektar.ru")
#driver.get("https://syn73.lp.moigektar.ru/")

# 8. проверка раздела "Подарочный сертификат"
# 8.1 модалка "Оставьте заявку!" №1 — проверяю наличие правильного атрибута lgForm
try:
    driver.get('https://moigektar.ru/gift')
    driver.find_element(by=By.XPATH, value='(//*[@id="gift-main-modal"]//*[@value="lg_cert"])[1]')
    print('     ОК: стр. "Подарочный сертификат", модалка "Оставьте заявку!" #1, lgForm')
except Exception as e:
    error_msg = str(e).split('\n')[0]
    print('Ошибка: стр. "Подарочный сертификат", модалка "Оставьте заявку!" #1, lgForm — ', error_msg)
# 8.2 модалка "Оставьте заявку!" №2 — проверяю наличие правильного атрибута lgForm
try:
    driver.get('https://moigektar.ru/gift')
    driver.find_element(by=By.XPATH, value='(//*[@id="plot-certificate-parents-modal"]//*[@value="lg_cert"])[1]')
    print('     ОК: стр. "Подарочный сертификат", модалка "Оставьте заявку!" #2, lgForm')
except Exception as e:
    error_msg = str(e).split('\n')[0]
    print('Ошибка: стр. "Подарочный сертификат", модалка "Оставьте заявку!" #2, lgForm — ', error_msg)
# 8.3 модалка "Оставьте заявку!" №3 — проверяю наличие правильного атрибута lgForm
try:
    driver.get('https://moigektar.ru/gift')
    driver.find_element(by=By.XPATH, value='(//*[@id="plot-certificate-friend-modal"]//*[@value="lg_cert"])[1]')
    print('     ОК: стр. "Подарочный сертификат", модалка "Оставьте заявку!" #3, lgForm')
except Exception as e:
    error_msg = str(e).split('\n')[0]
    print('Ошибка: стр. "Подарочный сертификат", модалка "Оставьте заявку!" #3, lgForm — ', error_msg)
# 8.4 модалка "Оставьте заявку!" №4 — проверяю наличие правильного атрибута lgForm
try:
    driver.get('https://moigektar.ru/gift')
    driver.find_element(by=By.XPATH, value='(//*[@id="plot-certificate-business-modal"]//*[@value="lg_cert"])[1]')
    print('     ОК: стр. "Подарочный сертификат", модалка "Оставьте заявку!" #4, lgForm')
except Exception as e:
    error_msg = str(e).split('\n')[0]
    print('Ошибка: стр. "Подарочный сертификат", модалка "Оставьте заявку!" #4, lgForm — ', error_msg)
# 8.5 модалка "Оставьте заявку!" №5 — проверяю наличие правильного атрибута lgForm
try:
    driver.get('https://moigektar.ru/gift')
    driver.find_element(by=By.XPATH, value='(//*[@id="gift-option-modal"]//*[@value="lg_cert"])[1]')
    print('     ОК: стр. "Подарочный сертификат", модалка "Оставьте заявку!" #5, lgForm')
except Exception as e:
    error_msg = str(e).split('\n')[0]
    print('Ошибка: стр. "Подарочный сертификат", модалка "Оставьте заявку!" #5, lgForm — ', error_msg)
# 8.6 модалка "Оставьте заявку!" №6 — проверяю наличие правильного атрибута lgForm
try:
    driver.get('https://moigektar.ru/gift')
    driver.find_element(by=By.XPATH, value='(//*[@id="gift-certificate-modal"]//*[@value="lg_cert"])[1]')
    print('     ОК: стр. "Подарочный сертификат", модалка "Оставьте заявку!" #6, lgForm')
except Exception as e:
    error_msg = str(e).split('\n')[0]
    print('Ошибка: стр. "Подарочный сертификат", модалка "Оставьте заявку!" #6, lgForm — ', error_msg)
# 8.7 модалка "Оставьте заявку!" №7 — проверяю наличие правильного атрибута lgForm
try:
    driver.get('https://moigektar.ru/gift')
    driver.find_element(by=By.XPATH, value='(//*[@id="select-certificate-plot-modal"]//*[@value="lg_cert"])[1]')
    print('     ОК: стр. "Подарочный сертификат", модалка "Оставьте заявку!" #7, lgForm')
except Exception as e:
    error_msg = str(e).split('\n')[0]
    print('Ошибка: стр. "Подарочный сертификат", модалка "Оставьте заявку!" #7, lgForm — ', error_msg)
# 8.8 модалка "Оставьте заявку!" №8 — проверяю наличие правильного атрибута lgForm
try:
    driver.get('https://moigektar.ru/gift')
    driver.find_element(by=By.XPATH, value='(//*[@id="select-certificate-sum-modal"]//*[@value="lg_cert"])[1]')
    print('     ОК: стр. "Подарочный сертификат", модалка "Оставьте заявку!" #8, lgForm')
except Exception as e:
    error_msg = str(e).split('\n')[0]
    print('Ошибка: стр. "Подарочный сертификат", модалка "Оставьте заявку!" #8, lgForm — ', error_msg)
# 8.9 модалка "Оставьте заявку!" №9 — проверяю наличие правильного атрибута lgForm
try:
    driver.get('https://moigektar.ru/gift')
    driver.find_element(by=By.XPATH, value='(//*[@id="gift-land-modal"]//*[@value="lg_cert"])[1]')
    print('     ОК: стр. "Подарочный сертификат", модалка "Оставьте заявку!" #9, lgForm')
except Exception as e:
    error_msg = str(e).split('\n')[0]
    print('Ошибка: стр. "Подарочный сертификат", модалка "Оставьте заявку!" #9, lgForm — ', error_msg)




time.sleep(5)
driver.quit()
