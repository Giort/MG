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
# далее на шести страницах проверка наличия формы, функционал которой уже проверен на главной
driver.get("https://moigektar.ru/about")
time.sleep(1)
if driver.find_element(by=By.XPATH, value="//h1/b").is_displayed():
    print(' OK: 2.1 форма "Хотите узнать подробнее о проекте?" на странице "О проекте" есть')
else:
    print('ERROR: 2.1 нет формы "Хотите узнать подробнее о проекте?" на странице "О проекте" \n       или селектор формы изменился')

# переход на страницу "О проекте - сервисная компания"
driver.get("https://moigektar.ru/about/management")
time.sleep(1)
if driver.find_element(by=By.XPATH, value="//h1/b").is_displayed():
    print(' OK: 2.2 форма "Хотите узнать подробнее о проекте?" на странице "О проекте - сервисная компания" есть')
else:
    print('ERROR: 2.2 нет формы "Хотите узнать подробнее о проекте?" на странице "О проекте - сервисная компания" \n       или селектор формы изменился')

# переход на страницу "О проекте - личный кабинет"
driver.get("https://moigektar.ru/about/cabinet")
time.sleep(1)
if driver.find_element(by=By.XPATH, value="//h1/b").is_displayed():
    print(' OK: 2.3 форма "Хотите узнать подробнее о проекте?" на странице "О проекте - личный кабинет" есть')
else:
    print('ERROR: 2.3 нет формы "Хотите узнать подробнее о проекте?" на странице "О проекте - личный кабинет" \n       или селектор формы изменился')

# переход на страницу "О проекте - партнеры"
driver.get("https://moigektar.ru/about/advantages")
time.sleep(1)
if driver.find_element(by=By.XPATH, value="//h1/b").is_displayed():
    print(' OK: 2.4 форма "Хотите узнать подробнее о проекте?" на странице "О проекте - партнеры" есть')
else:
    print('ERROR: 2.4 нет формы "Хотите узнать подробнее о проекте?" на странице "О проекте - партнеры" \n       или селектор формы изменился')

# переход на страницу "О проекте - союз садоводов"
driver.get("https://moigektar.ru/about/union")
time.sleep(1)
if driver.find_element(by=By.XPATH, value="//h1/b").is_displayed():
    print(' OK: 2.5 форма "Хотите узнать подробнее о проекте?" на странице "О проекте - союз садоводов" есть')
else:
    print('ERROR: 2.5 нет формы "Хотите узнать подробнее о проекте?" на странице "О проекте - союз садоводов" \n       или селектор формы изменился')

# переход на страницу "О проекте - отзывы"
driver.get("https://moigektar.ru/about/reviews")
time.sleep(1)
if driver.find_element(by=By.XPATH, value="//h1/b").is_displayed():
    print(' OK: 2.6 форма "Хотите узнать подробнее о проекте?" на странице "О проекте - отзывы" есть')
else:
    print('ERROR: 2.6 нет формы "Хотите узнать подробнее о проекте?" на странице "О проекте - отзывы" \n       или селектор формы изменился')




# переход на страницу "Каталог поселков"
# проверка наличия формы, функционал которой уже проверен на главной
driver.get("https://moigektar.ru/catalogue")
time.sleep(1)
if driver.find_element(by=By.XPATH, value="//div[25]/div/div/h1/b").is_displayed():
    print(' OK: 3.1 форма "Хотите узнать подробнее о проекте?" на странице "Каталог посёлков" есть')
else:
    print('ERROR: 3.1 нет формы "Хотите узнать подробнее о проекте?" на странице "Каталог посёлков" \n       или селектор формы изменился')




