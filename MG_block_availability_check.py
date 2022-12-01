from selenium import webdriver
from selenium.webdriver.chrome.options import Options
ch_options = Options()
ch_options.add_argument('--headless')
driver = webdriver.Chrome(options=ch_options)
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
actions = ActionChains(driver)
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import ElementNotVisibleException
from selenium.webdriver.common.keys import Keys
import time
driver.maximize_window()


# Скрипт проверяет наличие всех блоков на МГ

# 1. Главная
driver.get("https://moigektar.ru/")
print('Главная')
try:
    wait(driver,14).until(EC.presence_of_element_located((By.XPATH, "//li[@class='uk-active']/a[@href='/']")))
    print('   хедер: OK')
except (TimeoutException, NoSuchElementException):
    print('ERROR: проблема с хедером')

try:
    wait(driver,14).until(EC.visibility_of_element_located((By.XPATH, "//span[text()[contains(.,'Гектар')]]")))
    print('   баннер под хедером: OK')
except (NoSuchElementException, TimeoutException, ElementNotVisibleException):
    print('ERROR: проблема с баннером под хедером')

try:
    wait(driver,14).until(EC.visibility_of_element_located((By.XPATH, "//h1[text()[contains(.,'Проект')]]")))
    print('   блок "Проект МГ - это": OK')
except (NoSuchElementException, TimeoutException, ElementNotVisibleException):
    print('ERROR: проблема с блоком "Проект МГ - это"')

try:
    wait(driver,14).until(EC.visibility_of_element_located((By.XPATH, "//h1[text()[contains(.,'Гектар под ваши')]]")))
    print('   блок "Гектар под ваши цели": OK')
except (NoSuchElementException, TimeoutException, ElementNotVisibleException):
    print('ERROR: проблема с блоком "Гектар под ваши цели"')

try:
    wait(driver,14).until(EC.visibility_of_element_located((By.XPATH, "//h1[text()[contains(.,'Лучшее время')]]")))
    print('   блок "Лучшее время для покупки": OK')
except (NoSuchElementException, TimeoutException, ElementNotVisibleException):
    print('ERROR: проблема с блоком "Лучшее время для покупки"')

try:
    title = wait(driver,14).until(EC.visibility_of_element_located((By.XPATH, "//h1[text()[contains(.,'Специальное предложение')]]")))
    print('   блок "Специальное предложение": OK')
    try:
        actions.move_to_element(title).send_keys(Keys.PAGE_DOWN).perform()
        wait(driver,14).until(EC.visibility_of_element_located((By.XPATH, "//div[@id='catalogueSpecial']/div/div/div/div[1]//li[1]//button")))
        print('   карточки в СП: OK')
    except (NoSuchElementException, TimeoutException, ElementNotVisibleException):
        print('ERROR: проблема с карточками СП')
except (TimeoutException, NoSuchElementException, ElementNotVisibleException):
    print('ERROR: проблема с блоком "Специальное предложение"')

try:
    wait(driver,14).until(EC.visibility_of_element_located((By.XPATH, "//h2[text()[contains(.,'Виртуальный тур')]]")))
    print('   блок "Виртуальный тур": OK')
except (NoSuchElementException, TimeoutException, ElementNotVisibleException):
    print('ERROR: проблема с блоком "Виртуальный тур"')

try:
    wait(driver,14).until(EC.visibility_of_element_located((By.XPATH, "//h1[text()[contains(.,'Лучшие поселки')]]")))
    print('   блок "Лучшие поселки": OK')
except (NoSuchElementException, TimeoutException, ElementNotVisibleException):
    print('ERROR: проблема с блоком "Лучшие поселки проекта"')

try:
    wait(driver,14).until(EC.visibility_of_element_located((By.XPATH, "//h1[text()[contains(.,'Видео, которые')]]")))
    print('   блок "Видео, которые": OK')
except (NoSuchElementException, TimeoutException, ElementNotVisibleException):
    print('ERROR: проблема с блоком "Видео, которые вам стоит увидеть"')

try:
    wait(driver,14).until(EC.visibility_of_element_located((By.XPATH, "//div[text()[contains(.,'СМИ о проекте')]]")))
    print('   блок "СМИ о проекте": OK')
except (NoSuchElementException, TimeoutException, ElementNotVisibleException):
    print('ERROR: проблема с блоком "СМИ о проекте"')

try:
    wait(driver,14).until(EC.visibility_of_element_located((By.XPATH, "//h1[text()[contains(.,'Развитие вашего участка')]]")))
    print('   блок "Развитие вашего участка": OK')
except (NoSuchElementException, TimeoutException, ElementNotVisibleException):
    print('ERROR: проблема с блоком "Развитие вашего участка"')

try:
    wait(driver,14).until(EC.visibility_of_element_located((By.XPATH, "//h1[text()[contains(.,'Быстрый старт')]]")))
    print('   блок "Быстрый старт": OK')
except (NoSuchElementException, TimeoutException, ElementNotVisibleException):
    print('ERROR: проблема с блоком "Быстрый старт"')

