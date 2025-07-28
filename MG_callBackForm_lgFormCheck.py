from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
ch_options = Options()
ch_options.add_argument('--headless')
ch_options.page_load_strategy = 'eager'
driver = webdriver.Chrome(service = Service(ChromeDriverManager().install()), options = ch_options)
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.common.keys import Keys
import time
import json
from selenium.webdriver.common.action_chains import ActionChains
actions = ActionChains(driver)
driver.implicitly_wait(10)
driver.set_window_size(1660, 1000)

with open('data.json', 'r') as file:
    data = json.load(file)
    
# Скрипт заполняет одну форму корректными данными и отправляет их
# В этой форме и во всех остальных проверяет, что присутствует lgForm и он не изменился
#

# 1. проверка главной страницы "МГ"

# избавляемся от поп-апа, который перекрывает доступ ко кнопкам
try:
    driver.get("https://moigektar.ru/catalogue-no-auth")
    driver.get("https://moigektar.ru")
    time.sleep(1)
    popup_w = driver.find_element(by=By.XPATH, value="//div[@id='visitors-popup']")
    driver.execute_script("""
    var auth_win = arguments[0];
    auth_win.remove();
    """, popup_w)
except:
    print("Popup not found")

# 1.1 проверка формы "Оставьте заявку", форма с Софией №1
# проверяю отправку данных через форму
# проверяю наличие правильного атрибута lgForm и заголовка
try:
    title = driver.find_element(by=By.XPATH, value="/descendant::*[text()[contains(.,'София')]][2]")
    # сохраняю текущий динамический id формы в переменную для того, чтобы последующие локаторы не были такого вида:
    # //h1/*[text()[contains(.,'Хотите узнать')]]//parent::h1//following-sibling::ul[2]//input[@id='consultationform-phone']
    form_id = driver.find_element(by=By.XPATH, value="(//*[text()[contains(.,'София')]]/ancestor::div[contains(@id, 'cfw')])[1]").get_attribute("id")
    actions.move_to_element(title).perform()
    try: # проверка lgForm
        driver.find_element(by=By.XPATH, value="(//div[@id='"+ form_id +"']//*[@value='mg_main_page_sofia2_callback'])[2]")
        print("     ОК: главная, форма с Софией №1, lgForm")
    except Exception as e:
        error_msg = str(e).split('\n')[0]
        print("Ошибка: главная, форма с Софией, lgForm — ", error_msg)
    try: # проверка заголовка
        driver.find_element(by=By.XPATH, value="//div[@id='"+ form_id +"']//div[@class='uk-visible@s']//*[text()[contains(.,'проконсультирую')]]")
        print("     ОК: главная, форма с Софией №1, заголовок")
    except Exception as e:
        error_msg = str(e).split('\n')[0]
        print("Ошибка: главная, форма с Софией, заголовок — ", error_msg)
    try: # проверка отправки данных
        driver.find_element(by=By.XPATH,
                            value="(//div[@id='" + form_id + "']//*[@id='consultationform-phone'])[1]").send_keys(
            str(data["test_data_valid"]["phone"]))
        driver.find_element(by=By.XPATH,
                            value="(//div[@id='" + form_id + "']//*[text()[contains(.,'Отправить')]])[1]").click()
        name_input = driver.find_element(by=By.XPATH, value="(//div[@id='"+ form_id +"']//*[@id='consultationform-name'])[2]")
        name_input.click()
        print("     ОК: главная, форма с Софией №1, отправка через форму")
    except Exception as e:
        error_msg = str(e).split('\n')[0]
        print("Ошибка: главная, форма с Софией №1, отправка через форму — ", error_msg)
except Exception as e:
        error_msg = str(e).split('\n')[0]
        print("Ошибка: главная, форма с Софией №1 — ", error_msg)

# 1.2 проверка формы "Оставьте заявку", Арина #1 - проверяю наличие правильного атрибута lgForm и заголовка
try:
    driver.find_element(by=By.XPATH, value="(//*[text()[contains(.,'Арина')]]/ancestor::div[contains(@id, 'cfw')]//*[@value='mg_main_page_arina_callback'])[1]")
    print("     ОК: главная, форма с Ариной #1, lgForm")
except Exception as e:
    error_msg = str(e).split('\n')[0]
    print("Ошибка: главная, форма с Ариной #1, lgForm — ", error_msg)
try:
    driver.find_element(by=By.XPATH, value="(//*[text()[contains(.,'Арина')]]/ancestor::div[contains(@id, 'cfw')]//div[text()[contains(., 'Напишу вам в WhatsApp,')]])[2]")
    print("     ОК: главная, форма с Ариной #1, заголовок")
except Exception as e:
    error_msg = str(e).split('\n')[0]
    print("Ошибка: главная, форма с Ариной #1, заголовок — ", error_msg)

# 1.3 проверка формы "Оставьте заявку", Арина #2 - проверяю наличие правильного атрибута lgForm и заголовка
try:
    driver.find_element(by=By.XPATH, value="(//*[text()[contains(.,'Арина')]]/ancestor::div[contains(@id, 'cfw')]//*[@value='mg_main_page_arina2_callback'])[1]")
    print("     ОК: главная, форма с Ариной #2, lgForm")
except Exception as e:
    error_msg = str(e).split('\n')[0]
    print("Ошибка: главная, форма с Ариной #2, lgForm — ", error_msg)
try:
    driver.find_element(by=By.XPATH, value="(//*[text()[contains(.,'Арина')]]/ancestor::*[contains(@id, 'cfw')]//*[text()[contains(., 'Расскажу подробнее об акциях')]])[2]")
    print("     ОК: главная, форма с Ариной #2, заголовок")
except Exception as e:
    error_msg = str(e).split('\n')[0]
    print("Ошибка: главная, форма с Ариной #2, заголовок — ", error_msg)

# 1.4 проверка формы "Оставьте заявку", Анастасия - проверяю наличие правильного атрибута lgForm и заголовка
try:
    driver.find_element(by=By.XPATH, value="(//*[text()[contains(.,'Анастасия')]]/ancestor::div[contains(@id, 'cfw')]//*[@value='mg_main_page_anastasiya_callback'])[1]")
    print("     ОК: главная, форма с Анастасией, lgForm")
except Exception as e:
    error_msg = str(e).split('\n')[0]
    print("Ошибка: главная, форма с Анастасией, lgForm — ", error_msg)
try:
    driver.find_element(by=By.XPATH, value="(//*[text()[contains(.,'Анастасия')]]/ancestor::*[contains(@id, 'cfw')]//*[text()[contains(., 'Закажите развитие участка')]])[3]")
    print("     ОК: главная, форма с Анастасией, заголовок")
except Exception as e:
    error_msg = str(e).split('\n')[0]
    print("Ошибка: главная, форма с Анастасией, заголовок — ", error_msg)

