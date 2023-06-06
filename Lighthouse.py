# https://medium.com/@olimpiuseulean/use-python-to-automate-google-lighthouse-reports-and-keep-a-historical-record-of-these-65f378325d64

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
ch_options = Options()
ch_options.add_argument('--headless')
ch_options.page_load_strategy = 'eager'
driver = webdriver.Chrome(options= ch_options)
from selenium.webdriver.common.action_chains import ActionChains
actions = ActionChains(driver)
import time
import json
import os
import numpy
from numpy.lib.function_base import extract
from datetime import datetime
from os.path import join
from openpyxl import Workbook
wb1 = Workbook()
wb2 = Workbook()

name = "Report"
getdate = datetime.now().strftime("%m-%d-%y")

relative_path = '/home/giort/Documents/LighthouseReport/'

csv_file_mob = join(relative_path, 'lighthouse_mobile_' + getdate + '.csv')
csv_file_des = join(relative_path, 'lighthouse_desktop_' + getdate + '.csv')

ws_mob = wb1.active
ws_des = wb2.active

def last_row_mob(): return len(ws_mob['A'])
def last_row_des(): return len(ws_des['A'])

urls = [
"https://moigektar.ru"
]

base = { 1: 'First Run', 2: 'Second Run', 3: 'Third Run', 4: 'Fourth Run', 5: 'Fifth Run', 6: 'Sixth Run'}



def extract_info(run, preset):
     header = [run, 'Product_Name', 'URL', 'Performance', 'First_Contentful_Paint', 'Total_Blocking_Time', 'Speed_Index', 'Largest_Contentful_Paint']


### here you can set how many times to run the test on the links
num_of_call = 4
for i in range(1, num_of_call+1):
    extract_info(base[i], preset='perf') ### run the test on mobile
    extract_info(base[i], preset='desktop') ### run the test on desktop

wb1.save(csv_file_mob)  ### save the results for mobile in an EXCEL FILE
wb2.save(csv_file_des) ### save the results for desktop in an EXCEL FILE

# performance - средневзвешенная оценка метрик
# first contetntful paint - время, за которое пользователь увидит какое-то содержимое веб-страницы, например, текст
# total blocking time - суммарное время абсолютно всех интервалов от первой отрисовки контента до полной загрузки страницы
# speed index - среднее время до отображения видимых частей страницы. Метрика наглядно демонстрирует, насколько быстро сайт выстраивает структуру контента.
# largest contentful paint - определяет время, за которое браузер отрисовывает самый крупный видимый объект в области просмотра#

    if preset == 'desktop':     ### preset -> 2 values: 'desktop' & 'perf'(for mobile)
        last = last_row_des()+1
        working = ws_des
    else:
        last = last_row_mob()+1
        working = ws_mob

    if 'first' not in run.lower():
        last += 1

    for i, r in enumerate('ABCDEFGHI'):
        working[r+str(last)].value = header[i]

    for url in urls:
        stream = os.popen('lighthouse --chrome-flags="--headless"--disable-storage-reset="true" --preset=' + preset + ' --output=json --output-path='+relative_path + name+'_'+getdate+'.report.json ' + url)


       time.sleep(60)
        json_filename = join(relative_path, name + '_' +
                             getdate + '.report.json')

       with open(json_filename, encoding="utf8") as json_data:
            loaded_json = json.load(json_data)
            print(loaded_json)

       ### set the items you need from the JSON FILE here
        try:
            product_name = loaded_json["audits"]["largest-contentful-paint-element"]["details"]["items"][0]["node"]["nodeLabel"] ### get the name of the product to be descriptive
            fcps = str(round(loaded_json["audits"]["first-contentful-paint"]["score"] * 100))
            sis = str(round(loaded_json["audits"]["speed-index"]["score"] * 100))
            lcps = str(round(loaded_json["audits"]["largest-contentful-paint"]["score"] * 100))
            seo = str(round(loaded_json["categories"]["seo"]["score"] * 100))
            performance = str(round(loaded_json["categories"]["performance"]["score"] * 100))
            best_practices = str(round(loaded_json["categories"]["best-practices"]["score"] * 100))
        except Exception as e:
            product_name = fcps = sis = lcps = seo = performance = best_practices = '-'
            print(e)


time.sleep(1)
driver.quit()
