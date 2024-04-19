import chromedriver_binary
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
ch_options = Options()
ch_options.add_argument('--headless')
ch_options.page_load_strategy = 'eager'
service = ChromeService(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=ch_options)
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time
import json
actions = ActionChains(driver)
#driver.maximize_window()
driver.set_window_size(1680, 1000)

with open('data.json', 'r') as file:
    data = json.load(file)

# Скрипт последовательно заходит на каждый сервис МГ и проверяет видимость
# одного элемента на странице
#
# В лог выводится сообщение "ОК", если этот элемент найден
# В лог выводится сообщение "ERROR", если истекло время ожидания элемента
#


# 1. проверка "МГ" по видимости заголовка "Гектар под ваши цели" на главной
driver.get("https://moigektar.ru/")
count = 0
while count < 3:
    try:
        elem = wait(driver,14).until(EC.visibility_of_element_located((By.XPATH, "//h1[text()[contains(.,'Гектар под ваши цели')]]")))
        if elem:
            print(' \:/ МГ: OK')
            break
    except:
        count += 1
        if count == 3:
            print('ERROR (service_check): не дождался загрузки элемента на МГ')
        else:
            driver.refresh()


# 54. проверка сервиса генерации опросов по наличию поля "Логин"
# не дожидается загрузки элемента, если поместить его после проверки ЛК - независимо от того, какой элемент
# выбран в качестве селектора для сервиса опросов
# опять эта странная проблема с actionchains
driver.get("https://polls.moigektar.ru/")
count = 0
while count < 3:
    try:
        elem = wait(driver,14).until(EC.visibility_of_element_located((By.XPATH, "/html/body/div/div/section/div/div/div/h1")))
        if elem:
            print('  |  сервис генерации опросов: OK')
            break
    except:
        count += 1
        if count == 3:
            print('ERROR (service_check): не дождался загрузки элемента на сервисе генерации опросов')
        else:
            driver.refresh()

# 2. проверка ЛК по видимости баннера, который отображается при первом входе в ЛК
driver.get("https://cabinet.moigektar.ru/security/login")
try:
    btn=wait(driver,14).until(EC.presence_of_element_located((By.XPATH, "//a[text()[contains(.,'Войти в демо-версию')]]")))
    actions.move_to_element(btn).click(btn).perform()
    wait(driver,14).until(EC.visibility_of_element_located((By.XPATH, "//*[text()='Остаться в Демо-версии']")))
    print('  |  ЛК: ОК')
except:
    print('ERROR (service_check): не дождался загрузки элемента на ЛК')

# 3. проверка syn_9 по видимости элемента "стрелка"
driver.get("https://syn9.lp.moigektar.ru/")
count = 0
while count < 3:
    try:
        elem = wait(driver,14).until(EC.visibility_of_element_located((By.XPATH, '//a[@href="#w-descr"]')))
        if elem:
            print(' / \ syn_9: OK')
            break
    except:
        count += 1
        if count == 3:
            print('ERROR (service_check): не дождался загрузки элемента на син_9')
        else:
            driver.refresh()

# 4. проверка syn_33 по видимости элемента "стрелка"
driver.get("https://syn33.lp.moigektar.ru/")
count = 0
while count < 3:
    try:
        elem = wait(driver,14).until(EC.visibility_of_element_located((By.XPATH, '//a[@href="#w-descr"]')))
        if elem:
            print(' \ / syn_33: OK')
            break
    except:
        count += 1
        if count == 3:
            print('ERROR (service_check): не дождался загрузки элемента на син_33')
        else:
            driver.refresh()

# 5. проверка syn_34 по видимости элемента "стрелка"
driver.get("https://syn34.lp.moigektar.ru/")
count = 0
while count < 3:
    try:
        elem = wait(driver,14).until(EC.visibility_of_element_located((By.XPATH, '//a[@href="#w-descr"]')))
        if elem:
            print('  |  syn_34: OK')
            break
    except:
        count += 1
        if count == 3:
            print('ERROR (service_check): не дождался загрузки элемента на син_34')
        else:
            driver.refresh()

# 6. проверка syn_37 по видимости элемента "стрелка"
driver.get("https://syn37.lp.moigektar.ru/")
count = 0
while count < 3:
    try:
        elem = wait(driver,14).until(EC.visibility_of_element_located((By.XPATH, '//a[@href="#w-descr"]')))
        if elem:
            print('  |  syn_37: OK')
            break
    except:
        count += 1
        if count == 3:
            print('ERROR (service_check): не дождался загрузки элемента на син_37')
        else:
            driver.refresh()