# 1.5 проверка формы "Оставьте заявку", София №2 - проверяю наличие правильного атрибута lgForm и заголовка
try:
    driver.find_element(by=By.XPATH, value="(//*[text()[contains(.,'София')]]/ancestor::div[contains(@id, 'cfw')]//*[@value='mg_main_page_sofia_callback'])[1]")
    print("     ОК: главная, форма с Софией №2, lgForm")
except Exception as e:
    error_msg = str(e).split('\n')[0]
    print("Ошибка: главная, форма с Софией №2, lgForm — ", error_msg)
try:
    driver.find_element(by=By.XPATH, value="(//*[text()[contains(.,'София')]]/ancestor::*[contains(@id, 'cfw')]//*[text()[contains(., 'Расскажу про развитие участка')]])[2]")
    print("     ОК: главная, форма с Софией №2, заголовок")
except Exception as e:
    error_msg = str(e).split('\n')[0]
    print("Ошибка: главная, форма с Софией №2, заголовок — ", error_msg)

# 1.6 проверка формы "Оставьте заявку", Максим - проверяю наличие правильного атрибута lgForm и заголовка
try:
    driver.find_element(by=By.XPATH, value="(//*[text()[contains(.,'Максим')]]/ancestor::div[contains(@id, 'cfw')]//*[@value='mg_main_page_max_callback'])[1]")
    print("     ОК: главная, форма с Максимом, lgForm")
except Exception as e:
    error_msg = str(e).split('\n')[0]
    print("Ошибка: главная, форма с Максимом, lgForm — ", error_msg)
try:
    driver.find_element(by=By.XPATH, value="(//*[text()[contains(.,'София')]]/ancestor::*[contains(@id, 'cfw')]//*[text()[contains(., 'Расскажу про развитие участка')]])[2]")
    print("     ОК: главная, форма с Максимом, заголовок")
except Exception as e:
    error_msg = str(e).split('\n')[0]
    print("Ошибка: главная, форма с Максимом, заголовок — ", error_msg)


# 2. Проверка каталога
# 2.1 каталог, проверка формы "Оставьте заявку", Арина - проверяю наличие правильного атрибута lgForm и заголовка
try:
    driver.get("https://moigektar.ru/catalogue-no-auth")
    actions.send_keys(Keys.PAGE_DOWN).send_keys(Keys.PAGE_DOWN).perform()
    time.sleep(2)
    actions.send_keys(Keys.PAGE_DOWN).send_keys(Keys.ARROW_DOWN).perform()
    time.sleep(2)
    actions.send_keys(Keys.PAGE_DOWN).send_keys(Keys.ARROW_DOWN).perform()
    time.sleep(2)
    actions.send_keys(Keys.PAGE_DOWN).send_keys(Keys.ARROW_DOWN).perform()
    time.sleep(2)
    actions.send_keys(Keys.PAGE_DOWN).send_keys(Keys.ARROW_DOWN).perform()
    time.sleep(2)
    actions.send_keys(Keys.PAGE_DOWN).send_keys(Keys.ARROW_DOWN).perform()
    time.sleep(2)
    actions.send_keys(Keys.PAGE_DOWN).send_keys(Keys.ARROW_DOWN).perform()
    time.sleep(2)
    driver.find_element(by=By.XPATH, value="(//*[text()[contains(.,'Арина')]]/ancestor::div[contains(@id, 'cfw')]//*[@value='mg_catalog_arina_callback'])[1]")
    print("     ОК: каталог, форма с Ариной, lgForm")
except Exception as e:
    error_msg = str(e).split('\n')[0]
    print("Ошибка: каталог, форма с Ариной, lgForm — ", error_msg)
try:
    driver.find_element(by=By.XPATH, value="(//*[text()[contains(.,'Арина')]]/ancestor::*[contains(@id, 'cfw')]//div[text()[contains(., 'оставьте свой номер')]])[2]")
    print("     ОК: каталог, форма с Ариной, заголовок")
except Exception as e:
    error_msg = str(e).split('\n')[0]
    print("Ошибка: каталог, форма с Ариной, заголовок — ", error_msg)

# 2.2 страница актива, проверка формы "Оставьте заявку", Арина - проверяю наличие правильного атрибута lgForm и заголовка
try:
    driver.get("https://moigektar.ru/batches/44607")
    driver.find_element(by=By.XPATH, value="(//*[text()[contains(.,'Арина')]]/ancestor::div[contains(@id, 'cfw')]//*[@value='mg_batch_page_arina_callback'])[1]")
    print("     ОК: стр. актива, форма с Ариной, lgForm")
except Exception as e:
    error_msg = str(e).split('\n')[0]
    print("Ошибка: стр. актива, форма с Ариной, lgForm — ", error_msg)
try:
    driver.find_element(by=By.XPATH, value="(//*[text()[contains(.,'Арина')]]/ancestor::*[contains(@id, 'cfw')]//div[text()[contains(., 'Напишу вам в WhatsApp,')]])[2]")
    print("     ОК: стр. актива, форма с Ариной, заголовок")
except Exception as e:
    error_msg = str(e).split('\n')[0]
    print("Ошибка: стр. актива, форма с Ариной, заголовок — ", error_msg)


# 3. Проверка раздела "О проекте"
# 3.1 О проекте - основная страница, Арина - проверяю наличие правильного атрибута lgForm и заголовка
try:
    driver.get("https://moigektar.ru/about")
    driver.find_element(by=By.XPATH, value="(//*[text()[contains(.,'Арина')]]/ancestor::div[contains(@id, 'cfw')]//*[@value='mg_about_page_callback'])[1]")
    print('     ОК: "О проекте", форма с Ариной, lgForm')
except Exception as e:
    error_msg = str(e).split('\n')[0]
    print('Ошибка: "О проекте", форма с Ариной, lgForm — ', error_msg)
try:
    driver.find_element(by=By.XPATH, value="(//*[text()[contains(.,'Арина')]]/ancestor::*[contains(@id, 'cfw')]//div[text()[contains(., 'Напишу вам в WhatsApp,')]])[2]")
    print("     ОК: 'О проекте', форма с Ариной, заголовок")
except Exception as e:
    error_msg = str(e).split('\n')[0]
    print("Ошибка: 'О проекте', форма с Ариной, заголовок — ", error_msg)

# 3.2 О проекте - Партнеры, Арина - проверяю наличие правильного атрибута lgForm и заголовка
try:
    driver.get("https://moigektar.ru/about/advantages")
    driver.find_element(by=By.XPATH, value="(//*[text()[contains(.,'Арина')]]/ancestor::div[contains(@id, 'cfw')]//*[@value='mg_about_partners_page_callback'])[1]")
    print('     ОК: "О проекте - Партнеры", форма с Ариной, lgForm')
except Exception as e:
    error_msg = str(e).split('\n')[0]
    print('Ошибка: "О проекте - Партнеры", форма с Ариной, lgForm — ', error_msg)
