from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
service = ChromeService(executable_path=ChromeDriverManager().install())
from selenium.webdriver.chrome.options import Options
ch_options = Options()
ch_options.add_argument('--headless')
ch_options.page_load_strategy = 'eager'
driver = webdriver.Chrome(service=service, options= ch_options)
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
actions = ActionChains(driver)
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import ElementNotVisibleException
from selenium.webdriver.common.keys import Keys
import time
import json
driver.set_window_size(1660, 1000)
driver.implicitly_wait(10)

# Скрипт проверяет наличие всех блоков на МГ по заголовкам или (реже) другим элементам
#
# В лог выводится сообщение "ОК", если блок был найден
# В лог выводится сообщение "ERROR", если элемент не загрузился
#

with open('data.json', 'r') as file:
    data = json.load(file)

# 1. Главная
driver.get("https://moigektar.ru" + str(data['mg_loc']['mg_cur_release_2']))
print('Главная')

# баннер над хедером
# try:
#     assert driver.find_element(by=By.CLASS_NAME, value='w-banner').is_displayed()
#     print('   баннер над хедером: OK')
# except:
#     print('ERROR: проблема с баннером над хедером на главной МГ')

# хедер + квиз
count_h_1 = 0
while count_h_1 < 3:
    try:
        wait(driver, 20).until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
        header = wait(driver,14).until(EC.presence_of_element_located((By.XPATH, '(//div[(contains(@class, "w-navbar"))])[1]')))
        if header:
            print('   OK: хедер')
            count_h_1 = 3
            count_h_2 = 0
            while count_h_2 < 3:
                try:
                    header_q_btn = driver.find_element(by=By.XPATH, value="//li/div/*[text()[contains(., 'Подобрать участок')]]")
                    if header_q_btn.is_displayed():
                        print('     OK: кнопка квиза в хедере')
                        count_h_2 = 3
                        count_h_3 = 0
                        while count_h_3 < 3:
                            try:
                                actions.click(header_q_btn).perform()
                                m_iframe = driver.find_element(by=By.XPATH, value="//iframe[@class='marquiz__frame marquiz__frame_open']")
                                driver.switch_to.frame(m_iframe)
                                header_quiz = wait(driver,20).until(EC.visibility_of_element_located((By.XPATH, '//button[text()[contains(., "Настроить фильтр")]]')))
                                if header_quiz:
                                    print('     OK: квиз в хедере')
                                    driver.switch_to.default_content()
                                    driver.find_element(by=By.XPATH, value="//button[@id='marquiz__close']").click()
                                    break
                            except:
                                count_h_3 += 1
                                if count_h_3 == 3:
                                    print('ERROR: не отображается содержимое квиза в хедере')
                                else:
                                    driver.refresh()
                except:
                    count_h_2 += 1
                    if count_h_2 == 3:
                        print('ERROR: не отображается кнопка "Подобрать участок" в хедере')
                    else:
                        driver.refresh()
    except:
        count_h_1 += 1
        if count_h_1 == 3:
            print('ERROR: не отображается хедер')
        else:
            driver.refresh()