# 7. проверка syn_53 по видимости элемента "стрелка"
driver.get("https://syn53.lp.moigektar.ru/")
count = 0
while count < 3:
    try:
        elem = wait(driver,14).until(EC.visibility_of_element_located((By.XPATH, '//a[@href="#w-descr"]')))
        if elem:
            print(' / \ syn_53: OK')
            break
    except:
        count += 1
        if count == 3:
            print('ERROR (service_check): не дождался загрузки элемента на син_53')
        else:
            driver.refresh()

# 8. проверка syn_67 по видимости элемента "стрелка"
driver.get("https://syn67.lp.moigektar.ru/")
count = 0
while count < 3:
    try:
        elem = wait(driver,14).until(EC.visibility_of_element_located((By.XPATH, '//a[@href="#w-descr"]')))
        if elem:
            print(' \ / syn_67: OK')
            break
    except:
        count += 1
        if count == 3:
            print('ERROR (service_check): не дождался загрузки элемента на син_67')
        else:
            driver.refresh()

# 9. проверка vazuza2 по видимости фразы "10 поселков на одной территории"
driver.get("https://vazuza2.lp.moigektar.ru/")
count = 0
while count < 3:
    try:
        elem = wait(driver,14).until(EC.visibility_of_element_located((By.XPATH, '//p[text()[contains(., "10 поселков на одной территории")]]')))
        if elem:
            print('  |  vazuza2: OK')
            break
    except:
        count += 1
        if count == 3:
            print('ERROR (service_check): не дождался загрузки элемента на Вазузе')
        else:
            driver.refresh()

# 10. проверка pay.moigektar по видимости заголовка "Платёжные сервисы"
driver.get("https://pay.moigektar.ru/")
count = 0
while count < 3:
    try:
        elem = wait(driver,14).until(EC.visibility_of_element_located((By.XPATH, "//h3[text()[contains(.,'Платежные сервисы')]]")))
        if elem:
            print('  |  pay.moigektar: OK')
            break
    except:
        count += 1
        if count == 3:
            print('ERROR (service_check): не дождался загрузки элемента на Платёжных сервисах')
        else:
            driver.refresh()

# 11. проверка сервиса "Вынос границ" по наличию заголовка "Вынос границ участка"
driver.get("https://points.lp.moigektar.ru/")
count = 0
while count < 3:
    try:
        elem = wait(driver,14).until(EC.visibility_of_element_located((By.XPATH, "//p[text()[contains(.,'ВЫНОС ГРАНИЦ')]]")))
        if elem:
            print(' / \ Вынос границ: OK')
            break
    except:
        count += 1
        if count == 3:
            print('ERROR (service_check): не дождался загрузки элемента на Выносе границ')
        else:
            driver.refresh()

# 12. проверка сервиса "Инвестиции" по наличию заголовка "Инвестиции"
driver.get("https://investment.lp.moigektar.ru/")
count = 0
while count < 3:
    try:
        elem = wait(driver,14).until(EC.visibility_of_element_located((By.XPATH, "//h1[text()[contains(.,'Инвестиции')]]")))
        if elem:
            print(' \ / Инвестиции: OK')
            break
    except:
        count += 1
        if count == 3:
            print('ERROR (service_check): не дождался загрузки элемента на Инвестициях')
        else:
            driver.refresh()

# 13. проверка сервиса "Комплекс услуг" по наличию заголовка "Комплекс услуг"
driver.get("https://complex.lp.moigektar.ru/")
count = 0
while count < 3:
    try:
        elem = wait(driver,14).until(EC.visibility_of_element_located((By.XPATH, "//h1[text()[contains(.,'комплекс услуг')]]")))
        if elem:
            print('  |  Комплекс услуг: OK')
            break
    except:
        count += 1
        if count == 3:
            print('ERROR (service_check): не дождался загрузки элемента на Комплексе услуг')
        else:
            driver.refresh()

# 14. проверка сервиса "Кооперативы" по наличию заголовка "Вступайте в кооператив"
driver.get("https://cooperative.lp.moigektar.ru/")
count = 0
while count < 3:
    try:
        elem = wait(driver,14).until(EC.visibility_of_element_located((By.XPATH, "//h1[text()[contains(.,'Вступайте')]]")))
        if elem:
            print('  |  Кооперативы: OK')
            break
    except:
        count += 1
        if count == 3:
            print('ERROR (service_check): не дождался загрузки элемента на Кооперативах')
        else:
            driver.refresh()