# переход на страницу "Развитие - развитие поселков"
driver.get("https://moigektar.ru/growth")
time.sleep(1)
# проверка, что форма есть на странице
if driver.find_element(by=By.XPATH, value="//h1/b").is_displayed():
    print(' OK: 4.1.1 форма на странице "Развитие - Развитие поселков" есть')
    # 4.1.2 раз форма есть, то проверим, что заголовок соответствует шаблону
    # (в этой форме костыль в виде частичного сравнения текста из-за того, что название формы разорвано <br>)
    form_5 = driver.find_element(by=By.XPATH, value="//h1/b")
    form_5_text = form_5.text
    if form_5_text.startswith("Хотите узнать подробнее"):
        print(' OK: 4.1.2 заголовок формы "Хотите узнать подробнее о проекте?"')
    else:
        print('ERROR: 4.1.2 заголовок формы не "Хотите узнать подробнее об услугах и развитии?", а ' + form_5_text)
    # 4.3 проверим, что есть кнопка на форме
    if driver.find_element(by=By.XPATH, value="//div[4]/button").is_displayed():
        print(' OK: 4.1.3 на форме есть кнопка')
        # 4.4 если кнопка есть, проверим, что её название соответствует шаблону
        button_5 = driver.find_element(by=By.XPATH, value="//div[4]/button")
        button_5_text = button_5.text
        if button_5_text == "ОТПРАВИТЬ":
            print(' OK: 4.1.4 кнопка называется "ОТПРАВИТЬ"')
        else:
            print("ERROR: 4.1.4 название кнопки не \"ОТПРАВИТЬ\", а " + button_5_text)
        # 4.5 раз кнопка есть, проверим, что при корректных данных заявка будет отправлена
        driver.find_element(by=By.XPATH, value="//div[22]/div/div/div/div/ul[2]/li/form/div/div/input").send_keys("test")
        driver.find_element(by=By.XPATH, value="//div[22]/div/div/div/div/ul[2]/li/form/div[2]/div/div/input").send_keys(
            "9999999999")
        driver.find_element(by=By.XPATH, value="//div[22]/div/div/div/div/ul[2]/li/form/div[3]/div/input").send_keys("1@1.1")
        button_5.click()
        time.sleep(3)
        if driver.find_element(by=By.XPATH, value="//div[22]/div/div/div/div/ul[2]/li[2]/div/div[2]").is_displayed():
            print(" OK: 4.1.5 данные были отправлены")
        else:
            if driver.find_element(by=By.XPATH, value="//div[4]/button").is_displayed():
                print("ERROR: 4.1.5 данные не были отправлены")
            else:
                print("ПАМАГИТИ")
    else:
        print('ERROR: 4.1.3 нет кнопки или её селектор изменился')
else:
    print('ERROR: 4.1.1 формы "Хотите узнать подробнее об услугах и развитии?" нет или её селектор изменился')



# переход на страницу "Развитие - глазами инвестора"
# далее на шести страницах проверка наличия формы, функционал которой уже проверен на главной
driver.get("https://moigektar.ru/investment")
time.sleep(1)
if driver.find_element(by=By.XPATH, value="//h1/b").is_displayed():
    print(' OK: 4.2 форма "Хотите узнать подробнее о проекте?" на странице "Развитие - глазами инвестора" есть')
else:
    print('ERROR: 4.2 нет формы "Хотите узнать подробнее о проекте?" на странице "Развитие - глазами инвестора" \n       или селектор формы изменился')

# переход на страницу "Развитие - капитализация"
driver.get("https://moigektar.ru/investment/capitalization")
time.sleep(1)
if driver.find_element(by=By.XPATH, value="//h1/b").is_displayed():
    print(' OK: 4.3 форма "Хотите узнать подробнее о проекте?" на странице "Развитие - капитализация" есть')
else:
    print('ERROR: 4.3 нет формы "Хотите узнать подробнее о проекте?" на странице "Развитие - капитализация" \n       или селектор формы изменился')

# переход на страницу "Развитие - базовая стратегия"
driver.get("https://moigektar.ru/investment/basic")
time.sleep(1)
if driver.find_element(by=By.XPATH, value="//h1/b").is_displayed():
    print(' OK: 4.4 форма "Хотите узнать подробнее о проекте?" на странице "Развитие - базовая стратегия" есть')
else:
    print('ERROR: 4.4 нет формы "Хотите узнать подробнее о проекте?" на странице "Развитие - базовая стратегия" \n       или селектор формы изменился')

# переход на страницу "Развитие - предприниматель"
driver.get("https://moigektar.ru/investment/businessman")
time.sleep(1)
if driver.find_element(by=By.XPATH, value="//h1/b").is_displayed():
    print(' OK: 4.5 форма "Хотите узнать подробнее о проекте?" на странице "Развитие - предприниматель" есть')
else:
    print('ERROR: 4.5 нет формы "Хотите узнать подробнее о проекте?" на странице "Развитие - предприниматель" \n       или селектор формы изменился')

# переход на страницу "Развитие - фермер-садовод"
driver.get("https://moigektar.ru/investment/farmer")
time.sleep(1)
if driver.find_element(by=By.XPATH, value="//h1/b").is_displayed():
    print(' OK: 4.6 форма "Хотите узнать подробнее о проекте?" на странице "Развитие - фермер-садовод" есть')
else:
    print('ERROR: 4.6 нет формы "Хотите узнать подробнее о проекте?" на странице "Развитие - фермер-садовод" \n       или селектор формы изменился')