try:
    driver.find_element(by=By.XPATH, value="(//*[text()[contains(.,'Арина')]]/ancestor::*[contains(@id, 'cfw')]//div[text()[contains(., 'Напишу вам в WhatsApp,')]])[2]")
    print("     ОК: 'О проекте - Партнеры', форма с Ариной, заголовок")
except Exception as e:
    error_msg = str(e).split('\n')[0]
    print("Ошибка: 'О проекте - Партнеры', форма с Ариной, заголовок — ", error_msg)

# 3.3 О проекте - Союз садоводов, Арина - проверяю наличие правильного атрибута lgForm и заголовка
try:
    driver.get("https://moigektar.ru/about/union")
    driver.find_element(by=By.XPATH, value="(//*[text()[contains(.,'Арина')]]/ancestor::div[contains(@id, 'cfw')]//*[@value='mg_about_union_page_callback'])[1]")
    print('     ОК: "О проекте - Союз садоводов", форма с Ариной, lgForm')
except Exception as e:
    error_msg = str(e).split('\n')[0]
    print('Ошибка: "О проекте - Союз садоводов", форма с Ариной, lgForm — ', error_msg)
try:
    driver.find_element(by=By.XPATH, value="(//*[text()[contains(.,'Арина')]]/ancestor::*[contains(@id, 'cfw')]//div[text()[contains(., 'Напишу вам в WhatsApp,')]])[2]")
    print("     ОК: 'О проекте - Союз садоводов', форма с Ариной, заголовок")
except Exception as e:
    error_msg = str(e).split('\n')[0]
    print("Ошибка: 'О проекте - Союз садоводов', форма с Ариной, заголовок — ", error_msg)

# 3.4 О проекте - Отзывы, Арина - проверяю наличие правильного атрибута lgForm и заголовка
try:
    driver.get("https://moigektar.ru/about/reviews")
    driver.find_element(by=By.XPATH, value="(//*[text()[contains(.,'Арина')]]/ancestor::div[contains(@id, 'cfw')]//*[@value='mg_about_reviews_page_callback'])[1]")
    print('     ОК: "О проекте - Отзывы", форма с Ариной, lgForm')
except Exception as e:
    error_msg = str(e).split('\n')[0]
    print('Ошибка: "О проекте - Отзывы", форма с Ариной, lgForm — ', error_msg)
try:
    driver.find_element(by=By.XPATH, value="(//*[text()[contains(.,'Арина')]]/ancestor::*[contains(@id, 'cfw')]//div[text()[contains(., 'Напишу вам в WhatsApp,')]])[2]")
    print("     ОК: 'О проекте - Отзывы', форма с Ариной, заголовок")
except Exception as e:
    error_msg = str(e).split('\n')[0]
    print("Ошибка: 'О проекте - Отзывы', форма с Ариной, заголовок — ", error_msg)


# 4. Проверка раздела "Развитие"
# 4.1 Развитие - Развитие поселков, Арина - проверяю наличие правильного атрибута lgForm и заголовка
try:
    driver.get("https://moigektar.ru/growth")
    driver.find_element(by=By.XPATH, value="(//*[text()[contains(.,'Арина')]]/ancestor::div[contains(@id, 'cfw')]//*[@value='mg_growth_page_callback'])[1]")
    print('     ОК: "Развитие - Развитие поселков", форма с Ариной, lgForm')
except Exception as e:
    error_msg = str(e).split('\n')[0]
    print('Ошибка: "Развитие - Развитие поселков", форма с Ариной, lgForm — ', error_msg)
try:
    driver.find_element(by=By.XPATH, value="(//*[text()[contains(.,'Арина')]]/ancestor::*[contains(@id, 'cfw')]//div[text()[contains(., 'Напишу вам в WhatsApp,')]])[2]")
    print("     ОК: 'Развитие - Развитие поселков', форма с Ариной, заголовок")
except Exception as e:
    error_msg = str(e).split('\n')[0]
    print("Ошибка: 'Развитие - Развитие поселков', форма с Ариной, заголовок — ", error_msg)

# 4.2 Развитие - Глазами инвестора, Арина - проверяю наличие правильного атрибута lgForm и заголовка
try:
    driver.get("https://moigektar.ru/investment")
    driver.find_element(by=By.XPATH, value="(//*[text()[contains(.,'Арина')]]/ancestor::div[contains(@id, 'cfw')]//*[@value='mg_investment_page_callback'])[1]")
    print('     ОК: "Развитие - Глазами инвестора", форма с Ариной, lgForm')
except Exception as e:
    error_msg = str(e).split('\n')[0]
    print('Ошибка: "Развитие - Глазами инвестора", форма с Ариной, lgForm — ', error_msg)
try:
    driver.find_element(by=By.XPATH, value="(//*[text()[contains(.,'Арина')]]/ancestor::*[contains(@id, 'cfw')]//div[text()[contains(., 'Напишу вам в WhatsApp,')]])[2]")
    print("     ОК: 'Развитие - Глазами инвестора', форма с Ариной, заголовок")
except Exception as e:
    error_msg = str(e).split('\n')[0]
    print("Ошибка: 'Развитие - Глазами инвестора', форма с Ариной, заголовок — ", error_msg)

# 4.3 Развитие - Капитализация, Арина - проверяю наличие правильного атрибута lgForm и заголовка
try:
    driver.get("https://moigektar.ru/investment/capitalization")
    driver.find_element(by=By.XPATH, value="(//*[text()[contains(.,'Арина')]]/ancestor::div[contains(@id, 'cfw')]//*[@value='mg_capitalization_page_callback'])[1]")
    print('     ОК: "Развитие - Капитализация", форма с Ариной, lgForm')
except Exception as e:
    error_msg = str(e).split('\n')[0]
    print('Ошибка: "Развитие - Капитализация", форма с Ариной, lgForm — ', error_msg)
try:
    driver.find_element(by=By.XPATH, value="(//*[text()[contains(.,'Арина')]]/ancestor::*[contains(@id, 'cfw')]//div[text()[contains(., 'Напишу вам в WhatsApp,')]])[2]")
    print("     ОК: 'Развитие - Капитализация', форма с Ариной, заголовок")
except Exception as e:
    error_msg = str(e).split('\n')[0]
    print("Ошибка: 'Развитие - Капитализация', форма с Ариной, заголовок — ", error_msg)

# 4.4 Развитие - Базовая стратегия, Арина - проверяю наличие правильного атрибута lgForm и заголовка
try:
    driver.get("https://moigektar.ru/investment/basic")
    driver.find_element(by=By.XPATH, value="(//*[text()[contains(.,'Арина')]]/ancestor::div[contains(@id, 'cfw')]//*[@value='mg_invest_basic_page_callback'])[1]")
    print('     ОК: "Развитие - Базовая стратегия", форма с Ариной, lgForm')
except Exception as e:
    error_msg = str(e).split('\n')[0]
    print('Ошибка: "Развитие - Базовая стратегия", форма с Ариной, lgForm — ', error_msg)
