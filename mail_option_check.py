from selenium import webdriver
from selenium.webdriver.chrome.options import Options
ch_options = Options()
#ch_options.add_argument('--headless')
driver = webdriver.Chrome(options= ch_options)
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
actions = ActionChains(driver)
from selenium.webdriver.common.by import By
import time
driver.set_window_size(1600, 800)

driver.implicitly_wait(10)



login = "login"
passwd = "password"

try:
    # страница логина, логин в сервис
    driver.get("https://passport.yandex.ru/auth?retpath=https://mail.yandex.ru")
    driver.find_element(by=By.XPATH, value="//*[@data-type='login']").click()
    login_input = driver.find_element(by=By.ID, value="passp-field-login")
    login_input.send_keys(login)
    driver.find_element(by=By.ID, value="passp:sign-in").click()
    passwd_input = driver.find_element(by=By.ID, value="passp-field-passwd")
    passwd_input.send_keys(passwd)
    driver.find_element(by=By.ID, value="passp:sign-in").click()
    # страница "Входящие"
    # проверка, что страница загрузилась
    wait(driver, 15).until(EC.presence_of_element_located((By.XPATH, '//head/title[text()[contains(., "Входящие")]]')))
    # переход в Настройки
    driver.find_element(by=By.XPATH, value="//button[@aria-label='Настройки']").click()
    driver.find_element(by=By.XPATH, value="//a[@href='#setup']").click()
    # переход в Почтовые программы
    wait(driver, 15).until(EC.presence_of_element_located((By.XPATH, '//a[@href="#setup/client"]')))
    driver.find_element(by=By.XPATH, value='//a[@href="#setup/client"]').click()
    # установка чекбокса
    wait(driver, 15).until(EC.presence_of_element_located((By.NAME, 'enable_imap_auth_plain')))
    portal_passw = driver.find_element(by=By.NAME, value='enable_imap_auth_plain')
    danger_text = driver.find_element(by=By.XPATH, value='//*[text()[contains(., "Портальный пароль")]]//ancestor::div[1]//img').is_displayed()
    if danger_text == False:
        driver.find_element(by=By.XPATH, value='//*[text()[contains(., "Портальный пароль")]]//preceding::span[2]').click()
except:
    print("ERROR: что-то не так, пользователь " + login)


time.sleep(10)
driver.quit()