# 1-й экран / квиз / видео
count_f_1 = 0
while count_f_1 < 3:
    try:
        f_screen = driver.find_element(by=By.XPATH, value='(//div[@id="main"]//*[text()[contains(., "Гектар")]])[1]').is_displayed()
        if f_screen:
            print('   OK: заголовок на 1-м экране')
            count_f_1 = 3
            count_f_2 = 0
            while count_f_2 < 3:
                try:
                    f_screen_pic = driver.find_element(by=By.CLASS_NAME, value='w-main-bg')
                    if f_screen_pic.is_displayed():
                        print('     OK: бэкграунд 1-го экрана')
                        count_f_2 = 3
                        break
                except:
                    count_f_2 += 1
                    if count_f_2 == 3:
                        print('ERROR: не отображается бэкграунд 1-го экрана')
                    else:
                        driver.refresh()
            count_f_3 = 0 # quiz
            while count_f_3 < 3:
                try:
                    f_screen_q_btn = driver.find_element(by=By.XPATH, value='(//a[(contains(@class, "btn-mquiz"))])[2]')
                    if f_screen_q_btn.is_displayed():
                        print('     OK: кнопка квиза на 1-м экране')
                        count_f_3 = 3
                        count_f_4 = 0
                        while count_f_4 < 3:
                            try:
                                actions.click(f_screen_q_btn).perform()
                                m_iframe = driver.find_element(by=By.XPATH, value='//iframe[@class="marquiz__frame marquiz__frame_open"]')
                                driver.switch_to.frame(m_iframe)
                                f_screen_q = wait(driver,20).until(EC.visibility_of_element_located((By.XPATH, '//button[text()[contains(., "Настроить фильтр")]]')))
                                if f_screen_q:
                                    print('     OK: квиз на 1-м экране')
                                    driver.switch_to.default_content()
                                    driver.find_element(by=By.XPATH, value="//button[@id='marquiz__close']").click()
                                    break
                            except:
                                count_f_4 += 1
                                if count_f_4 == 3:
                                    print('ERROR: не отображается содержимое квиза на 1-м экране')
                                else:
                                    driver.refresh()
                except:
                    count_f_3 += 1
                    if count_f_3 == 3:
                        print('ERROR: не отображается кнопка квиза на 1-м экране')
                    else:
                        driver.refresh()
            count_f_5 = 0 #video
            while count_f_5 < 3:
                try:
                    f_screen_v_btn = driver.find_element(by=By.CLASS_NAME, value='w-main__video-wrapper')
                    if f_screen_v_btn.is_displayed():
                        print('     OK: кнопка видео на 1-м экране')
                        count_f_5 = 3
                        count_f_6 = 0
                        while count_f_6 < 3:
                            try:
                                actions.click(f_screen_v_btn).perform()
                                f_screen_video = driver.find_element(by=By.XPATH, value='//iframe[@class="uk-lightbox-iframe"]')
                                driver.switch_to.frame(f_screen_video)
                                f_screen_elem = wait(driver,20).until(EC.visibility_of_element_located((By.XPATH, '(//*[text()[contains(., "Как проект")]])[3]')))
                                if f_screen_elem.is_displayed():
                                    print('     OK: видео на 1-м экране')
                                    driver.refresh()
                                    break
                            except:
                                count_f_6 += 1
                                if count_f_6 == 3:
                                    print('ERROR: не отображается содержимое видео на 1-м экране')
                                else:
                                    driver.refresh()
                except:
                    count_f_5 += 1
                    if count_f_5 == 3:
                        print('ERROR: не отображается кнопка видео на 1-м экране')
                    else:
                        driver.refresh()
    except:
        count_f_1 += 1
        if count_f_1 == 3:
            print('ERROR: не отображается заголовок на 1-м экране')
        else:
            driver.refresh()