try:
    wait(driver,14).until(EC.visibility_of_element_located((By.XPATH, "//div[text()[contains(.,'Время вкладывать')]]")))
    print('   блок "Время вкладывать": OK')
except (NoSuchElementException, TimeoutException, ElementNotVisibleException):
    print('ERROR: проблема с блоком "Время вкладывать"')

try:
    wait(driver,14).until(EC.visibility_of_element_located((By.XPATH, "//h1[text()[contains(.,'Сохраните свои')]]")))
    print('   блок "Сохраните свои": OK')
except (NoSuchElementException, TimeoutException, ElementNotVisibleException):
    print('ERROR: проблема с блоком "Сохраните свои"')

try:
    wait(driver,14).until(EC.visibility_of_element_located((By.XPATH, "//div[text()[contains(.,'Почему нам')]]")))
    print('   блок "Почему нам доверяют": OK')
except (NoSuchElementException, TimeoutException, ElementNotVisibleException):
    print('ERROR: проблема с блоком "Почему нам доверяют"')

try:
    wait(driver,14).until(EC.visibility_of_element_located((By.XPATH, "//h1[text()[contains(.,'Государственная поддержка')]]")))
    print('   блок "Государственная поддержка": OK')
except (NoSuchElementException, TimeoutException, ElementNotVisibleException):
    print('ERROR: проблема с блоком "Государственная поддержка"')

try:
    wait(driver,14).until(EC.visibility_of_element_located((By.XPATH, "//b[text()[contains(.,'Хотите узнать ')]]")))
    print('   форма "Хотите узнать подробнее": OK')
except (NoSuchElementException, TimeoutException, ElementNotVisibleException):
    print('ERROR: проблема с формой "Хотите узнать подробнее о проекте?"')

try:
    wait(driver,14).until(EC.visibility_of_element_located((By.XPATH, "//div[text()[contains(.,'Центр')]]")))
    print('   блок "Центр правовой поддержки": OK')
except (NoSuchElementException, TimeoutException, ElementNotVisibleException):
    print('ERROR: проблема с блоком "Центр правовой поддержки"')

try:
    wait(driver,14).until(EC.visibility_of_element_located((By.XPATH, "//h1[text()[contains(.,'Варианты')]]")))
    print('   блок "Варианты строительства": OK')
except (NoSuchElementException, TimeoutException, ElementNotVisibleException):
    print('ERROR: проблема с блоком "Варианты строительства"')

try:
    wait(driver,14).until(EC.visibility_of_element_located((By.XPATH, "//b[text()[contains(.,'Получите каталог')]]")))
    print('   форма "Получите каталог": OK')
except (NoSuchElementException, TimeoutException, ElementNotVisibleException):
    print('ERROR: проблема с формой "Получите каталог"')

try:
    wait(driver,14).until(EC.visibility_of_element_located((By.XPATH, "//div[text()[contains(.,'Отзывы о проекте')]]")))
    print('   блок "Отзывы о проекте": OK')
except (NoSuchElementException, TimeoutException, ElementNotVisibleException):
    print('ERROR: проблема с блоком "Отзывы о проекте"')

try:
    wait(driver,14).until(EC.visibility_of_element_located((By.XPATH, "//h1[text()[contains(.,'Бизнес-планы')]]")))
    print('   блок "Бизнес-планы": OK')
except (NoSuchElementException, TimeoutException, ElementNotVisibleException):
    print('ERROR: проблема с блоком "Бизнес-планы"')

try:
    wait(driver,14).until(EC.visibility_of_element_located((By.XPATH, "//div[text()[contains(.,'Личный кабинет')]]")))
    print('   блок "Личный кабинет": OK')
except (NoSuchElementException, TimeoutException, ElementNotVisibleException):
    print('ERROR: проблема с блоком "Личный кабинет"')

try:
    wait(driver,14).until(EC.visibility_of_element_located((By.XPATH, "//div[text()[contains(.,'в соцсетях')]]")))
    print('   блок "Подпишитесь в соцсетях": OK')
except (NoSuchElementException, TimeoutException, ElementNotVisibleException):
    print('ERROR: проблема с блоком "Подпишитесь в соцсетях"')

try:
    wait(driver,14).until(EC.visibility_of_element_located((By.XPATH, "//b[text()[contains(.,'Подпишитесь на рассылку')]]")))
    print('   форма "Подпишитесь на рассылку": OK')
except (NoSuchElementException, TimeoutException, ElementNotVisibleException):
    print('ERROR: проблема с формой "Подпишитесь на рассылку"')

try:
    wait(driver,14).until(EC.visibility_of_element_located((By.XPATH, "//h1[text()[contains(.,'на новости проекта')]]")))
    print('   блок "Подпишитесь на новости проекта": OK')
except (NoSuchElementException, TimeoutException, ElementNotVisibleException):
    print('ERROR: проблема с блоком "Подпишитесь на новости проекта"')