# 15. проверка сервиса "Правовая поддержка" по наличию заголовка "Центр правовой поддержки"
driver.get("https://law.lp.moigektar.ru/")
count = 0
while count < 3:
    try:
        elem = wait(driver,14).until(EC.visibility_of_element_located((By.XPATH, "//h1[text()[contains(.,'центр правовой поддержки')]]")))
        if elem:
            print(' / \ Правовая поддержка: OK')
            break
    except:
        count += 1
        if count == 3:
            print('ERROR (service_check): не дождался загрузки элемента на Правовой поддержке')
        else:
            driver.refresh()

# 16. проверка сервиса "Разработка проекта" по наличию заголовка "Этапы работы по онлайн-показам"
driver.get("https://planning.moigektar.ru/")
count = 0
while count < 3:
    try:
        elem = wait(driver,14).until(EC.visibility_of_element_located((By.XPATH, "//p[text()[contains(.,'ЭТАПЫ РАБОТЫ')]]")))
        if elem:
            print(' \ / Разработка проекта: OK')
            break
    except:
        count += 1
        if count == 3:
            print('ERROR (service_check): не дождался загрузки элемента на Разработке проекта')
        else:
            driver.refresh()

# 17. проверка сервиса "Расчистка участка" по наличию заголовка "Расчистка участка"
driver.get("https://clearance.lp.moigektar.ru/")
count = 0
while count < 3:
    try:
        elem = wait(driver,14).until(EC.visibility_of_element_located((By.XPATH, "//p[text()[contains(.,'РАСЧИСТКА УЧАСТКА')]]")))
        if elem:
            print('  |  Расчистка участка: OK')
            break
    except:
        count += 1
        if count == 3:
            print('ERROR (service_check): не дождался загрузки элемента на Расчистке участка')
        else:
            driver.refresh()

# 18. проверка сервиса "Строительство въездной группы" по наличию заголовка "Коллективное строительство"
driver.get("http://syn9.entrance.lp.moigektar.ru/")
count = 0
while count < 3:
    try:
        elem = wait(driver,14).until(EC.visibility_of_element_located((By.XPATH, "//h1[text()[contains(.,'Коллективное')]]")))
        if elem:
            print('  |  Строительство въездной группы: OK')
            break
    except:
        count += 1
        if count == 3:
            print('ERROR (service_check): не дождался загрузки элемента на Въездной группе')
        else:
            driver.refresh()

# 19. проверка сервиса "Строительство дорог" по наличию заголовка "Коллективное строительство"
driver.get("https://syn23.roads.moigektar.ru/")
count = 0
while count < 3:
    try:
        elem = wait(driver,14).until(EC.visibility_of_element_located((By.XPATH, "//p[text()[contains(.,'КОЛЛЕКТИВНОЕ')]]")))
        if elem:
            print(' / \ Строительство дорог: OK')
            break
    except:
        count += 1
        if count == 3:
            print('ERROR (service_check): не дождался загрузки элемента на Строительстве дорог')
        else:
            driver.refresh()

# 20. проверка сервиса "Строительство центрального дома" по наличию заголовка "Коллективное строительство"
driver.get("https://house.lp.moigektar.ru/")
count = 0
while count < 3:
    try:
        elem = wait(driver,14).until(EC.visibility_of_element_located((By.XPATH, "//h1[text()[contains(.,'коллективное строительство')]]")))
        if elem:
            print(' \ / Строительство центрального дома: OK')
            break
    except:
        count += 1
        if count == 3:
            print('ERROR (service_check): не дождался загрузки элемента на Строительстве центрального дома')
        else:
            driver.refresh()

# 21. проверка сервиса "Установка видеонаблюдения" по наличию заголовка "Установка видеонаблюдения"
driver.get("https://barrier.lp.moigektar.ru/")
count = 0
while count < 3:
    try:
        elem = wait(driver,14).until(EC.visibility_of_element_located((By.XPATH, "//h1[text()[contains(.,'установка видеонаблюдения')]]")))
        if elem:
            print('  |  Установка видеонаблюдения: OK')
            break
    except:
        count += 1
        if count == 3:
            print('ERROR (service_check): не дождался загрузки элемента на Установке видеонаблюдения')
        else:
            driver.refresh()