try:
    driver.find_element(by=By.XPATH, value="(//*[text()[contains(.,'Арина')]]/ancestor::*[contains(@id, 'cfw')]//div[text()[contains(., 'Напишу вам в WhatsApp,')]])[2]")
    print("     ОК: 'Развитие - Базовая стратегия', форма с Ариной, заголовок")
except Exception as e:
    error_msg = str(e).split('\n')[0]
    print("Ошибка: 'Развитие - Базовая стратегия', форма с Ариной, заголовок — ", error_msg)

# 4.5 Развитие - Предприниматель, Арина - проверяю наличие правильного атрибута lgForm и заголовка
try:
    driver.get("https://moigektar.ru/investment/businessman")
    driver.find_element(by=By.XPATH, value="(//*[text()[contains(.,'Арина')]]/ancestor::div[contains(@id, 'cfw')]//*[@value='mg_invest_businessman_page_callback'])[1]")
    print('     ОК: "Развитие - Предприниматель", форма с Ариной, lgForm')
except Exception as e:
    error_msg = str(e).split('\n')[0]
    print('Ошибка: "Развитие - Предприниматель", форма с Ариной, lgForm — ', error_msg)
try:
    driver.find_element(by=By.XPATH, value="(//*[text()[contains(.,'Арина')]]/ancestor::*[contains(@id, 'cfw')]//div[text()[contains(., 'Напишу вам в WhatsApp,')]])[2]")
    print("     ОК: 'Развитие - Предприниматель', форма с Ариной, заголовок")
except Exception as e:
    error_msg = str(e).split('\n')[0]
    print("Ошибка: 'Развитие - Предприниматель', форма с Ариной, заголовок — ", error_msg)

# 4.6 Развитие - Садовод, Арина - проверяю наличие правильного атрибута lgForm и заголовка
try:
    driver.get("https://moigektar.ru/investment/farmer")
    driver.find_element(by=By.XPATH, value="(//*[text()[contains(.,'Арина')]]/ancestor::div[contains(@id, 'cfw')]//*[@value='mg_invest_farmer_page_callback'])[1]")
    print('     ОК: "Развитие - Садовод", форма с Ариной, lgForm')
except Exception as e:
    error_msg = str(e).split('\n')[0]
    print('Ошибка: "Развитие - Садовод", форма с Ариной, lgForm — ', error_msg)
try:
    driver.find_element(by=By.XPATH, value="(//*[text()[contains(.,'Арина')]]/ancestor::*[contains(@id, 'cfw')]//div[text()[contains(., 'Напишу вам в WhatsApp,')]])[2]")
    print("     ОК: 'Развитие - Садовод', форма с Ариной, заголовок")
except Exception as e:
    error_msg = str(e).split('\n')[0]
    print("Ошибка: 'Развитие - Садовод', форма с Ариной, заголовок — ", error_msg)

# 4.7 Развитие - Усадьба, Арина - проверяю наличие правильного атрибута lgForm и заголовка
try:
    driver.get("https://moigektar.ru/investment/family")
    driver.find_element(by=By.XPATH, value="(//*[text()[contains(.,'Арина')]]/ancestor::div[contains(@id, 'cfw')]//*[@value='mg_invest_family_page_callback'])[1]")
    print('     ОК: "Развитие - Усадьба", форма с Ариной, lgForm')
except Exception as e:
    error_msg = str(e).split('\n')[0]
    print('Ошибка: "Развитие - Усадьба", форма с Ариной, lgForm — ', error_msg)
try:
    driver.find_element(by=By.XPATH, value="(//*[text()[contains(.,'Арина')]]/ancestor::*[contains(@id, 'cfw')]//div[text()[contains(., 'Напишу вам в WhatsApp,')]])[2]")
    print("     ОК: 'Развитие - Усадьба', форма с Ариной, заголовок")
except Exception as e:
    error_msg = str(e).split('\n')[0]
    print("Ошибка: 'Развитие - Усадьба', форма с Ариной, заголовок — ", error_msg)


# 5. Проверка раздела "Меры поддержки"
# 5.1 Меры поддержки - основная, Арина - проверяю наличие правильного атрибута lgForm и заголовка
try:
    driver.get("https://moigektar.ru/documents/gos")
    driver.find_element(by=By.XPATH, value="(//*[text()[contains(.,'Арина')]]/ancestor::div[contains(@id, 'cfw')]//*[@value='mg_gos_page_callback'])[1]")
    print('     ОК: "Меры поддержки - основная", форма с Ариной, lgForm')
except Exception as e:
    error_msg = str(e).split('\n')[0]
    print('Ошибка: "Меры поддержки - основная", форма с Ариной, lgForm — ', error_msg)
try:
    driver.find_element(by=By.XPATH, value="(//*[text()[contains(.,'Арина')]]/ancestor::*[contains(@id, 'cfw')]//div[text()[contains(., 'Напишу вам в WhatsApp,')]])[2]")
    print("     ОК: 'Меры поддержки - основная', форма с Ариной, заголовок")
except Exception as e:
    error_msg = str(e).split('\n')[0]
    print("Ошибка: 'Меры поддержки - основная', форма с Ариной, заголовок — ", error_msg)

# 5.2 Меры поддержки - Для владельцев земли, Арина - проверяю наличие правильного атрибута lgForm и заголовка
try:
    driver.get("https://moigektar.ru/documents")
    driver.find_element(by=By.XPATH, value="(//*[text()[contains(.,'Арина')]]/ancestor::div[contains(@id, 'cfw')]//*[@value='mg_gos_page_callback'])[1]")
    print('     ОК: "Меры поддержки - Для владельцев земли", форма с Ариной, lgForm')
except Exception as e:
    error_msg = str(e).split('\n')[0]
    print('Ошибка: "Меры поддержки - Для владельцев земли", форма с Ариной, lgForm — ', error_msg)
try:
    driver.find_element(by=By.XPATH, value="(//*[text()[contains(.,'Арина')]]/ancestor::*[contains(@id, 'cfw')]//div[text()[contains(., 'Напишу вам в WhatsApp,')]])[2]")
    print("     ОК: 'Меры поддержки - Для владельцев земли', форма с Ариной, заголовок")
except Exception as e:
    error_msg = str(e).split('\n')[0]
    print("Ошибка: 'Меры поддержки - Для владельцев земли', форма с Ариной, заголовок — ", error_msg)

# 5.3 Меры поддержки - Начинающий фермер, Арина - проверяю наличие правильного атрибута lgForm и заголовка
try:
    driver.get("https://moigektar.ru/documents/farmer")
    driver.find_element(by=By.XPATH, value="(//*[text()[contains(.,'Арина')]]/ancestor::div[contains(@id, 'cfw')]//*[@value='mg_gos_page_callback'])[1]")
    print('     ОК: "Меры поддержки - Начинающий фермер", форма с Ариной, lgForm')
