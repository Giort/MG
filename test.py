from time import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
options = Options()
#options.add_argument('--headless')
ch_options = Options()
#ch_options.add_argument('--headless')
driver = webdriver.Chrome(options= ch_options)
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
actions = ActionChains(driver)
driver.maximize_window()
wait = WebDriverWait


from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import ElementNotVisibleException
import time


# 12. проверка спецпредложений на син_24
driver.get("https://syn24.lp.moigektar.ru/")
# 12.1 проверка, что есть слайдер СП, по наличию кнопки на карточке
try:
    btn = wait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//*[@data-slick-index='0']/div/div/div/div[2]/div[2]/div[2]/button")))
    print("   ОК 12.1: блок СП на странице есть")
    driver.implicitly_wait(10)
    ActionChains(driver).move_to_element(btn).click(btn).perform()
    # 12.2 проверка, что модаль открыта, по тому, есть ли на странице поле ввода этой модали
    try:
        name = wait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//*[@id='consultationform-name']")))
        print('   OK  12.2: модаль СП на син_24 открылась')
    except ElementNotVisibleException:
        print("ERROR: 12.2 модаль СП на син_24 не открылась")
except TimeoutException:
    print("ERROR: 12.1 не могу найти кнопку, чтобы открыть модаль СП на син_24")




time.sleep(5)
driver.quit()
