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


# Скрипт проверяет, сколько участков СП осталось у посёлка на странице СП на МГ
# и сообщает, если их осталось меньше 3
#
# В лог выводится сообщение "ERROR" + количество СП, если СП у участка меньше 3
#
# Прогон теста занимает примерно одну минуту
#


driver.get("https://moigektar.ru/batches/special")

list_len = 100
i = 1
qty_sp = 0
qty_withoutSold = 0

while i < list_len:
    # посчитать количество карточек СП на странице
    len_sp = len(driver.find_elements(by=By.XPATH, value='//*[@id="batchSpecialOffers"]/div/div/ul/li'))
    if i == 1:
        qty_sp = len_sp
    # откидываю из результата карточки проданных СП: это каждый пятый в списке у одного посёлка
    if i > 1:
        qty_withoutSold = len_sp - (len_sp // 5)
    # занести в переменную текущую надпись в окне дропдауна
    drop = driver.find_element(by=By.XPATH, value='//*[@id="main"]/div[2]/div/div/div/div[1]/ul/li/a')
    drop_text = drop.text
    if i == 1:
        print('  Количество СП на странице "' + drop_text + '" = ' + str(len_sp))
    else:
        print('  Количество СП на странице "' + drop_text + '" = ' + str(qty_withoutSold))
    # написать, если осталось 2 или меньше СП в посёлке
    if len_sp <= 2:
        print('ERROR: ' + str(len_sp) + ' СП в посёлке "' + drop_text + '"')
    # посчитать длину списка посёлков и занести её в переменную
    drop.click()
    time.sleep(3)
    list = driver.find_elements(by=By.XPATH, value="//a[text()[contains(., '" + drop_text + "')]]//parent::li//li/a")
    list_len = len(list)
    # нажать пункт списка, соответствующий текущему значению переменной - должен произойти переход на страницу посёлка
    list[i].click()
    i += 1
# для последнего пункта списка посёлков
if i == list_len:
    #print('  ' + str(i) + ' / ' + str(list_len))
    len_sp = len(driver.find_elements(by=By.XPATH, value='//*[@id="batchSpecialOffers"]/div/div/ul/li'))
    qty_withoutSold = len_sp - (len_sp // 5)
    drop = driver.find_element(by=By.XPATH, value='//*[@id="main"]/div[2]/div/div/div/div[1]/ul/li/a')
    drop_text = drop.text
    print('  Количество СП на странице "' + drop_text + '" = ' + str(qty_withoutSold))
    if len_sp <= 2:
        print('ERROR: ' + str(len_sp) + ' СП в посёлке "' + drop_text + '"')
    print('    Всего ' + str(list_len) + ' страниц и ' + str(qty_sp) + ' СП')


#time.sleep(5)
driver.quit()

