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
    
# Скрипт заполняет каждую форму корректными данными
#
# В лог выводится сообщение "ОК", если данные были отправлены и отобразилось сообщение об успехе
# В лог выводится сообщение "ERROR", если это сообщение не отобразилось
# В лог выводится сообщение "ERROR", если форма не была найдена по селектору
#


# 1. проверка главной страницы "МГ"

# избавляемся от поп-апа, который перекрывает доступ ко кнопкам
try:
    driver.get("http://moigektar.ru")
    time.sleep(1)
    popup_w = driver.find_element(by=By.XPATH, value="//div[@id='visitors-popup']")
    driver.execute_script("""
    var auth_win = arguments[0];
    auth_win.remove();
    """, popup_w)
except:
    print("Popup not found")

# 1.1 проверка формы "Оставьте заявку", Арина
# проверяю отправку данных через форму
# проверяю наличие правильного атрибута lgForm
try:
    title = driver.find_element(by=By.XPATH, value="/descendant::*[text()[contains(.,'Арина')]][2]")
    # сохраняю текущий динамический id формы в переменную для того, чтобы последующие локаторы не были такого вида:
    # //h1/*[text()[contains(.,'Хотите узнать')]]//parent::h1//following-sibling::ul[2]//input[@id='consultationform-phone']
    form_id = driver.find_element(by=By.XPATH, value="(//*[text()[contains(.,'Арина')]]/ancestor::div[contains(@id, 'cfw')])[1]").get_attribute("id")
    actions.move_to_element(title).perform()
    driver.find_element(by=By.XPATH, value="(//div[@id='"+ form_id +"']//*[@id='consultationform-phone'])[1]").send_keys(str(data["test_data_valid"]["phone"]))
    driver.find_element(by=By.XPATH, value="(//div[@id='"+ form_id +"']//*[text()[contains(.,'Отправить')]])[1]").click()
    try:
        name_input = driver.find_element(by=By.XPATH, value="(//div[@id='"+ form_id +"']//*[@id='consultationform-name'])[2]")
        name_input.click()
        print("     ОК: главная, форма с Ариной, отправка через форму")
    except Exception as e:
        error_msg = str(e).split('\n')[0]
        print("Ошибка: главная, форма с Ариной, отправка через форму — ", error_msg)
    try:
        driver.find_element(by=By.XPATH, value="(//div[@id='"+ form_id +"']//*[@value='mg_main_page_arina_callback'])[2]")
        print("     ОК: главная, форма с Ариной, lgForm")
    except Exception as e:
        error_msg = str(e).split('\n')[0]
        print("Ошибка: главная, форма с Ариной, lgForm — ", error_msg)
except Exception as e:
        error_msg = str(e).split('\n')[0]
        print("Ошибка: главная, форма с Ариной — ", error_msg)

# 1.2 проверка формы "Оставьте заявку", Андрей - проверяю наличие правильного атрибута lgForm
try:
    form_id = driver.find_element(by=By.XPATH, value="(//*[text()[contains(.,'Андрей')]]/ancestor::div[contains(@id, 'cfw')]//*[@value='mg_main_page_andrey_callback'])[1]")
    print("     ОК: главная, форма с Андреем, lgForm")
except Exception as e:
    error_msg = str(e).split('\n')[0]
    print("Ошибка: главная, форма с Андреем, lgForm — ", error_msg)

# 1.3 проверка формы "Оставьте заявку", София - проверяю наличие правильного атрибута lgForm
try:
    form_id = driver.find_element(by=By.XPATH, value="(//*[text()[contains(.,'София')]]/ancestor::div[contains(@id, 'cfw')]//*[@value='mg_main_page_sofia_callback'])[1]")
    print("     ОК: главная, форма с Софией, lgForm")
except Exception as e:
    error_msg = str(e).split('\n')[0]
    print("Ошибка: главная, форма с Софией, lgForm — ", error_msg)