except Exception as e:
    error_msg = str(e).split('\n')[0]
    print('Ошибка: "Меры поддержки - Начинающий фермер", форма с Ариной, lgForm — ', error_msg)
try:
    driver.find_element(by=By.XPATH, value="(//*[text()[contains(.,'Арина')]]/ancestor::*[contains(@id, 'cfw')]//div[text()[contains(., 'Напишу вам в WhatsApp,')]])[2]")
    print("     ОК: 'Меры поддержки - Начинающий фермер', форма с Ариной, заголовок")
except Exception as e:
    error_msg = str(e).split('\n')[0]
    print("Ошибка: 'Меры поддержки - Начинающий фермер', форма с Ариной, заголовок — ", error_msg)

# 5.4 Меры поддержки - Агростартап, Арина - проверяю наличие правильного атрибута lgForm и заголовка
try:
    driver.get("https://moigektar.ru/documents/startup")
    driver.find_element(by=By.XPATH, value="(//*[text()[contains(.,'Арина')]]/ancestor::div[contains(@id, 'cfw')]//*[@value='mg_gos_page_callback'])[1]")
    print('     ОК: "Меры поддержки - Агростартап", форма с Ариной, lgForm')
except Exception as e:
    error_msg = str(e).split('\n')[0]
    print('Ошибка: "Меры поддержки - Агростартап", форма с Ариной, lgForm — ', error_msg)
try:
    driver.find_element(by=By.XPATH, value="(//*[text()[contains(.,'Арина')]]/ancestor::*[contains(@id, 'cfw')]//div[text()[contains(., 'Напишу вам в WhatsApp,')]])[2]")
    print("     ОК: 'Меры поддержки - Агростартап', форма с Ариной, заголовок")
except Exception as e:
    error_msg = str(e).split('\n')[0]
    print("Ошибка: 'Меры поддержки - Агростартап', форма с Ариной, заголовок — ", error_msg)

# 5.5 Меры поддержки - Семейная ферма, Арина - проверяю наличие правильного атрибута lgForm и заголовка
try:
    driver.get("https://moigektar.ru/documents/family")
    driver.find_element(by=By.XPATH, value="(//*[text()[contains(.,'Арина')]]/ancestor::div[contains(@id, 'cfw')]//*[@value='mg_gos_page_callback'])[1]")
    print('     ОК: "Меры поддержки - Семейная ферма", форма с Ариной, lgForm')
except Exception as e:
    error_msg = str(e).split('\n')[0]
    print('Ошибка: "Меры поддержки - Семейная ферма", форма с Ариной, lgForm — ', error_msg)
try:
    driver.find_element(by=By.XPATH, value="(//*[text()[contains(.,'Арина')]]/ancestor::*[contains(@id, 'cfw')]//div[text()[contains(., 'Напишу вам в WhatsApp,')]])[2]")
    print("     ОК: 'Меры поддержки - Семейная ферма', форма с Ариной, заголовок")
except Exception as e:
    error_msg = str(e).split('\n')[0]
    print("Ошибка: 'Меры поддержки - Семейная ферма', форма с Ариной, заголовок — ", error_msg)

# 5.6 Меры поддержки - Сельская ипотека, Арина - проверяю наличие правильного атрибута lgForm и заголовка
try:
    driver.get("https://moigektar.ru/documents/ipoteka")
    driver.find_element(by=By.XPATH, value="(//*[text()[contains(.,'Арина')]]/ancestor::div[contains(@id, 'cfw')]//*[@value='mg_gos_page_callback'])[1]")
    print('     ОК: "Меры поддержки - Сельская ипотека", форма с Ариной, lgForm')
except Exception as e:
    error_msg = str(e).split('\n')[0]
    print('Ошибка: "Меры поддержки - Сельская ипотека", форма с Ариной, lgForm — ', error_msg)
try:
    driver.find_element(by=By.XPATH, value="(//*[text()[contains(.,'Арина')]]/ancestor::*[contains(@id, 'cfw')]//div[text()[contains(., 'Напишу вам в WhatsApp,')]])[2]")
    print("     ОК: 'Меры поддержки - Сельская ипотека', форма с Ариной, заголовок")
except Exception as e:
    error_msg = str(e).split('\n')[0]
    print("Ошибка: 'Меры поддержки - Сельская ипотека', форма с Ариной, заголовок — ", error_msg)


# 6. Проверка раздела "Вопрос-ответ"
# Инлайн-форма Юлия - проверяю наличие правильного атрибута lgForm и заголовка
try:
    driver.get("https://moigektar.ru/faq")
    driver.find_element(by=By.XPATH, value="(//*[text()[contains(.,'Юлия')]]/ancestor::div[contains(@id, 'cfw')]//*[@value='mg_question_page_adamova_callback'])[1]")
    print('     ОК: "Вопрос-ответ", форма с Юлией, lgForm')
except Exception as e:
    error_msg = str(e).split('\n')[0]
    print('Ошибка: "Вопрос-ответ", форма с Юлией, lgForm — ', error_msg)
try:
    driver.find_element(by=By.XPATH, value="(//*[text()[contains(.,'Юлия')]]/ancestor::*[contains(@id, 'cfw')]//div[text()[contains(., 'я вас проконсультирую')]])[1]")
    print('     ОК: "Вопрос-ответ", форма с Юлией, заголовок')
except Exception as e:
    error_msg = str(e).split('\n')[0]
    print('Ошибка: "Вопрос-ответ", форма с Юлией, заголовок — ', error_msg)


# 7. Проверка детальной страницы новости
# 7.1 Инлайн-форма Арина - проверяю наличие правильного атрибута lgForm и заголовка
try:
    driver.get("https://moigektar.ru/news/keys-statya-proekta-moy-gektar-dom-nikity-lovicha-usadba-v-zavidovo-W2fdhFEXcn")
    driver.find_element(by=By.XPATH, value="(//*[text()[contains(.,'Арина')]]/ancestor::div[contains(@id, 'cfw')]//*[@value='mg_news_page_callback'])[1]")
    print('     ОК: детальная страница новости, форма с Ариной, lgForm')
except Exception as e:
    error_msg = str(e).split('\n')[0]
    print('Ошибка: детальная страница новости, форма с Ариной, lgForm — ', error_msg)
try:
    driver.find_element(by=By.XPATH, value="(//*[text()[contains(.,'Арина')]]/ancestor::*[contains(@id, 'cfw')]//div[text()[contains(., 'Напишу вам в WhatsApp,')]])[2]")
    print("     ОК: детальная страница новости, форма с Ариной, заголовок")
except Exception as e:
    error_msg = str(e).split('\n')[0]
    print("Ошибка: детальная страница новости, форма с Ариной, заголовок — ", error_msg)