# переход на страницу "Развитие - фамильная усадьба"
driver.get("https://moigektar.ru/investment/family")
time.sleep(1)
if driver.find_element(by=By.XPATH, value="//h1/b").is_displayed():
    print(' OK: 4.7 форма "Хотите узнать подробнее о проекте?" на странице "Развитие - фамильная усадьба" есть')
else:
    print('ERROR: 4.7 нет формы "Хотите узнать подробнее о проекте?" на странице "Развитие - фамильная усадьба" \n       или селектор формы изменился')





# переход на страницу "Меры поддержки - государственная поддержка"
driver.get("https://moigektar.ru/documents/gos")
time.sleep(1)
# проверка, что форма есть на странице
if driver.find_element(by=By.XPATH, value="//h1/b").is_displayed():
    print(' OK: 5.1.1 форма на странице "Меры поддержки - господдержка" есть')
    # 5.1.2 раз форма есть, то проверим, что заголовок соответствует шаблону
    # (в этой форме костыль в виде частичного сравнения текста из-за того, что название формы разорвано <br>)
    form_6 = driver.find_element(by=By.XPATH, value="//h1/b")
    form_6_text = form_6.text
    if form_6_text.startswith("Хотите узнать подробнее"):
        print(' OK: 5.1.2 заголовок формы "Хотите узнать подробнее о господдержке?"')
    else:
        print('ERROR: 5.1.2 заголовок формы не "Хотите узнать подробнее о господдержке?", а ' + form_6_text)
    # 5.3 проверим, что есть кнопка на форме
    if driver.find_element(by=By.XPATH, value="//div[4]/button").is_displayed():
        print(' OK: 5.1.3 на форме есть кнопка')
        # 5.4 если кнопка есть, проверим, что её название соответствует шаблону
        button_6 = driver.find_element(by=By.XPATH, value="//div[4]/button")
        button_6_text = button_6.text
        if button_6_text == "ОТПРАВИТЬ":
            print(' OK: 5.1.4 кнопка называется "ОТПРАВИТЬ"')
        else:
            print("ERROR: 5.1.4 название кнопки не \"ОТПРАВИТЬ\", а " + button_6_text)
        # 5.5 раз кнопка есть, проверим, что при корректных данных заявка будет отправлена
        driver.find_element(by=By.XPATH, value="//div[2]/div/ul[2]/li/form/div/div/input").send_keys("test")
        driver.find_element(by=By.XPATH, value="//div[2]/div/ul[2]/li/form/div[2]/div/div/input").send_keys(
            "9999999999")
        driver.find_element(by=By.XPATH, value="//div[2]/div/ul[2]/li/form/div[3]/div/input").send_keys("1@1.1")
        button_6.click()
        time.sleep(3)
        if driver.find_element(by=By.XPATH, value="//div[2]/div/ul[2]/li[2]/div/div[2]").is_displayed():
            print(" OK: 5.1.5 данные были отправлены")
        else:
            if driver.find_element(by=By.XPATH, value="//div[4]/button").is_displayed():
                print("ERROR: 5.1.5 данные не были отправлены")
            else:
                print("ПАМАГИТИ")
    else:
        print('ERROR: 5.1.3 нет кнопки или её селектор изменился')
else:
    print('ERROR: 5.1.1 формы "Хотите узнать подробнее о господдержке?" нет или её селектор изменился')

# переход на страницу "Меры поддержки - для владельцев земли"
# далее на пяти страницах проверка наличия формы, функционал которой уже проверен на "Господдержке""
driver.get("https://moigektar.ru/documents")
time.sleep(1)
if driver.find_element(by=By.XPATH, value="//h1/b").is_displayed():
    print(' OK: 5.2 форма "Хотите узнать подробнее о господдержке?" на странице "Меры поддержки - для владельцев земли" есть')
else:
    print('ERROR: 5.2 нет формы "Хотите узнать подробнее о проекте?" на странице "Меры поддержки - для владельцев земли" \n       или селектор формы изменился')

# переход на страницу "Меры поддержки - для владельцев земли"
driver.get("https://moigektar.ru/documents/farmer")
time.sleep(1)
if driver.find_element(by=By.XPATH, value="//h1/b").is_displayed():
    print(' OK: 5.3 форма "Хотите узнать подробнее о господдержке?" на странице "Меры поддержки - грант "Начинающий фермер" есть')
else:
    print('ERROR: 5.3 нет формы "Хотите узнать подробнее о проекте?" на странице "Меры поддержки - грант "Начинающий фермер" \n       или селектор формы изменился')