# 1.4 проверка формы "Оставьте заявку", Максим - проверяю наличие правильного атрибута lgForm
try:
    form_id = driver.find_element(by=By.XPATH, value="(//*[text()[contains(.,'Максим')]]/ancestor::div[contains(@id, 'cfw')]//*[@value='mg_main_page_max_callback'])[1]")
    print("     ОК: главная, форма с Максимом, lgForm")
except Exception as e:
    error_msg = str(e).split('\n')[0]
    print("Ошибка: главная, форма с Максимом, lgForm — ", error_msg)


# 2. Проверка каталога
# 2.1 каталог, проверка формы "Оставьте заявку", Арина - проверяю наличие правильного атрибута lgForm
try:
    driver.get("https://moigektar.ru/catalogue-no-auth")
    actions.send_keys(Keys.PAGE_DOWN).send_keys(Keys.PAGE_DOWN).perform()
    time.sleep(2)
    actions.send_keys(Keys.PAGE_DOWN).send_keys(Keys.PAGE_DOWN).perform()
    time.sleep(2)
    actions.send_keys(Keys.PAGE_DOWN).send_keys(Keys.PAGE_DOWN).perform()
    form_id = driver.find_element(by=By.XPATH, value="(//*[text()[contains(.,'Арина')]]/ancestor::div[contains(@id, 'cfw')]//*[@value='mg_catalog_arina_callback'])[1]")
    print("     ОК: каталог, форма с Ариной, lgForm")
except Exception as e:
    error_msg = str(e).split('\n')[0]
    print("Ошибка: каталог, форма с Ариной, lgForm — ", error_msg)

# 2.2 страница актива, проверка формы "Оставьте заявку", Арина - проверяю наличие правильного атрибута lgForm
try:
    driver.get("https://moigektar.ru/batches/44607")
    form_id = driver.find_element(by=By.XPATH, value="(//*[text()[contains(.,'Арина')]]/ancestor::div[contains(@id, 'cfw')]//*[@value='mg_batch_page_arina_callback'])[1]")
    print("     ОК: стр. актива, форма с Ариной, lgForm")
except Exception as e:
    error_msg = str(e).split('\n')[0]
    print("Ошибка: стр. актива, форма с Ариной, lgForm — ", error_msg)


# 3. Проверка раздела "О проекте"
# 3.1 О проекте - основная страница, Арина - проверяю наличие правильного атрибута lgForm
try:
    driver.get("https://moigektar.ru/about")
    form_id = driver.find_element(by=By.XPATH, value="(//*[text()[contains(.,'Арина')]]/ancestor::div[contains(@id, 'cfw')]//*[@value='mg_about_page_callback'])[1]")
    print('     ОК: "О проекте", форма с Ариной, lgForm')
except Exception as e:
    error_msg = str(e).split('\n')[0]
    print('Ошибка: "О проекте", форма с Ариной, lgForm — ', error_msg)

# 3.2 О проекте - Партнеры, Арина - проверяю наличие правильного атрибута lgForm
try:
    driver.get("https://moigektar.ru/about/advantages")
    form_id = driver.find_element(by=By.XPATH, value="(//*[text()[contains(.,'Арина')]]/ancestor::div[contains(@id, 'cfw')]//*[@value='mg_about_partners_page_callback'])[1]")
    print('     ОК: "О проекте - Партнеры", форма с Ариной, lgForm')
except Exception as e:
    error_msg = str(e).split('\n')[0]
    print('Ошибка: "О проекте - Партнеры", форма с Ариной, lgForm — ', error_msg)

# 3.3 О проекте - Союз садоводов, Арина - проверяю наличие правильного атрибута lgForm
try:
    driver.get("https://moigektar.ru/about/union")
    form_id = driver.find_element(by=By.XPATH, value="(//*[text()[contains(.,'Арина')]]/ancestor::div[contains(@id, 'cfw')]//*[@value='mg_about_union_page_callback'])[1]")
    print('     ОК: "О проекте - Союз садоводов", форма с Ариной, lgForm')
