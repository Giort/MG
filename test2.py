from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
ch_options = Options()
ch_options.page_load_strategy = 'eager'
driver = webdriver.Chrome(service = Service(ChromeDriverManager().install()), options = ch_options)
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
actions = ActionChains(driver)
#ch_options.add_argument('--headless')
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
#driver.get("https://moigektar.ru" + str(data['mg_loc']['mg_cur_release_1']))
# wait(driver, 38).until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
#driver.get("https://syn33.lp.moigektar.ru/")

# блок "Господдержка" - фото в 1-й карточке / видео во 2-й карточке
count_g_1 = 0
while count_g_1 < 3:
    try: # фото
        g_title = driver.find_element(by=By.XPATH, value='//h2[text()[contains(., "Государственная поддержка")]]')
        actions.move_to_element(g_title).perform()
        actions.send_keys(Keys.ARROW_DOWN).send_keys(Keys.ARROW_DOWN).perform()
        assert EC.visibility_of_element_located((By.XPATH, '(//h2[text()[contains(., "Государственная поддержка")]]/parent::div//img)[6]'))
        print('   OK: 1-е фото в "Господдержке"')
        count_g_1 = 3
        count_g_2 = 0 # видео
        while count_g_2 < 3:
            try:
                g_2rd_dot = driver.find_element(by=By.XPATH, value='(//h2[text()[contains(., "Государственная поддержка")]]/parent::div//li)[2]')
                g_2rd_dot.click()
                time.sleep(3)
                g_video_btn = driver.find_element(by=By.XPATH, value='(//h2[text()[contains(., "Государственная поддержка")]]/parent::div//*[@data-src="/img/play.svg"])[3]')
                g_video_btn.click()
                g_video_iframe = driver.find_element(by=By.XPATH, value='//iframe[@class="uk-lightbox-iframe"]')
                driver.switch_to.frame(g_video_iframe)
                g_video = wait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, '//a[text()[contains(., "Вячеслав Фетисов")]]')))
                driver.switch_to.default_content()
                lb_btn = driver.find_element(by=By.CSS_SELECTOR, value = '.uk-lightbox.uk-overflow-hidden.uk-lightbox-panel.uk-open button')
                lightbox = driver.find_element(by=By.XPATH, value='//*[@class="uk-lightbox uk-overflow-hidden uk-lightbox-panel uk-open"]')
                driver.execute_script("arguments[0].setAttribute('class','uk-lightbox uk-overflow-hidden uk-lightbox-panel uk-open uk-active uk-transition-active')", lightbox)
                lb_btn.click()
                print('     OK: видео')
                count_g_3 = 3
                break
            except:
                count_g_2 += 1
                if count_g_2 == 3:
                    print('ERROR: не отображается видео')
                else:
                    driver.refresh()
    except:
        count_g_1 += 1
        if count_g_1 == 3:
            print('ERROR: не отображается фото в "Господдержке"')
        else:
            driver.refresh()


time.sleep(3)
driver.quit()
