from selenium import webdriver
from selenium.webdriver.chrome.options import Options
ch_options = Options()
ch_options.add_argument('--headless')
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
#driver.maximize_window()
driver.set_window_size(1920, 1080)






# # 11. vazuza2
# driver.get("https://vazuza2.lp.moigektar.ru/")
# title = driver.find_element(by=By.XPATH, value="//div[text()[contains(.,'Генеральный')]]")
# actions.move_to_element(title).perform()
# actions.send_keys(Keys.PAGE_DOWN).perform()
# time.sleep(3)
# driver.find_element(by=By.XPATH, value='//img[@data-src="/img/vazuza/select/overlay-touch.png"]').click()
# time.sleep(14)
# driver.find_element(by=By.CLASS_NAME, value='ymaps-2-1-79-events-pane').click()
# actions.click()



# 10. проверка спецпредложений на син_53
driver.get("https://moigektar.ru/")
# 10.1 проверка, что есть слайдер СП, по наличию кнопки на карточке
try:
    title_n = driver.find_element(by=By.XPATH, value="//h1[text()[contains(.,'на новости проекта')]]")
    print('   блок "Подпишитесь на новости проекта": OK')
    try:
        actions.move_to_element(title_n).perform()
        time.sleep(5)
        wait(driver,14).until(EC.visibility_of_element_located((By.XPATH, "//div[@class='w-news-wrapper']/div/ul/li[1]/a/div[1]/div/div[1]")))
        print('   блок "Подпишитесь на новости проекта": новости ВК отображаются, ОК')
    except:
        print('ERROR: проблема с новостями ВК на главной МГ')
except:
    print('ERROR: проблема с блоком "Подпишитесь на новости проекта" на главной МГ')




time.sleep(5)
driver.quit()
