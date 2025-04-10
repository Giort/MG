from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
ch_options = Options()
ch_options.add_argument('--headless')
ch_options.page_load_strategy = 'eager'
driver = webdriver.Chrome(options=ch_options)
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait as wait
import json
import time
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
actions = ActionChains(driver)
driver.implicitly_wait(10)
driver.set_window_size(1660, 1000)

with open('data.json', 'r') as file:
    data = json.load(file)

# Скрипт заполняет одну модалку корректными данными и отправляет их
# В этой модалке и во всех остальных проверяет, что присутствует lgForm и он не изменился
#

# driver.get("https://moigektar.ru"+ str(data["mg_loc"]["mg_cur_release_2"]))
driver.get("https://moigektar.ru")

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


# 1.1 проверка модалки "Доступ в личный кабинет" — проверяю наличие правильного атрибута lgForm
try:
    driver.find_element(by=By.XPATH, value='(//*[@id="modal-auth-lk"]//*[@value="catalog_auth_request"])[1]')
    print('     ОК: главная, модалка "Доступ в личный кабинет", lgForm')
except Exception as e:
    error_msg = str(e).split('\n')[0]
    print('Ошибка: главная, "Доступ в личный кабинет", lgForm — ', error_msg)
# 1.2 проверка модалки "Записаться на встречу"
# проверяю отправку данных через форму
# проверяю наличие правильного атрибута lgForm
try:
    btn = driver.find_element(by=By.XPATH, value="(//*[text()[contains(.,'Записаться на встречу')]])[2]")
    actions.move_to_element(btn).perform()
    actions.send_keys(Keys.ARROW_DOWN).perform()
    btn.click()
    try:
        driver.find_element(by=By.XPATH, value='(//*[@id="modal-meeting-meeting"]//*[@id="consultationform-phone"])[1]').send_keys(str(data["test_data_valid"]["phone"]))
        driver.find_element(by=By.XPATH, value='(//*[@id="modal-meeting-meeting"]//*[text()[contains(.,"Отправить заявку")]])[1]').click()
        name_input = driver.find_element(by=By.XPATH,
                                         value='(//*[@id="modal-meeting-meeting"]//*[@id="consultationform-name"])[2]')
        name_input.click()
        print('     ОК: главная, модалка "Записать на встречу", отправка через форму')
    except Exception as e:
        error_msg = str(e).split('\n')[0]
        print('Ошибка: главная, модалка "Записать на встречу", отправка через форму — ', error_msg)
    try:
        driver.find_element(by=By.XPATH, value='(//*[@id="modal-meeting-meeting"]//*[@value="meeting_book"])[1]')
        print('     ОК: главная, модалка "Записать на встречу", lgForm')
    except Exception as e:
        error_msg = str(e).split('\n')[0]
        print('Ошибка: главная, модалка "Записать на встречу", lgForm — ', error_msg)
except Exception as e:
        error_msg = str(e).split('\n')[0]
        print('Ошибка: главная, модалка "Записать на встречу" — ', error_msg)
# 1.3 проверка модалки "Получить консультацию" в футере — проверяю наличие правильного атрибута lgForm
try:
    driver.find_element(by=By.XPATH, value='(//*[@id="modal-main-consultation"]//*[@value="callback_main"])[1]')
    print('     ОК: главная, модалка "Получить консультацию" в футере, lgForm')
except Exception as e:
    error_msg = str(e).split('\n')[0]
    print('Ошибка: главная, "Получить консультацию" в футере, lgForm — ', error_msg)
# 1.4 проверка модалки "Получить консультацию" на фикс. кнопке — проверяю наличие правильного атрибута lgForm
try:
    driver.find_element(by=By.XPATH, value='(//*[@id="modal-fixed"]//*[@value="callback_fixed_btn"])[1]')
    print('     ОК: главная, модалка "Получить консультацию" на фикс. кнопке, lgForm')
except Exception as e:
    error_msg = str(e).split('\n')[0]
    print('Ошибка: главная, "Получить консультацию" на фикс. кнопке, lgForm — ', error_msg)


# 2. проверка страницы каталога
# 2.1 проверка модалки "Заявка на консультацию" — проверяю наличие правильного атрибута lgForm
try:
    driver.get('https://moigektar.ru/catalogue')
    driver.find_element(by=By.XPATH, value='(//*[@id="modal-auth"]//*[@value="catalog_auth_request"])[1]')
    print('     ОК: стр. каталога, модалка "Доступ в каталог", lgForm')
except Exception as e:
    error_msg = str(e).split('\n')[0]
    print('Ошибка: стр. каталога, модалка "Доступ в каталог", lgForm — ', error_msg)


# 3. проверка страницы актива
# 3.1 проверка модалки "Заявка на консультацию" — проверяю наличие правильного атрибута lgForm
try:
    driver.get('https://moigektar.ru/batches/55302')
    driver.find_element(by=By.XPATH, value='(//*[@id="modal-batch-detail"]//*[@value="buy-batch-modal"])[1]')
    print('     ОК: стр. актива, модалка "Заявка на консультацию", lgForm')
