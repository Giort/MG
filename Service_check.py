from selenium import webdriver
from selenium.webdriver.chrome.options import Options
ch_options = Options()
ch_options.add_argument('--headless')
ch_options.page_load_strategy = 'eager'
driver = webdriver.Chrome(options= ch_options)
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
actions = ActionChains(driver)
driver.maximize_window()
#driver.set_window_size(1920, 1080)

# Скрипт последовательно заходит на каждый сервис МГ и проверяет видимость
# одного элемента на странице
#
# В лог выводится сообщение "ОК", если этот элемент найден
# В лог выводится сообщение "ERROR", если истекло время ожидания элемента
#


# 1. проверка "МГ" по видимости заголовка "Ваши возможности" на главной
driver.get("https://moigektar.ru/")
try:
    wait(driver,14).until(EC.visibility_of_element_located((By.XPATH, "//h1[text()[contains(.,'Ваши возможности на гектаре')]]")))
    print('  |  МГ: OK')
except:
    print('ERROR (service_check): не дождался загрузки элемента на МГ')


# 54. проверка сервиса генерации опросов по наличию поля "Логин"
# не дожидается загрузки элемента, если поместить его после проверки ЛК - независимо от того, какой элемент
# выбран в качестве селектора для сервиса опросов
# опять эта странная проблема с actionchains
driver.get("https://polls.moigektar.ru/")
try:
    wait(driver,14).until(EC.visibility_of_element_located((By.XPATH, "/html/body/div/div/section/div/div/div/h1")))
    print('  |  сервис генерации опросов: OK')
except:
    print('ERROR (service_check): не дождался загрузки элемента на сервисе генерации опросов')

# 2. проверка ЛК по видимости баннера, который отображается при первом входе в ЛК
driver.get("https://cabinet.moigektar.ru/security/login")
try:
    btn=wait(driver,14).until(EC.presence_of_element_located((By.XPATH, "//a[text()[contains(.,'Попробовать прямо сейчас!')]]")))
    actions.move_to_element(btn).click(btn).perform()
    wait(driver,14).until(EC.visibility_of_element_located((By.XPATH, "//*[text()='Остаться в Демо-версии']")))
    print('  |  ЛК: ОК')
except:
    print('ERROR (service_check): не дождался загрузки элемента на ЛК')

# 3. проверка syn_9 по видимости заголовка "Генеральный"
driver.get("https://syn9.lp.moigektar.ru/")
try:
    wait(driver,14).until(EC.visibility_of_element_located((By.XPATH, "//div[text()[contains(.,'Генеральный')]]")))
    print(' / \ syn_9: OK')
except:
    print('ERROR (service_check): не дождался загрузки элемента на син_9')

# 4. проверка syn_33 по видимости заголовка "Генеральный"
driver.get("https://syn33.lp.moigektar.ru/")
try:
    wait(driver,14).until(EC.visibility_of_element_located((By.XPATH, "//span[text()[contains(.,'Генеральный')]]")))
    print(' \ / syn_33: OK')
except:
    print('ERROR (service_check): не дождался загрузки элемента на син_33')

# 5. проверка syn_34 по видимости заголовка "Генеральный"
driver.get("https://syn34.lp.moigektar.ru/")
try:
    wait(driver,14).until(EC.visibility_of_element_located((By.XPATH, "//span[text()[contains(.,'Генеральный')]]")))
    print('  |  syn_34: OK')
except:
    print('ERROR (service_check): не дождался загрузки элемента на син_34')

# 6. проверка syn_37 по видимости заголовка "Генеральный"
driver.get("https://syn37.lp.moigektar.ru/")
try:
    wait(driver,14).until(EC.visibility_of_element_located((By.XPATH, "//span[text()[contains(.,'Генеральный')]]")))
    print('  |  syn_37: OK')
except:
    print('ERROR (service_check): не дождался загрузки элемента на син_37')

# 7. проверка syn_53 по видимости заголовка "Генеральный"
driver.get("https://syn53.lp.moigektar.ru/")
try:
    wait(driver,14).until(EC.visibility_of_element_located((By.XPATH, "//div[text()[contains(.,'Генеральный')]]")))
    print(' / \ syn_53: OK')
