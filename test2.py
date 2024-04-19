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



driver.get("https://moigektar.ru")
#driver.get("https://syn33.lp.moigektar.ru/")



# форма со Снежанной
# поле ввода / кнопка / фото
count_sf_1 = 0
while count_sf_1 < 3:
    try:
        assert EC.visibility_of_element_located((By.XPATH, '(//*[(contains(@class, "snezh"))]//*[@id="consultationform-name"])[1]'))
        print('   OK: поле ввода в 1-й форме со Снежанной')
        count_sf_1 = 3
        count_sf_2 = 0 # кнопка
        while count_sf_2 < 3:
            try:
                assert EC.visibility_of_element_located((By.XPATH, '(//*[(contains(@class, "snezh"))]//button)[1]'))
                print('     OK: кнопка в форме со Снежанной')
                count_sf_2 = 3
            except:
                count_sf_2 += 1
                if count_sf_2 == 3:
                    print('ERROR: не отображается кнопка в форме со Снежанной')
                else:
                    driver.refresh()
            count_sf_3 = 0 # фото
            while count_sf_3 < 3:
                try:
                    assert EC.visibility_of_element_located((By.XPATH, '//*[@id="catalogueSpecial"]//*[@class="uk-text-center"]/a'))
                    print('     OK: отображается фото в форме со Снежанной')
                    count_sf_3 = 3
                except:
                    count_sf_3 += 1
                    if count_sf_3 == 3:
                        print('ERROR: не отображается фото в форме со Снежанной')
                    else:
                        driver.refresh()
    except:
        count_sf_1 += 1
        if count_sf_1 == 3:
            print('ERROR: не отображается поле ввода в форме со Снежанной')
        else:
            driver.refresh()

time.sleep(5)
driver.quit()