# 8. Проверка раздела "Акции"
# 8.1 Основная страница, Максим - проверяю наличие правильного атрибута lgForm и заголовка
try:
    driver.get("https://moigektar.ru/actions")
    driver.find_element(by=By.XPATH, value="(//*[text()[contains(.,'Максим')]]/ancestor::div[contains(@id, 'cfw')]//*[@value='mg_action_main_page_max_callback'])[1]")
    print('     ОК: Акции - Основная, форма с Максимом, lgForm')
except Exception as e:
    error_msg = str(e).split('\n')[0]
    print('Ошибка: Акции - Основная, форма с Максимом, lgForm — ', error_msg)
try:
    driver.find_element(by=By.XPATH, value="(//*[text()[contains(.,'Максим')]]/ancestor::*[contains(@id, 'cfw')]//div[text()[contains(., 'я вас проконсультирую')]])[1]")
    print("     ОК: Акции - Основная, форма с Максимом, заголовок")
except Exception as e:
    error_msg = str(e).split('\n')[0]
    print("Ошибка: Акции - Основная, форма с Максимом, заголовок — ", error_msg)

# 8.2 Страница 1 - проверяю наличие правильного атрибута lgForm и заголовка
try:
    driver.get("https://moigektar.ru/actions/1")
    driver.find_element(by=By.XPATH, value="(//*[text()[contains(.,'Арина')]]/ancestor::div[contains(@id, 'cfw')]//*[@value='mg_action_page_large_family_callback'])[1]")
    print('     ОК: Акции - страница 1, форма с Ариной, lgForm')
except Exception as e:
    error_msg = str(e).split('\n')[0]
    print('Ошибка: Акции - страница 1, форма с Ариной, lgForm — ', error_msg)
try:
    driver.find_element(by=By.XPATH, value="(//*[text()[contains(.,'Арина')]]/ancestor::*[contains(@id, 'cfw')]//div[text()[contains(., 'я вас проконсультирую')]])[1]")
    print("     ОК: Акции - страница 1, форма с Ариной, заголовок")
except Exception as e:
    error_msg = str(e).split('\n')[0]
    print("Ошибка: Акции - страница 1, форма с Ариной, заголовок — ", error_msg)

# 8.3 Страница 2 - проверяю наличие правильного атрибута lgForm и заголовка
try:
    driver.get("https://moigektar.ru/actions/2")
    driver.find_element(by=By.XPATH, value="(//*[text()[contains(.,'Максим')]]/ancestor::div[contains(@id, 'cfw')]//*[@value='mg_action_page_svo_callback'])[1]")
    print('     ОК: Акции - страница 2, форма с Максимом, lgForm')
except Exception as e:
    error_msg = str(e).split('\n')[0]
    print('Ошибка: Акции - страница 2, форма с Максимом, lgForm — ', error_msg)
try:
    driver.find_element(by=By.XPATH, value="(//*[text()[contains(.,'Максим')]]/ancestor::*[contains(@id, 'cfw')]//div[text()[contains(., 'я вас проконсультирую')]])[1]")
    print("     ОК: Акции - страница 2, форма с Максимом, заголовок")
except Exception as e:
    error_msg = str(e).split('\n')[0]
    print("Ошибка: Акции - страница 2, форма с Максимом, заголовок — ", error_msg)

# 8.4 Страница 3 - проверяю наличие правильного атрибута lgForm и заголовка
try:
    driver.get("https://moigektar.ru/actions/3")
    driver.find_element(by=By.XPATH, value="(//*[text()[contains(.,'Андрей')]]/ancestor::div[contains(@id, 'cfw')]//*[@value='mg_action_page_veteran_callback'])[1]")
    print('     ОК: Акции - страница 3, форма с Андреем, lgForm')
except Exception as e:
    error_msg = str(e).split('\n')[0]
    print('Ошибка: Акции - страница 3, форма с Андреем, lgForm — ', error_msg)
try:
    driver.find_element(by=By.XPATH, value="(//*[text()[contains(.,'Андрей')]]/ancestor::*[contains(@id, 'cfw')]//div[text()[contains(., 'я вас проконсультирую')]])[1]")
    print("     ОК: Акции - страница 3, форма с Андреем, заголовок")
except Exception as e:
    error_msg = str(e).split('\n')[0]
    print("Ошибка: Акции - страница 3, форма с Андреем, заголовок — ", error_msg)

# 8.5 Страница 4 - проверяю наличие правильного атрибута lgForm и заголовка
try:
    driver.get("https://moigektar.ru/actions/4")
    driver.find_element(by=By.XPATH, value="(//*[text()[contains(.,'София')]]/ancestor::div[contains(@id, 'cfw')]//*[@value='mg_action_page_facilities_callback'])[1]")
    print('     ОК: Акции - страница 4, форма с Софией, lgForm')
except Exception as e:
    error_msg = str(e).split('\n')[0]
    print('Ошибка: Акции - страница 4, форма с Софией, lgForm — ', error_msg)
try:
    driver.find_element(by=By.XPATH, value="(//*[text()[contains(.,'София')]]/ancestor::*[contains(@id, 'cfw')]//div[text()[contains(., 'я вас проконсультирую')]])[1]")
    print("     ОК: Акции - страница 4, форма с Софией, заголовок")
except Exception as e:
    error_msg = str(e).split('\n')[0]
    print("Ошибка: Акции - страница 4, форма с Софией, заголовок — ", error_msg)

# 8.6 Страница 5 - проверяю наличие правильного атрибута lgForm и заголовка
try:
    driver.get("https://moigektar.ru/actions/5")
    driver.find_element(by=By.XPATH, value="(//*[text()[contains(.,'Арина')]]/ancestor::div[contains(@id, 'cfw')]//*[@value='mg_action_page_certificate_friend_callback'])[1]")
    print('     ОК: Акции - страница 5, форма с Ариной, lgForm')
except Exception as e:
    error_msg = str(e).split('\n')[0]
    print('Ошибка: Акции - страница 5, форма с Ариной, lgForm — ', error_msg)
try:
    driver.find_element(by=By.XPATH, value="(//*[text()[contains(.,'Арина')]]/ancestor::*[contains(@id, 'cfw')]//div[text()[contains(., 'я вас проконсультирую')]])[1]")
    print("     ОК: Акции - страница 5, форма с Ариной, заголовок")
except Exception as e:
    error_msg = str(e).split('\n')[0]
    print("Ошибка: Акции - страница 5, форма с Ариной, заголовок — ", error_msg)

# 8.7 Страница 6 - проверяю наличие правильного атрибута lgForm и заголовка
try:
    driver.get("https://moigektar.ru/actions/6")
    driver.find_element(by=By.XPATH, value="(//*[text()[contains(.,'Андрей')]]/ancestor::div[contains(@id, 'cfw')]//*[@value='mg_action_page_refugees_callback'])[1]")
    print('     ОК: Акции - страница 6, форма с Андреем, lgForm')
except Exception as e:
    error_msg = str(e).split('\n')[0]
    print('Ошибка: Акции - страница 6, форма с Андреем, lgForm — ', error_msg)