except:
    print('ERROR (service_check): не дождался загрузки элемента на син_53')

# 8. проверка syn_67 по видимости заголовка "Генеральный"
driver.get("https://syn67.lp.moigektar.ru/")
try:
    wait(driver,14).until(EC.visibility_of_element_located((By.XPATH, "//div[text()[contains(.,'Генеральный')]]")))
    print(' \ / syn_67: OK')
except:
    print('ERROR (service_check): не дождался загрузки элемента на син_67')

# 9. проверка vazuza2 по видимости заголовка "Генеральный"
driver.get("https://vazuza2.lp.moigektar.ru/")
try:
    wait(driver,14).until(EC.visibility_of_element_located((By.XPATH, "//div[text()[contains(.,'Генеральный')]]")))
    print('  |  vazuza2: OK')
except:
    print('ERROR (service_check): не дождался загрузки элемента на Вазузе')

# 10. проверка pay.moigektar по видимости заголовка "Платёжные сервисы"
driver.get("https://pay.moigektar.ru/")
try:
    wait(driver,14).until(EC.visibility_of_element_located((By.XPATH, "//h3[text()[contains(.,'Платежные сервисы')]]")))
    print('  |  pay.moigektar: OK')
except:
    print('ERROR (service_check): не дождался загрузки элемента на Платёжных сервисах')

# 11. проверка сервиса "Вынос границ" по наличию заголовка "Вынос границ участка"
driver.get("https://points.lp.moigektar.ru/")
try:
    wait(driver,14).until(EC.visibility_of_element_located((By.XPATH, "//p[text()[contains(.,'ВЫНОС ГРАНИЦ')]]")))
    print(' / \ Вынос границ: OK')
except:
    print('ERROR (service_check): не дождался загрузки элемента на Выносе границ')

# 12. проверка сервиса "Инвестиции" по наличию заголовка "Инвестиции"
driver.get("https://investment.lp.moigektar.ru/")
try:
    wait(driver,14).until(EC.visibility_of_element_located((By.XPATH, "//h1[text()[contains(.,'Инвестиции')]]")))
    print(' \ / Инвестиции: OK')
except:
    print('ERROR (service_check): не дождался загрузки элемента на Инвестициях')

# 13. проверка сервиса "Комплекс услуг" по наличию заголовка "Комплекс услуг"
driver.get("https://complex.lp.moigektar.ru/")
try:
    wait(driver,14).until(EC.visibility_of_element_located((By.XPATH, "//h1[text()[contains(.,'комплекс услуг')]]")))
    print('  |  Комплекс услуг: OK')
except:
    print('ERROR (service_check): не дождался загрузки элемента на Комплексе услуг')

# 14. проверка сервиса "Кооперативы" по наличию заголовка "Вступайте в кооператив"
driver.get("https://cooperative.lp.moigektar.ru/")
try:
    wait(driver,14).until(EC.visibility_of_element_located((By.XPATH, "//h1[text()[contains(.,'Вступайте')]]")))
    print('  |  Кооперативы: OK')
except:
    print('ERROR (service_check): не дождался загрузки элемента на Кооперативах')

# 15. проверка сервиса "Правовая поддержка" по наличию заголовка "Центр правовой поддержки"
driver.get("https://law.lp.moigektar.ru/")
try:
    wait(driver,14).until(EC.visibility_of_element_located((By.XPATH, "//h1[text()[contains(.,'центр правовой поддержки')]]")))
    print(' / \ Правовая поддержка: OK')
except:
    print('ERROR (service_check): не дождался загрузки элемента на Правовой поддержке')

# 16. проверка сервиса "Разработка проекта" по наличию заголовка "Этапы работы по онлайн-показам"
driver.get("https://planning.moigektar.ru/")
try:
    wait(driver,14).until(EC.visibility_of_element_located((By.XPATH, "//p[text()[contains(.,'ЭТАПЫ РАБОТЫ')]]")))
    print(' \ / Разработка проекта: OK')
except:
    print('ERROR (service_check): не дождался загрузки элемента на Разработке проекта')