# блок "МГ - это" / видео / квиз / модалка
count_mg_1 = 0
while count_mg_1 < 3:
    try:
        f_screen = driver.find_element(by=By.XPATH, value='//*[text()="Проект «Мой гектар» — это:"]').is_displayed()
        if f_screen:
            print('   OK: блок "Проект МГ - это" есть')
            count_mg_1 = 3
            count_mg_2 = 0 # видео в 1-й секции
            while count_mg_2 < 3:
                try:
                    mg_v_btn = driver.find_element(by=By.XPATH, value='//*[@id="w-descr"]//*[text()="Смотреть "]')
                    if mg_v_btn.is_displayed():
                        print('     OK: кнопка "Смотреть видео о проекте"')
                        count_mg_2 = 3
                        count_mg_3 = 0
                        while count_mg_3 < 3:
                            try:
                                mg_v_btn.click()
                                mg_v_iframe = driver.find_element(by=By.XPATH, value='//iframe[@class="uk-lightbox-iframe"]')
                                driver.switch_to.frame(mg_v_iframe)
                                mg_video = wait(driver,20).until(EC.visibility_of_element_located((By.XPATH, '(//*[text()="Проект «Мой гектар»"])[2]')))
                                if mg_video:
                                    print('     OK: видео в блоке "МГ - это"')
                                    driver.refresh()
                                    break
                            except:
                                count_mg_3 += 1
                                if count_mg_3 == 3:
                                    print('ERROR: не отображается видео в блоке "МГ - это"')
                                else:
                                    driver.refresh()
                except:
                    count_mg_2 += 1
                    if count_mg_2 == 3:
                        print('ERROR: не отображается кнопка "Смотреть видео о проекте"')
                    else:
                        driver.refresh()
            count_mg_4 = 0 # quiz во второй секции
            while count_mg_4 < 3:
                try:
                    mg_q_btn = driver.find_element(by=By.XPATH, value='(//*[@id="mquiz-btn"])[2]')
                    if mg_q_btn.is_displayed():
                        print('     OK: кнопка квиза в "МГ - это"')
                        count_mg_4 = 3
                        count_mg_5 = 0
                        while count_mg_5 < 3:
                            try:
                                actions.click(mg_q_btn).perform()
                                mg_q = driver.find_element(by=By.XPATH, value='//iframe[@class="marquiz__frame marquiz__frame_open"]')
                                driver.switch_to.frame(mg_q)
                                mg_elem = wait(driver,20).until(EC.visibility_of_element_located((By.XPATH, '//button[text()[contains(., "Настроить фильтр")]]')))
                                if mg_elem.is_displayed():
                                    print('     OK: квиз в "МГ - это"')
                                    driver.switch_to.default_content()
                                    driver.find_element(by=By.XPATH, value="//button[@id='marquiz__close']").click()
                                    break
                            except:
                                count_mg_5 += 1
                                if count_mg_5 == 3:
                                    print('ERROR: не отображается содержимое квиза в "МГ - это"')
                                else:
                                    driver.refresh()
                except:
                    count_mg_4 += 1
                    if count_mg_4 == 3:
                        print('ERROR: не отображается кнопка квиза в "МГ - это"')
                    else:
                        driver.refresh()
            count_mg_6 = 0 # модалка в 5-й секции
            while count_mg_6 < 3:
                try:
                    mg_mod_btn = wait(driver,20).until(EC.visibility_of_element_located((By.XPATH, '//*[@href="#modal-descr-consult"]')))
                    if mg_mod_btn.is_displayed():
                        print('     OK: кнопка модалки в секции 5')
                        count_mg_6 = 3
                        count_mg_7 = 0
                        while count_mg_7 < 3:
                            try:
                                actions.click(mg_mod_btn).perform()
                                mg_input = wait(driver,20).until(EC.visibility_of_element_located((By.XPATH, '(//*[@id="consultationform-name"])[20]')))
                                if mg_input.is_displayed():
                                    print('     OK: модалка в секции 5')
                                    driver.refresh()
                                    break
                            except:
                                count_mg_7 += 1
                                if count_mg_7 == 3:
                                    print('ERROR: не отображается содержимое модалки в "МГ - это"')
                                else:
                                    driver.refresh()
                except:
                    count_mg_6 += 1
                    if count_mg_6 == 3:
                        print('ERROR: не отображается кнопка модалки в секции 5')
                    else:
                        driver.refresh()
    except:
        count_mg_1 += 1
        if count_mg_1 == 3:
            print('ERROR: не отображается блок "Проект МГ - это"')
        else:
            driver.refresh()

