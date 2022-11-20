from selenium import webdriver
from selenium.webdriver.chrome.options import Options
options = Options()
options.add_argument('--headless')
ch_options = Options()
ch_options.add_argument('--headless')
driver = webdriver.Chrome(options= ch_options)
driver.maximize_window()


from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
actions = ActionChains(driver)
import time

# Скрипт последовательно заходит на каждый сервис МГ и проверяет видимость
# одного элемента на странице



# 1. проверка "МГ" по видимости заголовка "Специальное преложение" на главной
driver.get("https://moigektar.ru/")
try:
    wait(driver,14).until(EC.presence_of_element_located((By.XPATH, "//h1[text()[contains(.,'Гектар под ваши цели')]]")))
    print('  |  МГ: OK')
except NoSuchElementException:
    print('ERROR: проблема на МГ')

# 2. проверка ЛК по видимости баннера, который отображается при первом входе в ЛК
driver.get("https://cabinet.moigektar.ru/security/login")
try:
    btn=wait(driver,14).until(EC.presence_of_element_located((By.XPATH, "//a[text()[contains(.,'Попробовать прямо сейчас!')]]")))
    actions.move_to_element(btn).click(btn).perform()
    wait(driver,14).until(EC.presence_of_element_located((By.XPATH, "//img[@src='/img/polls-banner.jpg']")))
    print('  |  ЛК: ОК')
except NoSuchElementException:
    print('ERROR: проблема на ЛК')

# 3. проверка syn_9 по видимости заголовка "Генеральный"
driver.get("https://syn9.lp.moigektar.ru/")
try:
    wait(driver,14).until(EC.presence_of_element_located((By.XPATH, "//span[text()[contains(.,'Генеральный')]]")))
    print(' / \ syn_9: OK')
except NoSuchElementException:
    print('ERROR: проблема на син_9')

# 4. проверка syn_33 по видимости заголовка "Генеральный"
driver.get("https://syn33.lp.moigektar.ru/")
time.sleep(3)
try:
    block4=driver.find_element(by=By.XPATH, value="//span[text()[contains(.,'Генеральный')]]")
    if block4.is_displayed():
        print(' \ / syn_33: OK')
except NoSuchElementException:
    print('ERROR: проблема на син_33')

# 5. проверка syn_34 по видимости заголовка "Генеральный"
driver.get("https://syn34.lp.moigektar.ru/")
time.sleep(3)
try:
    block5=driver.find_element(by=By.XPATH, value="//span[text()[contains(.,'Генеральный')]]")
    if block5.is_displayed():
        print('  |  syn_34: OK')
except NoSuchElementException:
    print('ERROR: проблема на син_34')

# 6. проверка syn_37 по видимости заголовка "Генеральный"
driver.get("https://syn37.lp.moigektar.ru/")
time.sleep(3)
try:
    block6 = wait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//span[text()[contains(.,'Генеральный')]]")))
    if block6.is_displayed():
        print('  |  syn_37: OK')
except NoSuchElementException:
    print('ERROR: проблема на син_37')

# 7. проверка syn_53 по видимости заголовка "Генеральный"
driver.get("https://syn53.lp.moigektar.ru/")
time.sleep(3)
try:
    block7=driver.find_element(by=By.XPATH, value="//h2[text()[contains(.,'Генеральный')]]")
    if block7.is_displayed():
        print(' / \ syn_53: OK')
except NoSuchElementException:
    print('ERROR: проблема на син_53')

# 8. проверка syn_67 по видимости заголовка "Генеральный"
driver.get("https://syn67.lp.moigektar.ru/")
time.sleep(3)
try:
    block8=driver.find_element(by=By.XPATH, value="//h2[text()[contains(.,'Генеральный')]]")
    if block8.is_displayed():
        print(' \ / syn_67: OK')
except NoSuchElementException:
    print('ERROR: проблема на син_67')

# 9. проверка vazuza2 по видимости заголовка "Генеральный"
driver.get("https://vazuza2.lp.moigektar.ru/")
time.sleep(3)
try:
    block9=driver.find_element(by=By.XPATH, value="//div[text()[contains(.,'Генеральный')]]")
    if block9.is_displayed():
        print('  |  vazuza2: OK')
except NoSuchElementException:
    print('ERROR: проблема на Вазузе')

