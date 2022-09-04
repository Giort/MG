from selenium import webdriver
from selenium.webdriver.chrome.options import Options
options = Options()
options.add_argument('--headless')
ch_options = Options()
ch_options.add_argument('--headless')
driver = webdriver.Chrome(options= ch_options)
driver.maximize_window()


from selenium.webdriver.common.by import By
import time


# открыть https://moigektar.ru/
driver.get("https://moigektar.ru/")

# на странице 4 формы. Скрипт ищет формы и сообщает, есть они или нет
# если форма есть, скрипт проверяет:
# - соответствует ли заголовок, видна ли кнопка и соответствует ли её название
# - что данные будут отправлены и отобразится сообщение об успехе, если ввести корректные данные


# 1. проверка главной страницы "МГ"
# 1.1 проверка формы "Хотите узнать подробнее о проекте?"
# 1.1.1 убедиться, что есть форма по указанному селектору:
time.sleep(1)
if driver.find_element(by=By.CSS_SELECTOR, value="div.presentation h1 > b").is_displayed():
    print(' OK: 1.1.1 первая форма на главной странице есть')
    # 1.1.2 раз форма есть, то проверим, что заголовок соответствует шаблону
    # (в этой форме костыль в виде частичного сравнения текста из-за того, что название формы разорвано <br>)
    form_1 = driver.find_element(by=By.CSS_SELECTOR, value="div.presentation h1 > b")
    form_1_text = form_1.text
    if form_1_text.startswith("Хотите узнать"):
        print(' OK: 1.1.2 заголовок формы "Хотите узнать подробнее о проекте?"')
    else:
        print('ERROR: 1.1.2 заголовок формы не "Хотите узнать подробнее о проекте?", а ' + form_1_text)
    # 1.3 проверим, что есть кнопка на форме
    if driver.find_element(by=By.CSS_SELECTOR, value="div.presentation button").is_displayed():
        print(' OK: 1.1.3 на форме есть кнопка')
        # 1.4 если кнопка есть, проверим, что её название соответствует шаблону
        button_1 = driver.find_element(by=By.CSS_SELECTOR, value="div.presentation button")
        button_1_text = button_1.text
        if button_1_text == "ОТПРАВИТЬ":
             print(' OK: 1.1.4 кнопка называется "ОТПРАВИТЬ"')
        else:
             print("ERROR: 1.1.4 название кнопки не \"ОТПРАВИТЬ\", а " + button_1_text)
        # 1.5 раз кнопка есть, проверим, что при корректных данных заявка будет отправлена
        driver.find_element(by=By.CSS_SELECTOR, value="div.presentation #consultationform-name").send_keys("test")
        driver.find_element(by=By.CSS_SELECTOR, value="div.presentation #consultationform-phone").send_keys("9999999999")
        driver.find_element(by=By.CSS_SELECTOR, value="div.presentation #consultationform-email").send_keys("1@1.1")
        button_1.click()
        time.sleep(3)
        if driver.find_element(by=By.CSS_SELECTOR, value="div.presentation div.uk-width-expand").is_displayed():
            print(" OK: 1.1.5 данные были отправлены")
        else:
            if driver.find_element(by=By.CSS_SELECTOR, value="div.presentation button").is_displayed():
                print("ERROR: 1.1.5 данные не были отправлены")
            else:
                print("ПАМАГИТИ")
    else:
        print('ERROR: 1.1.3 нет кнопки или её селектор изменилсz')
else:
    print('ERROR: 1.1.1 формы "Хотите узнать подробнее о проекте?" нет или её селектор изменился')


