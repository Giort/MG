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


# Скрипт проверяет наличие всех блоков на МГ по заголовкам или (реже) другим элементам
#
# В лог выводится сообщение "ОК", если блок был найден
# В лог выводится сообщение "ERROR", если элемент не загрузился


# 1. Главная
driver.get("https://moigektar.ru/")
print('Главная')
try:
    wait(driver,14).until(EC.presence_of_element_located((By.XPATH, "//li[@class='uk-active']/a[@href='/']")))
    print('   хедер: OK')
except:
    print('ERROR: проблема с хедером на главной МГ')

try:
    wait(driver,14).until(EC.visibility_of_element_located((By.XPATH, "//span[text()[contains(.,'Гектар')]]")))
    print('   баннер под хедером: OK')
except:
    print('ERROR: проблема с баннером под хедером на главной МГ')

try:
    wait(driver,14).until(EC.visibility_of_element_located((By.XPATH, "//h1[text()[contains(.,'Проект')]]")))
    print('   блок "Проект МГ - это": OK')
except:
    print('ERROR: проблема с блоком "Проект МГ - это" на главной МГ')

try:
    wait(driver,14).until(EC.visibility_of_element_located((By.XPATH, "//h1[text()[contains(.,'Гектар под ваши')]]")))
    print('   блок "Гектар под ваши цели": OK')
except:
    print('ERROR: проблема с блоком "Гектар под ваши цели" на главной МГ')

try:
    wait(driver,14).until(EC.visibility_of_element_located((By.XPATH, "//h1[text()[contains(.,'Лучшее время')]]")))
    print('   блок "Лучшее время для покупки": OK')
except:
    print('ERROR: проблема с блоком "Лучшее время для покупки" на главной МГ')

try:
    title = wait(driver,14).until(EC.visibility_of_element_located((By.XPATH, "//div[(contains(@class, 'uk-visible'))]//h1[text()[contains(.,'Специальное предложение')]]")))
    print('   блок "Специальное предложение": OK')
    try:
        actions.move_to_element(title).send_keys(Keys.PAGE_DOWN).perform()
        wait(driver,14).until(EC.visibility_of_element_located((By.XPATH, "//div[(contains(@class, 'uk-visible'))]//div[@id='catalogueSpecial']/div/div/div/div[1]//li[1]//button")))
        print('   карточки в СП: OK')
    except:
        print('ERROR: проблема с карточками СП на главной МГ')
except (TimeoutException, NoSuchElementException, ElementNotVisibleException):
    print('ERROR: проблема с блоком "Специальное предложение" на главной МГ')

try:
    wait(driver,14).until(EC.visibility_of_element_located((By.XPATH, "//h2[text()[contains(.,'Виртуальный тур')]]")))
    print('   блок "Виртуальный тур": OK')
except:
    print('ERROR: проблема с блоком "Виртуальный тур" на главной МГ')

try:
    wait(driver,14).until(EC.visibility_of_element_located((By.XPATH, "//h1[text()[contains(.,'Лучшие поселки')]]")))
    print('   блок "Лучшие поселки": OK')
except:
    print('ERROR: проблема с блоком "Лучшие поселки проекта" на главной МГ')

try:
    wait(driver,14).until(EC.visibility_of_element_located((By.XPATH, "//h1[text()[contains(.,'Видео, которые')]]")))
    print('   блок "Видео, которые": OK')
except:
    print('ERROR: проблема с блоком "Видео, которые вам стоит увидеть" на главной МГ')

try:
    wait(driver,14).until(EC.visibility_of_element_located((By.XPATH, "//div[text()[contains(.,'Награды проекта')]]")))
    print('   блок "Награды проекта": OK')
except:
    print('ERROR: проблема с блоком "Награды проекта" на главной МГ')

try:
    wait(driver,14).until(EC.visibility_of_element_located((By.XPATH, "//div[text()[contains(.,'СМИ о проекте')]]")))
    print('   блок "СМИ о проекте": OK')
except:
    print('ERROR: проблема с блоком "СМИ о проекте" на главной МГ')

try:
    wait(driver,14).until(EC.visibility_of_element_located((By.XPATH, "//h1[text()[contains(.,'Развитие вашего участка')]]")))
    print('   блок "Развитие вашего участка": OK')
except:
    print('ERROR: проблема с блоком "Развитие вашего участка" на главной МГ')

try:
    wait(driver,14).until(EC.visibility_of_element_located((By.XPATH, "//h1[text()[contains(.,'Быстрый старт')]]")))
    print('   блок "Быстрый старт": OK')
