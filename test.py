from time import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
options = Options()
options.add_argument('--headless')
ch_options = Options()
ch_options.add_argument('--headless')
driver = webdriver.Chrome(options= ch_options)
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
driver.maximize_window()


from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time



# 1. проверка "МГ" по видимости заголовка "Специальное преложение" на главной
driver.get("https://moigektar.ru/")
time.sleep(3)
driver.find_element(by=By.XPATH, value="//h1[text()[contains(.,'Специальное предложение')]]")

# 2. проверка ЛК по видимости баннера, который отображается при первом входе в ЛК
driver.get("https://cabinet.moigektar.ru/security/login")
time.sleep(1)
driver.find_element(by=By.XPATH, value="//a[text()[contains(.,'Попробовать прямо сейчас!')]]").click()
time.sleep(3)
driver.find_element(by=By.XPATH, value="//img[@src='/img/polls-banner.jpg']")

# 3. проверка syn_9 по видимости заголовка "Генеральный"
driver.get("https://syn9.lp.moigektar.ru/")
time.sleep(3)
driver.find_element(by=By.XPATH, value="//span[text()[contains(.,'Генеральный')]]")

# 4. проверка syn_33 по видимости заголовка "Генеральный"
driver.get("https://syn33.lp.moigektar.ru/")
time.sleep(3)
driver.find_element(by=By.XPATH, value="//span[text()[contains(.,'Генеральный')]]")

# 5. проверка syn_34 по видимости заголовка "Генеральный"
driver.get("https://syn34.lp.moigektar.ru/")
time.sleep(3)
driver.find_element(by=By.XPATH, value="//span[text()[contains(.,'Генеральный')]]")

# 6. проверка syn_37 по видимости заголовка "Генеральный"
driver.get("https://syn37.lp.moigektar.ru/")
time.sleep(3)
driver.find_element(by=By.XPATH, value="//div[@class='d-none d-xs-block']//span[text()[contains(.,'Генеральный')]]")

# 7. проверка syn_53 по видимости заголовка "Генеральный"
driver.get("https://syn53.lp.moigektar.ru/")
time.sleep(3)
driver.find_element(by=By.XPATH, value="//h2[text()[contains(.,'Генеральный')]]")

# 8. проверка syn_67 по видимости заголовка "Генеральный"
driver.get("https://syn67.lp.moigektar.ru/")
time.sleep(3)
driver.find_element(by=By.XPATH, value="//h2[text()[contains(.,'Генеральный')]]")

# 9. проверка vazuza2 по видимости заголовка "Генеральный"
driver.get("https://vazuza2.lp.moigektar.ru/")
time.sleep(3)
driver.find_element(by=By.XPATH, value="//div[text()[contains(.,'Генеральный')]]")

# 10. проверка pay.moigektar по видимости заголовка "Платёжные сервисы"
driver.get("https://pay.moigektar.ru/")
time.sleep(3)
driver.find_element(by=By.XPATH, value="//h3[text()[contains(.,'Платежные сервисы')]]")

# 11. проверка сервиса "Вынос границ" по наличию заголовка "Вынос границ участка"
driver.get("https://points.lp.moigektar.ru/")
time.sleep(3)
driver.find_element(by=By.XPATH, value="//p[text()[contains(.,'ВЫНОС ГРАНИЦ')]]")

# 12. проверка сервиса "Инвестиции" по наличию заголовка "Инвестиции"
driver.get("https://investment.lp.moigektar.ru/")
time.sleep(3)
driver.find_element(by=By.XPATH, value="//h1[text()[contains(.,'Инвестиции')]]")

# 13. проверка сервиса "Комплекс услуг" по наличию заголовка "Комплекс услуг"
driver.get("https://complex.lp.moigektar.ru/")
time.sleep(3)
driver.find_element(by=By.XPATH, value="//h1[text()[contains(.,'комплекс услуг')]]")

# 14. проверка сервиса "Кооперативы" по наличию заголовка "Вступайте в кооператив"
driver.get("https://cooperative.lp.moigektar.ru/")
time.sleep(3)
driver.find_element(by=By.XPATH, value="//h1[text()[contains(.,'Вступайте')]]")

# 15. проверка сервиса "Правовая поддержка" по наличию заголовка "Центр правовой поддержки"
driver.get("https://law.lp.moigektar.ru/")
time.sleep(3)
driver.find_element(by=By.XPATH, value="//h1[text()[contains(.,'центр правовой поддержки')]]")