# 22. проверка сервиса "Электрификация" по наличию заголовка "Коллективное строительство"
driver.get("https://syn9.electrification.lp.moigektar.ru/")
count = 0
while count < 3:
    try:
        elem = wait(driver,14).until(EC.visibility_of_element_located((By.XPATH, "//h1[text()[contains(.,'коллективное')]]")))
        if elem:
            print('  |  Электрификация: OK')
            break
    except:
        count += 1
        if count == 3:
            print('ERROR (service_check): не дождался загрузки элемента на Электрификации')
        else:
            driver.refresh()

# 23. проверка сервиса "GIS" по наличию заголовка "Login"
driver.get("https://gis.bigland.ru/site/login")
count = 0
while count < 3:
    try:
        elem = wait(driver,14).until(EC.visibility_of_element_located((By.XPATH, "//h1[text()[contains(.,'Login')]]")))
        if elem:
            print(' / \ GIS: OK')
            break
    except:
        count += 1
        if count == 3:
            print('ERROR (service_check): не дождался загрузки элемента на ГИС')
        else:
            driver.refresh()

# 24. проверка сервиса генерации КП по наличию заголовка "Сервис генерации КП"
driver.get("https://offers.bigland.ru/")
count = 0
while count < 3:
    try:
        elem = wait(driver,14).until(EC.visibility_of_element_located((By.XPATH, "//h1[text()[contains(.,'Сервис генерации КП')]]")))
        if elem:
            print(' \ / Сервис генерации КП: OK')
            break
    except:
        count += 1
        if count == 3:
            print('ERROR (service_check): не дождался загрузки элемента на Генерации КП')
        else:
            driver.refresh()

# 25. проверка syn_99 по наличию заголовка "Генеральный"
driver.get("https://syn99.lp.moigektar.ru/")
count = 0
while count < 3:
    try:
        elem = wait(driver,14).until(EC.visibility_of_element_located((By.XPATH, '//a[@href="#w-descr"]')))
        if elem:
            print('  |  syn_99: OK')
            break
    except:
        count += 1
        if count == 3:
            print('ERROR (service_check): не дождался загрузки элемента на син_99')
        else:
            driver.refresh()

# 26. проверка syn_11 по видимости заголовка "Интерактивный выбор"
driver.get("https://syn11.lp.moigektar.ru/")
count = 0
while count < 3:
    try:
        elem = wait(driver,14).until(EC.visibility_of_element_located((By.XPATH, "//span[text()[contains(.,'Интерактивный')]]")))
        if elem:
            print('  |  syn_11: OK')
            break
    except:
        count += 1
        if count == 3:
            print('ERROR (service_check): не дождался загрузки элемента на син_11')
        else:
            driver.refresh()

# 27. проверка syn_12 по видимости заголовка "Интерактивный выбор"
driver.get("https://syn12.lp.moigektar.ru/")
count = 0
while count < 3:
    try:
        elem = wait(driver,14).until(EC.visibility_of_element_located((By.XPATH, "//span[text()[contains(.,'Интерактивный')]]")))
        if elem:
            print(' / \ syn_12: OK')
            break
    except:
        count += 1
        if count == 3:
            print('ERROR (service_check): не дождался загрузки элемента на син_12')
        else:
            driver.refresh()

# 28. проверка syn_6 по видимости заголовка "Выбрать участок"
driver.get("https://syn6.lp.moigektar.ru/")
count = 0
while count < 3:
    try:
        elem = wait(driver,14).until(EC.visibility_of_element_located((By.XPATH, "//h2[text()[contains(.,'Выбрать участок')]]")))
        if elem:
            print(' \ / syn_6: OK')
            break
    except:
        count += 1
        if count == 3:
            print('ERROR (service_check): не дождался загрузки элемента на син_6')
        else:
            driver.refresh()

# 29. проверка syn_14 по видимости заголовка "Интерактивный"
driver.get("https://syn14.lp.moigektar.ru/")
count = 0
while count < 3:
    try:
        elem = wait(driver,14).until(EC.visibility_of_element_located((By.XPATH, "//span[text()[contains(.,'Интерактивный')]]")))
        if elem:
            print('  |  syn_14: OK')
            break
    except:
        count += 1
        if count == 3:
            print('ERROR (service_check): не дождался загрузки элемента на син_14')
        else:
            driver.refresh()

# 30. проверка syn_15 по видимости заголовка "Виртуальные туры"
driver.get("https://syn15.lp.moigektar.ru/")
count = 0
while count < 3:
    try:
        elem = wait(driver,14).until(EC.visibility_of_element_located((By.XPATH, "//span[text()[contains(.,'Виртуальные туры')]]")))
        if elem:
            print('  |  syn_15: OK')
            break
    except:
        count += 1
        if count == 3:
            print('ERROR (service_check): не дождался загрузки элемента на син_15')
        else:
            driver.refresh()

