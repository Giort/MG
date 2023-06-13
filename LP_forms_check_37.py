from selenium import webdriver
from selenium.webdriver.chrome.options import Options
ch_options = Options()
ch_options.add_argument('--headless')
ch_options.page_load_strategy = 'eager'
driver = webdriver.Chrome(options= ch_options)
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.common.action_chains import ActionChains
actions = ActionChains(driver)
from selenium.webdriver.common.by import By
import time
import json
driver.set_window_size(1660, 1080)
driver.implicitly_wait(10)

with open('data.json', 'r') as file:
    data = json.load(file)

driver.get("https://syn37.lp.moigektar.ru/")

# квиз в хедере
try:
    wait(driver, 10).until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
    driver.find_element(by=By.CSS_SELECTOR, value=".navbar-nav .ml-3").click()
    m_iframe = driver.find_element(by=By.XPATH, value="//iframe[@class='marquiz__frame marquiz__frame_open']")
    driver.switch_to.frame(m_iframe)
    driver.find_element(by=By.CLASS_NAME, value="start-page__button").click()
    print('   OK: syn_37 квиз в хедере')
except:
    print('ERROR: квиз в хедере на syn_37')

time.sleep(5)
driver.quit()