# 1.2. проверка формы "Получите каталог посёлков"
# 1.2.1 убедиться, что есть форма по указанному селектору:
if driver.find_element(by=By.CSS_SELECTOR, value="div.catalogue h1 > b").is_displayed():
    print(' OK: 1.2.1 вторая форма на главной странице есть')
    # 2.2 раз форма есть, то проверим, что заголовок соответствует шаблону
    form_2 = driver.find_element(by=By.CSS_SELECTOR, value="div.catalogue h1 > b")
    form_2_text = form_2.text
    if form_2_text == "Получите каталог посёлков":
        print(' OK: 1.2.2 заголовок формы "Получите каталог посёлков"')
    else:
        print('ERROR: 1.2.2 заголовок формы не "Получите каталог посёлков", а ' + form_2_text)
    # 2.3 проверим, что есть кнопка на форме
    if driver.find_element(by=By.CSS_SELECTOR, value="div.catalogue button").is_displayed():
        print(' OK: 1.2.3 на форме есть кнопка')
        # 2.4 если кнопка есть, проверим, что её название соответствует шаблону
        button_2 = driver.find_element(by=By.CSS_SELECTOR, value="div.catalogue button")
        button_2_text = button_2.text
        if button_2_text == "ПОЛУЧИТЬ":
            print(' OK: 1.2.4 кнопка называется "ПОЛУЧИТЬ"')
        else:
            print("ERROR: 1.2.4 название кнопки не \"ПОЛУЧИТЬ\", а " + button_2_text)
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
            print(" OK: 1.2.5 данные были отправлены")
        else:
            if driver.find_element(by=By.CSS_SELECTOR, value="div.catalogue button").is_displayed():
                print("ERROR: 1.2.5 данные не были отправлены")
            else:
                print("ПАМАГИТИ")
    else:
        print('ERROR: 1.2.3 нет кнопки или её селектор изменился')
else:
    print('ERROR: 1.2.1 формы "Получите каталог посёлков" нет или её селектор изменился')



# 1.3. проверка формы "Подпишитесь на рассылку"
# 1.3.1 убедиться, что есть форма по указанному селектору:
if driver.find_element(by=By.XPATH, value="//div[47]/div/div/div/h1/b").is_displayed():
    print(' OK: 1.3.1 третья форма на главной странице есть')
    # 3.2 раз форма есть, то проверим, что заголовок соответствует шаблону
    form_3 = driver.find_element(by=By.XPATH, value="//div[47]/div/div/div/h1/b")
    form_3_text = form_3.text
    if form_3_text == "Подпишитесь на рассылку":
        print(' OK: 1.3.2 заголовок формы "Подпишитесь на рассылку"')
    else:
        print('ERROR: 1.3.2 заголовок формы не "Подпишитесь на рассылку", а ' + form_3_text)
    # 2.3 проверим, что есть кнопка на форме
    if driver.find_element(by=By.XPATH, value="//form/div[2]/button").is_displayed():
        print(' OK: 1.3.3 на форме есть кнопка')
        # 2.4 если кнопка есть, проверим, что её название соответствует шаблону
        button_3 = driver.find_element(by=By.XPATH, value="//form/div[2]/button")
        button_3_text = button_3.text
        if button_3_text == "ПОДПИСАТЬСЯ":
            print(' OK: 1.3.4 кнопка называется "ПОДПИСАТЬСЯ"')
        else:
            print("ERROR: 1.3.4 название кнопки не \"ПОДПИСАТЬСЯ\", а " + button_3_text)
        # 3.5 раз кнопка есть, проверим, что при корректных данных заявка будет отправлена
        driver.find_element(by=By.XPATH, value="//div[47]/div/div/div/ul/li/form/div/div/input").send_keys("1@1.1")
        button_3.click()
        time.sleep(3)
        if driver.find_element(by=By.XPATH, value="//div[47]/div/div/div/ul[2]/li[2]/div/div[2]").is_displayed():
            print(" OK: 1.3.5 данные были отправлены")
        else:
            if driver.find_element(by=By.XPATH, value="//form/div[2]/button").is_displayed():
                print("ERROR: 1.3.5 данные не были отправлены")
            else:
                print("ПАМАГИТИ")
    else:
            print('ERROR: 1.3.3 нет кнопки или её селектор изменился')
else:
    print('ERROR: 1.3.1 формы "Подпишитесь на рассылку" нет или её селектор изменился')