# 31. проверка syn_16 по видимости заголовка "Интерактивный выбор"
driver.get("https://syn16.lp.moigektar.ru/")
count = 0
while count < 3:
    try:
        elem = wait(driver,14).until(EC.visibility_of_element_located((By.XPATH, "//span[text()[contains(.,'Интерактивный')]]")))
        if elem:
            print(' / \ syn_16: OK')
            break
    except:
        count += 1
        if count == 3:
            print('ERROR (service_check): не дождался загрузки элемента на син_16')
        else:
            driver.refresh()

# 32. проверка syn_17 по видимости заголовка "Виртуальные туры"
driver.get("https://syn17.lp.moigektar.ru/")
count = 0
while count < 3:
    try:
        elem = wait(driver,14).until(EC.visibility_of_element_located((By.XPATH, "//span[text()[contains(.,'Виртуальные')]]")))
        if elem:
            print(' \ / syn_17: OK')
            break
    except:
        count += 1
        if count == 3:
            print('ERROR (service_check): не дождался загрузки элемента на син_17')
        else:
            driver.refresh()

# 33. проверка syn_18 по видимости заголовка "Интерактивный"
driver.get("https://syn18.lp.moigektar.ru/")
count = 0
while count < 3:
    try:
        elem = wait(driver,14).until(EC.visibility_of_element_located((By.XPATH, "//span[text()[contains(.,'Интерактивный')]]")))
        if elem:
            print('  |  syn_18: OK')
            break
    except:
        count += 1
        if count == 3:
            print('ERROR (service_check): не дождался загрузки элемента на син_18')
        else:
            driver.refresh()

# 34. проверка syn_19 по видимости элемента "стрелка"
driver.get("https://syn19.lp.moigektar.ru/")
count = 0
while count < 3:
    try:
        elem = wait(driver,14).until(EC.visibility_of_element_located((By.XPATH, '//a[@href="#w-descr"]')))
        if elem:
            print('  |  syn_19: OK')
            break
    except:
        count += 1
        if count == 3:
            print('ERROR (service_check): не дождался загрузки элемента на син_19')
        else:
            driver.refresh()

# 35. проверка syn_21 по видимости заголовка "Генеральный"
driver.get("https://syn21.lp.moigektar.ru/")
count = 0
while count < 3:
    try:
        elem = wait(driver,14).until(EC.visibility_of_element_located((By.XPATH, '//span[text()[contains(.,"Генеральный")]]')))
        if elem:
            print(' / \ syn_21: OK')
            break
    except:
        count += 1
        if count == 3:
            print('ERROR (service_check): не дождался загрузки элемента на син_21')
        else:
            driver.refresh()

# 36. проверка syn_22 по видимости заголовка "Генеральный"
driver.get("https://syn22.lp.moigektar.ru/")
count = 0
while count < 3:
    try:
        elem = wait(driver,14).until(EC.visibility_of_element_located((By.XPATH, '//span[text()[contains(.,"Генеральный")]]')))
        if elem:
            print(' \ / syn_22: OK')
            break
    except:
        count += 1
        if count == 3:
            print('ERROR (service_check): не дождался загрузки элемента на син_22')
        else:
            driver.refresh()

# 37. проверка syn_23 по видимости заголовка "Генеральный"
driver.get("https://syn23.lp.moigektar.ru/")
count = 0
while count < 3:
    try:
        elem = wait(driver,14).until(EC.visibility_of_element_located((By.XPATH, '//span[text()[contains(.,"Генеральный")]]')))
        if elem:
            print('  |  syn_23: OK')
            break
    except:
        count += 1
        if count == 3:
            print('ERROR (service_check): не дождался загрузки элемента на син_23')
        else:
            driver.refresh()

# 38. проверка syn_24 по видимости заголовка "Генеральный"
driver.get("https://syn24.lp.moigektar.ru/")
count = 0
while count < 3:
    try:
        elem = wait(driver,14).until(EC.visibility_of_element_located((By.XPATH, '//span[text()[contains(.,"Генеральный")]]')))
        if elem:
            print('  |  syn_24: OK')
            break
    except:
        count += 1
        if count == 3:
            print('ERROR (service_check): не дождался загрузки элемента на син_24')
        else:
            driver.refresh()