except Exception as e:
    error_msg = str(e).split('\n')[0]
    print('Ошибка: "О проекте - Союз садоводов", форма с Ариной, lgForm — ', error_msg)

# 3.4 О проекте - Отзывы, Арина - проверяю наличие правильного атрибута lgForm
try:
    driver.get("https://moigektar.ru/about/reviews")
    form_id = driver.find_element(by=By.XPATH, value="(//*[text()[contains(.,'Арина')]]/ancestor::div[contains(@id, 'cfw')]//*[@value='mg_about_reviews_page_callback'])[1]")
    print('     ОК: "О проекте - Отзывы", форма с Ариной, lgForm')
except Exception as e:
    error_msg = str(e).split('\n')[0]
    print('Ошибка: "О проекте - Отзывы", форма с Ариной, lgForm — ', error_msg)


# 4. Проверка раздела "Развитие"
# 4.1 Развитие - Развитие поселков, Арина - проверяю наличие правильного атрибута lgForm
try:
    driver.get("https://moigektar.ru/growth")
    form_id = driver.find_element(by=By.XPATH, value="(//*[text()[contains(.,'Арина')]]/ancestor::div[contains(@id, 'cfw')]//*[@value='mg_growth_page_callback'])[1]")
    print('     ОК: "Развитие - Развитие поселков", форма с Ариной, lgForm')
except Exception as e:
    error_msg = str(e).split('\n')[0]
    print('Ошибка: "Развитие - Развитие поселков", форма с Ариной, lgForm — ', error_msg)

# 4.2 Развитие - Глазами инвестора, Арина - проверяю наличие правильного атрибута lgForm
try:
    driver.get("https://moigektar.ru/investment")
    form_id = driver.find_element(by=By.XPATH, value="(//*[text()[contains(.,'Арина')]]/ancestor::div[contains(@id, 'cfw')]//*[@value='mg_investment_page_callback'])[1]")
    print('     ОК: "Развитие - Глазами инвестора", форма с Ариной, lgForm')
except Exception as e:
    error_msg = str(e).split('\n')[0]
    print('Ошибка: "Развитие - Глазами инвестора", форма с Ариной, lgForm — ', error_msg)

# 4.3 Развитие - Капитализация, Арина - проверяю наличие правильного атрибута lgForm
try:
    driver.get("https://moigektar.ru/investment/capitalization")
    form_id = driver.find_element(by=By.XPATH, value="(//*[text()[contains(.,'Арина')]]/ancestor::div[contains(@id, 'cfw')]//*[@value='mg_capitalization_page_callback'])[1]")
    print('     ОК: "Развитие - Капитализация", форма с Ариной, lgForm')
except Exception as e:
    error_msg = str(e).split('\n')[0]
    print('Ошибка: "Развитие - Капитализация", форма с Ариной, lgForm — ', error_msg)

# 4.4 Развитие - Базовая стратегия, Арина - проверяю наличие правильного атрибута lgForm
try:
    driver.get("https://moigektar.ru/investment/basic")
    form_id = driver.find_element(by=By.XPATH, value="(//*[text()[contains(.,'Арина')]]/ancestor::div[contains(@id, 'cfw')]//*[@value='mg_invest_basic_page_callback'])[1]")
    print('     ОК: "Развитие - Базовая стратегия", форма с Ариной, lgForm')
except Exception as e:
    error_msg = str(e).split('\n')[0]
    print('Ошибка: "Развитие - Базовая стратегия", форма с Ариной, lgForm — ', error_msg)

# 4.5 Развитие - Предприниматель, Арина - проверяю наличие правильного атрибута lgForm
try:
    driver.get("https://moigektar.ru/investment/businessman")
    form_id = driver.find_element(by=By.XPATH, value="(//*[text()[contains(.,'Арина')]]/ancestor::div[contains(@id, 'cfw')]//*[@value='mg_invest_businessman_page_callback'])[1]")
    print('     ОК: "Развитие - Предприниматель", форма с Ариной, lgForm')
