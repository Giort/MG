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

with open('data.json', 'r') as file:
    data = json.load(file)

#driver.get("https://moigektar.ru/")


driver.get("https://syn9.lp.moigektar.ru/")

try:
    time.sleep(2)
    btn_1 = wait(driver, 14).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "nav > div > div > .btn-mquiz")))
    btn_1.click()
    m_frame = driver.find_element(by=By.XPATH, value='//iframe[@class="marquiz__frame marquiz__frame_open"]')
    driver.switch_to.frame(m_frame)
    wait(driver, 14).until(EC.visibility_of_element_located((By.XPATH, "//h1[text()[contains(., 'Ответьте на 6 вопросов')]]")))
    print('   OK: syn_9 квиз в хедере')
except:
    print('ERROR: что-то не так с квизом в хедере на син_9')

time.sleep(3)
driver.quit()