try:
    wait(driver,14).until(EC.visibility_of_element_located((By.XPATH, "//h1[text()[contains(.,'От сохи')]]")))
    print('   блок "От сохи до сохи": OK')
except (NoSuchElementException, TimeoutException, ElementNotVisibleException):
    print('ERROR: проблема с блоком "Проект "От сохи до сохи"')

try:
    wait(driver,14).until(EC.visibility_of_element_located((By.XPATH, "//b[text()[contains(.,'Действуйте')]]")))
    print('   форма "Действуйте": OK')
except (NoSuchElementException, TimeoutException, ElementNotVisibleException):
    print('ERROR: проблема с формой "Действуйте"')

try:
    wait(driver,14).until(EC.visibility_of_element_located((By.XPATH, "//div[text()[contains(.,'Приглашаем на встречу')]]")))
    print('   блок "Приглашаем на встречу": OK')
except (NoSuchElementException, TimeoutException, ElementNotVisibleException):
    print('ERROR: проблема с блоком "Приглашаем на встречу"')

try:
    wait(driver,14).until(EC.presence_of_element_located((By.XPATH, "//div[@class='w-footer']/div/div/div/div/button[text()[contains(.,'Связаться')]]")))
    print('   футер: OK\n')
except (TimeoutException, NoSuchElementException):
    print('ERROR: проблема с футером\n')

# 2. Каталог
driver.get('https://moigektar.ru/catalogue')
print("Каталог")
try:
    wait(driver,14).until(EC.visibility_of_element_located((By.XPATH, "//h1[text()[contains(.,'Специальное предложение')]]")))
    print('   блок "Специальное предложение": OK')
    try:
        wait(driver,14).until(EC.visibility_of_element_located((By.XPATH, "//*[text()[contains(., 'Специальное предложение')]]//parent::div//div[@uk-slider='sets: true']//li[1]//div/button/span")))
        print('   карточки в СП: OK')
    except (NoSuchElementException, TimeoutException, ElementNotVisibleException):
        print('ERROR: проблема с карточками СП')
except (TimeoutException, NoSuchElementException, ElementNotVisibleException):
    print('ERROR: проблема с блоком "Специальное предложение"')

try:
    wait(driver,14).until(EC.presence_of_element_located((By.XPATH, "//h1[text()[contains(.,'Лучшие поселки')]]")))
    print('   блок "Лучшие поселки": OK')
except (TimeoutException, NoSuchElementException):
    print('ERROR: проблема с блоком "Лучшие поселки"')

try:
    wait(driver,14).until(EC.presence_of_element_located((By.XPATH, "//h1[text()[contains(.,'Поселки в развитии')]]")))
    print('   блок "Поселки в развитии": OK')
except (TimeoutException, NoSuchElementException):
    print('ERROR: проблема с блоком "Поселки в развитии"')

try:
    title = wait(driver,14).until(EC.visibility_of_element_located((By.XPATH, "//h1[text()[contains(., 'Дачные участки')]]")))
    print('   блок "Дачные участки": OK')
    try:
        actions.move_to_element(title).send_keys(Keys.PAGE_DOWN).perform()
        wait(driver,14).until(EC.visibility_of_element_located((By.XPATH, "//h1[text()[contains(., 'Дачные участки')]]//parent::div//div[1]/div/div//li[1]//button/span")))
        print('   карточки в "Дачных участках": OK')
    except (NoSuchElementException, TimeoutException, ElementNotVisibleException):
        print('ERROR: проблема с карточками в "Дачных участках"')
except (TimeoutException, NoSuchElementException, ElementNotVisibleException):
    print('ERROR: проблема с блоком "Дачные участки"')

try:
    wait(driver,14).until(EC.presence_of_element_located((By.XPATH, "//h1[text()[contains(.,'Подберите ваш')]]")))
    print('   баннер "Подберите ваш ...": OK')
except (TimeoutException, NoSuchElementException):
    print('ERROR: проблема с баннером "Подберите ваш идеальный гектар"')

try:
    wait(driver,14).until(EC.presence_of_element_located((By.XPATH, "//h1[text()[contains(.,'Инвестиционные')]]")))
    print('   блок "Инвестпроекты": OK')
except (TimeoutException, NoSuchElementException):
    print('ERROR: проблема с блоком "Инвестиционные проекты"')

try:
    wait(driver,14).until(EC.presence_of_element_located((By.XPATH, "//h1[text()[contains(.,'Долина')]]")))
    print('   баннер "Долина Вазузы": OK')
except (TimeoutException, NoSuchElementException):
    print('ERROR: проблема с баннером "Долина Вазузы"')

try:
    wait(driver,14).until(EC.visibility_of_element_located((By.XPATH, "//b[text()[contains(.,'Хотите узнать ')]]")))
    print('   форма "Хотите узнать подробнее": OK\n')
except (NoSuchElementException, TimeoutException, ElementNotVisibleException):
    print('ERROR: проблема с формой "Хотите узнать подробнее о проекте?"\n')

time.sleep(1)
driver.quit()
