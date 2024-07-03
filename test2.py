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


# "Видео, которые вам ..." - 1-я карточка / видео / дотсы
count_vw_1 = 0
while count_vw_1 < 3:
    try:
        vw_title = driver.find_element(by=By.XPATH, value='//*[text()[contains(., "Видео, которые")]]')
        actions.move_to_element(vw_title).perform()
        assert EC.visibility_of_element_located((By.XPATH, '(//*[@id="b-video"]//*[@class="uk-object-cover"])[1]'))
        count_vw_1 = 3
        print('   OK: 1-я карточка в "Видео, которые вам ..."')
        count_vw_2 = 0 # видео
        while count_vw_2 < 3:
            try:
                driver.find_element(by=By.XPATH, value='(//*[@id="b-video"]//*[@class="uk-object-cover"])[1]').click()
                vw_video = driver.find_element(by=By.XPATH, value='//iframe[@class="uk-lightbox-iframe"]')
                driver.switch_to.frame(vw_video)
                vw_video_title = driver.find_element(by=By.CSS_SELECTOR, value='#player a.ytp-title-link')
                if vw_video_title.is_displayed():
                    driver.switch_to.default_content()
                    lb_btn = driver.find_element(by=By.CSS_SELECTOR, value = '.uk-lightbox.uk-overflow-hidden.uk-lightbox-panel.uk-open button')
                    lightbox = driver.find_element(by=By.XPATH, value='//*[@class="uk-lightbox uk-overflow-hidden uk-lightbox-panel uk-open"]')
                    driver.execute_script("arguments[0].setAttribute('class','uk-lightbox uk-overflow-hidden uk-lightbox-panel uk-open uk-active uk-transition-active')", lightbox)
                    lb_btn.click()
                    count_vw_2 = 3
                    print('     OK: видео в 1-й карточке')
                    break
            except:
                driver.refresh()
                count_vw_2 += 1
                if count_vw_2 == 3:
                    print('ERROR: не отображается видео в 1-й карточке')
                else:
                    driver.refresh()
        count_vw_3 = 0 # дотсы
        while count_vw_3 < 3:
            try:
                assert EC.visibility_of_element_located((By.XPATH, '(//*[@id="b-video"]//*[(contains(@class, "uk-dotnav"))]/li)[1]'))
                count_vw_3 = 3
                print('     OK: дотсы')
                break
            except:
                count_vw_3 += 1
                if count_vw_3 == 3:
                    print('ERROR: не отображаются дотсы в "Видео, которые вам ..."')
                else:
                    driver.refresh()
    except:
        count_vw_1 += 1
        if count_vw_1 == 3:
            print('ERROR: не отображается 1-я карточка в "Видео, которые вам ..."')
        else:
            driver.refresh()



time.sleep(3)
driver.quit()