except Exception as e:
    error_msg = str(e).split('\n')[0]
    print('Ошибка: "Развитие - Предприниматель", форма с Ариной, lgForm — ', error_msg)

# 4.6 Развитие - Садовод, Арина - проверяю наличие правильного атрибута lgForm
try:
    driver.get("https://moigektar.ru/investment/farmer")
    form_id = driver.find_element(by=By.XPATH, value="(//*[text()[contains(.,'Арина')]]/ancestor::div[contains(@id, 'cfw')]//*[@value='mg_invest_farmer_page_callback'])[1]")
    print('     ОК: "Развитие - Садовод", форма с Ариной, lgForm')
except Exception as e:
    error_msg = str(e).split('\n')[0]
    print('Ошибка: "Развитие - Садовод", форма с Ариной, lgForm — ', error_msg)

# 4.7 Развитие - Усадьба, Арина - проверяю наличие правильного атрибута lgForm
try:
    driver.get("https://moigektar.ru/investment/family")
    form_id = driver.find_element(by=By.XPATH, value="(//*[text()[contains(.,'Арина')]]/ancestor::div[contains(@id, 'cfw')]//*[@value='mg_invest_family_page_callback'])[1]")
    print('     ОК: "Развитие - Усадьба", форма с Ариной, lgForm')
except Exception as e:
    error_msg = str(e).split('\n')[0]
    print('Ошибка: "Развитие - Усадьба", форма с Ариной, lgForm — ', error_msg)


# 5. Проверка раздела "Меры поддержки"
# 5.1 Меры поддержки - основная, Арина - проверяю наличие правильного атрибута lgForm
try:
    driver.get("https://moigektar.ru/documents/gos")
    form_id = driver.find_element(by=By.XPATH, value="(//*[text()[contains(.,'Арина')]]/ancestor::div[contains(@id, 'cfw')]//*[@value='mg_gos_page_callback'])[1]")
    print('     ОК: "Меры поддержки - основная", форма с Ариной, lgForm')
except Exception as e:
    error_msg = str(e).split('\n')[0]
    print('Ошибка: "Меры поддержки - основная", форма с Ариной, lgForm — ', error_msg)

# 5.2 Меры поддержки - Для владельцев земли, Арина - проверяю наличие правильного атрибута lgForm
try:
    driver.get("https://moigektar.ru/documents")
    form_id = driver.find_element(by=By.XPATH, value="(//*[text()[contains(.,'Арина')]]/ancestor::div[contains(@id, 'cfw')]//*[@value='mg_gos_page_callback'])[1]")
    print('     ОК: "Меры поддержки - Для владельцев земли", форма с Ариной, lgForm')
except Exception as e:
    error_msg = str(e).split('\n')[0]
    print('Ошибка: "Меры поддержки - Для владельцев земли", форма с Ариной, lgForm — ', error_msg)

# 5.3 Меры поддержки - Начинающий фермер, Арина - проверяю наличие правильного атрибута lgForm
try:
    driver.get("https://moigektar.ru/documents/farmer")
    form_id = driver.find_element(by=By.XPATH, value="(//*[text()[contains(.,'Арина')]]/ancestor::div[contains(@id, 'cfw')]//*[@value='mg_gos_page_callback'])[1]")
    print('     ОК: "Меры поддержки - Начинающий фермер", форма с Ариной, lgForm')
except Exception as e:
    error_msg = str(e).split('\n')[0]
    print('Ошибка: "Меры поддержки - Начинающий фермер", форма с Ариной, lgForm — ', error_msg)

# 5.4 Меры поддержки - Агростартап, Арина - проверяю наличие правильного атрибута lgForm
try:
    driver.get("https://moigektar.ru/documents/startup")
    form_id = driver.find_element(by=By.XPATH, value="(//*[text()[contains(.,'Арина')]]/ancestor::div[contains(@id, 'cfw')]//*[@value='mg_gos_page_callback'])[1]")
    print('     ОК: "Меры поддержки - Агростартап", форма с Ариной, lgForm')
