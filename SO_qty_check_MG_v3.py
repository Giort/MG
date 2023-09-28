from selenium import webdriver
from selenium.webdriver.chrome.options import Options
ch_options = Options()
#ch_options.add_argument('--headless')
ch_options.page_load_strategy = 'eager'
driver = webdriver.Chrome(options= ch_options)
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
actions = ActionChains(driver)
import time
import json
driver.set_window_size(1660, 1000)
driver.implicitly_wait(10)

with open('data.json', 'r') as file:
    data = json.load(file)


# !!! сейчас этот скрипт требует доработки после того,
# как были добавлены все доступные посёлки
#
# Скрипт проверяет, сколько участков СП есть у посёлка на странице Каталог участков на сайте МГ
# и сообщает, если их осталось меньше 3
#
# В лог выводится сообщение с количеством посёлков и названия этих посёлков с количеством
# участков СП для каждого из них
# В этом списке выводится сообщение "ERROR" + количество СП, если СП у посёлка меньше 3
#
#

driver.get("https://moigektar.ru/catalogue?sortId=-special")
# избавляемся от модалки авторизации
try:
    time.sleep(1)
    auth_win = driver.find_element(by=By.ID, value='modal-auth-batches')
    driver.execute_script("""
    var auth_win = arguments[0];
    auth_win.remove();
    """, auth_win)
except:
    print('ERROR: не получилось удалить модалку авторизации в Каталоге участков')

# избавляемся от квиза
try:
    time.sleep(1)
    quiz = driver.find_element(by=By.CSS_SELECTOR, value='div.marquiz__bg')
    driver.execute_script("""
    var quiz = arguments[0];
    quiz.remove();
    """, quiz)
except:
    print('ERROR: не получилось удалить квиз в Каталоге участков')

# избавляемся от модалки roistat
try:
    time.sleep(1)
    roi = driver.find_element(by=By.CLASS_NAME, value='roistat-lh-popup')
    driver.execute_script("""
    var roi = arguments[0];
    roi.remove();
    """, roi)
except:
    print('ERROR: не получилось удалить модалку роистат в Каталоге участков')

# нужно зайти в окно фильтра и раскрыть дропдаун, иначе список не инициализируется
driver.find_element(by=By.XPATH, value='//*[text()="Все фильтры"]').click()
driver.find_element(by=By.XPATH, value='//*[@id="containerciw_w3"]//button').click()
# узнать количество посёлков в списке
list_len = len(driver.find_elements(by=By.XPATH, value='//div[@id="containerciw_w3"]//following-sibling::span[@class="uk-text-small"]'))
print('Всего посёлков в списке: ' + str(list_len))
# получить названия всех посёлков, которые сейчас есть в списке, и создать список
villages = []
i = 1
while i <= list_len:
    village = driver.find_element(by=By.XPATH, value='(//div[@id="containerciw_w3"]//following-sibling::span[@class="uk-text-small"])[' + str(i) + ']').text
    #village = driver.find_element(by=By.XPATH, value="//li//div[" + str(i) + "]/label/input[@data-select-id='select_ciw_w2']//following-sibling::span[@class='uk-text-small']").text
    villages.append(village)
    i += 1

print(villages)
# закрыть окно фильтра
driver.find_element(by=By.XPATH, value="//div[@class='uk-flex uk-flex-center uk-flex-middle uk-position-relative']/a//following-sibling::*[@href='#offcanvas-special-filter']").click()

# подставить последовательно в поле ввода все элементы списка и посмотреть, сколько есть участков СП для каждого посёлка
n = 0
while n < list_len:
    inp_field = driver.find_element(by=By.XPATH, value="//div[(contains(@uk-sticky, 'show-on-up'))]//*[(contains(@placeholder, 'Поиск по'))]")
    inp_field.click()
    inp_field.clear()
    inp_field.send_keys(str(villages[n]))
    time.sleep(4)
    # подсчёт участков СП по атрибуту карточки - метке "Специальное предложение".
    # предполагается, что СП одного посёлка всегда помещаются на одной странице (т. е. не больше 20 штук)
    sp_count = len(driver.find_elements(by=By.XPATH, value='//span[text()[contains(., "Специальное предложение")]]'))
    if sp_count:
        if sp_count <= 2:
            print('ERROR: ' + str(villages[n]) + ': ' + str(sp_count) + ' СП')
        else:
            print('       ' + str(villages[n]) + ': ' + str(sp_count) + ' СП')
        n += 1
    else:
        n += 1


time.sleep(3)
driver.quit()