# "Специальное предложение"
# заголовок / 1-я карточка / количество карточек / переход в каталог
count_so_1 = 0
while count_so_1 < 3:
    try:
        so_title = driver.find_element(by=By.XPATH, value='//*[text()[contains(., "Специальная цена")]]')
        if so_title.is_displayed():
            print('   OK: заголовок "Специальная цена"')
            count_so_1 = 3
            count_so_2 = 0
            while count_so_2 < 3:
                try:
                    actions.move_to_element(so_title).perform()
                    time.sleep(1)
                    so_card = driver.find_element(by=By.XPATH, value='(//*[(contains(@class, "sow-special-offer-item"))])[1]')
                    if so_title.is_displayed():
                        print('     OK: 1-я карточка в блоке "Специальная цена"')
                        count_so_2 = 3
                        count_so_3 = 0
                        while count_so_3 < 3:
                            try:
                                so_count = len(driver.find_elements(by=By.XPATH, value='//*[@id="catalogueSpecial"]/div/div/div/div/ul/li'))
                                if so_count == 6:
                                    print('     OK: количество карточек в СП = 6')
                                    count_so_3 = 3
                                    break
                            except:
                                count_so_3 += 1
                                if count_so_3 == 3:
                                    print('ERROR: количество карточек в СП не равно 6')
                                else:
                                    driver.refresh()
                except:
                    count_so_2 += 1
                    if count_so_2 == 3:
                        print('ERROR: не отображаются карточки в блоке "Специальная цена"')
                    else:
                        driver.refresh()
            count_so_4 = 0
            while count_so_4 < 3:
                try:
                    so_btn = driver.find_element(by=By.XPATH, value='//*[@id="catalogueSpecial"]//*[@class="uk-text-center"]/a')
                    so_btn.click()
                    cat_title = driver.find_element(By.XPATH, value='//h2[text()="Подобрать участок"]')
                    if cat_title.is_displayed():
                        print('     OK: из "Спеццены" выполняется переход в каталог')
                        driver.execute_script("window.history.go(-1)")
                        count_so_4 = 3
                        break
                except:
                    count_so_4 += 1
                    if count_so_4 == 3:
                        print('ERROR: из "Спеццены" не выполняется переход в каталог')
                        driver.get("https://moigektar.ru")
                    else:
                        driver.refresh()
    except:
        count_so_1 += 1
        if count_so_1 == 3:
            print('ERROR: не отображается заголовок "Специальная цена"')
        else:
            driver.refresh()

# форма со Снежанной
# поле ввода / кнопка / фото
count_sf_1 = 0
while count_sf_1 < 3:
    try:
        assert EC.visibility_of_element_located((By.XPATH, '(//*[(contains(@class, "snezh"))]//*[@id="consultationform-name"])[1]'))
        print('   OK: поле ввода в 1-й форме со Снежанной')
        count_sf_1 = 3
        count_sf_2 = 0 # кнопка
        while count_sf_2 < 3:
            try:
                assert EC.visibility_of_element_located((By.XPATH, '(//*[(contains(@class, "snezh"))]//button)[1]'))
                print('     OK: кнопка в форме со Снежанной')
                count_sf_2 = 3
            except:
                count_sf_2 += 1
                if count_sf_2 == 3:
                    print('ERROR: не отображается кнопка в форме со Снежанной')
                else:
                    driver.refresh()
            count_sf_3 = 0 # фото
            while count_sf_3 < 3:
                try:
                    assert EC.visibility_of_element_located((By.XPATH, '//*[@id="catalogueSpecial"]//*[@class="uk-text-center"]/a'))
                    print('     OK: отображается фото в форме со Снежанной')
                    count_sf_3 = 3
                except:
                    count_sf_3 += 1
                    if count_sf_3 == 3:
                        print('ERROR: не отображается фото в форме со Снежанной')
                    else:
                        driver.refresh()
    except:
        count_sf_1 += 1
        if count_sf_1 == 3:
            print('ERROR: не отображается поле ввода в форме со Снежанной')
        else:
            driver.refresh()