except Exception as e:
    error_msg = str(e).split('\n')[0]
    print('Ошибка: "Меры поддержки - Агростартап", форма с Ариной, lgForm — ', error_msg)

# 5.5 Меры поддержки - Семейная ферма, Арина - проверяю наличие правильного атрибута lgForm
try:
    driver.get("https://moigektar.ru/documents/family")
    form_id = driver.find_element(by=By.XPATH, value="(//*[text()[contains(.,'Арина')]]/ancestor::div[contains(@id, 'cfw')]//*[@value='mg_gos_page_callback'])[1]")
    print('     ОК: "Меры поддержки - Семейная ферма", форма с Ариной, lgForm')
except Exception as e:
    error_msg = str(e).split('\n')[0]
    print('Ошибка: "Меры поддержки - Семейная ферма", форма с Ариной, lgForm — ', error_msg)

# 5.6 Меры поддержки - Сельская ипотека, Арина - проверяю наличие правильного атрибута lgForm
try:
    driver.get("https://moigektar.ru/documents/ipoteka")
    form_id = driver.find_element(by=By.XPATH, value="(//*[text()[contains(.,'Арина')]]/ancestor::div[contains(@id, 'cfw')]//*[@value='mg_gos_page_callback'])[1]")
    print('     ОК: "Меры поддержки - Сельская ипотека", форма с Ариной, lgForm')
except Exception as e:
    error_msg = str(e).split('\n')[0]
    print('Ошибка: "Меры поддержки - Сельская ипотека", форма с Ариной, lgForm — ', error_msg)


# 6. Проверка раздела "Вопрос-ответ"
# Инлайн-форма Юлия - проверяю наличие правильного атрибута lgForm
try:
    driver.get("https://moigektar.ru/faq")
    form_id = driver.find_element(by=By.XPATH, value="(//*[text()[contains(.,'Юлия')]]/ancestor::div[contains(@id, 'cfw')]//*[@value='mg_question_page_adamova_callback'])[1]")
    print('     ОК: "Вопрос-ответ", форма с Юлией, lgForm')
except Exception as e:
    error_msg = str(e).split('\n')[0]
    print('Ошибка: "Вопрос-ответ", форма с Юлией, lgForm — ', error_msg)


# 7. Проверка детальной страницы новости
# 7.1 Инлайн-форма Арина - проверяю наличие правильного атрибута lgForm
try:
    driver.get("https://moigektar.ru/news/novosti-servisnoy-kompanii-moy-gektar-za-period-11-17-iyulya-ob7OQtWgcC")
    form_id = driver.find_element(by=By.XPATH, value="(//*[text()[contains(.,'Арина')]]/ancestor::div[contains(@id, 'cfw')]//*[@value='mg_news_page_callback'])[1]")
    print('     ОК: детальная страница новости, форма с Ариной, lgForm')
except Exception as e:
    error_msg = str(e).split('\n')[0]
    print('Ошибка: детальная страница новости, форма с Ариной, lgForm — ', error_msg)


# 8. Проверка раздела "Акции"
# 8.1 Основная страница, Максим - проверяю наличие правильного атрибута lgForm
try:
    driver.get("https://moigektar.ru/actions")
    form_id = driver.find_element(by=By.XPATH, value="(//*[text()[contains(.,'Максим')]]/ancestor::div[contains(@id, 'cfw')]//*[@value='mg_action_main_page_max_callback'])[1]")
    print('     ОК: Акции - Основная, форма с Максимом, lgForm')
except Exception as e:
    error_msg = str(e).split('\n')[0]
    print('Ошибка: Акции - Основная, форма с Максимом, lgForm — ', error_msg)


# 9. Проверка раздела "Фонд добра"
# 9.1 Инлайн-форма Юлия - проверяю наличие правильного атрибута lgForm
try:
    driver.get("https://moigektar.ru/good-fund")
    form_id = driver.find_element(by=By.XPATH, value="(//*[text()[contains(.,'гораздо')]]/ancestor::div[contains(@id, 'cfw')]//*[@value='mg_fond_dobra_callback'])[1]")
    print('     ОК: Фонд добра, форма с Юлией, lgForm')