# 1.4. проверка формы "Подпишитесь на рассылку"
# 1.4.1 убедиться, что есть форма по указанному селектору:
if driver.find_element(by=By.CSS_SELECTOR, value="div.doit h1 > b").is_displayed():
    print(' OK: 1.4.1 четвёртая форма на главной странице есть')
    # 1.4.2 раз форма есть, то проверим, что заголовок соответствует шаблону
    # (в этой форме костыль в виде частичного сравнения текста из-за того, что название формы разорвано <br>)
    form_4 = driver.find_element(by=By.CSS_SELECTOR, value="div.doit h1 > b")
    form_4_text = form_4.text
    if form_4_text.startswith("Действуйте!"):
        print(' OK: 1.4.2 заголовок формы "Действуйте! Лучшие участки уже бронируют!"')
    else:
        print('ERROR: 1.4.2 заголовок формы не "Действуйте! Лучшие участки уже бронируют!", а ' + form_4_text)
    # 4.3 проверим, что есть кнопка на форме
    if driver.find_element(by=By.CSS_SELECTOR, value="div.doit button").is_displayed():
        print(' OK: 1.4.3 на форме есть кнопка')
        # 4.4 если кнопка есть, проверим, что её название соответствует шаблону
        button_4 = driver.find_element(by=By.CSS_SELECTOR, value="div.doit button")
        button_4_text = button_4.text
        if button_4_text == "УЗНАТЬ":
            print(' OK: 1.4.4 кнопка называется "УЗНАТЬ"')
        else:
            print("ERROR: 1.4.4 название кнопки не \"УЗНАТЬ\", а " + button_4_text)
        # 4.5 раз кнопка есть, проверим, что при корректных данных заявка будет отправлена
        driver.find_element(by=By.CSS_SELECTOR, value="div.doit #consultationform-name").send_keys("test")
        driver.find_element(by=By.CSS_SELECTOR, value="div.doit #consultationform-phone").send_keys("9999999999")
        button_4.click()
        time.sleep(3)
        if driver.find_element(by=By.CSS_SELECTOR, value="div.doit div.uk-width-expand").is_displayed():
            print(" OK: 1.4.5 данные были отправлены")
        else:
            if driver.find_element(by=By.CSS_SELECTOR, value="div.doit button").is_displayed():
                 print("ERROR: 1.4.5 данные не были отправлены")
            else:
                 print("ПАМАГИТИ")
    else:
        print('ERROR: 1.4.3 нет кнопки или её селектор изменился')
else:
    print('ERROR: 1.4.1 формы "Действуйте! Лучшие участки уже бронируют!" нет или её селектор изменился')



# переход на страницу "О проекте"
# тут просто проверка, что форма "Хотите узнать подробнее о проекте?" на страницах есть
# так как предполагается, что её функционал уже проверен на главной
time.sleep(3)
driver.get("https://moigektar.ru/about")
if driver.find_element(by=By.XPATH, value="//h1/b").is_displayed():
    print(' OK: 2.1 форма "Хотите узнать подробнее о проекте?" на странице "О проекте" есть')
else:
    print('ERROR: нет формы "Хотите узнать подробнее о проекте?" на странице "О проекте" \n       или селектор формы изменился')

# переход на страницу "О проекте - сервисная компания"
time.sleep(3)
driver.get("https://moigektar.ru/about/management")
if driver.find_element(by=By.XPATH, value="//h1/b").is_displayed():
    print(' OK: 2.2 форма "Хотите узнать подробнее о проекте?" на странице "О проекте - сервисная компания" есть')
else:
    print('ERROR: нет формы "Хотите узнать подробнее о проекте?" на странице "О проекте - сервисная компания" \n       или селектор формы изменился')

# переход на страницу "О проекте - личный кабинет"
time.sleep(3)
driver.get("https://moigektar.ru/about/cabinet")
if driver.find_element(by=By.XPATH, value="//h1/b").is_displayed():
    print(' OK: 2.3 форма "Хотите узнать подробнее о проекте?" на странице "О проекте - личный кабинет" есть')
else:
    print('ERROR: нет формы "Хотите узнать подробнее о проекте?" на странице "О проекте - личный кабинет" \n       или селектор формы изменился')

# переход на страницу "О проекте - партнеры"
time.sleep(3)
driver.get("https://moigektar.ru/about/advantages")
if driver.find_element(by=By.XPATH, value="//h1/b").is_displayed():
    print(' OK: 2.4 форма "Хотите узнать подробнее о проекте?" на странице "О проекте - партнеры" есть')
else:
    print('ERROR: нет формы "Хотите узнать подробнее о проекте?" на странице "О проекте - партнеры" \n       или селектор формы изменился')