# 17. проверка сервиса "Расчистка участка" по наличию заголовка "Расчистка участка"
driver.get("https://clearance.lp.moigektar.ru/")
try:
    wait(driver,14).until(EC.visibility_of_element_located((By.XPATH, "//p[text()[contains(.,'РАСЧИСТКА УЧАСТКА')]]")))
    print('  |  Расчистка участка: OK')
except:
    print('ERROR (service_check): не дождался загрузки элемента на Расчистке участка')

# 18. проверка сервиса "Строительство въездной группы" по наличию заголовка "Коллективное строительство"
driver.get("http://syn9.entrance.lp.moigektar.ru/")
try:
    wait(driver,14).until(EC.visibility_of_element_located((By.XPATH, "//h1[text()[contains(.,'Коллективное')]]")))
    print('  |  Строительство въездной группы: OK')
except:
    print('ERROR (service_check): не дождался загрузки элемента на Въездной группе')

# 19. проверка сервиса "Строительство дорог" по наличию заголовка "Коллективное строительство"
driver.get("https://syn23.roads.moigektar.ru/")
try:
    wait(driver,14).until(EC.visibility_of_element_located((By.XPATH, "//p[text()[contains(.,'КОЛЛЕКТИВНОЕ')]]")))
    print(' / \ Строительство дорог: OK')
except:
    print('ERROR (service_check): не дождался загрузки элемента на Строительстве дорог')

# 20. проверка сервиса "Строительство центрального дома" по наличию заголовка "Коллективное строительство"
driver.get("https://house.lp.moigektar.ru/")
try:
    wait(driver,14).until(EC.visibility_of_element_located((By.XPATH, "//h1[text()[contains(.,'коллективное строительство')]]")))
    print(' \ / Строительство центрального дома: OK')
except:
    print('ERROR (service_check): не дождался загрузки элемента на Строительстве центрального дома')

# 21. проверка сервиса "Установка видеонаблюдения" по наличию заголовка "Установка видеонаблюдения"
driver.get("https://barrier.lp.moigektar.ru/")
try:
    wait(driver,14).until(EC.visibility_of_element_located((By.XPATH, "//h1[text()[contains(.,'установка видеонаблюдения')]]")))
    print('  |  Установка видеонаблюдения: OK')
except:
    print('ERROR (service_check): не дождался загрузки элемента на Установке видеонаблюдения')

# 22. проверка сервиса "Электрификация" по наличию заголовка "Коллективное строительство"
driver.get("https://syn9.electrification.lp.moigektar.ru/")
try:
    wait(driver,14).until(EC.visibility_of_element_located((By.XPATH, "//h1[text()[contains(.,'коллективное')]]")))
    print('  |  Электрификация: OK')
except:
    print('ERROR (service_check): не дождался загрузки элемента на Электрификации')

# 23. проверка сервиса "GIS" по наличию заголовка "Login"
driver.get("https://gis.bigland.ru/site/login")
try:
    wait(driver,14).until(EC.visibility_of_element_located((By.XPATH, "//h1[text()[contains(.,'Login')]]")))
    print(' / \ GIS: OK')
except:
    print('ERROR (service_check): не дождался загрузки элемента на ГИС')

# 24. проверка сервиса генерации КП по наличию заголовка "Сервис генерации КП"
driver.get("https://offers.bigland.ru/")
try:
    wait(driver,14).until(EC.visibility_of_element_located((By.XPATH, "//h1[text()[contains(.,'Сервис генерации КП')]]")))
    print(' \ / Сервис генерации КП: OK')
except:
    print('ERROR (service_check): не дождался загрузки элемента на Генерации КП')

# 25. проверка syn_6 по видимости заголовка "Выбрать участок"
driver.get("https://syn6.lp.moigektar.ru/")
try:
    wait(driver,14).until(EC.visibility_of_element_located((By.XPATH, "//h2[text()[contains(.,'Выбрать участок')]]")))
    print('  |  syn_6: OK')
except:
    print('ERROR (service_check): не дождался загрузки элемента на син_6')

# 26. проверка syn_11 по видимости заголовка "Интерактивный выбор"
driver.get("https://syn11.lp.moigektar.ru/")
try:
    wait(driver,14).until(EC.visibility_of_element_located((By.XPATH, "//span[text()[contains(.,'Интерактивный')]]")))
    print('  |  syn_11: OK')