# 16. проверка сервиса "Разработка проекта" по наличию заголовка "Разработка эскизного проекта"
driver.get("https://planning.moigektar.ru/")
time.sleep(3)
driver.find_element(by=By.XPATH, value="//p[text()[contains(.,'разработка')]]")

# 17. проверка сервиса "Расчистка участка" по наличию заголовка "Расчистка участка"
driver.get("https://clearance.lp.moigektar.ru/")
time.sleep(3)
driver.find_element(by=By.XPATH, value="//p[text()[contains(.,'РАСЧИСТКА УЧАСТКА')]]")

# 18. проверка сервиса "Строительство въездной группы" по наличию заголовка "Коллективное строительство"
driver.get("https://syn9.entrance.lp.moigektar.ru/")
time.sleep(3)
driver.find_element(by=By.XPATH, value="//h1[text()[contains(.,'Коллективное')]]")

# 19. проверка сервиса "Строительство дорог" по наличию заголовка "Коллективное строительство"
driver.get("https://syn23.roads.moigektar.ru/")
time.sleep(3)
driver.find_element(by=By.XPATH, value="//p[text()[contains(.,'КОЛЛЕКТИВНОЕ')]]")

# 20. проверка сервиса "Строительство центрального дома" по наличию заголовка "Коллективное строительство"
driver.get("https://house.lp.moigektar.ru/")
time.sleep(3)
driver.find_element(by=By.XPATH, value="//h1[text()[contains(.,'коллективное строительство')]]")

# 21. проверка сервиса "Установка видеонаблюдения" по наличию заголовка "Установка видеонаблюдения"
driver.get("https://barrier.lp.moigektar.ru/")
time.sleep(3)
driver.find_element(by=By.XPATH, value="//h1[text()[contains(.,'установка видеонаблюдения')]]")

# 22. проверка сервиса "Электрификация" по наличию заголовка "Коллективное строительство"
driver.get("https://syn9.electrification.lp.moigektar.ru/")
time.sleep(3)
driver.find_element(by=By.XPATH, value="//h1[text()[contains(.,'коллективное')]]")

# 23. проверка сервиса "GIS" по наличию заголовка "Login"
driver.get("https://gis.bigland.ru/site/login")
time.sleep(1)
driver.find_element(by=By.XPATH, value="//h1[text()[contains(.,'Login')]]")

# 24. проверка сервиса генерации КП по наличию заголовка "Сервис генерации КП"
driver.get("https://offers.bigland.ru/")
time.sleep(1)
driver.find_element(by=By.XPATH, value="//h1[text()[contains(.,'Сервис генерации КП')]]")

# 25. проверка syn_6 по видимости заголовка "Выбрать участок"
driver.get("https://syn6.lp.moigektar.ru/")
time.sleep(3)
driver.find_element(by=By.XPATH, value="//h2[text()[contains(.,'Выбрать участок')]]")

# 26. проверка syn_11 по видимости заголовка "Интерактивный"
driver.get("https://syn11.lp.moigektar.ru/")
time.sleep(3)
driver.find_element(by=By.XPATH, value="//span[text()[contains(.,'Интерактивный')]]")

# 27. проверка syn_12 по видимости заголовка "Интерактивный"
driver.get("https://syn12.lp.moigektar.ru/")
time.sleep(3)
driver.find_element(by=By.XPATH, value="//span[text()[contains(.,'Интерактивный')]]")

# 28. проверка syn_13 по видимости заголовка "Выберите поселок"
driver.get("https://syn13.lp.moigektar.ru/")
time.sleep(3)
driver.find_element(by=By.XPATH, value="//p[text()[contains(.,'Выберите поселок')]]")

# 29. проверка syn_14 по видимости заголовка "Интерактивный"
driver.get("https://syn14.lp.moigektar.ru/")
time.sleep(3)
driver.find_element(by=By.XPATH, value="//span[text()[contains(.,'Интерактивный')]]")

# 30. проверка syn_15 по видимости заголовка "Виртуальные туры"
driver.get("https://syn15.lp.moigektar.ru/")
time.sleep(3)
driver.find_element(by=By.XPATH, value="//span[text()[contains(.,'Виртуальные туры')]]")

# 31. проверка syn_16 по видимости заголовка "Интерактивный выбор"
driver.get("https://syn16.lp.moigektar.ru/")
time.sleep(3)
driver.find_element(by=By.XPATH, value="//span[text()[contains(.,'Интерактивный')]]")