# 39. проверка syn_27 по видимости заголовка "Забронировать"
driver.get("https://syn27.lp.moigektar.ru/")
try:
    wait(driver,14).until(EC.visibility_of_element_located((By.XPATH, "//h3[text()[contains(.,'Забронировать')]]")))
    print(' / \ syn_27: OK')
except:
    print('ERROR (service_check): не дождался загрузки элемента на син_27')

# 40. проверка "Полевых работ" по наличию текста "Запомнить"
driver.get("https://fields.bigland.ru/site/login")
count = 0
while count < 3:
    try:
        elem = wait(driver,14).until(EC.visibility_of_element_located((By.XPATH, "//*[text()[contains(.,'Запомнить')]]")))
        if elem:
            print(' \ / Полевые работы: OK')
            break
    except:
        count += 1
        if count == 3:
            print('ERROR (service_check): не дождался загрузки элемента на Полевых работах')
        else:
            driver.refresh()

# 41. проверка syn_35 по видимости заголовка "Генеральный"
driver.get("https://syn35.lp.moigektar.ru/")
count = 0
while count < 3:
    try:
        elem = wait(driver,14).until(EC.visibility_of_element_located((By.XPATH, '//span[text()[contains(.,"Генеральный")]]')))
        if elem:
            print('  |  syn_35: OK')
            break
    except:
        count += 1
        if count == 3:
            print('ERROR (service_check): не дождался загрузки элемента на син_35')
        else:
            driver.refresh()

# 42. проверка syn_36 по видимости заголовка "Генеральный"
driver.get("https://syn36.lp.moigektar.ru/")
count = 0
while count < 3:
    try:
        elem = wait(driver,14).until(EC.visibility_of_element_located((By.XPATH, '//span[text()[contains(.,"Генеральный")]]')))
        if elem:
            print('  |  syn_36: OK')
            break
    except:
        count += 1
        if count == 3:
            print('ERROR (service_check): не дождался загрузки элемента на син_36')
        else:
            driver.refresh()

# 44. проверка syn_39 по видимости элемента "стрелка"
driver.get("https://syn39.lp.moigektar.ru/")
count = 0
while count < 3:
    try:
        elem = wait(driver,14).until(EC.visibility_of_element_located((By.XPATH, '//a[@href="#w-descr"]')))
        if elem:
            print(' / \ syn_39: OK')
            break
    except:
        count += 1
        if count == 3:
            print('ERROR (service_check): не дождался загрузки элемента на син_39')
        else:
            driver.refresh()

# 45. проверка syn_42 по видимости элемента "стрелка"
driver.get("https://syn42.lp.moigektar.ru/")
count = 0
while count < 3:
    try:
        elem = wait(driver,14).until(EC.visibility_of_element_located((By.XPATH, '//a[@href="#w-descr"]')))
        if elem:
            print(' \ / syn_42: OK')
            break
    except:
        count += 1
        if count == 3:
            print('ERROR (service_check): не дождался загрузки элемента на син_42')
        else:
            driver.refresh()

# 46. проверка syn_48 по видимости элемента "стрелка"
driver.get("https://syn48.lp.moigektar.ru/")
count = 0
while count < 3:
    try:
        elem = wait(driver,14).until(EC.visibility_of_element_located((By.XPATH, '//a[@href="#w-descr"]')))
        if elem:
            print('  |  syn_48: OK')
            break
    except:
        count += 1
        if count == 3:
            print('ERROR (service_check): не дождался загрузки элемента на син_48')
        else:
            driver.refresh()

# 47. проверка syn_58 по видимости заголовка "Забронировать"
driver.get("https://syn58.lp.moigektar.ru/")
count = 0
while count < 3:
    try:
        elem = wait(driver,14).until(EC.visibility_of_element_located((By.XPATH, "//h3[text()[contains(.,'Забронировать')]]")))
        if elem:
            print('  |  syn_58: OK')
            break
    except:
        count += 1
        if count == 3:
            print('ERROR (service_check): не дождался загрузки элемента на син_58')
        else:
            driver.refresh()

# 48. проверка syn_61 по видимости заголовка "Генеральный"
driver.get("https://syn61.lp.moigektar.ru/")
count = 0
while count < 3:
    try:
        elem = wait(driver,14).until(EC.visibility_of_element_located((By.XPATH, '//span[text()[contains(.,"Генеральный")]]')))
        if elem:
            print(' / \ syn_61: OK')
            break
    except:
        count += 1
        if count == 3:
            print('ERROR (service_check): не дождался загрузки элемента на син_61')
        else:
            driver.refresh()