# блок "Лучшие посёлки"
# try:
#     driver.refresh()
#     wait(driver, 10).until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
#     l_title = driver.find_element(by=By.XPATH, value='//h1[text()[contains(.,"Лучшие поселки")]]')
#     ActionChains(driver).move_to_element(l_title).send_keys(Keys.PAGE_DOWN).perform()
#     assert EC.visibility_of_element_located((By.XPATH, "//h1[text()[contains(.,'Лучшие поселки')]]"))
#     print('   блок "Лучшие поселки": OK')
#     try:
#         wait(driver,14).until(EC.visibility_of_element_located((By.XPATH, "//*[@id='catalogue']//div[1]/div/div[1]//li[1]//button")))
#         print('   карточки в Лучших посёлках на главной: OK')
#     except:
#         print('ERROR: проблема с карточками Лучшие посёлки на главной МГ')
# except:
#     print('ERROR: проблема с блоком "Лучшие поселки проекта" на главной МГ')

# блок "Виртуальный тур"
# try:
#     wait(driver,14).until(EC.visibility_of_element_located((By.XPATH, "//h1[text()[contains(.,'Виртуальный тур')]]")))
#     print('   блок "Виртуальный тур": есть')
#     try:
#         t_btn = driver.find_element(by=By.XPATH, value="//*[@id='w-select-map-preview']/div[3]//img")
#         actions.move_to_element(t_btn).pause(3).click(t_btn).perform()
#         try:
#             iframe = driver.find_element(by=By.XPATH, value="//iframe[@class='embed-responsive-item']")
#             driver.switch_to.frame(iframe)
#             wait(driver,20).until(EC.visibility_of_element_located((By.XPATH, "//*[@id='krpanoSWFObject']//div[(contains(@style, 'z-index: 205'))]")))
#             print('   блок "Виртуальный тур": тур загрузился, OK')
#             driver.switch_to.default_content()
#         except:
#             driver.switch_to.default_content()
#             print('ERROR: не загрузился "Виртуальный тур" на главной МГ')
#     except:
#         print('ERROR: что-то с кнопкой в блоке "Виртуальный тур" на главной МГ')
# except:
#     print('ERROR: проблема с блоком "Виртуальный тур" на главной МГ')

# "Новости развития посёлков"
# заголовок / 1-я карточка / модалка
count_n_1 = 0
while count_n_1 < 3:
    try:
        title = driver.find_element(by=By.XPATH, value='(//*[text()[contains(., "Новости развития поселков")]])[1]')
        if title.is_displayed():
            print('   OK: заголовок "Новости развития поселков"')
            count_n_1 = 3
            count_n_2 = 0
            while count_n_2 < 3:
                try:
                    actions.move_to_element(title).perform()
                    time.sleep(1)
                    card = driver.find_element(by=By.XPATH, value='(//*[@class="w-news-wrapper"]//*[(contains(@class, "uk-background-cover uk-width-1-1"))])[1]')
                    if card.is_displayed():
                        print('     OK: 1-я карточка в блоке "Новости развития поселков"')
                        count_n_2 = 3
                        count_n_3 = 0
                        while count_n_3 < 3:
                            try:
                                actions.click(card).perform()
                                heading = wait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, '//*[@class="uk-modal-container js-news-view-modal uk-modal uk-open"]//div[@class="uk-padding uk-article js-news-view-modal-content"]')))
                                if heading:
                                    print('     OK: модалка новости в блоке "Новости развития поселков"')
                                    driver.find_element(By.XPATH, value='//*[@class="uk-modal-container js-news-view-modal uk-modal uk-open"]//div[@class="uk-padding uk-article js-news-view-modal-content"]/parent::div/button').click()
                                    break
                            except:
                                count_n_3 += 1
                                if count_n_3 == 3:
                                    print('ERROR: не отображается модалка новости в блоке "Новости развития поселков"')
                                else:
                                    driver.refresh()
                except:
                    count_n_2 += 1
                    if count_n_2 == 3:
                        print('ERROR: не отображается заголовок "Новости развития поселков" на главной МГ')
                    else:
                        driver.refresh()
    except:
        count_n_1 += 1
        if count_n_1 == 3:
            print('ERROR: не отображается заголовок "Новости развития поселков" на главной МГ')
        else:
            driver.refresh()