# переход на страницу "О проекте - союз садоводов"
time.sleep(3)
driver.get("https://moigektar.ru/about/union")
if driver.find_element(by=By.XPATH, value="//h1/b").is_displayed():
    print(' OK: 2.5 форма "Хотите узнать подробнее о проекте?" на странице "О проекте - союз садоводов" есть')
else:
    print('ERROR: нет формы "Хотите узнать подробнее о проекте?" на странице "О проекте - союз садоводов" \n       или селектор формы изменился')

# переход на страницу "О проекте - отзывы"
time.sleep(3)
driver.get("https://moigektar.ru/about/reviews")
if driver.find_element(by=By.XPATH, value="//h1/b").is_displayed():
    print(' OK: 2.6 форма "Хотите узнать подробнее о проекте?" на странице "О проекте - отзывы" есть')
else:
    print('ERROR: нет формы "Хотите узнать подробнее о проекте?" на странице "О проекте - отзывы" \n       или селектор формы изменился')




# переход на страницу "Каталог поселков"
time.sleep(3)
driver.get("https://moigektar.ru/catalogue")
if driver.find_element(by=By.XPATH, value="//div[25]/div/div/h1/b").is_displayed():
    print(' OK: 3.1 форма "Хотите узнать подробнее о проекте?" на странице "Каталог посёлков" есть')
else:
    print('ERROR: нет формы "Хотите узнать подробнее о проекте?" на странице "Каталог посёлков" \n       или селектор формы изменился')




# переход на страницу "Развитие - развитие поселков"
time.sleep(3)
driver.get("https://moigektar.ru/growth")
# проверка, что форма есть на странице
if driver.find_element(by=By.XPATH, value="//h1/b").is_displayed():
    print(' OK: 4.1 форма на странице "Развитие - Развитие поселков" есть')
    # 4.2 раз форма есть, то проверим, что заголовок соответствует шаблону
    # (в этой форме костыль в виде частичного сравнения текста из-за того, что название формы разорвано <br>)
    form_5 = driver.find_element(by=By.XPATH, value="//h1/b")
    form_5_text = form_5.text
    if form_5_text.startswith("Хотите узнать подробнее"):
        print(' OK: 4.2 заголовок формы "Хотите узнать подробнее о проекте?"')
    else:
        print('ERROR: 4.2 заголовок формы не "Хотите узнать подробнее об услугах и развитии?", а ' + form_5_text)
    # 3.3 проверим, что есть кнопка на форме
    if driver.find_element(by=By.XPATH, value="//div[4]/button").is_displayed():
        print(' OK: 4.3 на форме есть кнопка')
        # 4.4 если кнопка есть, проверим, что её название соответствует шаблону
        button_5 = driver.find_element(by=By.XPATH, value="//div[4]/button")
        button_5_text = button_5.text
        if button_5_text == "ОТПРАВИТЬ":
            print(' OK: 4.4 кнопка называется "ОТПРАВИТЬ"')
        else:
            print("ERROR: 4.4 название кнопки не \"ОТПРАВИТЬ\", а " + button_5_text)
        # 4.5 раз кнопка есть, проверим, что при корректных данных заявка будет отправлена
        driver.find_element(by=By.XPATH, value="//div[22]/div/div/div/div/ul[2]/li/form/div/div/input").send_keys("test")
        driver.find_element(by=By.XPATH, value="//div[22]/div/div/div/div/ul[2]/li/form/div[2]/div/div/input").send_keys(
            "9999999999")
        driver.find_element(by=By.XPATH, value="//div[22]/div/div/div/div/ul[2]/li/form/div[3]/div/input").send_keys("1@1.1")
        button_5.click()
        time.sleep(3)
        if driver.find_element(by=By.XPATH, value="//div[22]/div/div/div/div/ul[2]/li[2]/div/div[2]").is_displayed():
            print(" OK: 4.5 данные были отправлены")
        else:
            if driver.find_element(by=By.XPATH, value="//div[4]/button").is_displayed():
                print("ERROR: 4.5 данные не были отправлены")
            else:
                print("ПАМАГИТИ")
    else:
        print('ERROR: 4.3 нет кнопки или её селектор изменился')
else:
    print('ERROR: 4.1 формы "Хотите узнать подробнее о проекте?" нет или её селектор изменился')

time.sleep(10)
driver.quit()