# 49. проверка сервиса редактирования дорог по наличию заголовка "Login"
driver.get("https://editor.roads.bigland.ru/site/login")
count = 0
while count < 3:
    try:
        elem = wait(driver,14).until(EC.visibility_of_element_located((By.XPATH, "//h1[text()[contains(.,'Login')]]")))
        if elem:
            print(' \ / Сервис дорог: OK')
            break
    except:
        count += 1
        if count == 3:
            print('ERROR (service_check): не дождался загрузки элемента на Сервисе дорог')
        else:
            driver.refresh()

# 50. проверка syn_85 по наличию заголовка "Генеральный"
driver.get("https://syn85.lp.moigektar.ru/")
count = 0
while count < 3:
    try:
        elem = wait(driver,14).until(EC.visibility_of_element_located((By.XPATH, '//a[@href="#w-descr"]')))
        if elem:
            print('  |  syn_85: OK')
            break
    except:
        count += 1
        if count == 3:
            print('ERROR (service_check): не дождался загрузки элемента на син_85')
        else:
            driver.refresh()

# 51. проверка syn_84 по наличию заголовка "Генеральный"
driver.get("https://syn84.lp.moigektar.ru/")
count = 0
while count < 3:
    try:
        elem = wait(driver,14).until(EC.visibility_of_element_located((By.XPATH, '//a[@href="#w-descr"]')))
        if elem:
            print('  |  syn_84: OK')
            break
    except:
        count += 1
        if count == 3:
            print('ERROR (service_check): не дождался загрузки элемента на син_84')
        else:
            driver.refresh()

# 52. проверка syn_8 по наличию заголовка "Генеральный"
driver.get("https://syn8.lp.moigektar.ru/")
count = 0
while count < 3:
    try:
        elem = wait(driver,14).until(EC.visibility_of_element_located((By.XPATH, '//span[text()[contains(.,"Генеральный")]]')))
        if elem:
            print(' / \ syn_8: OK')
            break
    except:
        count += 1
        if count == 3:
            print('ERROR (service_check): не дождался загрузки элемента на син_8')
        else:
            driver.refresh()

# 53. проверка syn_89 по наличию заголовка "Генеральный"
driver.get("https://syn89.lp.moigektar.ru/")
count = 0
while count < 3:
    try:
        elem = wait(driver,14).until(EC.visibility_of_element_located((By.XPATH, '//a[@href="#w-descr"]')))
        if elem:
            print(' \ / syn_89: OK')
            break
    except:
        count += 1
        if count == 3:
            print('ERROR (service_check): не дождался загрузки элемента на син_89')
        else:
            driver.refresh()

# 55. проверка сервиса по работе с портал ТП по наличию поля "Логин"
driver.get("https://electrification.bigland.ru/site/login")
count = 0
while count < 3:
    try:
        elem = wait(driver,14).until(EC.visibility_of_element_located((By.XPATH, "//*[@id='loginparams-username']")))
        if elem:
            print('  |  сервис по работе с портал ТП: OK')
            break
    except:
        count += 1
        if count == 3:
            print('ERROR (service_check): не дождался загрузки элемента на сервисе по работе с портал ТП')
        else:
            driver.refresh()


# 56. проверка сервиса статей по наличию поля "Логин"
driver.get("https://a.bigland.ru/")
count = 0
while count < 3:
    try:
        elem = wait(driver,14).until(EC.visibility_of_element_located((By.XPATH, "//*[@id='loginform-username']")))
        if elem:
            print('  |  сервис статей: OK')
            break
    except:
        count += 1
        if count == 3:
            print('ERROR (service_check): не дождался загрузки элемента на сервисе статей')
        else:
            driver.refresh()

# 57. проверка syn_87 по наличию заголовка "Генеральный"
driver.get("https://mt.lp.moigektar.ru/")
count = 0
while count < 3:
    try:
        elem = wait(driver,14).until(EC.visibility_of_element_located((By.XPATH, '//a[@href="#w-descr"]')))
        if elem:
            print(' / \ syn_87: OK')
            break
    except:
        count += 1
        if count == 3:
            print('ERROR (service_check): не дождался загрузки элемента на син_92')
        else:
            driver.refresh()

# 58. проверка syn_92 по наличию заголовка "Генеральный"
driver.get("https://syn92.lp.moigektar.ru/")
count = 0
while count < 3:
    try:
        elem = wait(driver,14).until(EC.visibility_of_element_located((By.XPATH, '//a[@href="#w-descr"]')))
        if elem:
            print(' \ / syn_92: OK')
            break
    except:
        count += 1
        if count == 3:
            print('ERROR (service_check): не дождался загрузки элемента на син_92')
        else:
            driver.refresh()

