from selenium import webdriver
from selenium.webdriver.chrome.options import Options
ch_options = Options()
ch_options.add_argument('--headless')
ch_options.page_load_strategy = 'eager'
driver = webdriver.Chrome(options= ch_options)
from selenium.webdriver.common.by import By
import time
driver.set_window_size(1660, 1000)
driver.implicitly_wait(10)


# Скрипт проверяет, сколько участков СП есть у посёлка на странице Каталог участков на сайте МГ
# и сообщает, если их осталось меньше 3
#
# В лог выводится сообщение с количеством посёлков и названия этих посёлков с количеством
# участков СП для каждого из них
# В этом списке выводится сообщение "ERROR" + количество СП, если СП у посёлка меньше 3
#

driver.get("https://moigektar.ru/batches?sortId=-special")
# нужно зайти в окно фильтра и раскрыть дропдаун, иначе список не инициализируется
driver.find_element(by=By.XPATH, value='//*[text()="Все фильтры"]').click()
driver.find_element(by=By.XPATH, value='//*[@id="containerciw_w2"]//button').click()
# узнать количество посёлков в списке
list_len = len(driver.find_elements(by=By.XPATH, value="//li//input[@data-select-id='select_ciw_w2']//following-sibling::span[@class='uk-text-small']"))
print('Всего посёлков в списке: ' + str(list_len))
# получить названия всех посёлков, которые сейчас есть в списке, и создать список
villages = []
i = 1
while i <= list_len:
    village = driver.find_element(by=By.XPATH, value="//li//div[" + str(i) + "]/label/input[@data-select-id='select_ciw_w2']//following-sibling::span[@class='uk-text-small']").text
    villages.append(village)
    i += 1

# закрыть окно фильтра
driver.find_element(by=By.XPATH, value="//a//following-sibling::*[@href='#offcanvas-special-filter']").click()

# подставить последовательно в поле ввода все элементы списка и посмотреть, сколько есть участков СП для каждого посёлка
n = 0
while n < list_len:
    inp_field = driver.find_element(by=By.XPATH, value="//form//*[(contains(@placeholder, 'Поиск по'))]")
    inp_field.clear()
    inp_field.send_keys(str(villages[n]))
    time.sleep(8)
    # подсчёт участков СП по атрибуту карточки "звёздочка".
    # предполагается, что СП одного посёлка всегда помещаются на одной странице
    sp_count = len(driver.find_elements(by=By.CSS_SELECTOR, value='span[uk-icon="star"]'))
    if sp_count <= 2:
        print('ERROR: ' + str(villages[n]) + ': ' + str(sp_count) + ' СП')
    else:
        print('       ' + str(villages[n]) + ': ' + str(sp_count) + ' СП')
    n += 1


time.sleep(3)
driver.quit()
