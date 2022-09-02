from selenium import webdriver
from selenium.webdriver.chrome.options import Options
options = Options()
#options.add_argument('--headless')
ch_options = Options()
#ch_options.add_argument('--headless')
driver = webdriver.Chrome(options= ch_options)
driver.maximize_window()


from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time


# открыть https://moigektar.ru/
driver.get("https://moigektar.ru/")

# на странице 4 формы. Скрипт ищет формы и сообщает, есть они или нет
# если форма есть, скрипт проверяет, соответствует ли заголовок, видна ли кнопка и соответствует ли её название

# 1. найти форму "Хотите узнать подробнее о проекте?" и кнопку "Отправить" на ней
# 1.1 убедиться, что есть форма по указанному селектору:
time.sleep(1)
if driver.find_element(by=By.CSS_SELECTOR, value="div.presentation h1 > b").is_displayed():
    print(' OK: 1.1 первая форма на странице есть')
    # 1.2 раз форма есть, то проверим, что заголовок соответствует шаблону
    # (в этой форме костыль в виде частичного сравнения текста из-за того, что название формы разорвано <br>)
    form_1 = driver.find_element(by=By.CSS_SELECTOR, value="div.presentation h1 > b")
    form_1_text = form_1.text
    if form_1_text.startswith("Хотите узнать"):
        print(' OK: 1.2 заголовок формы "Хотите узнать подробнее о проекте?"')
    else:
        print('ERROR: 1.2 заголовок формы не "Хотите узнать подробнее о проекте?", а ' + form_1_text)
    # 1.3 проверим, что есть кнопка на форме
    if driver.find_element(by=By.CSS_SELECTOR, value="div.presentation button").is_displayed():
        print(' OK: 1.3 на форме есть кнопка')
        # 1.4 если кнопка есть, проверим, что её название соответствует шаблону
        button_1 = driver.find_element(by=By.CSS_SELECTOR, value="div.presentation button")
        button_1_text = button_1.text
        if button_1_text == "ОТПРАВИТЬ":
             print(' OK: 1.4 кнопка называется "ОТПРАВИТЬ"')
        else:
             print("ERROR: 1.4 название кнопки не \"ОТПРАВИТЬ\", а " + button_1_text)
        # 1.5 раз кнопка есть, проверим, что при корректных данных заявка будет отправлена
        driver.find_element(by=By.CSS_SELECTOR, value="div.presentation #consultationform-name").send_keys("test")
        driver.find_element(by=By.CSS_SELECTOR, value="div.presentation #consultationform-phone").send_keys("9999999999")
        driver.find_element(by=By.CSS_SELECTOR, value="div.presentation #consultationform-email").send_keys("1@1.1")
        button_1.click()
        time.sleep(3)
        if driver.find_element(by=By.CSS_SELECTOR, value="div.presentation div.uk-width-expand").is_displayed():
            print(" OK: 1.5 данные были отправлены")
        else:
            if driver.find_element(by=By.CSS_SELECTOR, value="div.presentation button").is_displayed():
                print("ERROR: 1.5 данные не были отправлены")
            else:
                print("ПАМАГИТИ")
    else:
        print('ERROR: 1.3 нет кнопки или её селектор изменилсz')
else:
    print('ERROR: 1.1 формы "Хотите узнать подробнее о проекте?" нет или её селектор изменился')


# 2. найти форму "Получите каталог посёлков"
# 2.1 убедиться, что есть форма по указанному селектору:
if driver.find_element(by=By.CSS_SELECTOR, value="div.catalogue h1 > b").is_displayed():
    print(' OK: 2.1 вторая форма на странице есть')
    # 2.2 раз форма есть, то проверим, что заголовок соответствует шаблону
    form_2 = driver.find_element(by=By.CSS_SELECTOR, value="div.catalogue h1 > b")
    form_2_text = form_2.text
    if form_2_text == "Получите каталог посёлков":
        print(' OK: 2.2 заголовок формы "Получите каталог посёлков"')
    else:
        print('ERROR: 2.2 заголовок формы не "Получите каталог посёлков", а ' + form_2_text)
    # 2.3 проверим, что есть кнопка на форме
    if driver.find_element(by=By.CSS_SELECTOR, value="div.catalogue button").is_displayed():
        print(' OK: 2.3 на форме есть кнопка')
        # 2.4 если кнопка есть, проверим, что её название соответствует шаблону
        button_2 = driver.find_element(by=By.CSS_SELECTOR, value="div.catalogue button")
        button_2_text = button_2.text
        if button_2_text == "ПОЛУЧИТЬ":
            print(' OK: 2.4 кнопка называется "ПОЛУЧИТЬ"')
        else:
            print("ERROR: 2.4 название кнопки не \"ПОЛУЧИТЬ\", а " + button_2_text)
        # 2.5 раз кнопка есть, проверим, что при корректных данных заявка будет отправлена
        driver.find_element(by=By.CSS_SELECTOR, value="div.catalogue #consultationform-name").send_keys(
                        "test")
        driver.find_element(by=By.CSS_SELECTOR, value="div.catalogue #consultationform-phone").send_keys(
                        "9999999999")
        driver.find_element(by=By.CSS_SELECTOR, value="div.catalogue #consultationform-email").send_keys(
                        "1@1.1")
        button_2.click()
        time.sleep(3)
        if driver.find_element(by=By.CSS_SELECTOR,
                                           value="div.catalogue div.uk-width-expand").is_displayed():
            print(" OK: 2.5 данные были отправлены")
        else:
            if driver.find_element(by=By.CSS_SELECTOR, value="div.catalogue button").is_displayed():
                print("ERROR: 2.5 данные не были отправлены")
            else:
                print("ПАМАГИТИ")
    else:
        print('ERROR: 2.3 нет кнопки или её селектор изменился')
