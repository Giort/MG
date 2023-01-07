from selenium import webdriver
from selenium.webdriver.chrome.options import Options
ch_options = Options()
ch_options.add_argument('--headless')
driver = webdriver.Chrome(options= ch_options)
from selenium.webdriver.common.action_chains import ActionChains
actions = ActionChains(driver)
from selenium.webdriver.common.by import By
import time
driver.set_window_size(1920, 1080)


# Скрипт проверяет, сколько участков СП осталось у посёлка
# и сообщает, если их осталось 2 или меньше
#
# При подсчёте скрипт не учитывает количество карточек "продано", так как
# если оставшихся СП 4 и меньше, то карточки "продано" уже не отображаются
#


driver.get("https://moigektar.ru/batches/special")

list_len = 50
i = 1
while i < list_len:
    # написать текущее значение переменной/ порядковый номер страницы, на которой выполнен подсчёт
    # c косяком на первой итерации, но я не буду трогать, потому что и так работает
    print(str(i) + ' / ' + str(list_len))
    # посчитать количество карточек СП на странице
    len_sp = len(driver.find_elements(by=By.XPATH, value='//*[@id="batchSpecialOffers"]/div/div/ul/li'))
    # занести в переменную текущую надпись в окне дропдауна
    drop = driver.find_element(by=By.XPATH, value='//*[@id="main"]/div[2]/div/div/div/div[1]/ul/li/a')
    drop_text = drop.text
    print('Количество СП на странице "' + drop_text + '" = ' + str(len_sp))
    # написать, если осталось 2 или меньше СП в посёлке
    if len_sp <= 2:
        print('ERROR: ' + str(len_sp) + ' СП в посёлке "' + drop_text + '"')
    # посчитать длину списка посёлков и занести её в переменную
    drop.click()
    time.sleep(3)
    list = driver.find_elements(by=By.XPATH, value="//a[text()[contains(., '" + drop_text + "')]]//parent::li//li/a")
    list_len = len(list)
    # нажать пункт списка, соответствующий текущему значению переменной - должен произойти переход на страницу посёлка
    print('Сейчас перейду на страницу "' + list[i].text + '"')
    list[i].click()
    i += 1
# для последнего пункта списка посёлков
if i == list_len:
    print(str(i) + ' / ' + str(list_len))
    drop = driver.find_element(by=By.XPATH, value='//*[@id="main"]/div[2]/div/div/div/div[1]/ul/li/a')
    drop_text = drop.text
    print('Количество СП на странице "' + drop_text + '" = ' + str(len_sp))
    if len_sp <= 2:
        print('ERROR: ' + str(len_sp) + ' СП в посёлке "' + drop_text + '"')




time.sleep(5)
driver.quit()