# блок "Лучшее время"
# try:
#     wait(driver,14).until(EC.presence_of_element_located((By.XPATH, "//h1[text()[contains(.,'Лучшее время')]]")))
#     print('   блок "Лучшее время для покупки": OK')
# except:
#     print('ERROR: проблема с блоком "Лучшее время для покупки" на главной МГ')

# блок "Видео, которые"
# try:
#     wait(driver,14).until(EC.visibility_of_element_located((By.XPATH, "//h1[text()[contains(.,'Видео, которые')]]")))
#     print('   блок "Видео, которые": OK')
# except:
#     print('ERROR: проблема с блоком "Видео, которые вам стоит увидеть" на главной МГ')

# блок "Награды проекта"
# try:
#     wait(driver,14).until(EC.visibility_of_element_located((By.XPATH, "//div[text()[contains(.,'Награды проекта')]]")))
#     print('   блок "Награды проекта": OK')
# except:
#     print('ERROR: проблема с блоком "Награды проекта" на главной МГ')

# блок "СМИ о проекте"
# try:
#     smi = driver.find_element(by=By.XPATH, value="//div[text()[contains(.,'СМИ о проекте')]]")
#     ActionChains(driver).move_to_element(smi).send_keys(Keys.PAGE_DOWN).perform()
#     assert EC.visibility_of_element_located((By.XPATH, '//div[text()[contains(.,"СМИ о проекте")]]//parent::div[1]//*[@class="uk-first-column"]'))
#     print('   блок "СМИ о проекте": OK')
# except:
#     print('ERROR: проблема с блоком "СМИ о проекте" на главной МГ')

# блок "Развитие вашего участка"
# try:
#     driver.refresh()
#     wait(driver, 10).until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
#     growth = driver.find_element(by=By.XPATH, value="//h1[text()[contains(.,'Развитие вашего участка')]]")
#     ActionChains(driver).move_to_element(growth).send_keys(Keys.PAGE_DOWN).perform()
#     assert EC.visibility_of_element_located((By.XPATH, "//h1[text()[contains(.,'Развитие вашего участка')]]"))
#     print('   блок "Развитие вашего участка": OK')
# except:
#     print('ERROR: проблема с блоком "Развитие вашего участка" на главной МГ')

# блок "Сохраните свои"
# try:
#     driver.refresh()
#     wait(driver, 10).until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
#     save = driver.find_element(by=By.XPATH, value="//h1[text()[contains(.,'Сохраните свои')]]")
#     ActionChains(driver).move_to_element(save).send_keys(Keys.PAGE_DOWN).perform()
#     wait(driver,14).until(EC.visibility_of_element_located((By.XPATH, "//h1[text()[contains(.,'Сохраните свои')]]")))
#     print('   блок "Сохраните свои": OK')
# except:
#     print('ERROR: проблема с блоком "Сохраните свои" на главной МГ')

# блок "Почему нам доверяют"
# try:
#     why = driver.find_element(by=By.XPATH, value="//div[text()[contains(.,'Почему нам')]]")
#     ActionChains(driver).move_to_element(why).send_keys(Keys.PAGE_DOWN).perform()
#     assert EC.visibility_of_element_located((By.XPATH, "//div[text()[contains(.,'Почему нам')]]"))
#     print('   блок "Почему нам доверяют": OK')
#     try:
#         time.sleep(3)
#         driver.find_element(by=By.XPATH, value="//*[text()[contains(.,'Почему нам доверяют')]]//parent::div//a[text()[contains(., 'Подобрать участок')]]").click()
#         m_iframe = driver.find_element(by=By.XPATH, value="//iframe[@class='marquiz__frame marquiz__frame_open']")
#         driver.switch_to.frame(m_iframe)
#         wait(driver,20).until(EC.visibility_of_element_located((By.XPATH, "//*[@id='start']/div/div[2]/div[1]/button")))
#         print('   квиз в "Почему нам доверяют": OK')
#     except:
#         print('ERROR: не загрузился квиз в "почему нам доверяют" на главной"')
# except:
#     print('ERROR: проблема с блоком "Почему нам доверяют" на главной МГ')