except:
    print('ERROR: проблема с блоком "Быстрый старт" на главной МГ')

try:
    wait(driver,14).until(EC.visibility_of_element_located((By.XPATH, "//div[text()[contains(.,'Время вкладывать')]]")))
    print('   блок "Время вкладывать": OK')
except:
    print('ERROR: проблема с блоком "Время вкладывать" на главной МГ')

try:
    wait(driver,14).until(EC.visibility_of_element_located((By.XPATH, "//h1[text()[contains(.,'Сохраните свои')]]")))
    print('   блок "Сохраните свои": OK')
except:
    print('ERROR: проблема с блоком "Сохраните свои" на главной МГ')

try:
    wait(driver,14).until(EC.visibility_of_element_located((By.XPATH, "//div[text()[contains(.,'Почему нам')]]")))
    print('   блок "Почему нам доверяют": OK')
except:
    print('ERROR: проблема с блоком "Почему нам доверяют" на главной МГ')

try:
    wait(driver,14).until(EC.visibility_of_element_located((By.XPATH, "//h1[text()[contains(.,'Государственная поддержка')]]")))
    print('   блок "Государственная поддержка": OK')
except:
    print('ERROR: проблема с блоком "Государственная поддержка" на главной МГ')

try:
    wait(driver,14).until(EC.visibility_of_element_located((By.XPATH, "//b[text()[contains(.,'Хотите узнать ')]]")))
    print('   форма "Хотите узнать подробнее": OK')
except:
    print('ERROR: проблема с формой "Хотите узнать подробнее о проекте?" на главной МГ')

try:
    wait(driver,14).until(EC.visibility_of_element_located((By.XPATH, "//div[text()[contains(.,'Центр')]]")))
    print('   блок "Центр правовой поддержки": OK')
except:
    print('ERROR: проблема с блоком "Центр правовой поддержки" на главной МГ')

try:
    wait(driver,14).until(EC.visibility_of_element_located((By.XPATH, "//h1[text()[contains(.,'Варианты')]]")))
    print('   блок "Варианты строительства": OK')
except:
    print('ERROR: проблема с блоком "Варианты строительства" на главной МГ')

try:
    wait(driver,14).until(EC.visibility_of_element_located((By.XPATH, "//b[text()[contains(.,'Получите каталог')]]")))
    print('   форма "Получите каталог": OK')
except:
    print('ERROR: проблема с формой "Получите каталог" на главной МГ')

try:
    wait(driver,14).until(EC.visibility_of_element_located((By.XPATH, "//div[text()[contains(.,'Отзывы о проекте')]]")))
    print('   блок "Отзывы о проекте": OK')
except:
    print('ERROR: проблема с блоком "Отзывы о проекте" на главной МГ')

try:
    wait(driver,14).until(EC.visibility_of_element_located((By.XPATH, "//h1[text()[contains(.,'Бизнес-планы')]]")))
    print('   блок "Бизнес-планы": OK')
except:
    print('ERROR: проблема с блоком "Бизнес-планы" на главной МГ')

try:
    wait(driver,14).until(EC.visibility_of_element_located((By.XPATH, "//div[text()[contains(.,'Личный кабинет')]]")))
    print('   блок "Личный кабинет": OK')
except:
    print('ERROR: проблема с блоком "Личный кабинет" на главной МГ')

try:
    wait(driver,14).until(EC.visibility_of_element_located((By.XPATH, "//div[text()[contains(.,'в соцсетях')]]")))
    print('   блок "Подпишитесь в соцсетях": OK')
except:
    print('ERROR: проблема с блоком "Подпишитесь в соцсетях" на главной МГ')

try:
    wait(driver,14).until(EC.visibility_of_element_located((By.XPATH, "//b[text()[contains(.,'Подпишитесь на рассылку')]]")))
    print('   форма "Подпишитесь на рассылку": OK')
except:
    print('ERROR: проблема с формой "Подпишитесь на рассылку" на главной МГ')

try:
    wait(driver,14).until(EC.visibility_of_element_located((By.XPATH, "//h1[text()[contains(.,'на новости проекта')]]")))
    print('   блок "Подпишитесь на новости проекта": OK')
except:
    print('ERROR: проблема с блоком "Подпишитесь на новости проекта" на главной МГ')

try:
    wait(driver,14).until(EC.visibility_of_element_located((By.XPATH, "//h1[text()[contains(.,'От сохи')]]")))
    print('   блок "От сохи до сохи": OK')
