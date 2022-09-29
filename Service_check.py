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
import time

# Скрипт последовательно заходит на каждый сервис МГ и проверяет видимость
# одного графического элемента на странице



# 1. проверка "МГ" по видимости заголовка "Специальное преложение" на главной
driver.get("https://moigektar.ru/")
time.sleep(3)
block1=driver.find_element(by=By.XPATH, value="//h1[text()[contains(.,'Специальное предложение')]]")
if block1.is_displayed():
    print('  1 МГ: OK')

# 2. проверка ЛК по видимости баннера, который отображается при первом входе в ЛК
driver.get("https://cabinet.moigektar.ru/security/login")
time.sleep(1)
driver.find_element(by=By.XPATH, value="//a[text()[contains(.,'Попробовать прямо сейчас!')]]").click()
time.sleep(3)
button=driver.find_element(by=By.XPATH, value="//img[@src='/img/polls-banner.jpg']")
if button.is_displayed():
    print('  2 ЛК: ОК')

# 3. проверка syn_9 по видимости заголовка "Генеральный"
driver.get("https://syn9.lp.moigektar.ru/")
time.sleep(3)
block3=driver.find_element(by=By.XPATH, value="//span[text()[contains(.,'Генеральный')]]")
if block3.is_displayed():
    print('  3 syn_9: OK')

# 4. проверка syn_33 по видимости заголовка "Генеральный"
driver.get("https://syn33.lp.moigektar.ru/")
time.sleep(3)
block4=driver.find_element(by=By.XPATH, value="//span[text()[contains(.,'Генеральный')]]")
if block4.is_displayed():
    print('  4 syn_33: OK')

# 5. проверка syn_34 по видимости заголовка "Генеральный"
driver.get("https://syn34.lp.moigektar.ru/")
time.sleep(3)
block5=driver.find_element(by=By.XPATH, value="//span[text()[contains(.,'Генеральный')]]")
if block5.is_displayed():
    print('  5 syn_34: OK')

# 6. проверка syn_37 по видимости заголовка "Генеральный"
driver.get("https://syn37.lp.moigektar.ru/")
time.sleep(3)
block6=driver.find_element(by=By.XPATH, value="//div[@class='d-none d-xs-block']//span[text()[contains(.,'Генеральный')]]")
if block6.is_displayed():
    print('  6 syn_37: OK')

# 7. проверка syn_53 по видимости заголовка "Генеральный"
driver.get("https://syn53.lp.moigektar.ru/")
time.sleep(3)
block7=driver.find_element(by=By.XPATH, value="//h2[text()[contains(.,'Генеральный')]]")
if block7.is_displayed():
    print('  7 syn_53: OK')

# 8. проверка syn_67 по видимости заголовка "Генеральный"
driver.get("https://syn67.lp.moigektar.ru/")
time.sleep(3)
block8=driver.find_element(by=By.XPATH, value="//h2[text()[contains(.,'Генеральный')]]")
if block8.is_displayed():
    print('  8 syn_67: OK')

# 9. проверка vazuza2 по видимости заголовка "Генеральный"
driver.get("https://vazuza2.lp.moigektar.ru/")
time.sleep(3)
block9=driver.find_element(by=By.XPATH, value="//div[text()[contains(.,'Генеральный')]]")
if block9.is_displayed():
    print('  9 vazuza2: OK')

# 10. проверка pay.moigektar по видимости заголовка "Платёжные сервисы"
driver.get("https://pay.moigektar.ru/")
time.sleep(3)
block10=driver.find_element(by=By.XPATH, value="//h3[text()[contains(.,'Платежные сервисы')]]")
if block10.is_displayed():
    print(' 10 pay.moigektar: OK')

# 11. проверка сервиса "Вынос границ" по наличию заголовка "Вынос границ участка"
driver.get("https://points.lp.moigektar.ru/")
time.sleep(3)
block11=driver.find_element(by=By.XPATH, value="//p[text()[contains(.,'ВЫНОС ГРАНИЦ')]]")
if block11.is_displayed():
    print(' 11 Вынос границ: OK')

# 12. проверка сервиса "Инвестиции" по наличию заголовка "Инвестиции"
driver.get("https://investment.lp.moigektar.ru/")
time.sleep(3)
block12=driver.find_element(by=By.XPATH, value="//h1[text()[contains(.,'Инвестиции')]]")
if block12.is_displayed():
    print(' 12 Инвестиции: OK')

# 13. проверка сервиса "Комплекс услуг" по наличию заголовка "Комплекс услуг"
driver.get("https://complex.lp.moigektar.ru/")
time.sleep(3)
block13=driver.find_element(by=By.XPATH, value="//h1[text()[contains(.,'комплекс услуг')]]")
if block13.is_displayed():
    print(' 13 Комплекс услуг: OK')

# 14. проверка сервиса "Кооперативы" по наличию заголовка "Вступайте в кооператив"
driver.get("https://cooperative.lp.moigektar.ru/")
time.sleep(3)
block14=driver.find_element(by=By.XPATH, value="//h1[text()[contains(.,'Вступайте')]]")
if block14.is_displayed():
    print(' 14 Кооперативы: OK')

