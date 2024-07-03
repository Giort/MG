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
#driver.get("https://syn73.lp.moigektar.ru/")


# блок "Сми о проекте"
# заголовок / 1-я карточка / модалка / "Показать еще"
count_smi_1 = 0
while count_smi_1 < 3:
    try: # заголовок
        smi_title = driver.find_element(by=By.XPATH, value='(//*[text()[contains(., "СМИ о проекте")]])[3]')
        assert EC.visibility_of_element_located((By.XPATH, "" + str(smi_title)))
        print('   OK: заголовок в "Сми о проекте"')
        count_smi_1 = 3
        count_smi_2 = 0 # 1-я карточка
        while count_smi_2 < 3:
            try:
                actions.move_to_element(smi_title).perform()
                assert EC.visibility_of_element_located((By.XPATH, '((//*[text()[contains(., "СМИ о проекте")]])[3]/parent::div//img)[1]'))
                print('     OK: 1-я карточка')
                count_smi_2 = 3
                count_smi_3 = 0 # модалка
                while count_smi_3 < 3:
                    try:
                        driver.find_element(by=By.XPATH, value='((//*[text()[contains(., "СМИ о проекте")]])[3]/parent::div//img)[1]').click()
                        assert EC.visibility_of_element_located((By.XPATH, '//div[@class="uk-modal-container js-news-view-modal uk-modal uk-open"]//div[@class="uk-padding uk-article js-news-view-modal-content"]'))
                        driver.find_element(by=By.XPATH, value='//div[@class="uk-modal-container js-news-view-modal uk-modal uk-open"]/div/button').click()
                        print('     OK: модалка новости')
                        count_smi_3 = 3
                        break
                    except:
                        count_smi_3 += 1
                        if count_smi_3 == 3:
                            print('ERROR: не отображается модалка новости')
                        else:
                            driver.refresh()
            except:
                count_smi_2 += 1
                if count_smi_2 == 3:
                    print('ERROR: не отображается 1-я карточка')
                else:
                    driver.refresh()
        count_smi_4 = 0 # "Показать еще" и 5-я карточка"
        while count_smi_4 < 3:
            try:
                smi_btn = driver.find_element(by=By.XPATH, value='(//*[text()[contains(., "СМИ о проекте")]])[3]/parent::div//*[text()[contains(., "Показать еще")]]')
                smi_btn.click()
                smi_6th_card = driver.find_element(by=By.XPATH, value='((//*[text()[contains(., "СМИ о проекте")]])[3]/parent::div//a)[6]')
                smi_6th_card.click()
                driver.find_element(by=By.XPATH, value='//div[@class="uk-modal-container js-news-view-modal uk-modal uk-open"]/div/button').click()
                print('     OK: если нажать "Показать еще" - видны остальные карточки')
                count_smi_4 = 3
                break
            except:
                count_smi_4 += 1
                if count_smi_4 == 3:
                    print('ERROR: если нажать "Показать еще" - не видны остальные карточки')
                else:
                    driver.refresh()
    except:
        count_smi_1 += 1
        if count_smi_1 == 3:
            print('ERROR: не отображается заголовок в "Сми о проекте"')
        else:
            driver.refresh()

time.sleep(5)
driver.quit()