except:
    print('ERROR (service_check): не дождался загрузки элемента на син_11')

# 27. проверка syn_12 по видимости заголовка "Интерактивный выбор"
driver.get("https://syn12.lp.moigektar.ru/")
try:
    wait(driver,14).until(EC.visibility_of_element_located((By.XPATH, "//span[text()[contains(.,'Интерактивный')]]")))
    print(' / \ syn_12: OK')
except:
    print('ERROR (service_check): не дождался загрузки элемента на син_12')

# 28. проверка syn_13 по видимости заголовка "Выберите поселок"
driver.get("https://syn13.lp.moigektar.ru/")
try:
    wait(driver,14).until(EC.visibility_of_element_located((By.XPATH, "//p[text()[contains(.,'Выберите поселок')]]")))
    print(' \ / syn_13: OK')
except:
    print('ERROR (service_check): не дождался загрузки элемента на син_13')

# 29. проверка syn_14 по видимости заголовка "Интерактивный"
driver.get("https://syn14.lp.moigektar.ru/")
try:
    wait(driver,14).until(EC.visibility_of_element_located((By.XPATH, "//span[text()[contains(.,'Интерактивный')]]")))
    print('  |  syn_14: OK')
except:
    print('ERROR (service_check): не дождался загрузки элемента на син_14')

# 30. проверка syn_15 по видимости заголовка "Виртуальные туры"
driver.get("https://syn15.lp.moigektar.ru/")
try:
    wait(driver,14).until(EC.visibility_of_element_located((By.XPATH, "//span[text()[contains(.,'Виртуальные туры')]]")))
    print('  |  syn_15: OK')
except:
    print('ERROR (service_check): не дождался загрузки элемента на син_15')

# 31. проверка syn_16 по видимости заголовка "Интерактивный выбор"
driver.get("https://syn16.lp.moigektar.ru/")
try:
    wait(driver,14).until(EC.visibility_of_element_located((By.XPATH, "//span[text()[contains(.,'Интерактивный')]]")))
    print(' / \ syn_16: OK')
except:
    print('ERROR (service_check): не дождался загрузки элемента на син_16')

# 32. проверка syn_17 по видимости заголовка "Виртуальные туры"
driver.get("https://syn17.lp.moigektar.ru/")
try:
    wait(driver,14).until(EC.visibility_of_element_located((By.XPATH, "//span[text()[contains(.,'Виртуальные')]]")))
    print(' \ / syn_17: OK')
except:
    print('ERROR (service_check): не дождался загрузки элемента на син_17')

# 33. проверка syn_18 по видимости заголовка "Интерактивный"
driver.get("https://syn18.lp.moigektar.ru/")
try:
    wait(driver,14).until(EC.visibility_of_element_located((By.XPATH, "//span[text()[contains(.,'Интерактивный')]]")))
    print('  |  syn_18: OK')
except:
    print('ERROR (service_check): не дождался загрузки элемента на син_18')

# 34. проверка syn_19 по видимости заголовка "Генеральный"
driver.get("https://syn19.lp.moigektar.ru/")
try:
    wait(driver,14).until(EC.visibility_of_element_located((By.XPATH, "//div[text()[contains(.,'Генеральный')]]")))
    print('  |  syn_19: OK')
except:
    print('ERROR (service_check): не дождался загрузки элемента на син_19')

# 35. проверка syn_21 по видимости заголовка "Генеральный"
driver.get("https://syn21.lp.moigektar.ru/")
try:
    wait(driver,14).until(EC.visibility_of_element_located((By.XPATH, "//span[text()[contains(.,'Генеральный')]]")))
    print(' / \ syn_21: OK')
except:
    print('ERROR (service_check): не дождался загрузки элемента на син_21')

# 36. проверка syn_22 по видимости заголовка "Генеральный"
driver.get("https://syn22.lp.moigektar.ru/")
try:
    wait(driver,14).until(EC.visibility_of_element_located((By.XPATH, "//span[text()[contains(.,'Генеральный')]]")))
    print(' \ / syn_22: OK')