# 15. проверка сервиса "Правовая поддержка" по наличию заголовка "Центр правовой поддержки"
driver.get("https://law.lp.moigektar.ru/")
time.sleep(3)
block15=driver.find_element(by=By.XPATH, value="//h1[text()[contains(.,'центр правовой поддержки')]]")
if block15.is_displayed():
    print(' 15 Правовая поддержка: OK')

# 16. проверка сервиса "Разработка проекта" по наличию заголовка "Разработка эскизного проекта"
driver.get("https://planning.moigektar.ru/")
time.sleep(3)
block16=driver.find_element(by=By.XPATH, value="//p[text()[contains(.,'разработка')]]")
if block16.is_displayed():
    print(' 16 Разработка проекта: OK')

# 17. проверка сервиса "Расчистка участка" по наличию заголовка "Расчистка участка"
driver.get("https://clearance.lp.moigektar.ru/")
time.sleep(3)
block17=driver.find_element(by=By.XPATH, value="//p[text()[contains(.,'РАСЧИСТКА УЧАСТКА')]]")
if block17.is_displayed():
    print(' 17 Расчистка участка: OK')

# 18. проверка сервиса "Строительство въездной группы" по наличию заголовка "Коллективное строительство"
driver.get("https://syn9.entrance.lp.moigektar.ru/")
time.sleep(3)
block18=driver.find_element(by=By.XPATH, value="//h1[text()[contains(.,'Коллективное')]]")
if block18.is_displayed():
    print(' 18 Строительство въездной группы: OK')

# 19. проверка сервиса "Строительство дорог" по наличию заголовка "Коллективное строительство"
driver.get("https://syn23.roads.moigektar.ru/")
time.sleep(3)
block19=driver.find_element(by=By.XPATH, value="//p[text()[contains(.,'КОЛЛЕКТИВНОЕ')]]")
if block19.is_displayed():
    print(' 19 Строительство дорог: OK')

# 20. проверка сервиса "Строительство центрального дома" по наличию заголовка "Коллективное строительство"
driver.get("https://house.lp.moigektar.ru/")
time.sleep(3)
block20=driver.find_element(by=By.XPATH, value="//h1[text()[contains(.,'коллективное строительство')]]")
if block20.is_displayed():
    print(' 20 Строительство центрального дома: OK')

# 21. проверка сервиса "Установка видеонаблюдения" по наличию заголовка "Установка видеонаблюдения"
driver.get("https://barrier.lp.moigektar.ru/")
time.sleep(3)
block21=driver.find_element(by=By.XPATH, value="//h1[text()[contains(.,'установка видеонаблюдения')]]")
if block21.is_displayed():
    print(' 21 Установка видеонаблюдения: OK')

# 22. проверка сервиса "Электрификация" по наличию заголовка "Коллективное строительство"
driver.get("https://syn9.electrification.lp.moigektar.ru/")
time.sleep(3)
block22=driver.find_element(by=By.XPATH, value="//h1[text()[contains(.,'коллективное')]]")
if block22.is_displayed():
    print(' 22 Электрификация: OK')

# 23. проверка сервиса "GIS" по наличию заголовка "Login"
driver.get("https://gis.bigland.ru/site/login")
time.sleep(1)
block23=driver.find_element(by=By.XPATH, value="//h1[text()[contains(.,'Login')]]")
if block23.is_displayed():
    print(' 23 GIS: OK')

# 24. проверка сервиса генерации КП по наличию заголовка "Сервис генерации КП"
driver.get("https://offers.bigland.ru/")
time.sleep(1)
block24=driver.find_element(by=By.XPATH, value="//h1[text()[contains(.,'Сервис генерации КП')]]")
if block24.is_displayed():
    print(' 24 Сервис генерации КП: OK')

# 25. проверка syn_6 по видимости заголовка "Выбрать участок"
driver.get("https://syn6.lp.moigektar.ru/")
time.sleep(3)
block25=driver.find_element(by=By.XPATH, value="//h2[text()[contains(.,'Выбрать участок')]]")
if block25.is_displayed():
    print(' 25 syn_6: OK')

# 26. проверка syn_11 по видимости заголовка "Выбрать участок"
driver.get("https://syn11.lp.moigektar.ru/")
time.sleep(3)
block26=driver.find_element(by=By.XPATH, value="//span[text()[contains(.,'Интерактивный')]]")
if block26.is_displayed():
    print(' 26 syn_11: OK')

# 27. проверка syn_12 по видимости заголовка "Выбрать участок"
driver.get("https://syn12.lp.moigektar.ru/")
time.sleep(3)
block27=driver.find_element(by=By.XPATH, value="//span[text()[contains(.,'Интерактивный')]]")
if block27.is_displayed():
    print(' 27 syn_12: OK')

# 28. проверка syn_13 по видимости заголовка "Выберите поселок"
driver.get("https://syn13.lp.moigektar.ru/")
time.sleep(3)
block28=driver.find_element(by=By.XPATH, value="//p[text()[contains(.,'Выберите поселок')]]")
if block28.is_displayed():
    print(' 28 syn_13: OK')








time.sleep(2)
driver.quit()
