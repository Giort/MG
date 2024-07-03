from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
service = ChromeService(executable_path=ChromeDriverManager().install())
from selenium.webdriver.chrome.options import Options
ch_options = Options()
ch_options.add_argument('--headless')
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
driver.set_window_size(1680, 1000)
driver.implicitly_wait(10)





driver.get("https://moigektar.ru/catalogue-no-auth")
window_before = driver.window_handles[0]
btn = driver.find_element(by=By.XPATH, value='(//*[(contains(@class, "js-analytics-catalog-batch-presentation-download"))])[2]')
btn.click()
window_after = driver.window_handles[1]
driver.switch_to.window(window_after)


count_1 = 0
while count_1 < 3:
    try:
        look_btn = wait(driver,40).until(EC.visibility_of_element_located((By.XPATH, '//*[@title="Посмотреть"]')))
        if look_btn:
            print('    OK: КП сгенерировано')
            break
    except:
        count_1 += 1
        if count_1 == 3:
            print('ERROR: на странице генерации КП нет кнопки "Посмотреть"')
            break
        else:
            driver.refresh()



time.sleep(3)
driver.quit()