# блок "Господдержка"
# try:
#     driver.refresh()
#     wait(driver, 10).until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
#     gos = driver.find_element(by=By.XPATH, value="//h1[text()[contains(.,'Государственная поддержка')]]")
#     ActionChains(driver).move_to_element(gos).send_keys(Keys.PAGE_DOWN).perform()
#     wait(driver,14).until(EC.visibility_of_element_located((By.XPATH, "//h1[text()[contains(.,'Государственная поддержка')]]")))
#     print('   блок "Государственная поддержка": OK')
# except:
#     print('ERROR: проблема с блоком "Государственная поддержка" на главной МГ')

# форма "Узнайте все подробности"
# try:
#     wait(driver,14).until(EC.visibility_of_element_located((By.XPATH, "//b[text()[contains(.,'Узнайте все подробности')]]")))
#     print('   форма "Узнайте все подробности": OK')
# except:
#     print('ERROR: проблема с формой "Узнайте все подробности" на главной МГ')

# блок "Гектар под ваши цели"
count_gg_1 = 0
while count_gg_1 < 3:
    try:
        gg_title = wait(driver,14).until(EC.presence_of_element_located((By.XPATH, '//*[text()="Гектар под ваши цели"]')))
        actions.move_to_element(gg_title).perform()
        if gg_title.is_displayed():
            print('   OK: блок "Гектар под ваши цели" есть')
            count_gg_1 = 3
            count_gg_2 = 0 # 1-я карточка
            while count_gg_2 < 3:
                try:
                    gg_card = driver.find_element(by=By.XPATH, value='(//*[@id="w-goals"]//li)[1]')
                    if gg_card.is_displayed():
                        print('     OK: 1-я карточка в "Гектар под ваши цели"')
                        count_gg_2 = 3
                        break
                except:
                    count_gg_2 += 1
                    if count_gg_2 == 3:
                        print('ERROR: не отображается 1-я карточка в "Гектар под ваши цели"')
                    else:
                        driver.refresh()
            count_gg_3 = 0 # кнопка "Показать еще"
            while count_gg_3 < 3:
                try:
                    gg_btn = driver.find_element(by=By.XPATH, value='//*[@id="w-goals"]//a[text()="Показать еще"]')
                    if gg_btn.is_displayed():
                        print('     OK: кнопка в "Гектар под ваши цели"')
                        count_gg_3 = 3
                        break
                except:
                    count_gg_3 += 1
                    if count_gg_3 == 3:
                        print('ERROR: не отображается кнопка кнопка в "Гектар под ваши цели"')
                    else:
                        driver.refresh()
    except:
        count_gg_1 += 1
        if count_gg_1 == 3:
            print('ERROR: не отображается блок "Гектар под ваши цели"')
        else:
            driver.refresh()

# блок "Отзывы о проекте"
# try:
#     wait(driver,14).until(EC.visibility_of_element_located((By.XPATH, "//div[text()[contains(.,'Отзывы о проекте')]]")))
#     print('   блок "Отзывы о проекте": OK')
# except:
#     print('ERROR: проблема с блоком "Отзывы о проекте" на главной МГ')

# блок "Бизнес-планы"
# try:
#     wait(driver,14).until(EC.visibility_of_element_located((By.XPATH, "//h1[text()[contains(.,'Бизнес-планы')]]")))
#     print('   блок "Бизнес-планы": OK')
# except:
#     print('ERROR: проблема с блоком "Бизнес-планы" на главной МГ')

# блок "Личный кабинет"
# try:
#     wait(driver,14).until(EC.visibility_of_element_located((By.XPATH, '//*[@class="w-community-content"]/div[text()[contains(.,"Личный кабинет")]]')))
#     print('   блок "Личный кабинет": OK')
# except:
#     print('ERROR: проблема с блоком "Личный кабинет" на главной МГ')