# переход на страницу "Меры поддержки - для владельцев земли"
driver.get("https://moigektar.ru/documents/startup")
time.sleep(1)
if driver.find_element(by=By.XPATH, value="//h1/b").is_displayed():
    print(' OK: 5.4 форма "Хотите узнать подробнее о господдержке?" на странице "Меры поддержки - грант "Агростартап" есть')
else:
    print('ERROR: 5.4 нет формы "Хотите узнать подробнее о проекте?" на странице "Меры поддержки - грант "Агростартап" \n       или селектор формы изменился')

# переход на страницу "Меры поддержки - для владельцев земли"
driver.get("https://moigektar.ru/documents/family")
time.sleep(1)
if driver.find_element(by=By.XPATH, value="//h1/b").is_displayed():
    print(' OK: 5.5 форма "Хотите узнать подробнее о господдержке?" на странице "Меры поддержки - грант на семейную ферму" есть')
else:
    print('ERROR: 5.5 нет формы "Хотите узнать подробнее о проекте?" на странице "Меры поддержки - грант на семейную ферму" \n       или селектор формы изменился')

# переход на страницу "Меры поддержки - для владельцев земли"
driver.get("https://moigektar.ru/documents/ipoteka")
time.sleep(1)
if driver.find_element(by=By.XPATH, value="//h1/b").is_displayed():
    print(' OK: 5.6 форма "Хотите узнать подробнее о господдержке?" на странице "Меры поддержки - сельская ипотека" есть')
else:
    print('ERROR: 5.6 нет формы "Хотите узнать подробнее о проекте?" на странице "Меры поддержки - сельская ипотека" \n       или селектор формы изменился')




# переход на страницу "Вопрос-ответ - подробности о проектах"
driver.get("https://moigektar.ru/faq")
time.sleep(1)
# проверка, что форма есть на странице
if driver.find_element(by=By.XPATH, value="//h1/b").is_displayed():
    print(' OK: 6.1.1 форма на странице "Вопрос-ответ - подробности о проектах" есть')
    # 6.1.2 раз форма есть, то проверим, что заголовок соответствует шаблону
    # (в этой форме костыль в виде частичного сравнения текста из-за того, что название формы разорвано <br>)
    form_7 = driver.find_element(by=By.XPATH, value="//h1/b")
    form_7_text = form_7.text
    if form_7_text.startswith("Не нашли нужного ответа"):
        print(' OK: 6.1.2 заголовок формы "Не нашли нужного ответа на Ваш вопрос?"')
    else:
        print('ERROR: 6.1.2 заголовок формы не "Не нашли нужного ответа на Ваш вопрос?", а ' + form_7_text)
    # 6.3 проверим, что есть кнопка на форме
    if driver.find_element(by=By.XPATH, value="//div[4]/button").is_displayed():
        print(' OK: 6.1.3 на форме есть кнопка')
        # 6.4 если кнопка есть, проверим, что её название соответствует шаблону
        button_7 = driver.find_element(by=By.XPATH, value="//div[4]/button")
        button_7_text = button_7.text
        if button_7_text == "ОТПРАВИТЬ":
            print(' OK: 6.1.4 кнопка называется "ОТПРАВИТЬ"')
        else:
            print("ERROR: 6.1.4 название кнопки не \"ОТПРАВИТЬ\", а " + button_7_text)
        # 6.5 раз кнопка есть, проверим, что при корректных данных заявка будет отправлена
        driver.find_element(by=By.XPATH, value="//div[22]/div/div[2]/div/div/div/div/ul[2]/li/form/div/div/input").send_keys("test")
        driver.find_element(by=By.XPATH, value="//div[22]/div/div[2]/div/div/div/div/ul[2]/li/form/div[2]/div/div/input").send_keys(
            "9999999999")
        driver.find_element(by=By.XPATH, value="//div[22]/div/div[2]/div/div/div/div/ul[2]/li/form/div[3]/div/input").send_keys("1@1.1")
        button_7.click()
        time.sleep(3)
        if driver.find_element(by=By.XPATH, value="//div[22]/div/div[2]/div/div/div/div/ul[2]/li[2]/div/div[2]").is_displayed():
            print(" OK: 6.1.5 данные были отправлены")
        else:
            if driver.find_element(by=By.XPATH, value="//div[4]/button").is_displayed():
                print("ERROR: 6.1.5 данные не были отправлены")
            else:
                print("ПАМАГИТИ")
    else:
        print('ERROR: 6.1.3 нет кнопки или её селектор изменился')