except Exception as e:
    error_msg = str(e).split('\n')[0]
    print('Ошибка: Фонд добра, форма с Юлией, lgForm — ', error_msg)


# 10. Проверка раздела "Вакансии"
# 10.1 Инлайн-форма Юлия - проверяю наличие правильного атрибута lgForm
try:
    driver.get("https://moigektar.ru/hr")
    form_id = driver.find_element(by=By.XPATH, value="(//*[text()[contains(.,'Юлия')]]/ancestor::div[contains(@id, 'cfw')]//*[@value='callback_hr_form'])[1]")
    print('     ОК: Вакансии, форма с Юлией, lgForm')
except Exception as e:
    error_msg = str(e).split('\n')[0]
    print('Ошибка: Вакансии, форма с Юлией, lgForm — ', error_msg)


# 11. Проверка раздела "Контакты"
# 11.1 Инлайн-форма Арина - проверяю наличие правильного атрибута lgForm
try:
    driver.get("https://moigektar.ru/contacts")
    form_id = driver.find_element(by=By.XPATH, value="(//*[text()[contains(.,'Арина')]]/ancestor::div[contains(@id, 'cfw')]//*[@value='mg_contact_page_callback'])[1]")
    print('     ОК: Контакты, форма с Ариной, lgForm')
except Exception as e:
    error_msg = str(e).split('\n')[0]
    print('Ошибка: Контакты, форма с Ариной, lgForm — ', error_msg)


# 12. Проверка раздела "Глэмпинг"
# 12.1 Инлайн-форма Андрей - проверяю наличие правильного атрибута lgForm
try:
    driver.get("https://moigektar.ru/goal/glamping")
    form_id = driver.find_element(by=By.XPATH, value="(//*[text()[contains(.,'Андрей')]]/ancestor::div[contains(@id, 'cfw')]//*[@value='mg_glamping_page_andrey_callback'])[1]")
    print('     ОК: Глэмпинг, форма с Андреем, lgForm')
except Exception as e:
    error_msg = str(e).split('\n')[0]
    print('Ошибка: Глэмпинг, форма с Андреем, lgForm — ', error_msg)


# 13. Проверка раздела "Фермы и агробизнес"
# 13.1 Инлайн-форма Андрей - проверяю наличие правильного атрибута lgForm
try:
    driver.get("https://moigektar.ru/goal/farm")
    form_id = driver.find_element(by=By.XPATH, value="(//*[text()[contains(.,'Андрей')]]/ancestor::div[contains(@id, 'cfw')]//*[@value='mg_farm_page_andrey_callback'])[1]")
    print('     ОК: Фермы и агробизнес, форма с Андреем, lgForm')
except Exception as e:
    error_msg = str(e).split('\n')[0]
    print('Ошибка: Фермы и агробизнес, форма с Андреем, lgForm — ', error_msg)


# 14. Проверка раздела "Родовые поселения"
# 14.1 Инлайн-форма Андрей - проверяю наличие правильного атрибута lgForm
try:
    driver.get("http://moigektar.ru/goal/settlements")
    form_id = driver.find_element(by=By.XPATH, value="(//*[text()[contains(.,'Андрей')]]/ancestor::div[contains(@id, 'cfw')]//*[@value='mg_settlements_page_andrey_callback'])[1]")
    print('     ОК: Родовые поселения, форма с Андреем, lgForm')
except Exception as e:
    error_msg = str(e).split('\n')[0]
    print('Ошибка: Родовые поселения, форма с Андреем, lgForm — ', error_msg)