else:
    print('ERROR: 2.1 формы "Получите каталог посёлков" нет или её селектор изменился')



# 3. найти форму "Подпишитесь на рассылку"
# 3.1 убедиться, что есть форма по указанному селектору:
if driver.find_element(by=By.XPATH, value="//div[47]/div/div/div/h1/b").is_displayed():
    print(' OK: 3.1 вторая форма на странице есть')
    # 3.2 раз форма есть, то проверим, что заголовок соответствует шаблону
    form_3 = driver.find_element(by=By.XPATH, value="//div[47]/div/div/div/h1/b")
    form_3_text = form_3.text
    if form_3_text == "Подпишитесь на рассылку":
        print(' OK: 3.2 заголовок формы "Подпишитесь на рассылку"')
    else:
        print('ERROR: 3.2 заголовок формы не "Подпишитесь на рассылку", а ' + form_3_text)
    # 2.3 проверим, что есть кнопка на форме
    if driver.find_element(by=By.XPATH, value="//form/div[2]/button").is_displayed():
        print(' OK: 3.3 на форме есть кнопка')
        # 2.4 если кнопка есть, проверим, что её название соответствует шаблону
        button_3 = driver.find_element(by=By.XPATH, value="//form/div[2]/button")
        button_3_text = button_3.text
        if button_3_text == "ПОДПИСАТЬСЯ":
            print(' OK: 3.4 кнопка называется "ПОДПИСАТЬСЯ"')
        else:
            print("ERROR: 3.4 название кнопки не \"ПОДПИСАТЬСЯ\", а " + button_3_text)
        # 3.5 раз кнопка есть, проверим, что при корректных данных заявка будет отправлена
        driver.find_element(by=By.XPATH, value="//div[47]/div/div/div/ul/li/form/div/div/input").send_keys("1@1.1")
        button_3.click()
        time.sleep(3)
        if driver.find_element(by=By.XPATH, value="//div[47]/div/div/div/ul[2]/li[2]/div/div[2]").is_displayed():
            print(" OK: 3.5 данные были отправлены")
        else:
            if driver.find_element(by=By.XPATH, value="//form/div[2]/button").is_displayed():
                print("ERROR: 3.5 данные не были отправлены")
            else:
                print("ПАМАГИТИ")
    else:
            print('ERROR: 3.3 нет кнопки или её селектор изменился')
else:
    print('ERROR: 3.1 формы "Подпишитесь на рассылку" нет или её селектор изменился')



# 4. найти форму "Подпишитесь на рассылку"
# 4.1 убедиться, что есть форма по указанному селектору:
if driver.find_element(by=By.CSS_SELECTOR, value="div.doit h1 > b").is_displayed():
    print(' OK: 4.1 вторая форма на странице есть')
    # 4.2 раз форма есть, то проверим, что заголовок соответствует шаблону
    # (в этой форме костыль в виде частичного сравнения текста из-за того, что название формы разорвано <br>)
    form_4 = driver.find_element(by=By.CSS_SELECTOR, value="div.doit h1 > b")
    form_4_text = form_4.text
    if form_4_text.startswith("Действуйте!"):
        print(' OK: 4.2 заголовок формы "Действуйте! Лучшие участки уже бронируют!"')
    else:
        print('ERROR: 4.2 заголовок формы не "Действуйте! Лучшие участки уже бронируют!", а ' + form_4_text)
    # 4.3 проверим, что есть кнопка на форме
    if driver.find_element(by=By.CSS_SELECTOR, value="div.doit button").is_displayed():
        print(' OK: 4.3 на форме есть кнопка')
        # 4.4 если кнопка есть, проверим, что её название соответствует шаблону
        button_4 = driver.find_element(by=By.CSS_SELECTOR, value="div.doit button")
        button_4_text = button_4.text
        if button_4_text == "УЗНАТЬ":
            print(' OK: 4.4 кнопка называется "УЗНАТЬ"')
        else:
            print("ERROR: 4.4 название кнопки не \"УЗНАТЬ\", а " + button_4_text)
        # 4.5 раз кнопка есть, проверим, что при корректных данных заявка будет отправлена
        driver.find_element(by=By.CSS_SELECTOR, value="div.doit #consultationform-name").send_keys("test")
        driver.find_element(by=By.CSS_SELECTOR, value="div.doit #consultationform-phone").send_keys("9999999999")
        button_4.click()
        time.sleep(3)
        if driver.find_element(by=By.CSS_SELECTOR, value="div.doit div.uk-width-expand").is_displayed():
            print(" OK: 4.5 данные были отправлены")
        else:
            if driver.find_element(by=By.CSS_SELECTOR, value="div.doit button").is_displayed():
                 print("ERROR: 4.5 данные не были отправлены")
            else:
                 print("ПАМАГИТИ")
    else:
        print('ERROR: 4.3 нет кнопки или её селектор изменился')
else:
    print('ERROR: 4.1 формы "Действуйте! Лучшие участки уже бронируют!" нет или её селектор изменился')


time.sleep(15)
driver.quit()