except:
    print('ERROR (service_check): не дождался загрузки элемента на син_22')

# 37. проверка syn_23 по видимости заголовка "Генеральный"
driver.get("https://syn23.lp.moigektar.ru/")
try:
    wait(driver,14).until(EC.visibility_of_element_located((By.XPATH, "//span[text()[contains(.,'Генеральный')]]")))
    print('  |  syn_23: OK')
except:
    print('ERROR (service_check): не дождался загрузки элемента на син_23')

# 38. проверка syn_24 по видимости заголовка "Генеральный"
driver.get("https://syn24.lp.moigektar.ru/")
try:
    wait(driver,14).until(EC.visibility_of_element_located((By.XPATH, "//span[text()[contains(.,'Генеральный')]]")))
    print('  |  syn_24: OK')
except:
    print('ERROR (service_check): не дождался загрузки элемента на син_24')

# 39. проверка syn_27 по видимости заголовка "Забронировать"
driver.get("https://syn27.lp.moigektar.ru/")
try:
    wait(driver,14).until(EC.visibility_of_element_located((By.XPATH, "//h3[text()[contains(.,'Забронировать')]]")))
    print(' / \ syn_27: OK')
except:
    print('ERROR (service_check): не дождался загрузки элемента на син_27')

# 40. проверка syn_29 по видимости заголовка "Генеральный"
driver.get("https://syn29.lp.moigektar.ru/")
try:
    wait(driver,14).until(EC.visibility_of_element_located((By.XPATH, "//span[text()[contains(.,'Генеральный')]]")))
    print(' \ / syn_29: OK')
except:
    print('ERROR (service_check): не дождался загрузки элемента на син_29')

# 41. проверка syn_35 по видимости заголовка "Генеральный"
driver.get("https://syn35.lp.moigektar.ru/")
try:
    wait(driver,14).until(EC.visibility_of_element_located((By.XPATH, "//span[text()[contains(.,'Генеральный')]]")))
    print('  |  syn_35: OK')
except:
    print('ERROR (service_check): не дождался загрузки элемента на син_35')

# 42. проверка syn_36 по видимости заголовка "Генеральный"
driver.get("https://syn36.lp.moigektar.ru/")
try:
    wait(driver,14).until(EC.visibility_of_element_located((By.XPATH, "//span[text()[contains(.,'Генеральный')]]")))
    print('  |  syn_36: OK')
except:
    print('ERROR (service_check): не дождался загрузки элемента на син_36')

# 44. проверка syn_39 по видимости заголовка "Генеральный"
driver.get("https://syn39.lp.moigektar.ru/")
try:
    wait(driver,14).until(EC.visibility_of_element_located((By.XPATH, "//div[text()[contains(.,'Генеральный')]]")))
    print(' / \ syn_39: OK')
except:
    print('ERROR (service_check): не дождался загрузки элемента на син_39')

# 45. проверка syn_42 по видимости заголовка "Генеральный"
driver.get("https://syn42.lp.moigektar.ru/")
try:
    wait(driver,14).until(EC.visibility_of_element_located((By.XPATH, "//span[text()[contains(.,'Генеральный')]]")))
    print(' \ / syn_42: OK')
except:
    try:
        driver.refresh()
        wait(driver,14).until(EC.visibility_of_element_located((By.XPATH, "//span[text()[contains(.,'Генеральный')]]")))
        print(' \ / syn_42: OK')
    except:
        print('ERROR (service_check): не дождался загрузки элемента на син_42')

# 46. проверка syn_48 по видимости заголовка "Генеральный"
driver.get("https://syn48.lp.moigektar.ru/")
try:
    wait(driver,14).until(EC.visibility_of_element_located((By.XPATH, "//h2[text()[contains(.,'Генеральный')]]")))
    print('  |  syn_48: OK')
except:
    print('ERROR (service_check): не дождался загрузки элемента на син_48')

# 47. проверка syn_58 по видимости заголовка "Забронировать"
driver.get("https://syn58.lp.moigektar.ru/")
try:
    wait(driver,14).until(EC.visibility_of_element_located((By.XPATH, "//h3[text()[contains(.,'Забронировать')]]")))
    print('  |  syn_58: OK')