except Exception as e:
    error_msg = str(e).split('\n')[0]
    print('Ошибка: стр. актива, модалка "Заявка на консультацию", lgForm — ', error_msg)
# 3.2 проверка модалки "Рассчитайте рассрочку" — проверяю наличие правильного атрибута lgForm
try:
    driver.get('https://moigektar.ru/batches/55302')
    driver.find_element(by=By.XPATH, value='(//*[@id="modal-batch-installment"]//*[@value="batch_installment_special_offer"])[1]')
    print('     ОК: стр. актива, модалка "Рассчитайте рассрочку", lgForm')
except Exception as e:
    error_msg = str(e).split('\n')[0]
    print('Ошибка: стр. актива, модалка "Рассчитайте рассрочку", lgForm — ', error_msg)


# 4. проверка раздела "Развитие"
# 4.1 стр. "Базовая стратегия", модалка "Заказать услугу" — проверяю наличие правильного атрибута lgForm
try:
    driver.get('https://moigektar.ru/investment/basic')
    driver.find_element(by=By.XPATH, value='(//*[@id="modal-select"]//*[@value="mg_invest_basic_page_callback"])[1]')
    print('     ОК: стр. "Базовая стратегия", модалка "Заказать услугу", lgForm')
except Exception as e:
    error_msg = str(e).split('\n')[0]
    print('Ошибка: стр. "Базовая стратегия", модалка "Заказать услугу", lgForm — ', error_msg)
# 4.2 стр. "Предприниматель", модалка "Заказать услугу" — проверяю наличие правильного атрибута lgForm
try:
    driver.get('https://moigektar.ru/investment/businessman')
    driver.find_element(by=By.XPATH, value='(//*[@id="modal-select"]//*[@value="capitalization_count"])[1]')
    print('     ОК: стр. "Предприниматель", модалка "Заказать услугу", lgForm')
except Exception as e:
    error_msg = str(e).split('\n')[0]
    print('Ошибка: стр. "Предприниматель", модалка "Заказать услугу", lgForm — ', error_msg)


# 5. проверка раздела "Бизнес-планы"
# модалка "Получить консультацию" — проверяю наличие правильного атрибута lgForm
try:
    driver.get('https://moigektar.ru/business-plans')
    driver.find_element(by=By.XPATH, value='(//*[@id="modal-main"]//*[@value="callback_business"])[1]')
    print('     ОК: стр. "Бизнес-планы", модалка "Получить консультацию", lgForm')
except Exception as e:
    error_msg = str(e).split('\n')[0]
    print('Ошибка: стр. "Бизнес-планы", модалка "Получить консультацию", lgForm — ', error_msg)


# 6. проверка раздела "Вакансии"
# модалка "Оставьте анкету ..." — проверяю наличие правильного атрибута lgForm
try:
    driver.get('https://moigektar.ru/hr')
    driver.find_element(by=By.XPATH, value='(//*[@id="hr-main-modal"]//*[@value="callback_hr"])[1]')
    print('     ОК: стр. "Вакансии", модалка "Оставьте анкету ...", lgForm')
except Exception as e:
    error_msg = str(e).split('\n')[0]
    print('Ошибка: стр. "Вакансии", модалка "Оставьте анкету ...", lgForm — ', error_msg)


# 7. проверка раздела "Родовые поселения"
# 7.1 1-й экран, модалка "Оставьте заявку!" — проверяю наличие правильного атрибута lgForm
try:
    driver.get('http://moigektar.ru/goal/settlements')
    driver.find_element(by=By.XPATH, value='(//*[@id="settlements-main-modal"]//*[@value="callback_main_settlements"])[1]')
    print('     ОК: стр. "Родовые поселения", 1-й экран, модалка "Оставьте заявку!", lgForm')
except Exception as e:
    error_msg = str(e).split('\n')[0]
    print('Ошибка: стр. "Родовые поселения", 1-й экран, модалка "Оставьте заявку!", lgForm — ', error_msg)
# 7.2 описание, модалка "Оставьте заявку!" — проверяю наличие правильного атрибута lgForm
try:
    driver.get('http://moigektar.ru/goal/settlements')
    driver.find_element(by=By.XPATH, value='(//*[@id="settlements-descr-modal"]//*[@value="callback_descr_settlements"])[1]')
    print('     ОК: стр. "Родовые поселения", описание, модалка "Оставьте заявку!", lgForm')
except Exception as e:
    error_msg = str(e).split('\n')[0]
    print('Ошибка: стр. "Родовые поселения", описание, модалка "Оставьте заявку!", lgForm — ', error_msg)


# 8. проверка раздела "Подарочный сертификат"
# 8.1 модалка "Оставьте заявку!" №1 — проверяю наличие правильного атрибута lgForm
try:
    driver.get('https://moigektar.ru/gift')
    driver.find_element(by=By.XPATH, value='(//*[@id="gift-main-modal"]//*[@value="lg_cert"])[1]')
    print('     ОК: стр. "Подарочный сертификат", модалка "Оставьте заявку!" #1, lgForm')