# 10. проверка pay.moigektar по видимости заголовка "Платёжные сервисы"
driver.get("https://pay.moigektar.ru/")
time.sleep(3)
try:
    block10=driver.find_element(by=By.XPATH, value="//h3[text()[contains(.,'Платежные сервисы')]]")
    if block10.is_displayed():
        print('  |  pay.moigektar: OK')
except NoSuchElementException:
    print('ERROR: проблема на сервисе оплаты')

# 11. проверка сервиса "Вынос границ" по наличию заголовка "Вынос границ участка"
driver.get("https://points.lp.moigektar.ru/")
time.sleep(3)
try:
    block11=driver.find_element(by=By.XPATH, value="//p[text()[contains(.,'ВЫНОС ГРАНИЦ')]]")
    if block11.is_displayed():
        print(' / \ Вынос границ: OK')
except NoSuchElementException:
    print('ERROR: проблема на Выносе границ')

# 12. проверка сервиса "Инвестиции" по наличию заголовка "Инвестиции"
driver.get("https://investment.lp.moigektar.ru/")
time.sleep(3)
try:
    block12=driver.find_element(by=By.XPATH, value="//h1[text()[contains(.,'Инвестиции')]]")
    if block12.is_displayed():
        print(' \ / Инвестиции: OK')
except NoSuchElementException:
    print('ERROR: проблема на Инвестициях')

# 13. проверка сервиса "Комплекс услуг" по наличию заголовка "Комплекс услуг"
driver.get("https://complex.lp.moigektar.ru/")
time.sleep(3)
try:
    block13=driver.find_element(by=By.XPATH, value="//h1[text()[contains(.,'комплекс услуг')]]")
    if block13.is_displayed():
        print('  |  Комплекс услуг: OK')
except NoSuchElementException:
    print('ERROR: проблема на Комплексе услуг')

# 14. проверка сервиса "Кооперативы" по наличию заголовка "Вступайте в кооператив"
driver.get("https://cooperative.lp.moigektar.ru/")
time.sleep(3)
try:
    block14=driver.find_element(by=By.XPATH, value="//h1[text()[contains(.,'Вступайте')]]")
    if block14.is_displayed():
        print('  |  Кооперативы: OK')
except NoSuchElementException:
    print('ERROR: проблема на Кооперативах')

# 15. проверка сервиса "Правовая поддержка" по наличию заголовка "Центр правовой поддержки"
driver.get("https://law.lp.moigektar.ru/")
time.sleep(3)
try:
    block15=driver.find_element(by=By.XPATH, value="//h1[text()[contains(.,'центр правовой поддержки')]]")
    if block15.is_displayed():
        print(' / \ Правовая поддержка: OK')
except NoSuchElementException:
    print('ERROR: проблема на Правовой поддержке')

# 16. проверка сервиса "Разработка проекта" по наличию заголовка "Разработка эскизного проекта"
driver.get("https://planning.moigektar.ru/")
time.sleep(3)
try:
    block16=driver.find_element(by=By.XPATH, value="//p[text()[contains(.,'разработка')]]")
    if block16.is_displayed():
        print(' \ / Разработка проекта: OK')
except NoSuchElementException:
    print('ERROR: проблема на Разработке проекта')

# 17. проверка сервиса "Расчистка участка" по наличию заголовка "Расчистка участка"
driver.get("https://clearance.lp.moigektar.ru/")
time.sleep(3)
try:
    block17=driver.find_element(by=By.XPATH, value="//p[text()[contains(.,'РАСЧИСТКА УЧАСТКА')]]")
    if block17.is_displayed():
        print('  |  Расчистка участка: OK')
except NoSuchElementException:
    print('ERROR: проблема на Расчистке участка')

# 18. проверка сервиса "Строительство въездной группы" по наличию заголовка "Коллективное строительство"
driver.get("https://syn9.entrance.lp.moigektar.ru/")
time.sleep(3)
try:
    block18=driver.find_element(by=By.XPATH, value="//h1[text()[contains(.,'Коллективное')]]")
    if block18.is_displayed():
        print('  |  Строительство въездной группы: OK')
except NoSuchElementException:
    print('ERROR: проблема на Въездной группе')

# 19. проверка сервиса "Строительство дорог" по наличию заголовка "Коллективное строительство"
driver.get("https://syn23.roads.moigektar.ru/")
time.sleep(3)
try:
    block19=driver.find_element(by=By.XPATH, value="//p[text()[contains(.,'КОЛЛЕКТИВНОЕ')]]")
    if block19.is_displayed():
        print(' / \ Строительство дорог: OK')