try:
    driver.find_element(by=By.XPATH, value="(//*[text()[contains(.,'Андрей')]]/ancestor::*[contains(@id, 'cfw')]//div[text()[contains(., 'я вас проконсультирую')]])[1]")
    print("     ОК: Акции - страница 6, форма с Андреем, заголовок")
except Exception as e:
    error_msg = str(e).split('\n')[0]
    print("Ошибка: Акции - страница 6, форма с Андреем, заголовок — ", error_msg)

# 8.8 Страница 7 - проверяю наличие правильного атрибута lgForm и заголовка
try:
    driver.get("https://moigektar.ru/actions/7")
    driver.find_element(by=By.XPATH, value="(//*[text()[contains(.,'Максим')]]/ancestor::div[contains(@id, 'cfw')]//*[@value='mg_action_page_certificate_self_callback'])[1]")
    print('     ОК: Акции - страница 7, форма с Максимом, lgForm')
except Exception as e:
    error_msg = str(e).split('\n')[0]
    print('Ошибка: Акции - страница 7, форма с Максимом, lgForm — ', error_msg)
try:
    driver.find_element(by=By.XPATH, value="(//*[text()[contains(.,'Максим')]]/ancestor::*[contains(@id, 'cfw')]//div[text()[contains(., 'я вас проконсультирую')]])[1]")
    print("     ОК: Акции - страница 7, форма с Максимом, заголовок")
except Exception as e:
    error_msg = str(e).split('\n')[0]
    print("Ошибка: Акции - страница 7, форма с Максимом, заголовок — ", error_msg)


# 9. Проверка раздела "Фонд добра"
# 9.1 Инлайн-форма Юлия - проверяю наличие правильного атрибута lgForm и заголовка
try:
    driver.get("https://moigektar.ru/good-fund")
    driver.find_element(by=By.XPATH, value="(//*[text()[contains(.,'гораздо')]]/ancestor::div[contains(@id, 'cfw')]//*[@value='mg_fond_dobra_callback'])[1]")
    print('     ОК: Фонд добра, форма с Юлией, lgForm')
except Exception as e:
    error_msg = str(e).split('\n')[0]
    print('Ошибка: Фонд добра, форма с Юлией, lgForm — ', error_msg)
try:
    driver.find_element(by=By.XPATH, value="(//*[text()[contains(.,'гораздо')]]/ancestor::*[contains(@id, 'cfw')]//div[text()[contains(., 'я вас проконсультирую')]])[1]")
    print('     ОК: Фонд добра, форма с Юлией, заголовок')
except Exception as e:
    error_msg = str(e).split('\n')[0]
    print('Ошибка: Фонд добра, форма с Юлией, заголовок — ', error_msg)


# 10. Проверка раздела "Вакансии"
# 10.1 Инлайн-форма Юлия - проверяю наличие правильного атрибута lgForm и заголовка
try:
    driver.get("https://moigektar.ru/hr")
    driver.find_element(by=By.XPATH, value="(//*[text()[contains(.,'Юлия')]]/ancestor::div[contains(@id, 'cfw')]//*[@value='callback_hr_form'])[1]")
    print('     ОК: Вакансии, форма с Юлией, lgForm')
except Exception as e:
    error_msg = str(e).split('\n')[0]
    print('Ошибка: Вакансии, форма с Юлией, lgForm — ', error_msg)
try:
    driver.find_element(by=By.XPATH, value="(//*[text()[contains(.,'Юлия')]]/ancestor::*[contains(@id, 'cfw')]//div[text()[contains(., 'я вас проконсультирую')]])[2]")
    print('     ОК: Вакансии, форма с Юлией, заголовок')
except Exception as e:
    error_msg = str(e).split('\n')[0]
    print('Ошибка: Вакансии, форма с Юлией, заголовок — ', error_msg)


# 11. Проверка раздела "Контакты"
# 11.1 Инлайн-форма Арина - проверяю наличие правильного атрибута lgForm и заголовка
try:
    driver.get("https://moigektar.ru/contacts")
    driver.find_element(by=By.XPATH, value="(//*[text()[contains(.,'Арина')]]/ancestor::div[contains(@id, 'cfw')]//*[@value='mg_contact_page_callback'])[1]")
    print('     ОК: Контакты, форма с Ариной, lgForm')
except Exception as e:
    error_msg = str(e).split('\n')[0]
    print('Ошибка: Контакты, форма с Ариной, lgForm — ', error_msg)
try:
    driver.find_element(by=By.XPATH, value="(//*[text()[contains(.,'Арина')]]/ancestor::*[contains(@id, 'cfw')]//div[text()[contains(., 'оставьте свой номер')]])[2]")
    print("     ОК: Контакты, форма с Ариной, заголовок")
except Exception as e:
    error_msg = str(e).split('\n')[0]
    print("Ошибка: Контакты, форма с Ариной, заголовок — ", error_msg)


# 12. Проверка раздела "Глэмпинг"
# 12.1 Инлайн-форма Андрей - проверяю наличие правильного атрибута lgForm и заголовка
try:
    driver.get("https://moigektar.ru/goal/glamping")
    driver.find_element(by=By.XPATH, value="(//*[text()[contains(.,'Андрей')]]/ancestor::div[contains(@id, 'cfw')]//*[@value='mg_glamping_page_andrey_callback'])[1]")
    print('     ОК: Глэмпинг, форма с Андреем, lgForm')
except Exception as e:
    error_msg = str(e).split('\n')[0]
    print('Ошибка: Глэмпинг, форма с Андреем, lgForm — ', error_msg)
try:
    driver.find_element(by=By.XPATH, value="(//*[text()[contains(.,'Андрей')]]/ancestor::*[contains(@id, 'cfw')]//div[text()[contains(., 'я вас проконсультирую')]])[1]")
    print("     ОК: Глэмпинг, форма с Андреем, заголовок")
except Exception as e:
    error_msg = str(e).split('\n')[0]
    print("Ошибка: Глэмпинг, форма с Андреем, заголовок — ", error_msg)


# 13. Проверка раздела "Фермы и агробизнес"
# 13.1 Инлайн-форма Андрей - проверяю наличие правильного атрибута lgForm и заголовка
try:
    driver.get("https://moigektar.ru/goal/farm")
    driver.find_element(by=By.XPATH, value="(//*[text()[contains(.,'Андрей')]]/ancestor::div[contains(@id, 'cfw')]//*[@value='mg_farm_page_andrey_callback'])[1]")
    print('     ОК: Фермы и агробизнес, форма с Андреем, lgForm')
except Exception as e:
    error_msg = str(e).split('\n')[0]
    print('Ошибка: Фермы и агробизнес, форма с Андреем, lgForm — ', error_msg)
try:
    driver.find_element(by=By.XPATH, value="(//*[text()[contains(.,'Андрей')]]/ancestor::*[contains(@id, 'cfw')]//div[text()[contains(., 'я вас проконсультирую')]])[1]")
    print("     ОК: Фермы и агробизнес, форма с Андреем, заголовок")
