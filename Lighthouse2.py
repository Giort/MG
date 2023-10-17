# https://importsem.com/use-python-to-automate-lighthouse-reports/
import chromedriver_binary
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
import pandas as pd
import numpy
from numpy.lib.function_base import extract
from datetime import datetime
from os.path import join
from openpyxl import Workbook
wb1 = Workbook()
wb2 = Workbook()

df = pd.DataFrame([], columns=['URL', 'Performance', 'First_Contentful_Paint', 'Total_Blocking_Time', 'Speed_Index', 'Largest_Contentful_Paint'])

name = "Report"
getdate = datetime.now().strftime("%m-%d-%y")
urls = ["https://www.moigektar.ru"]
path1 = '/home/giort/Documents/LighthouseReport1/'
path2 = '/home/giort/Documents/LighthouseReport2/'

for url in urls:
    stream = os.popen('lighthouse --quiet --no-update-notifier --no-enable-error-reporting --output=json --output-path=YOUR_LOCAL_PATH'+name+'_'+getdate+'.report.json --chrome-flags="--headless" ' + url)

    time.sleep(220)
    print("Report complete for: " + url)

    json_filename = path1 + name + '_' + getdate + '.report.json'

    with open(json_filename) as json_data:
        loaded_json = json.load(json_data)

    performance = str(round(loaded_json["categories"]["performance"]["score"] * 100))
    firstContPaint = str(round(loaded_json["categories"]["firstContPaint"]["score"] * 100))
    totalBlockTime = str(round(loaded_json["categories"]["totalBlockTime"]["score"] * 100))
    speedIndex = str(round(loaded_json["categories"]["speedIndex"]["score"] * 100))
    largContpaint = str(round(loaded_json["categories"]["largContpaint"]["score"] * 100))

    dict = {"URL":url, "Performance":performance, "First_Contetntful_Paint":firstContPaint, "Total_Blocking_Time":totalBlockTime, "Speed_Index":speedIndex, "Largest_Contentful_Paint":largContpaint}
    df = df.append(dict, ignore_index=True).sort_values(by='Performance', ascending=False)

    df.to_csv(path2/'lighthouse_' + name + '_' + getdate + '.csv')
    print(df)

time.sleep(1)
driver.quit()