# 32. проверка syn_17 по видимости заголовка "Виртуальные туры"
driver.get("https://syn17.lp.moigektar.ru/")
time.sleep(3)
driver.find_element(by=By.XPATH, value="//span[text()[contains(.,'Виртуальные')]]")

# 33. проверка syn_18 по видимости заголовка "Интерактивный"
driver.get("https://syn18.lp.moigektar.ru/")
time.sleep(3)
driver.find_element(by=By.XPATH, value="//span[text()[contains(.,'Интерактивный')]]")

# 34. проверка syn_19 по видимости заголовка "Генеральный"
driver.get("https://syn19.lp.moigektar.ru/")
time.sleep(3)
driver.find_element(by=By.XPATH, value="//span[text()[contains(.,'Генеральный')]]")

# 35. проверка syn_21 по видимости заголовка "Генеральный"
driver.get("https://syn21.lp.moigektar.ru/")
time.sleep(3)
driver.find_element(by=By.XPATH, value="//span[text()[contains(.,'Генеральный')]]")

# 36. проверка syn_22 по видимости заголовка "Генеральный"
driver.get("https://syn22.lp.moigektar.ru/")
time.sleep(3)
driver.find_element(by=By.XPATH, value="//span[text()[contains(.,'Генеральный')]]")

# 37. проверка syn_23 по видимости заголовка "Генеральный"
driver.get("https://syn23.lp.moigektar.ru/")
time.sleep(3)
driver.find_element(by=By.XPATH, value="//span[text()[contains(.,'Генеральный')]]")

# 38. проверка syn_24 по видимости заголовка "Генеральный"
driver.get("https://syn24.lp.moigektar.ru/")
time.sleep(3)
driver.find_element(by=By.XPATH, value="//span[text()[contains(.,'Генеральный')]]")

# 39. проверка syn_27 по видимости заголовка "Забронировать"
driver.get("https://syn27.lp.moigektar.ru/")
time.sleep(3)
driver.find_element(by=By.XPATH, value="//h3[text()[contains(.,'Забронировать')]]")

# 40. проверка syn_29 по видимости заголовка "Генеральный"
driver.get("https://syn29.lp.moigektar.ru/")
time.sleep(3)
driver.find_element(by=By.XPATH, value="//span[text()[contains(.,'Генеральный')]]")

# 41. проверка syn_35 по видимости заголовка "Генеральный"
driver.get("https://syn35.lp.moigektar.ru/")
time.sleep(3)
driver.find_element(by=By.XPATH, value="//span[text()[contains(.,'Генеральный')]]")

# 42. проверка syn_36 по видимости заголовка "Генеральный"
driver.get("https://syn36.lp.moigektar.ru/")
time.sleep(3)
driver.find_element(by=By.XPATH, value="//span[text()[contains(.,'Генеральный')]]")

# 44. проверка syn_39 по видимости заголовка "Генеральный"
driver.get("https://syn39.lp.moigektar.ru/")
time.sleep(3)
driver.find_element(by=By.XPATH, value="//span[text()[contains(.,'Генеральный')]]")

# 45. проверка syn_42 по видимости заголовка "Генеральный"
driver.get("https://syn42.lp.moigektar.ru/")
time.sleep(3)
driver.find_element(by=By.XPATH, value="//span[text()[contains(.,'Генеральный')]]")

# 46. проверка syn_48 по видимости заголовка "Генеральный"
driver.get("https://syn48.lp.moigektar.ru/")
time.sleep(3)
driver.find_element(by=By.XPATH, value="//h2[text()[contains(.,'Генеральный')]]")

# 47. проверка syn_58 по видимости заголовка "Забронировать"
driver.get("https://syn58.lp.moigektar.ru/")
time.sleep(3)
driver.find_element(by=By.XPATH, value="//h3[text()[contains(.,'Забронировать')]]")

# 48. проверка syn_61 по видимости заголовка "Генеральный"
driver.get("https://syn61.lp.moigektar.ru/")
time.sleep(3)
driver.find_element(by=By.XPATH, value="//span[text()[contains(.,'Генеральный')]]")

# 49. проверка сервиса дорог по наличию заголовка "Login"
driver.get("https://editor.roads.bigland.ru/site/login")
time.sleep(2)
driver.find_element(by=By.XPATH, value="//h1[text()[contains(.,'Login')]]")


#time.sleep(2)
driver.quit()
