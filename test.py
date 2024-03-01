from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
service = ChromeService(executable_path=ChromeDriverManager().install())
from selenium.webdriver.chrome.options import Options
ch_options = Options()
#ch_options.add_argument('--headless')
ch_options.page_load_strategy = 'eager'
driver = webdriver.Chrome(service=service, options= ch_options)
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



#driver.get("https://moigektar.ru/")
#driver.get("https://syn33.lp.moigektar.ru/")

# vazuza2
count = 0
driver.get("https://vazuza2.lp.moigektar.ru/")
while count < 3:
    try:
        title = wait(driver, 14).until(EC.presence_of_element_located((By.XPATH, '//div[@id="plan"]/div/div/div/div/div[text()[contains(.,"Генеральный")]]')))
        actions.move_to_element(title).perform()
        driver.find_element(by=By.XPATH, value='//div[(contains(@class, "w-plan__video-btn"))]').click()
        genplan_elem = wait(driver, 14).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'ymaps.ymaps-2-1-79-inner-panes')))
        if genplan_elem:
            print('   OK: генплан на Вазузе')
            break
    except:
        count += 1
        if count == 3:
            print('ERROR: генплан на Вазузе')
        else:
            driver.refresh()


time.sleep(5)
driver.quit()