# 59. проверка syn_95 по видимости текста "«Усадьба Императрицы»"
driver.get("https://syn95.lp.moigektar.ru/")
count = 0
while count < 3:
    try:
        elem = wait(driver,14).until(EC.visibility_of_element_located((By.XPATH, '//*[text()[contains(., "«Усадьба Императрицы»")]]')))
        if elem:
            print('  |  syn_95: OK')
            break
    except:
        count += 1
        if count == 3:
            print('ERROR (service_check): не дождался загрузки элемента на син_95')
        else:
            driver.refresh()

# 60. проверка syn_47 по видимости фразы "Клубный поселок"
driver.get("https://syn47.lp.moigektar.ru/")
count = 0
while count < 3:
    try:
        elem = wait(driver,14).until(EC.visibility_of_element_located((By.XPATH, '//*[text()[contains(., "Клубный поселок")]]')))
        if elem:
            print('  |  syn_47: OK')
            break
    except:
        count += 1
        if count == 3:
            print('ERROR (service_check): не дождался загрузки элемента на син_47')
        else:
            driver.refresh()

# 61. проверка syn_111 по видимости элемента "стрелка"
driver.get("https://syn111.lp.moigektar.ru/")
login = driver.find_element(by=By.ID, value='loginconfig-username')
password = driver.find_element(by=By.ID, value='loginconfig-password')
submit = driver.find_element(by=By.CSS_SELECTOR, value='div button')
login.send_keys(str(data["111_cred"]["login"]))
password.send_keys(str(data["111_cred"]["password"]))
submit.click()
time.sleep(2)
count = 0
while count < 3:
    try:
        elem = wait(driver,14).until(EC.visibility_of_element_located((By.XPATH, '//a[@href="#w-descr"]')))
        if elem:
            print(' / \ syn_111: OK')
            break
    except:
        count += 1
        if count == 3:
            print('ERROR (service_check): не дождался загрузки элемента на син_111')
        else:
            driver.refresh()

# 62. проверка сайта СК по видимости заголовка "Наша цель"
driver.get("https://sc.lp.moigektar.ru/")
count = 0
while count < 3:
    try:
        elem = wait(driver,14).until(EC.visibility_of_element_located((By.XPATH, '//*[text()[contains(., "Наша цель")]]')))
        if elem:
            print(' \ / сайт СК: OK')
            break
    except:
        count += 1
        if count == 3:
            print('ERROR (service_check): не дождался загрузки элемента на сайте СК')
        else:
            driver.refresh()

# 63. проверка syn_73 по наличию заголовка "Генеральный"
driver.get("https://syn73.lp.moigektar.ru/")
count = 0
while count < 3:
    try:
        elem = wait(driver,14).until(EC.visibility_of_element_located((By.XPATH, '//a[@href="#w-descr"]')))
        if elem:
            print('  |  syn_73: OK')
            break
    except:
        count += 1
        if count == 3:
            print('ERROR (service_check): не дождался загрузки элемента на син_73')
        else:
            driver.refresh()

# 65. проверка сайта "Барская Усадьба" по видимости ссылки "Меню завтраков"
driver.get("https://xn--80aacl7dl0e.xn--p1ai/")
count = 0
while count < 3:
    try:
        elem = wait(driver,14).until(EC.visibility_of_element_located((By.XPATH, '//span[text()[contains(., "Меню завтраков")]]')))
        if elem:
            print('  |  Барская усадьба: OK')
            break
    except:
        count += 1
        if count == 3:
            print('ERROR (service_check): не дождался загрузки элемента на Барской усадьбе')
        else:
            driver.refresh()

# 66. проверка сайта "Онлайн-показ" по видимости текста "онлайн-показ"
driver.get("https://presentation.lp.moigektar.ru/")
count = 0
while count < 3:
    try:
        elem = wait(driver,14).until(EC.visibility_of_element_located((By.XPATH, '//span[text()[contains(., "онлайн-показ")]]')))
        if elem:
            print(' / \ сайт "Онлайн-показ": OK')
            break
    except:
        count += 1
        if count == 3:
            print('ERROR (service_check): не дождался загрузки элемента на сайте "Онлайн-показ"')
        else:
            driver.refresh()

time.sleep(2)
driver.quit()