# блок "Подпишитесь в соцсетях"
# try:
#     sMedia = driver.find_element(by=By.XPATH, value="//div[text()[contains(.,'в соцсетях')]]")
#     ActionChains(driver).move_to_element(sMedia).send_keys(Keys.PAGE_DOWN).perform()
#     assert EC.visibility_of_element_located((By.XPATH, '//*[@id="elfsight_social_container"]//*[@data-elfsight-app-lazy=""]/div/div/div/div/div'))
#     print('   блок "Подпишитесь в соцсетях": OK')
# except:
#     print('ERROR: проблема с блоком "Подпишитесь в соцсетях" на главной МГ')

# форма "Подпишитесь на рассылку"
# try:
#     wait(driver,14).until(EC.visibility_of_element_located((By.XPATH, "//*[text()[contains(.,'Подпишитесь на рассылку')]]")))
#     print('   форма "Подпишитесь на рассылку": OK')
# except:
#     print('ERROR: проблема с формой "Подпишитесь на рассылку" на главной МГ')

# блок "Подпишитесь на новости развития"
# try:
#     title_r = driver.find_element(by=By.XPATH, value="//h1[text()[contains(.,'на новости развития')]]")
#     print('   блок "Подпишитесь на новости развития": OK')
#     try:
#         actions.move_to_element(title_r).perform()
#         time.sleep(5)
#         wait(driver,14).until(EC.visibility_of_element_located((By.XPATH, "//div[@class='w-news-wrapper']/div/ul/li[1]/a/div[1]/div/div[1]")))
#         print('   блок "Подпишитесь на новости развития": карточки отображаются, ОК')
#     except:
#         print('ERROR: проблема с блоком "Подпишитесь на новости развития" на главной МГ')
# except:
#     print('ERROR: проблема с блоком "Подпишитесь на новости развития" на главной МГ')

# блок "Проект от сохи до сохи"
# try:
#     title_n = driver.find_element(by=By.XPATH, value="//h1[text()[contains(.,'От сохи')]]")
#     print('   блок "От сохи до сохи": OK')
#     try:
#         actions.move_to_element(title_n).perform()
#         actions.send_keys(Keys.PAGE_DOWN).perform()
#         time.sleep(5)
#         wait(driver,14).until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".yottie-widget-inner div:nth-of-type(1) > div:nth-of-type(1) > a span img")))
#         print('   блок "От сохи до сохи": карточки отображаются, ОК')
#     except:
#         print('ERROR: проблема с блоком "От сохи до сохи" на главной МГ')
# except:
#     print('ERROR: проблема с блоком "От сохи до сохи" на главной МГ')

# блок "Приглашаем на встречу"
# try:
#     wait(driver,14).until(EC.visibility_of_element_located((By.XPATH, "//div[text()[contains(.,'Приглашаем на встречу')]]")))
#     print('   блок "Приглашаем на встречу": OK')
# except:
#     print('ERROR: проблема с блоком "Приглашаем на встречу" на главной МГ')

# блок Футер
# try:
#     wait(driver,14).until(EC.presence_of_element_located((By.XPATH, "//div[@class='w-footer']/div/div/div/div/button[text()[contains(.,'Связаться')]]")))
#     print('   футер: OK\n')
# except:
#     print('ERROR: проблема с футером на главной МГ\n')



# 2. Каталог посёлков
# driver.get('https://moigektar.ru/catalogue')
# print("Каталог поселков")

#блок "Специальное предложение"
# try:
#     wait(driver,14).until(EC.visibility_of_element_located((By.XPATH, "" + str(data["mg_loc"]["mg_catalog_sow_title"]))))
#     print('   блок "Специальное предложение": OK')
#     try:
#         wait(driver,14).until(EC.visibility_of_element_located((By.XPATH, ""  + str(data["mg_loc"]["mg_catalog_country_sow_btn"]))))
#         print('   карточки в СП: OK')
#     except:
#         print('ERROR: проблема с карточками СП в Каталоге поселков')
# except (TimeoutException, NoSuchElementException, ElementNotVisibleException):
#     print('ERROR: проблема с блоком "Специальное предложение" в Каталоге поселков')



time.sleep(1)
driver.quit()