except Exception as e:
    error_msg = str(e).split('\n')[0]
    print('Ошибка: стр. "Подарочный сертификат", модалка "Оставьте заявку!" #1, lgForm — ', error_msg)
# 8.2 модалка "Оставьте заявку!" №2 — проверяю наличие правильного атрибута lgForm
try:
    driver.get('https://moigektar.ru/gift')
    driver.find_element(by=By.XPATH, value='(//*[@id="plot-certificate-parents-modal"]//*[@value="lg_cert"])[1]')
    print('     ОК: стр. "Подарочный сертификат", модалка "Оставьте заявку!" #2, lgForm')
except Exception as e:
    error_msg = str(e).split('\n')[0]
    print('Ошибка: стр. "Подарочный сертификат", модалка "Оставьте заявку!" #2, lgForm — ', error_msg)
# 8.3 модалка "Оставьте заявку!" №3 — проверяю наличие правильного атрибута lgForm
try:
    driver.get('https://moigektar.ru/gift')
    driver.find_element(by=By.XPATH, value='(//*[@id="plot-certificate-friend-modal"]//*[@value="lg_cert"])[1]')
    print('     ОК: стр. "Подарочный сертификат", модалка "Оставьте заявку!" #3, lgForm')
except Exception as e:
    error_msg = str(e).split('\n')[0]
    print('Ошибка: стр. "Подарочный сертификат", модалка "Оставьте заявку!" #3, lgForm — ', error_msg)
# 8.4 модалка "Оставьте заявку!" №4 — проверяю наличие правильного атрибута lgForm
try:
    driver.get('https://moigektar.ru/gift')
    driver.find_element(by=By.XPATH, value='(//*[@id="plot-certificate-business-modal"]//*[@value="lg_cert"])[1]')
    print('     ОК: стр. "Подарочный сертификат", модалка "Оставьте заявку!" #4, lgForm')
except Exception as e:
    error_msg = str(e).split('\n')[0]
    print('Ошибка: стр. "Подарочный сертификат", модалка "Оставьте заявку!" #4, lgForm — ', error_msg)
# 8.5 модалка "Оставьте заявку!" №5 — проверяю наличие правильного атрибута lgForm
try:
    driver.get('https://moigektar.ru/gift')
    driver.find_element(by=By.XPATH, value='(//*[@id="gift-option-modal"]//*[@value="lg_cert"])[1]')
    print('     ОК: стр. "Подарочный сертификат", модалка "Оставьте заявку!" #5, lgForm')
except Exception as e:
    error_msg = str(e).split('\n')[0]
    print('Ошибка: стр. "Подарочный сертификат", модалка "Оставьте заявку!" #5, lgForm — ', error_msg)
# 8.6 модалка "Оставьте заявку!" №6 — проверяю наличие правильного атрибута lgForm
try:
    driver.get('https://moigektar.ru/gift')
    driver.find_element(by=By.XPATH, value='(//*[@id="gift-certificate-modal"]//*[@value="lg_cert"])[1]')
    print('     ОК: стр. "Подарочный сертификат", модалка "Оставьте заявку!" #6, lgForm')
except Exception as e:
    error_msg = str(e).split('\n')[0]
    print('Ошибка: стр. "Подарочный сертификат", модалка "Оставьте заявку!" #6, lgForm — ', error_msg)
# 8.7 модалка "Оставьте заявку!" №7 — проверяю наличие правильного атрибута lgForm
try:
    driver.get('https://moigektar.ru/gift')
    driver.find_element(by=By.XPATH, value='(//*[@id="select-certificate-plot-modal"]//*[@value="lg_cert"])[1]')
    print('     ОК: стр. "Подарочный сертификат", модалка "Оставьте заявку!" #7, lgForm')
except Exception as e:
    error_msg = str(e).split('\n')[0]
    print('Ошибка: стр. "Подарочный сертификат", модалка "Оставьте заявку!" #7, lgForm — ', error_msg)
# 8.8 модалка "Оставьте заявку!" №8 — проверяю наличие правильного атрибута lgForm
try:
    driver.get('https://moigektar.ru/gift')
    driver.find_element(by=By.XPATH, value='(//*[@id="select-certificate-sum-modal"]//*[@value="lg_cert"])[1]')
    print('     ОК: стр. "Подарочный сертификат", модалка "Оставьте заявку!" #8, lgForm')
except Exception as e:
    error_msg = str(e).split('\n')[0]
    print('Ошибка: стр. "Подарочный сертификат", модалка "Оставьте заявку!" #8, lgForm — ', error_msg)
# 8.9 модалка "Оставьте заявку!" №9 — проверяю наличие правильного атрибута lgForm
try:
    driver.get('https://moigektar.ru/gift')
    driver.find_element(by=By.XPATH, value='(//*[@id="gift-land-modal"]//*[@value="lg_cert"])[1]')
    print('     ОК: стр. "Подарочный сертификат", модалка "Оставьте заявку!" #9, lgForm')
except Exception as e:
    error_msg = str(e).split('\n')[0]
    print('Ошибка: стр. "Подарочный сертификат", модалка "Оставьте заявку!" #9, lgForm — ', error_msg)




#time.sleep(8)
driver.quit()

