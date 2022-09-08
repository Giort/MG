from selenium import webdriver
from selenium.webdriver.chrome.options import Options
options = Options()
#options.add_argument('--headless')
ch_options = Options()
#ch_options.add_argument('--headless')
driver = webdriver.Chrome(options= ch_options)
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
driver.maximize_window()


from selenium.webdriver.common.by import By
import time



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
        driver.find_element(by=By.XPATH, value="//div[24]/div/div[2]/div/ul[2]/li[1]/form/div[1]/div/input").send_keys("test")
        driver.find_element(by=By.XPATH, value="/html/body/div[24]/div/div[2]/div/ul[2]/li[1]/form/div[2]/div/div[1]/input").send_keys(
            "9999999999")
        driver.find_element(by=By.XPATH, value="/html/body/div[24]/div/div[2]/div/ul[2]/li[1]/form/div[3]/div/input").send_keys("1@1.1")
        button_6.click()
        time.sleep(3)
        if driver.find_element(by=By.XPATH, value="/html/body/div[24]/div/div[2]/div/ul[2]/li[2]/div/div[2]").is_displayed():
            print(" OK: 5.1.5 данные были отправлены")
        else:
            if driver.find_element(by=By.XPATH, value="//div[4]/button").is_displayed():
                print("ERROR: 5.1.5 данные не были отправлены")
            else:
                print("SMTHNG WRNG")
    else:
        print('ERROR: 5.1.3 нет кнопки или её селектор изменился')
else:
    print('ERROR: 5.1.1 формы "Хотите узнать подробнее о господдержке?" нет или её селектор изменился')


time.sleep(20)
driver.quit()