except:
    print('ERROR (service_check): не дождался загрузки элемента на син_58')

# 48. проверка syn_61 по видимости заголовка "Генеральный"
driver.get("https://syn61.lp.moigektar.ru/")
try:
    wait(driver,14).until(EC.visibility_of_element_located((By.XPATH, "//span[text()[contains(.,'Генеральный')]]")))
    print(' / \ syn_61: OK')
except:
    print('ERROR (service_check): не дождался загрузки элемента на син_61')

# 49. проверка сервиса редактирования дорог по наличию заголовка "Login"
driver.get("https://editor.roads.bigland.ru/site/login")
try:
    wait(driver,14).until(EC.visibility_of_element_located((By.XPATH, "//h1[text()[contains(.,'Login')]]")))
    print(' \ / Сервис дорог: OK')
except:
    print('ERROR (service_check): не дождался загрузки элемента на Сервисе дорог')

# 50. проверка syn_85 по наличию заголовка "Генеральный"
driver.get("https://syn85.lp.moigektar.ru/")
try:
    wait(driver,14).until(EC.visibility_of_element_located((By.XPATH, "//div[text()[contains(.,'Генеральный')]]")))
    print('  |  syn_85: OK')
except:
    print('ERROR (service_check): не дождался загрузки элемента на син_85')

# 51. проверка syn_84 по наличию заголовка "Генеральный"
driver.get("https://syn84.lp.moigektar.ru/")
try:
    wait(driver,14).until(EC.visibility_of_element_located((By.XPATH, "//div[text()[contains(.,'Генеральный')]]")))
    print('  |  syn_84: OK')
except:
    print('ERROR (service_check): не дождался загрузки элемента на син_84')

# 52. проверка syn_8 по наличию заголовка "Генеральный"
driver.get("https://syn8.lp.moigektar.ru/")
try:
    wait(driver,14).until(EC.visibility_of_element_located((By.XPATH, "//span[text()[contains(.,'Генеральный')]]")))
    print(' / \ syn_8: OK')
except:
    print('ERROR (service_check): не дождался загрузки элемента на син_8')

# 53. проверка syn_89 по наличию заголовка "Генеральный"
driver.get("https://syn89.lp.moigektar.ru/")
try:
    wait(driver,14).until(EC.visibility_of_element_located((By.XPATH, "//div[text()[contains(.,'Генеральный')]]")))
    print(' \ / syn_89: OK')
except:
    print('ERROR (service_check): не дождался загрузки элемента на син_89')

# 55. проверка сервиса по работе с портал ТП по наличию поля "Логин"
driver.get("https://electrification.bigland.ru/site/login")
try:
    wait(driver,14).until(EC.visibility_of_element_located((By.XPATH, "//*[@id='loginparams-username']")))
    print('  |  сервис по работе с портал ТП: OK')
except:
    print('ERROR (service_check): не дождался загрузки элемента на сервисе по работе с портал ТП')

# 56. проверка сервиса статей по наличию поля "Логин"
driver.get("https://a.bigland.ru/")
try:
    wait(driver,14).until(EC.visibility_of_element_located((By.XPATH, "//*[@id='loginform-username']")))
    print('  |   сервис статей: OK')
except:
    print('ERROR (service_check): не дождался загрузки элемента на сервисе статей')

# 57. проверка MT-3 по наличию заголовка "Генеральный"
driver.get("https://mt.lp.moigektar.ru/")
try:
    wait(driver,14).until(EC.visibility_of_element_located((By.XPATH, "//div[text()[contains(.,'Генеральный')]]")))
    print(' / \ syn_87: OK')
except:
    print('ERROR (service_check): не дождался загрузки элемента на син_87')

# 58. проверка "Бесконечных Знаний"" по наличию заголовка "Бесконечные знания"
driver.get("https://wiki.bug.land/login")
try:
    wait(driver,14).until(EC.visibility_of_element_located((By.XPATH, "//span[text()[contains(.,'Бесконечные')]]")))
    print(' \ / Бесконечные Знания: OK')
except:
    print('ERROR (service_check): не дождался загрузки элемента на "Бесконечных Знаниях"')





#time.sleep(2)
driver.quit()