except:
    print('ERROR: проблема с блоком "Проект "От сохи до сохи" на главной МГ')

try:
    wait(driver,14).until(EC.visibility_of_element_located((By.XPATH, "//b[text()[contains(.,'Действуйте')]]")))
    print('   форма "Действуйте": OK')
except:
    print('ERROR: проблема с формой "Действуйте" на главной МГ')

try:
    wait(driver,14).until(EC.visibility_of_element_located((By.XPATH, "//div[text()[contains(.,'Приглашаем на встречу')]]")))
    print('   блок "Приглашаем на встречу": OK')
except:
    print('ERROR: проблема с блоком "Приглашаем на встречу" на главной МГ')

try:
    wait(driver,14).until(EC.presence_of_element_located((By.XPATH, "//div[@class='w-footer']/div/div/div/div/button[text()[contains(.,'Связаться')]]")))
    print('   футер: OK\n')
except:
    print('ERROR: проблема с футером на главной МГ\n')

# 2. Каталог
driver.get('https://moigektar.ru/catalogue')
print("Каталог")
try:
    wait(driver,14).until(EC.visibility_of_element_located((By.XPATH, "//h1[text()[contains(.,'Специальное предложение')]]")))
    print('   блок "Специальное предложение": OK')
    try:
        wait(driver,14).until(EC.visibility_of_element_located((By.XPATH, "//*[text()[contains(., 'Специальное предложение')]]//parent::div//div[@uk-slider='sets: true']//li[1]//div/button/span")))
        print('   карточки в СП: OK')
    except:
        print('ERROR: проблема с карточками СП в каталоге')
except (TimeoutException, NoSuchElementException, ElementNotVisibleException):
    print('ERROR: проблема с блоком "Специальное предложение" в каталоге')

try:
    wait(driver,14).until(EC.presence_of_element_located((By.XPATH, "//h1[text()[contains(.,'Лучшие поселки')]]")))
    print('   блок "Лучшие поселки": OK')
except:
    print('ERROR: проблема с блоком "Лучшие поселки" в каталоге')

try:
    wait(driver,14).until(EC.presence_of_element_located((By.XPATH, "//h1[text()[contains(.,'Поселки в развитии')]]")))
    print('   блок "Поселки в развитии": OK')
except:
    print('ERROR: проблема с блоком "Поселки в развитии" в каталоге')

try:
    title = wait(driver,14).until(EC.visibility_of_element_located((By.XPATH, "//h1[text()[contains(., 'Дачные участки')]]")))
    print('   блок "Дачные участки": OK')
    try:
        actions.move_to_element(title).send_keys(Keys.PAGE_DOWN).send_keys(Keys.ARROW_DOWN).perform()
        wait(driver,14).until(EC.visibility_of_element_located((By.XPATH, "//h1[text()[contains(., 'Дачные участки')]]//parent::div//div[1]/div/div//li[1]//button/span")))
        print('   карточки в "Дачных участках": OK')
    except:
        print('ERROR: проблема с карточками в "Дачных участках" в каталоге')
except (TimeoutException, NoSuchElementException, ElementNotVisibleException):
    print('ERROR: проблема с блоком "Дачные участки" в каталоге')

try:
    wait(driver,14).until(EC.presence_of_element_located((By.XPATH, "//h1[text()[contains(.,'Подберите ваш')]]")))
    print('   баннер "Подберите ваш ...": OK')
except:
    print('ERROR: проблема с баннером "Подберите ваш идеальный гектар" в каталоге')

try:
    wait(driver,14).until(EC.presence_of_element_located((By.XPATH, "//h1[text()[contains(.,'Инвестиционные')]]")))
    print('   блок "Инвестпроекты": OK')
except:
    print('ERROR: проблема с блоком "Инвестиционные проекты" в каталоге')

try:
    wait(driver,14).until(EC.presence_of_element_located((By.XPATH, "//h1[text()[contains(.,'Долина')]]")))
    print('   баннер "Долина Вазузы": OK')
except:
    print('ERROR: проблема с баннером "Долина Вазузы" в каталоге')

try:
    wait(driver,14).until(EC.visibility_of_element_located((By.XPATH, "//b[text()[contains(.,'Хотите узнать ')]]")))
    print('   форма "Хотите узнать подробнее": OK\n')
except:
    print('ERROR: проблема с формой "Хотите узнать подробнее о проекте?" в каталоге\n')

time.sleep(1)
driver.quit()