# 15. Проверка раздела "Подарочный сертификат"
# 15.1 Инлайн-форма Андрей - проверяю наличие правильного атрибута lgForm
try:
    driver.get("https://moigektar.ru/gift")
    form_id = driver.find_element(by=By.XPATH, value="(//*[text()[contains(.,'Арина')]]/ancestor::div[contains(@id, 'cfw')]//*[@value='mg_gift_page_callback'])[1]")
    print('     ОК: Подарочный сертификат, форма с Ариной, lgForm')
except Exception as e:
    error_msg = str(e).split('\n')[0]
    print('Ошибка: Подарочный сертификат, форма с Ариной, lgForm — ', error_msg)


# 16. Проверка раздела "Вебинары"
# 16.1 "Узнай, как заработать на гектаре"
# 1-я инлайн-форма - проверяю наличие правильного атрибута lgForm
try:
    driver.get("https://moigektar.ru/webinar/invest")
    form_id = driver.find_element(by=By.XPATH, value="(//*[text()[contains(.,'вебинара')]]/ancestor::div[contains(@id, 'cfw')]//*[@value='mg_webinar'])[1]")
    print('     ОК: Вебинар "Как заработать на гектаре", 1-я инлайн-форма, lgForm')
except Exception as e:
    error_msg = str(e).split('\n')[0]
    print('Ошибка: Вебинар "Как заработать на гектаре", 1-я инлайн-форма, lgForm — ', error_msg)


# 17. Проверка раздела "Личный кабинет"
# 17.1 Инлайн-форма с Ариной, проверяю наличие правильного атрибута lgForm
try:
    driver.get("https://moigektar.ru/cabinet")
    form_id = driver.find_element(by=By.XPATH, value="(//*[text()[contains(.,'Арина')]]/ancestor::div[contains(@id, 'cfw')]//*[@value='mg_lk_page_page_arina_callback'])[1]")
    print('     ОК: раздел личного кабинета, форма с Ариной, lgForm')
except Exception as e:
    error_msg = str(e).split('\n')[0]
    print('Ошибка: раздел личного кабинета, форма с Ариной, lgForm — ', error_msg)
# 17.2 Инлайн-форма с Игорем, проверяю наличие правильного атрибута lgForm
try:
    driver.get("https://moigektar.ru/cabinet")
    form_id = driver.find_element(by=By.XPATH, value="(//*[text()[contains(.,'Игорь')]]/ancestor::div[contains(@id, 'cfw')]//*[@value='mg_lk_page_kalinin_callback'])[1]")
    print('     ОК: раздел личного кабинета, форма с Игорем, lgForm')
except Exception as e:
    error_msg = str(e).split('\n')[0]
    print('Ошибка: раздел личного кабинета, форма с Игорем, lgForm — ', error_msg)


# 18. Проверка раздела регистрации от стойки
# 18.1 Инлайн-форма "Оставьте заявку ...", проверяю наличие правильного атрибута lgForm
try:
    driver.get("https://moigektar.ru/public-event")
    form_id = driver.find_element(by=By.XPATH, value="(//*[text()[contains(.,'Оставьте')]]/ancestor::div[contains(@id, 'cfw')]//*[@value='public-event'])[1]")
    print('     ОК: раздел регистрации от стойки, инлайн-форма, lgForm')
except Exception as e:
    error_msg = str(e).split('\n')[0]
    print('Ошибка: раздел регистрации от стойки, инлайн-форма, lgForm — ', error_msg)


# 19. Проверка раздела закрытого предложения
# 19.1 Инлайн-форма "Узнать о закрытом предложении", проверяю наличие правильного атрибута lgForm
try:
    driver.get("https://moigektar.ru/closed-offer")
    form_id = driver.find_element(by=By.XPATH, value="//*[text()[contains(.,'закрытом')]]/ancestor::div//*[@value='lg_closed_offer']")
    print('     ОК: раздел закрытого предложения, инлайн-форма, lgForm')
except Exception as e:
    error_msg = str(e).split('\n')[0]
    print('Ошибка: раздел закрытого предложения, инлайн-форма, lgForm — ', error_msg)

time.sleep(5)
driver.quit()