except NoSuchElementException:
    print('ERROR: проблема на Строительстве дорог')

# 20. проверка сервиса "Строительство центрального дома" по наличию заголовка "Коллективное строительство"
driver.get("https://house.lp.moigektar.ru/")
time.sleep(3)
try:
    block20=driver.find_element(by=By.XPATH, value="//h1[text()[contains(.,'коллективное строительство')]]")
    if block20.is_displayed():
        print(' \ / Строительство центрального дома: OK')
except NoSuchElementException:
    print('ERROR: проблема на Строительстве центрального дома')

# 21. проверка сервиса "Установка видеонаблюдения" по наличию заголовка "Установка видеонаблюдения"
driver.get("https://barrier.lp.moigektar.ru/")
time.sleep(3)
try:
    block21=driver.find_element(by=By.XPATH, value="//h1[text()[contains(.,'установка видеонаблюдения')]]")
    if block21.is_displayed():
        print('  |  Установка видеонаблюдения: OK')
except NoSuchElementException:
    print('ERROR: проблема на Установке видеонаблюдения')

# 22. проверка сервиса "Электрификация" по наличию заголовка "Коллективное строительство"
driver.get("https://syn9.electrification.lp.moigektar.ru/")
time.sleep(3)
try:
    block22=driver.find_element(by=By.XPATH, value="//h1[text()[contains(.,'коллективное')]]")
    if block22.is_displayed():
        print('  |  Электрификация: OK')
except NoSuchElementException:
    print('ERROR: проблема на Электрификации')

# 23. проверка сервиса "GIS" по наличию заголовка "Login"
driver.get("https://gis.bigland.ru/site/login")
time.sleep(1)
try:
    block23=driver.find_element(by=By.XPATH, value="//h1[text()[contains(.,'Login')]]")
    if block23.is_displayed():
        print(' / \ GIS: OK')
except NoSuchElementException:
    print('ERROR: проблема на ГИС')

# 24. проверка сервиса генерации КП по наличию заголовка "Сервис генерации КП"
driver.get("https://offers.bigland.ru/")
time.sleep(1)
try:
    block24=driver.find_element(by=By.XPATH, value="//h1[text()[contains(.,'Сервис генерации КП')]]")
    if block24.is_displayed():
        print(' \ / Сервис генерации КП: OK')
except NoSuchElementException:
    print('ERROR: проблема на Сервисе генерации КП')

# 25. проверка syn_6 по видимости заголовка "Выбрать участок"
driver.get("https://syn6.lp.moigektar.ru/")
time.sleep(3)
try:
    block25=driver.find_element(by=By.XPATH, value="//h2[text()[contains(.,'Выбрать участок')]]")
    if block25.is_displayed():
        print('  |  syn_6: OK')
except NoSuchElementException:
    print('ERROR: проблема на син_6')

# 26. проверка syn_11 по видимости заголовка "Интерактивный выбор"
driver.get("https://syn11.lp.moigektar.ru/")
time.sleep(3)
try:
    block26=driver.find_element(by=By.XPATH, value="//span[text()[contains(.,'Интерактивный')]]")
    if block26.is_displayed():
        print('  |  syn_11: OK')
except NoSuchElementException:
    print('ERROR: проблема на син_11')

# 27. проверка syn_12 по видимости заголовка "Интерактивный выбор"
driver.get("https://syn12.lp.moigektar.ru/")
time.sleep(3)
try:
    block27=driver.find_element(by=By.XPATH, value="//span[text()[contains(.,'Интерактивный')]]")
    if block27.is_displayed():
        print(' / \ syn_12: OK')
except NoSuchElementException:
    print('ERROR: проблема на син_12')

# 28. проверка syn_13 по видимости заголовка "Выберите поселок"
driver.get("https://syn13.lp.moigektar.ru/")
time.sleep(3)
try:
    block28=driver.find_element(by=By.XPATH, value="//p[text()[contains(.,'Выберите поселок')]]")
    if block28.is_displayed():
        print(' \ / syn_13: OK')
except NoSuchElementException:
    print('ERROR: проблема на син_13')