except Exception as e:
    error_msg = str(e).split('\n')[0]
    print("Ошибка: Фермы и агробизнес, форма с Андреем, заголовок — ", error_msg)


# 14. Проверка раздела "Родовые поселения"
# 14.1 Инлайн-форма Андрей - проверяю наличие правильного атрибута lgForm и заголовка
try:
    driver.get("https://moigektar.ru/goal/settlements")
    driver.find_element(by=By.XPATH, value="(//*[text()[contains(.,'Андрей')]]/ancestor::div[contains(@id, 'cfw')]//*[@value='mg_settlements_page_andrey_callback'])[1]")
    print('     ОК: Родовые поселения, форма с Андреем, lgForm')
except Exception as e:
    error_msg = str(e).split('\n')[0]
    print('Ошибка: Родовые поселения, форма с Андреем, lgForm — ', error_msg)
try:
    driver.find_element(by=By.XPATH, value="(//*[text()[contains(.,'Андрей')]]/ancestor::*[contains(@id, 'cfw')]//div[text()[contains(., 'я вас проконсультирую')]])[1]")
    print("     ОК: Родовые поселения, форма с Андреем, заголовок")
except Exception as e:
    error_msg = str(e).split('\n')[0]
    print("Ошибка: Родовые поселения, форма с Андреем, заголовок — ", error_msg)


# 15. Проверка раздела "Подарочный сертификат"
# 15.1 Инлайн-форма Андрей - проверяю наличие правильного атрибута lgForm и заголовка
try:
    driver.get("https://moigektar.ru/gift")
    driver.find_element(by=By.XPATH, value="(//*[text()[contains(.,'Арина')]]/ancestor::div[contains(@id, 'cfw')]//*[@value='mg_gift_page_callback'])[1]")
    print('     ОК: Подарочный сертификат, форма с Ариной, lgForm')
except Exception as e:
    error_msg = str(e).split('\n')[0]
    print('Ошибка: Подарочный сертификат, форма с Ариной, lgForm — ', error_msg)
try:
    driver.find_element(by=By.XPATH, value="(//*[text()[contains(.,'Арина')]]/ancestor::*[contains(@id, 'cfw')]//div[text()[contains(., 'оставьте свой номер')]])[2]")
    print("     ОК: Подарочный сертификат, форма с Ариной, заголовок")
except Exception as e:
    error_msg = str(e).split('\n')[0]
    print("Ошибка: Подарочный сертификат, форма с Ариной, заголовок — ", error_msg)


# 16. Проверка раздела "Вебинары"
# 16.1 "Узнай, как заработать на гектаре"
# 1-я инлайн-форма - проверяю наличие правильного атрибута lgForm и заголовка
try:
    driver.get("https://moigektar.ru/webinar/invest")
    driver.find_element(by=By.XPATH, value="(//*[text()[contains(.,'вебинара')]]/ancestor::div[contains(@id, 'cfw')]//*[@value='mg_webinar'])[1]")
    print('     ОК: Вебинар "Как заработать на гектаре", 1-я инлайн-форма, lgForm')
except Exception as e:
    error_msg = str(e).split('\n')[0]
    print('Ошибка: Вебинар "Как заработать на гектаре", 1-я инлайн-форма, lgForm — ', error_msg)


# 17. Проверка раздела "Личный кабинет"
# 17.1 Инлайн-форма с Ариной, проверяю наличие правильного атрибута lgForm и заголовка
try:
    driver.get("https://moigektar.ru/cabinet")
    driver.find_element(by=By.XPATH, value="(//*[text()[contains(.,'Арина')]]/ancestor::div[contains(@id, 'cfw')]//*[@value='mg_lk_page_page_arina_callback'])[1]")
    print('     ОК: раздел личного кабинета, форма с Ариной, lgForm')
except Exception as e:
    error_msg = str(e).split('\n')[0]
    print('Ошибка: раздел личного кабинета, форма с Ариной, lgForm — ', error_msg)
try:
    driver.find_element(by=By.XPATH, value="(//*[text()[contains(.,'Арина')]]/ancestor::*[contains(@id, 'cfw')]//div[text()[contains(., 'я вас проконсультирую')]])[1]")
    print("     ОК: раздел личного кабинет, форма с Ариной, заголовок")
except Exception as e:
    error_msg = str(e).split('\n')[0]
    print("Ошибка: раздел личного кабинет, форма с Ариной, заголовок — ", error_msg)
# 17.2 Инлайн-форма с Игорем, проверяю наличие правильного атрибута lgForm и заголовка
try:
    driver.get("https://moigektar.ru/cabinet")
    driver.find_element(by=By.XPATH, value="(//*[text()[contains(.,'Игорь')]]/ancestor::div[contains(@id, 'cfw')]//*[@value='mg_lk_page_kalinin_callback'])[1]")
    print('     ОК: раздел личного кабинета, форма с Игорем, lgForm')
except Exception as e:
    error_msg = str(e).split('\n')[0]
    print('Ошибка: раздел личного кабинета, форма с Игорем, lgForm — ', error_msg)
try:
    driver.find_element(by=By.XPATH, value="(//*[text()[contains(.,'Игорь')]]/ancestor::*[contains(@id, 'cfw')]//div[text()[contains(., 'к личному кабинету')]])[1]")
    print("     ОК: раздел личного кабинет, форма с Игорем, заголовок")
except Exception as e:
    error_msg = str(e).split('\n')[0]
    print("Ошибка: раздел личного кабинет, форма с Игорем, заголовок — ", error_msg)


# 18. Проверка раздела регистрации от стойки
# 18.1 Инлайн-форма "Оставьте заявку ...", проверяю наличие правильного атрибута lgForm и заголовка
try:
    driver.get("https://moigektar.ru/public-event")
    driver.find_element(by=By.XPATH, value="(//*[text()[contains(.,'Оставьте')]]/ancestor::div[contains(@id, 'cfw')]//*[@value='public-event'])[1]")
    print('     ОК: раздел регистрации от стойки, инлайн-форма, lgForm')
except Exception as e:
    error_msg = str(e).split('\n')[0]
    print('Ошибка: раздел регистрации от стойки, инлайн-форма, lgForm — ', error_msg)


# 19. Проверка раздела закрытого предложения
# 19.1 Инлайн-форма "Узнать о закрытом предложении", проверяю наличие правильного атрибута lgForm и заголовка
try:
    driver.get("https://moigektar.ru/closed-offer")
    driver.find_element(by=By.XPATH, value="//*[text()[contains(.,'закрытом')]]/ancestor::div//*[@value='lg_closed_offer']")
    print('     ОК: раздел закрытого предложения, инлайн-форма, lgForm')
except Exception as e:
    error_msg = str(e).split('\n')[0]
    print('Ошибка: раздел закрытого предложения, инлайн-форма, lgForm — ', error_msg)

time.sleep(5)
driver.quit()