else:
    print('ERROR: 6.1.1 формы "Хотите узнать подробнее о господдержке?" нет или её селектор изменился')

# переход на страницу "Вопрос-ответ - о развитии участка"
# далее на трёх страницах проверка наличия формы, функционал которой уже проверен на странице "Подробности о проектах"
driver.get("https://moigektar.ru/faq/growth")
time.sleep(1)
if driver.find_element(by=By.XPATH, value="//h1/b").is_displayed():
    print(' OK: 6.2 форма "Не нашли нужного ответа на свой вопрос?" на странице "Вопрос-ответ - о развитии участка" есть')
else:
    print('ERROR: 6.2 нет формы "Не нашли нужного ответа на свой вопрос?" на странице "Вопрос-ответ - о развитии участка" \n       или селектор формы изменился')

# переход на страницу "Вопрос-ответ - стоимость земли"
driver.get("https://moigektar.ru/faq/cost")
time.sleep(1)
if driver.find_element(by=By.XPATH, value="//h1/b").is_displayed():
    print(' OK: 6.2 форма "Не нашли нужного ответа на свой вопрос?" на странице "Вопрос-ответ - стоимость земли" есть')
else:
    print('ERROR: 6.2 нет формы "Не нашли нужного ответа на свой вопрос?" на странице "Вопрос-ответ - стоимость земли" \n       или селектор формы изменился')

# переход на страницу "Вопрос-ответ - оформление земли"
driver.get("https://moigektar.ru/faq/own")
time.sleep(1)
if driver.find_element(by=By.XPATH, value="//h1/b").is_displayed():
    print(' OK: 6.2 форма "Не нашли нужного ответа на свой вопрос?" на странице "Вопрос-ответ - оформление земли" есть')
else:
    print('ERROR: 6.2 нет формы "Не нашли нужного ответа на свой вопрос?" на странице "Вопрос-ответ - оформление земли" \n       или селектор формы изменился')





# переход на страницу "Контакты"
driver.get("https://moigektar.ru/contacts")
time.sleep(1)
# проверка, что форма есть на странице
if driver.find_element(by=By.XPATH, value="//h1/b").is_displayed():
    print(' OK: 7.1 форма на странице "Контакты" есть')
    # 7.2 раз форма есть, то проверим, что заголовок соответствует шаблону
    form_6 = driver.find_element(by=By.XPATH, value="//h1/b")
    form_6_text = form_6.text
    if form_6_text.startswith("Хотите задать вопрос"):
        print(' OK: 7.2 заголовок формы "Хотите задать вопрос специалисту?"')
    else:
        print('ERROR: 7.2 заголовок формы не "Хотите задать вопрос специалисту?", а ' + form_6_text)
    # 7.3 проверим, что есть кнопка на форме
    if driver.find_element(by=By.XPATH, value="//div[4]/button").is_displayed():
        print(' OK: 7.3 на форме есть кнопка')
        # 7.4 если кнопка есть, проверим, что её название соответствует шаблону
        button_6 = driver.find_element(by=By.XPATH, value="//div[4]/button")
        button_6_text = button_6.text
        if button_6_text == "ОТПРАВИТЬ":
            print(' OK: 7.4 кнопка называется "ОТПРАВИТЬ"')
        else:
            print("ERROR: 7.4 название кнопки не \"ОТПРАВИТЬ\", а " + button_6_text)
        # 7.5 раз кнопка есть, проверим, что при корректных данных заявка будет отправлена
        driver.find_element(by=By.XPATH, value="//div[2]/div/ul[2]/li/form/div/div/input").send_keys("test")
        driver.find_element(by=By.XPATH, value="//div[2]/div/ul[2]/li/form/div[2]/div/div/input").send_keys(
            "9999999999")
        driver.find_element(by=By.XPATH, value="//div[2]/div/ul[2]/li/form/div[3]/div/input").send_keys("1@1.1")
        button_6.click()
        time.sleep(3)
        if driver.find_element(by=By.XPATH, value="//div[2]/div/ul[2]/li[2]/div/div[2]").is_displayed():
            print(" OK: 7.5 данные были отправлены")
        else:
            if driver.find_element(by=By.XPATH, value="//div[4]/button").is_displayed():
                print("ERROR: 7.5 данные не были отправлены")
            else:
                print("ПАМАГИТИ")
    else:
        print('ERROR: 7.3 нет кнопки или её селектор изменился')
else:
    print('ERROR: 7.1 формы "Хотите задать вопрос специалисту?" нет или её селектор изменился')


#time.sleep(10)
driver.quit()