# 29. проверка syn_14 по видимости заголовка "Интерактивный"
driver.get("https://syn14.lp.moigektar.ru/")
time.sleep(3)
try:
    block29=driver.find_element(by=By.XPATH, value="//span[text()[contains(.,'Интерактивный')]]")
    if block29.is_displayed():
        print('  |  syn_14: OK')
except NoSuchElementException:
    print('ERROR: проблема на син_14')

# 30. проверка syn_15 по видимости заголовка "Виртуальные туры"
driver.get("https://syn15.lp.moigektar.ru/")
time.sleep(3)
try:
    block30=driver.find_element(by=By.XPATH, value="//span[text()[contains(.,'Виртуальные туры')]]")
    if block30.is_displayed():
        print('  |  syn_15: OK')
except NoSuchElementException:
    print('ERROR: проблема на син_15')

# 31. проверка syn_16 по видимости заголовка "Интерактивный выбор"
driver.get("https://syn16.lp.moigektar.ru/")
time.sleep(3)
try:
    block31=driver.find_element(by=By.XPATH, value="//span[text()[contains(.,'Интерактивный')]]")
    if block31.is_displayed():
        print(' / \ syn_16: OK')
except NoSuchElementException:
    print('ERROR: проблема на син_16')

# 32. проверка syn_17 по видимости заголовка "Виртуальные туры"
driver.get("https://syn17.lp.moigektar.ru/")
time.sleep(3)
try:
    block32=driver.find_element(by=By.XPATH, value="//span[text()[contains(.,'Виртуальные')]]")
    if block32.is_displayed():
        print(' \ / syn_17: OK')
except NoSuchElementException:
    print('ERROR: проблема на син_17')

# 33. проверка syn_18 по видимости заголовка "Интерактивный"
driver.get("https://syn18.lp.moigektar.ru/")
time.sleep(3)
try:
    block33=driver.find_element(by=By.XPATH, value="//span[text()[contains(.,'Интерактивный')]]")
    if block33.is_displayed():
        print('  |  syn_18: OK')
except NoSuchElementException:
    print('ERROR: проблема на син_18')

# 34. проверка syn_19 по видимости заголовка "Генеральный"
driver.get("https://syn19.lp.moigektar.ru/")
time.sleep(3)
try:
    block34=driver.find_element(by=By.XPATH, value="//span[text()[contains(.,'Генеральный')]]")
    if block34.is_displayed():
        print('  |  syn_19: OK')
except NoSuchElementException:
    print('ERROR: проблема на син_19')

# 35. проверка syn_21 по видимости заголовка "Генеральный"
driver.get("https://syn21.lp.moigektar.ru/")
time.sleep(3)
try:
    block35=driver.find_element(by=By.XPATH, value="//span[text()[contains(.,'Генеральный')]]")
    if block35.is_displayed():
        print(' / \ syn_21: OK')
except NoSuchElementException:
    print('ERROR: проблема на син_21')

# 36. проверка syn_22 по видимости заголовка "Генеральный"
driver.get("https://syn22.lp.moigektar.ru/")
time.sleep(3)
try:
    block36=driver.find_element(by=By.XPATH, value="//span[text()[contains(.,'Генеральный')]]")
    if block36.is_displayed():
        print(' \ / syn_22: OK')
except NoSuchElementException:
    print('ERROR: проблема на син_22')

# 37. проверка syn_23 по видимости заголовка "Генеральный"
driver.get("https://syn23.lp.moigektar.ru/")
time.sleep(3)
try:
    block37=driver.find_element(by=By.XPATH, value="//span[text()[contains(.,'Генеральный')]]")
    if block37.is_displayed():
        print('  |  syn_23: OK')
except NoSuchElementException:
    print('ERROR: проблема на син_23')

# 38. проверка syn_24 по видимости заголовка "Генеральный"
driver.get("https://syn24.lp.moigektar.ru/")
time.sleep(3)
try:
    block38=driver.find_element(by=By.XPATH, value="//span[text()[contains(.,'Генеральный')]]")
    if block38.is_displayed():
        print('  |  syn_24: OK')
except NoSuchElementException:
    print('ERROR: проблема на син_24')

# 39. проверка syn_27 по видимости заголовка "Забронировать"
driver.get("https://syn27.lp.moigektar.ru/")
time.sleep(3)
try:
    block39=driver.find_element(by=By.XPATH, value="//h3[text()[contains(.,'Забронировать')]]")
    if block39.is_displayed():
        print(' / \ syn_27: OK')
