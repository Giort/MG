import chromedriver_binary
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
ch_options = Options()
#ch_options.add_argument('--headless')
ch_options.page_load_strategy = 'eager'
driver = webdriver.Chrome(options= ch_options)
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
actions = ActionChains(driver)
from selenium.webdriver.common.by import By
import time
import json
driver.set_window_size(1600, 880)

with open('credentials.json', 'r') as file:
    cred = json.load(file)

list = len(cred['users'])
i = 0

for acc in range(list):
    try:
        # страница логина, логин в сервис
        if i != 0:  # для всех пользователей, кроме первого, в форму уже будет подставлен предыдущий логин, поэтому
            driver.get("https://passport.yandex.ru/auth?retpath=https://mail.yandex.ru")
            acc_change = wait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//a[@class='CurrentAccount CurrentAccount_theme_default']")))
            acc_change.click() # нужно выбрать вход в другой аккаунт
            acc_add = wait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//*[@class='AddAccountButton-icon']")))
            acc_add.click()
            driver.find_element(by=By.XPATH, value="//*[@data-type='login']").click()
            login_input = driver.find_element(by=By.ID, value="passp-field-login")
            login_input.send_keys(cred['users'][i]['login'])
            driver.find_element(by=By.ID, value="passp:sign-in").click()
            passwd_input = wait(driver, 20).until(EC.element_to_be_clickable((By.ID, "passp-field-passwd")))
            passwd_input.send_keys(cred['users'][i]['password'])
            driver.find_element(by=By.ID, value="passp:sign-in").click()
        else: # только для первого пользователя
            driver.get("https://passport.yandex.ru/auth?retpath=https://mail.yandex.ru")
            login_by_pass_btn = wait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//*[@data-type='login']")))
            login_by_pass_btn.click()
            login_input = wait(driver, 20).until(EC.element_to_be_clickable((By.ID, "passp-field-login")))
            login_input.send_keys(cred['users'][i]['login'])
            driver.find_element(by=By.ID, value="passp:sign-in").click()
            passwd_input = wait(driver, 20).until(EC.element_to_be_clickable((By.ID, "passp-field-passwd")))
            passwd_input.send_keys(cred['users'][i]['password'])
            driver.find_element(by=By.ID, value="passp:sign-in").click()
        try: # если открылась страница проверки на роботность
            robot_on = wait(driver,3).until(EC.element_to_be_clickable((By.XPATH, '//input[@type="submit"]')))
            if robot_on:
                driver.find_element(by=By.XPATH, value='//*[@type="submit"]').click()
        except:
            pass
        try: # если открылась страница с предложением добавить дополнительный имейл
            add_mail_on = wait(driver,1).until(EC.element_to_be_clickable((By.XPATH, '//button[@data-t="button:pseudo"]')))
            if add_mail_on:
                driver.find_element(by=By.XPATH, value='//button[@data-t="button:pseudo"]').click()
        except:
            pass
        try: # если открылась страница с предложением принять условия
            acc_terms = wait(driver,1).until(EC.element_to_be_clickable((By.XPATH, '//form[@data-form-name="complete-pdd"]//button')))
            if acc_terms:
                driver.find_element(by=By.XPATH, value='//form[@data-form-name="complete-pdd"]//button').click()
        except:
            pass
        # страница "Входящие", проверка, что страница загрузилась
        wait(driver, 15).until(EC.presence_of_element_located((By.XPATH, '//head/title[text()[contains(., "Входящие")]]')))
        # переход в Настройки
        driver.find_element(by=By.XPATH, value="//button[@aria-label='Настройки']").click()
        driver.find_element(by=By.XPATH, value="//a[@href='#setup']").click()
        # переход в Почтовые программы
        wait(driver, 15).until(EC.presence_of_element_located((By.XPATH, '//a[@href="#setup/client"]')))
        driver.find_element(by=By.XPATH, value='//a[@href="#setup/client"]').click()
        # установка чекбокса
        wait(driver, 15).until(EC.presence_of_element_located((By.NAME, 'enable_imap_auth_plain')))
        danger_text = driver.find_element(by=By.XPATH, value='//*[text()[contains(., "Портальный пароль")]]//ancestor::div[1]//img').is_displayed()
        if danger_text == False:
            driver.find_element(by=By.XPATH, value='//*[text()[contains(., "Портальный пароль")]]//preceding::span[2]').click()
            driver.find_element(by=By.XPATH, value='//*[text()[contains(., "сохранить изменения")]]').click()
            print("Пользователь " + cred['users'][i]['login'] + ": чекбокс установлен, изменения сохранены")
        elif danger_text:
            print("Пользователь " + cred['users'][i]['login'] + ": чекбокс уже был включён")
        driver.find_element(by=By.XPATH, value='//a[@href="https://passport.yandex.ru"]').click()
        driver.find_element(by=By.XPATH, value='//*[text()[contains(., "Выйти из сервисов Яндекса")]]').click()
        i += 1
    except:
        print("Пользователь " + cred['users'][i]['login'] + ": что-то пошло не так")


time.sleep(10)
driver.quit()