except NoSuchElementException:
    print('ERROR: проблема на син_27')

# 40. проверка syn_29 по видимости заголовка "Генеральный"
driver.get("https://syn29.lp.moigektar.ru/")
time.sleep(3)
try:
    block40=driver.find_element(by=By.XPATH, value="//span[text()[contains(.,'Генеральный')]]")
    if block40.is_displayed():
        print(' \ / syn_29: OK')
except NoSuchElementException:
    print('ERROR: проблема на син_29')

# 41. проверка syn_35 по видимости заголовка "Генеральный"
driver.get("https://syn35.lp.moigektar.ru/")
time.sleep(3)
try:
    block41=driver.find_element(by=By.XPATH, value="//span[text()[contains(.,'Генеральный')]]")
    if block41.is_displayed():
        print('  |  syn_35: OK')
except NoSuchElementException:
    print('ERROR: проблема на син_35')

# 42. проверка syn_36 по видимости заголовка "Генеральный"
driver.get("https://syn36.lp.moigektar.ru/")
time.sleep(3)
try:
    block42=driver.find_element(by=By.XPATH, value="//span[text()[contains(.,'Генеральный')]]")
    if block42.is_displayed():
        print('  |  syn_36: OK')
except NoSuchElementException:
    print('ERROR: проблема на син_36')

# 44. проверка syn_39 по видимости заголовка "Генеральный"
driver.get("https://syn39.lp.moigektar.ru/")
time.sleep(3)
try:
    block44=driver.find_element(by=By.XPATH, value="//span[text()[contains(.,'Генеральный')]]")
    if block44.is_displayed():
        print(' / \ syn_39: OK')
except NoSuchElementException:
    print('ERROR: проблема на син_39')

# 45. проверка syn_42 по видимости заголовка "Генеральный"
driver.get("https://syn42.lp.moigektar.ru/")
time.sleep(3)
try:
    block45=driver.find_element(by=By.XPATH, value="//span[text()[contains(.,'Генеральный')]]")
    if block45.is_displayed():
        print(' \ / syn_42: OK')
except NoSuchElementException:
    print('ERROR: проблема на син_42')

# 46. проверка syn_48 по видимости заголовка "Генеральный"
driver.get("https://syn48.lp.moigektar.ru/")
time.sleep(3)
try:
    block46=driver.find_element(by=By.XPATH, value="//h2[text()[contains(.,'Генеральный')]]")
    if block46.is_displayed():
        print('  |  syn_48: OK')
except NoSuchElementException:
    print('ERROR: проблема на син_48')

# 47. проверка syn_58 по видимости заголовка "Забронировать"
driver.get("https://syn58.lp.moigektar.ru/")
time.sleep(3)
try:
    block47=driver.find_element(by=By.XPATH, value="//h3[text()[contains(.,'Забронировать')]]")
    if block47.is_displayed():
        print('  |  syn_58: OK')
except NoSuchElementException:
    print('ERROR: проблема на син_58')

# 48. проверка syn_61 по видимости заголовка "Генеральный"
driver.get("https://syn61.lp.moigektar.ru/")
time.sleep(3)
try:
    block48=driver.find_element(by=By.XPATH, value="//span[text()[contains(.,'Генеральный')]]")
    if block48.is_displayed():
        print(' / \ syn_61: OK')
except NoSuchElementException:
    print('ERROR: проблема на син_61')

# 49. проверка сервиса дорог по наличию заголовка "Login"
driver.get("https://editor.roads.bigland.ru/site/login")
time.sleep(2)
try:
    block49=driver.find_element(by=By.XPATH, value="//h1[text()[contains(.,'Login')]]")
    if block49.is_displayed():
        print(' \ / Сервис дорог: OK')
except NoSuchElementException:
    print('ERROR: проблема на Сервисе дорог')

# 50. проверка syn_85 по наличию заголовка "Login"
driver.get("https://syn85.lp.moigektar.ru/")
time.sleep(2)
try:
    block50=driver.find_element(by=By.XPATH, value="//h2[text()[contains(.,'Генеральный')]]")
    if block50.is_displayed():
        print('  |  syn_85: OK')
except NoSuchElementException:
    print('ERROR: проблема на син_85')


time.sleep(2)
driver.quit()
