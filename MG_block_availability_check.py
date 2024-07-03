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

# Скрипт проверяет наличие и работу элементов в блоках на МГ
#
# В лог выводится сообщение "ОК", если блок был найден
# В лог выводится сообщение "ERROR", если элемент не загрузился
#

with open('data.json', 'r') as file:
    data = json.load(file)

# 1. Главная
driver.get("https://moigektar.ru")
#driver.get("https://moigektar.ru" + str(data['mg_loc']['mg_cur_release_2']))
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
        header_q_btn = driver.find_element(by=By.XPATH, value="//li/div/*[text()[contains(., 'Подобрать участок')]]")
        actions.click(header_q_btn).perform()
        m_iframe = driver.find_element(by=By.XPATH, value="//iframe[@class='marquiz__frame marquiz__frame_open']")
        driver.switch_to.frame(m_iframe)
        header_quiz = wait(driver,20).until(EC.visibility_of_element_located((By.XPATH, '//button[text()[contains(., "Настроить фильтр")]]')))
        if header_quiz:
            driver.switch_to.default_content()
            driver.find_element(by=By.XPATH, value="//button[@id='marquiz__close']").click()
            print('     OK: хедер и квиз в нём')
            count_h_1 = 3
    except:
        count_h_1 += 1
        if count_h_1 == 3:
            print('ERROR: что-то не так в хедере')
        else:
            driver.refresh()

# 1-й экран - картинка / квиз / видео
count_f_1 = 0
while count_f_1 < 3:
    try:
        f_screen_pic = driver.find_element(by=By.CLASS_NAME, value='w-main-bg')
        if f_screen_pic.is_displayed():
            print('   OK: бэкграунд на 1-м экране')
            count_f_1 = 3
            count_f_2 = 0 # quiz
            while count_f_2 < 3:
                try:
                    f_screen_q_btn = driver.find_element(by=By.XPATH, value='(//a[(contains(@class, "btn-mquiz"))])[2]')
                    actions.click(f_screen_q_btn).perform()
                    m_iframe = driver.find_element(by=By.XPATH, value='//iframe[@class="marquiz__frame marquiz__frame_open"]')
                    driver.switch_to.frame(m_iframe)
                    f_screen_q = wait(driver,20).until(EC.visibility_of_element_located((By.XPATH, '//button[text()[contains(., "Настроить фильтр")]]')))
                    if f_screen_q:
                        driver.switch_to.default_content()
                        driver.find_element(by=By.XPATH, value="//button[@id='marquiz__close']").click()
                        print('     OK: квиз')
                        break
                except:
                    count_f_2 += 1
                    if count_f_2 == 3:
                        print('ERROR: не отображается содержимое квиза на 1-м экране')
                    else:
                        driver.refresh()
            count_f_3 = 0 #video
            while count_f_3 < 3:
                try:
                    f_screen_v_btn = driver.find_element(by=By.CLASS_NAME, value='w-main__video-wrapper')
                    actions.click(f_screen_v_btn).perform()
                    f_screen_video = driver.find_element(by=By.XPATH, value='//iframe[@class="uk-lightbox-iframe"]')
                    driver.switch_to.frame(f_screen_video)
                    f_screen_elem = wait(driver,20).until(EC.visibility_of_element_located((By.XPATH, '(//*[text()[contains(., "Как проект")]])[3]')))
                    if f_screen_elem.is_displayed():
                        driver.switch_to.default_content()
                        lb_btn = driver.find_element(by=By.CSS_SELECTOR, value = '.uk-lightbox.uk-overflow-hidden.uk-lightbox-panel.uk-open button')
                        lightbox = driver.find_element(by=By.XPATH, value='//*[@class="uk-lightbox uk-overflow-hidden uk-lightbox-panel uk-open"]')
                        driver.execute_script("arguments[0].setAttribute('class','uk-lightbox uk-overflow-hidden uk-lightbox-panel uk-open uk-active uk-transition-active')", lightbox)
                        lb_btn.click()
                        print('     OK: видео')
                        count_f_3 = 3
                        break
                except:
                    count_f_3 += 1
                    if count_f_3 == 3:
                        print('ERROR: не отображается видео на 1-м экране')
                    else:
                        driver.refresh()
    except:
        count_f_1 += 1
        if count_f_1 == 3:
            print('ERROR: не отображается бэкграунд на 1-м экране')
        else:
            driver.refresh()

# блок "МГ - это" - видео / квиз / модалка
count_mg_1 = 0
while count_mg_1 < 3:
    try:
        mg_v_btn = driver.find_element(by=By.XPATH, value='//*[@id="w-descr"]//*[text()="Смотреть "]')
        mg_v_btn.click()
        mg_v_iframe = driver.find_element(by=By.XPATH, value='//iframe[@class="uk-lightbox-iframe"]')
        driver.switch_to.frame(mg_v_iframe)
        mg_video = wait(driver,20).until(EC.visibility_of_element_located((By.XPATH, '(//*[text()="Проект «Мой гектар»"])[2]')))
        if mg_video:
            driver.switch_to.default_content()
            lb_btn = driver.find_element(by=By.CSS_SELECTOR, value = '.uk-lightbox.uk-overflow-hidden.uk-lightbox-panel.uk-open button')
            lightbox = driver.find_element(by=By.XPATH, value='//*[@class="uk-lightbox uk-overflow-hidden uk-lightbox-panel uk-open"]')
            driver.execute_script("arguments[0].setAttribute('class','uk-lightbox uk-overflow-hidden uk-lightbox-panel uk-open uk-active uk-transition-active')", lightbox)
            lb_btn.click()
            print('   OK: блок "Проект МГ - это", видео')
            count_mg_1 = 3
            count_mg_2 = 0 # quiz во второй секции
            while count_mg_2 < 3:
                try:
                    mg_q_btn = driver.find_element(by=By.XPATH, value='(//*[@id="mquiz-btn"])[2]')
                    actions.click(mg_q_btn).perform()
                    mg_q = driver.find_element(by=By.XPATH, value='//iframe[@class="marquiz__frame marquiz__frame_open"]')
                    driver.switch_to.frame(mg_q)
                    mg_elem = wait(driver,20).until(EC.visibility_of_element_located((By.XPATH, '//button[text()[contains(., "Настроить фильтр")]]')))
                    if mg_elem.is_displayed():
                        driver.switch_to.default_content()
                        driver.find_element(by=By.XPATH, value="//button[@id='marquiz__close']").click()
                        print('     OK: квиз')
                        count_mg_2 = 3
                except:
                    count_mg_2 += 1
                    if count_mg_2 == 3:
                        print('ERROR: не отображается содержимое квиза в "МГ - это"')
                    else:
                        driver.refresh()
            count_mg_3 = 0 # модалка в 5-й секции
            while count_mg_3 < 3:
                try:
                    mg_mod_btn = wait(driver,20).until(EC.visibility_of_element_located((By.XPATH, '//*[@href="#modal-descr-consult"]')))
                    actions.click(mg_mod_btn).perform()
                    mg_input = wait(driver,20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '#modal-descr-consult #consultationform-name')))
                    if mg_input.is_displayed():
                        driver.find_element(by=By.CSS_SELECTOR, value='#modal-descr-consult>div>div>button').click()
                        count_mg_3 = 3
                        print('     OK: модалка в секции 5')
                except:
                    count_mg_3 += 1
                    if count_mg_3 == 3:
                        print('ERROR: не отображается содержимое модалки в "МГ - это"')
                    else:
                        driver.refresh()
    except:
        count_mg_1 += 1
        if count_mg_1 == 3:
            print('ERROR: не отображается видео в блоке "Проект МГ - это"')
        else:
            driver.refresh()

# блок "Господдержка" - фото в 1-й карточке / видео во 2-й карточке
count_g_1 = 0
while count_g_1 < 3:
    try: # фото
        g_title = driver.find_element(by=By.XPATH, value='//h1[text()[contains(., "Государственная поддержка")]]')
        actions.move_to_element(g_title).perform()
        assert EC.visibility_of_element_located((By.XPATH, '(//h1[text()[contains(., "Государственная поддержка")]]/parent::div//img)[1]'))
        print('   OK: 1-е фото в "Господдержке"')
        count_g_1 = 3
        count_g_2 = 0 # видео
        while count_g_2 < 3:
            try:
                g_2rd_dot = driver.find_element(by=By.XPATH, value='(//h1[text()[contains(., "Государственная поддержка")]]/parent::div//li)[2]')
                g_2rd_dot.click()
                time.sleep(3)
                g_video_btn = driver.find_element(by=By.XPATH, value='(//h1[text()[contains(., "Государственная поддержка")]]/parent::div//*[@data-src="/img/play.svg"])[1]')
                g_video_btn.click()
                g_video_iframe = driver.find_element(by=By.XPATH, value='//iframe[@class="uk-lightbox-iframe"]')
                driver.switch_to.frame(g_video_iframe)
                g_video = wait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, '//a[text()[contains(., "Вячеслав Фетисов")]]')))
                driver.switch_to.default_content()
                lb_btn = driver.find_element(by=By.CSS_SELECTOR, value = '.uk-lightbox.uk-overflow-hidden.uk-lightbox-panel.uk-open button')
                lightbox = driver.find_element(by=By.XPATH, value='//*[@class="uk-lightbox uk-overflow-hidden uk-lightbox-panel uk-open"]')
                driver.execute_script("arguments[0].setAttribute('class','uk-lightbox uk-overflow-hidden uk-lightbox-panel uk-open uk-active uk-transition-active')", lightbox)
                lb_btn.click()
                print('     OK: видео')
                count_g_3 = 3
                break
            except:
                count_g_2 += 1
                if count_g_2 == 3:
                    print('ERROR: не отображается видео')
                else:
                    driver.refresh()
    except:
        count_g_1 += 1
        if count_g_1 == 3:
            print('ERROR: не отображается фото в "Господдержке"')
        else:
            driver.refresh()

# блок "Премьера фильма" - видео
count_pm_1 = 0
while count_pm_1 < 3:
    try:
        pm_btn = driver.find_element(by=By.CSS_SELECTOR, value='#tour img')
        actions.move_to_element(pm_btn).perform()
        pm_btn.click()
        pm_video = driver.find_element(by=By.XPATH, value='//iframe[@class="uk-lightbox-iframe"]')
        driver.switch_to.frame(pm_video)
        assert EC.visibility_of_element_located((By.XPATH, '//a[text()[contains(., "«ВРЕМЯ ЖИТЬ»")]]'))
        driver.switch_to.default_content()
        lb_btn = driver.find_element(by=By.CSS_SELECTOR, value = '.uk-lightbox.uk-overflow-hidden.uk-lightbox-panel.uk-open button')
        lightbox = driver.find_element(by=By.XPATH, value='//*[@class="uk-lightbox uk-overflow-hidden uk-lightbox-panel uk-open"]')
        driver.execute_script("arguments[0].setAttribute('class','uk-lightbox uk-overflow-hidden uk-lightbox-panel uk-open uk-active uk-transition-active')", lightbox)
        lb_btn.click()
        count_pm_2 = 3
        print('   OK: видео в "Премьере фильма"')
        break
    except:
        count_pm_2 += 1
        if count_pm_2 == 3:
            print('ERROR: не отображается видео в "Премьере фильма"')
        else:
            driver.refresh()

# блок "Награды проекта" - 1-я карточка / модалка / дотсы
count_re_1 = 0
while count_re_1 < 3:
    try: # 1-я карточка
        re_title = driver.find_element(by=By.XPATH, value='(//*[text()[contains(., "Награды проекта")]])[2]')
        actions.move_to_element(re_title).perform()
        assert EC.visibility_of_element_located((By.XPATH, '((//*[text()[contains(., "Награды проекта")]])[2]/parent::div//img)[1]'))
        print('   OK: 1-я карточка в "Наградах проекта"')
        count_re_1 = 3
        count_re_2 = 0 # модалка
        while count_re_2 < 3:
            try:
                driver.find_element(by=By.XPATH, value='(//*[text()[contains(., "Награды проекта")]]/parent::div//img)[1]').click()
                assert EC.visibility_of_element_located((By.XPATH, '//div[@class="uk-modal-container js-news-view-modal uk-modal uk-open"]//div[@class="uk-padding uk-article js-news-view-modal-content"]'))
                driver.find_element(by=By.XPATH, value='//div[@class="uk-modal-container js-news-view-modal uk-modal uk-open"]/div/button').click()
                print('     OK: модалка новости')
                count_re_2 = 3
            except:
                count_re_2 += 1
                if count_re_2 == 3:
                    print('ERROR: не отображается модалка новости')
                else:
                    driver.refresh()
        count_re_3 = 0 # дотсы
        while count_re_3 < 3:
            try:
                assert EC.visibility_of_element_located((By.XPATH, '((//*[text()[contains(., "Награды проекта")]])[2]/parent::div//ul/li)[1]'))
                print('     OK: дотсы')
                count_re_3 = 3
                break
            except:
                count_re_3 += 1
                if count_re_3 == 3:
                    print('ERROR: не отображаются дотсы в "Наградах проекта"')
                else:
                    driver.refresh()
    except:
        count_re_1 += 1
        if count_re_1 == 3:
            print('ERROR: не отображается 1-я карточка в "Наградах проекта"')
        else:
            driver.refresh()

# "Специальная цена" - 1-я карточка / количество карточек / переход в каталог
count_so_1 = 0
while count_so_1 < 3:
    try:
        so_title = driver.find_element(by=By.XPATH, value='//*[text()[contains(., "Специальная цена")]]')
        actions.move_to_element(so_title).perform()
        time.sleep(1)
        so_card = driver.find_element(by=By.XPATH, value='(//*[(contains(@class, "sow-special-offer-item"))])[1]')
        if so_title.is_displayed():
            print('   OK: 1-я карточка в блоке "Специальная цена"')
            count_so_1 = 3
            count_so_2 = 0 # количество карточек
            while count_so_2 < 3:
                try:
                    so_count = len(driver.find_elements(by=By.XPATH, value='//*[@id="catalogueSpecial"]/div/div/div/div/ul/li'))
                    if so_count == 6:
                        count_so_2 = 3
                        print('     OK: количество карточек в СП = 6')
                        break
                except:
                    count_so_2 += 1
                    if count_so_2 == 3:
                        print('ERROR: количество карточек в СП не равно 6')
                    else:
                        driver.refresh()
            count_so_3 = 0
            while count_so_3 < 3:
                try:
                    so_btn = driver.find_element(by=By.XPATH, value='//*[@id="catalogueSpecial"]//*[@class="uk-text-center"]/a')
                    so_btn.click()
                    cat_title = driver.find_element(By.XPATH, value='//h2[text()="Подобрать участок"]')
                    if cat_title.is_displayed():
                        driver.execute_script("window.history.go(-1)")
                        count_so_3 = 3
                        print('     OK: из "Спеццены" выполняется переход в каталог')
                        break
                except:
                    count_so_3 += 1
                    if count_so_3 == 3:
                        print('ERROR: из "Спеццены" не выполняется переход в каталог')
                        driver.get("https://moigektar.ru")
                    else:
                        driver.refresh()
    except:
        count_so_1 += 1
        if count_so_1 == 3:
            print('ERROR: не отображаются карточки в блоке "Специальная цена"')
        else:
            driver.refresh()

# форма со Снежанной 1-я - поле ввода / кнопка / фото
count_sf_1 = 0
while count_sf_1 < 3:
    try:
        assert EC.visibility_of_element_located((By.XPATH, '(//*[(contains(@class, "snezh"))]//*[@id="consultationform-name"])[1]'))
        count_sf_1 = 3
        print('   OK: поле ввода в 1-й форме со Снежанной')
        count_sf_2 = 0 # кнопка
        while count_sf_2 < 3:
            try:
                assert EC.visibility_of_element_located((By.XPATH, '(//*[(contains(@class, "snezh"))]//button)[1]'))
                count_sf_2 = 3
                print('     OK: кнопка в форме')
                break
            except:
                count_sf_2 += 1
                if count_sf_2 == 3:
                    print('ERROR: не отображается кнопка в форме со Снежанной')
                else:
                    driver.refresh()
        count_sf_3 = 0 # фото
        while count_sf_3 < 3:
            try:
                assert EC.visibility_of_element_located((By.XPATH, '(//*[@data-src="/img/form/snezhana.png"])[1]'))
                count_sf_3 = 3
                print('     OK: отображается фото')
                break
            except:
                count_sf_3 += 1
                if count_sf_3 == 3:
                    print('ERROR: не отображается фото в форме со Снежанной')
                else:
                    driver.refresh()
    except:
        count_sf_1 += 1
        if count_sf_1 == 3:
            print('ERROR: не отображается поле ввода в 1-й форме со Снежанной')
        else:
            driver.refresh()

# форма со Снежанной 2-я - поле ввода / кнопка / фото
count_sf_1 = 0
while count_sf_1 < 3:
    try:
        assert EC.visibility_of_element_located((By.XPATH, '(//*[(contains(@class, "snezh"))]//*[@id="consultationform-name"])[2]'))
        count_sf_1 = 3
        print('   OK: поле ввода во 2-й форме со Снежанной')
        count_sf_2 = 0 # кнопка
        while count_sf_2 < 3:
            try:
                assert EC.visibility_of_element_located((By.XPATH, '(//*[(contains(@class, "snezh"))]//button)[3]'))
                count_sf_2 = 3
                print('     OK: кнопка в форме')
                break
            except:
                count_sf_2 += 1
                if count_sf_2 == 3:
                    print('ERROR: не отображается кнопка в форме со Снежанной')
                else:
                    driver.refresh()
        count_sf_3 = 0 # фото
        while count_sf_3 < 3:
            try:
                assert EC.visibility_of_element_located((By.XPATH, '(//*[@data-src="/img/form/snezhana.png"])[2]'))
                count_sf_3 = 3
                print('     OK: отображается фото')
                break
            except:
                count_sf_3 += 1
                if count_sf_3 == 3:
                    print('ERROR: не отображается фото в форме со Снежанной')
                else:
                    driver.refresh()
    except:
        count_sf_1 += 1
        if count_sf_1 == 3:
            print('ERROR: не отображается поле ввода во 2-й форме со Снежанной')
        else:
            driver.refresh()

# блок "Лучшее время для покупки"  - 1-я карточка / запуск квиза
count_bt_1 = 0
while count_bt_1 < 3:
    try: # 1-я карточка
        bt_title = driver.find_element(by=By.XPATH, value='//*[text()[contains(., "Лучшее время")]]')
        actions.move_to_element(bt_title).perform()
        assert EC.visibility_of_element_located((By.XPATH, '(//*[text()[contains(., "Лучшее время")]]/parent::div//ul/li)[1]'))
        print('   OK: отображается 1-я карточка в "Лучшее время ..."')
        count_bt_1 = 3
        count_bt_2 = 0 # запуск квиза
        while count_bt_2 < 3:
            try:
                bt_btn = driver.find_element(by=By.XPATH, value='//*[text()[contains(., "Лучшее время")]]/parent::div//*[text()[contains(., "Подобрать участок")]]')
                actions.click(bt_btn).perform()
                bt_iframe = driver.find_element(by=By.XPATH, value="//iframe[@class='marquiz__frame marquiz__frame_open']")
                driver.switch_to.frame(bt_iframe)
                bt_quiz = wait(driver,20).until(EC.visibility_of_element_located((By.XPATH, '//button[text()[contains(., "Настроить фильтр")]]')))
                if bt_quiz:
                    driver.switch_to.default_content()
                    driver.find_element(by=By.XPATH, value="//button[@id='marquiz__close']").click()
                    print('     OK: запустился квиз')
                    count_bt_2 = 3
                    break
            except:
                count_bt_2 += 1
                if count_bt_2 == 3:
                    print('ERROR: не запустился квиз')
                else:
                    driver.refresh()
    except:
        count_bt_1 += 1
        if count_bt_1 == 3:
            print('ERROR: не отображается 1-я карточка в "Лучшее время ..."')
        else:
            driver.refresh()

# блок "Виртуальный тур" - тур запустился
count_t_1 = 0
while count_t_1 < 3:
    try:
        t_title = driver.find_element(by=By.XPATH, value='//*[text()[contains(., "Виртуальный тур")]]')
        actions.move_to_element(t_title).perform()
        btn = driver.find_element(by=By.XPATH, value='//*[(contains(@class, "w-select__tour-icon"))]')
        actions.click(btn).perform()
        iframe = driver.find_element(by=By.XPATH, value='//iframe[@class="embed-responsive-item"]')
        driver.switch_to.frame(iframe)
        elem = wait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, "//div[(contains(@style, 'z-index: 231'))]")))
        if elem:
            print('   OK: запустился Виртур')
            driver.refresh()
            count_t_1 = 3
            break
    except:
        count_t_1 += 1
        if count_t_1 == 3:
            driver.refresh()
            print('ERROR: не запустился Виртур')
        else:
            driver.refresh()

# "Новости развития посёлков" - 1-я карточка / модалка
count_n_1 = 0
while count_n_1 < 3:
    try:
        title = driver.find_element(by=By.XPATH, value='(//*[text()[contains(., "Новости развития поселков")]])[1]')
        actions.move_to_element(title).perform()
        time.sleep(1)
        card = driver.find_element(by=By.XPATH, value='(//*[@class="w-news-wrapper"]//*[(contains(@class, "uk-background-cover uk-width-1-1"))])[1]')
        if card.is_displayed():
            count_n_1 = 3
            print('   OK: 1-я карточка в "Новости развития поселков"')
            count_n_2 = 0
            while count_n_2 < 3:
                try:
                    actions.click(card).perform()
                    heading = wait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, '//*[@class="uk-modal-container js-news-view-modal uk-modal uk-open"]//div[@class="uk-padding uk-article js-news-view-modal-content"]')))
                    if heading:
                        driver.find_element(By.XPATH, value='//*[@class="uk-modal-container js-news-view-modal uk-modal uk-open"]//div[@class="uk-padding uk-article js-news-view-modal-content"]/parent::div/button').click()
                        print('     OK: модалка новости')
                        break
                except:
                    count_n_2 += 1
                    if count_n_2 == 3:
                        print('ERROR: не отображается модалка новости в блоке "Новости развития поселков"')
                    else:
                        driver.refresh()
    except:
        count_n_1 += 1
        if count_n_1 == 3:
            print('ERROR: не отображается карточка в "Новости развития поселков"')
        else:
            driver.refresh()

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

# блок "Сми о проекте" - 1-я карточка / модалка / "Показать еще"
count_smi_1 = 0
while count_smi_1 < 3:
    try: # 1-я карточка
        smi_title = driver.find_element(by=By.XPATH, value='(//*[text()[contains(., "СМИ о проекте")]])[3]')
        actions.move_to_element(smi_title).perform()
        assert EC.visibility_of_element_located((By.XPATH, '((//*[text()[contains(., "СМИ о проекте")]])[3]/parent::div//img)[1]'))
        print('   OK: 1-я карточка в "Сми о проекте"')
        count_smi_1 = 3
        count_smi_2 = 0 # модалка
        while count_smi_2 < 3:
            try:
                driver.find_element(by=By.XPATH, value='((//*[text()[contains(., "СМИ о проекте")]])[3]/parent::div//img)[1]').click()
                assert EC.visibility_of_element_located((By.XPATH, '//div[@class="uk-modal-container js-news-view-modal uk-modal uk-open"]//div[@class="uk-padding uk-article js-news-view-modal-content"]'))
                driver.find_element(by=By.XPATH, value='//div[@class="uk-modal-container js-news-view-modal uk-modal uk-open"]/div/button').click()
                print('     OK: модалка новости')
                count_smi_2 = 3
                break
            except:
                count_smi_2 += 1
                if count_smi_2 == 3:
                    print('ERROR: не отображается модалка новости')
                else:
                    driver.refresh()
        count_smi_3 = 0 # "Показать еще" и 5-я карточка"
        while count_smi_3 < 3:
            try:
                smi_btn = driver.find_element(by=By.XPATH, value='(//*[text()[contains(., "СМИ о проекте")]])[3]/parent::div//*[text()[contains(., "Показать еще")]]')
                smi_btn.click()
                smi_6th_card = driver.find_element(by=By.XPATH, value='((//*[text()[contains(., "СМИ о проекте")]])[3]/parent::div//a)[6]')
                smi_6th_card.click()
                driver.find_element(by=By.XPATH, value='//div[@class="uk-modal-container js-news-view-modal uk-modal uk-open"]/div/button').click()
                print('     OK: если нажать "Показать еще" - видны остальные карточки')
                count_smi_3 = 3
                break
            except:
                count_smi_3 += 1
                if count_smi_3 == 3:
                    print('ERROR: если нажать "Показать еще" - не видны остальные карточки')
                else:
                    driver.refresh()
    except:
        count_smi_1 += 1
        if count_smi_1 == 3:
            print('ERROR: не отображается 1-я карточка в "Сми о проекте"')
        else:
            driver.refresh()

# блок "Гектар под ваши цели" - 1-я карточка / кнопка "Показать еще"
count_gg_1 = 0
while count_gg_1 < 3:
    try:
        gg_title = wait(driver,14).until(EC.presence_of_element_located((By.XPATH, '//*[text()="Гектар под ваши цели"]')))
        actions.move_to_element(gg_title).perform()
        gg_card = driver.find_element(by=By.XPATH, value='(//*[@id="w-goals"]//li)[1]')
        if gg_card.is_displayed():
            count_gg_1 = 3
            print('   OK: 1-я карточка в "Гектар под ваши цели"')
            count_gg_2 = 0 # кнопка "Показать еще"
            while count_gg_2 < 3:
                try:
                    gg_btn = driver.find_element(by=By.XPATH, value='//*[@id="w-goals"]//a[text()="Показать еще"]')
                    if gg_btn.is_displayed():
                        count_gg_2 = 3
                        print('     OK: кнопка')
                        break
                except:
                    count_gg_2 += 1
                    if count_gg_2 == 3:
                        print('ERROR: не отображается кнопка кнопка в "Гектар под ваши цели"')
                    else:
                        driver.refresh()
    except:
        count_gg_1 += 1
        if count_gg_1 == 3:
            print('ERROR: не отображается 1-я карточка в "Гектар под ваши цели"')
        else:
            driver.refresh()

# блок "Успешные кейсы" - фото / видео / модалка / переключение кейсов
count_sc_1 = 0
while count_sc_1 < 3:
    try: # 1-е фото
        sc_title = driver.find_element(by=By.XPATH, value='//*[text()[contains(., "Успешные кейсы")]]')
        actions.move_to_element(sc_title).perform()
        assert EC.visibility_of_element_located((By.XPATH, '(//*[@id="best-example"]//img[(contains(@class, "uk-visible@s"))])[1]'))
        print('   OK: блок "Успешные кейсы ..." фото в 1-м кейсе')
        count_sc_1 = 3
        count_sc_2 = 0 # видео
        while count_sc_2 < 3:
            try:
                sc_v_btn = driver.find_element(by=By.XPATH, value='(//*[@id="best-example"]//*[@data-type="iframe"]//img[(contains(@class, "w-best-example-icon-play"))])[1]')
                actions.move_to_element(sc_v_btn).perform()
                sc_v_btn.click()
                sc_video = driver.find_element(by=By.XPATH, value='//iframe[@class="uk-lightbox-iframe"]')
                driver.switch_to.frame(sc_video)
                assert EC.visibility_of_element_located((By.XPATH, '//a[text()[contains(., "«Только земля спасет»")]]'))
                driver.switch_to.default_content()
                lb_btn = driver.find_element(by=By.CSS_SELECTOR, value = '.uk-lightbox.uk-overflow-hidden.uk-lightbox-panel.uk-open button')
                lightbox = driver.find_element(by=By.XPATH, value='//*[@class="uk-lightbox uk-overflow-hidden uk-lightbox-panel uk-open"]')
                driver.execute_script("arguments[0].setAttribute('class','uk-lightbox uk-overflow-hidden uk-lightbox-panel uk-open uk-active uk-transition-active')", lightbox)
                lb_btn.click()
                count_sc_2 = 3
                print('     OK: 1-е видео')
                break
            except:
                count_sc_2 += 1
                if count_sc_2 == 3:
                    print('ERROR: не отображается 1-е видео в кейсах')
                else:
                    driver.refresh()
        count_sc_3 = 0 # модалка
        while count_sc_3 < 3:
            try:
                sc_m_btn = driver.find_element(by=By.XPATH, value='//a[@data-id="7194"]')
                sc_m_btn.click()
                assert EC.visibility_of_element_located((By.XPATH, '(//*[text()[contains(., "Кейс проекта «Мой гектар»:")]])[3]'))
                driver.find_element(By.XPATH, value='//*[@class="uk-modal-container js-news-view-modal uk-modal uk-open"]/div/button').click()
                print('     OK: модалка')
                count_sc_3 = 3
                break
            except:
                count_sc_3 += 1
                if count_sc_3 == 3:
                    print('ERROR: не отображается модалка в "Кейсах"')
                else:
                    driver.refresh()
        count_sc_4 = 0 # переключение на 2-й кейс
        while count_sc_4 < 3:
            try:
                sc_2_btn = driver.find_element(by=By.XPATH, value='//div[text()="Усадьба в Завидово"]')
                sc_2_btn.click()
                assert EC.visibility_of_element_located((By.XPATH, '//div[text()="Никита Лович"]'))
                assert EC.visibility_of_element_located((By.XPATH, '//div[text()="Никита Лович"]'))
                print('     OK: выполнено переключение на 2-й кейс')
                count_sc_4 = 3
                break
            except:
                count_sc_4 += 1
                if count_sc_4 == 3:
                    print('ERROR: не выполнено переключение на 2-й кейс в "Кейсах"')
                else:
                    driver.refresh()
    except:
        count_sc_1 += 1
        if count_sc_1 == 3:
            print('ERROR: не отображается фото в "Успешных кейсах')
        else:
            driver.refresh()

# блок "Лучшие поселки ..."
# фото / кнопка "Еще"
count_bv_1 = 0
while count_bv_1 < 3:
    try: # 1-е фото
        bv_title = driver.find_element(by=By.XPATH, value='//*[text()[contains(., "Лучшие поселки")]]')
        actions.move_to_element(bv_title).perform()
        assert EC.visibility_of_element_located((By.XPATH, '(//*[@id="w-descr-catalog"]//*[(contains(@class, "uk-background-cover"))])[1]'))
        print('   OK: "Лучшие поселки", фото в 1-й секции')
        count_bv_1 = 3
        count_bv_2 = 0 # кнопка "Показать еще"
        while count_bv_2 < 3:
            try:
                bv_btn = driver.find_element(by=By.XPATH, value='//*[@id="w-descr-catalog"]//*[text()[contains(., "Показать")]]')
                bv_btn.click()
                bv_3rd_elem = driver.find_element(by=By.XPATH, value='(//*[@id="w-descr-catalog"]//*[(contains(@class, "w-descr__list-item__title-catalog"))])[3]')
                bv_3rd_elem.click()
                # Тут не получается использовать element_to_be_clickable: по какой-то причине драйвер считает,
                # что элемент кликабельный, когда секция ещё не раскрыта - хотя на самом деле нажать на элемент нельзя.
                # Поэтому пришлось проверять с помощью прямого нажатия
                count_bv_2 = 3
                print('     OK: после нажатия на "Показать ещё" видна скрытая ранее секция')
                break
            except:
                count_bv_2 += 1
                if count_bv_2 == 3:
                    print('ERROR: после нажатия на "Показать ещё" не видна скрытая секция')
                else:
                    driver.refresh()
    except:
        count_bv_1 += 1
        if count_bv_1 == 3:
            print('ERROR: не отображается фото в 1-й секции')
        else:
            driver.refresh()

# блок "Отзывы о проекте" - 1-я карточка / видео / дотсы / переход на стр. отзывов
count_rew_1 = 0
while count_rew_1 < 3:
    try: # 1-я карточка
        rew_title = driver.find_element(by=By.XPATH, value='(//*[text()[contains(., "Отзывы о проекте")]])[2]')
        actions.move_to_element(rew_title).perform()
        assert EC.visibility_of_element_located((By.XPATH, '((//*[text()[contains(., "Отзывы о проекте")]])[2]/parent::div//ul/li)[1]'))
        print('   OK: 1-я карточка "Отзывов"')
        count_rew_1 = 3
        count_rew_2 = 0 # видео
        while count_rew_2 < 3:
            try:
                driver.find_element(by=By.XPATH, value='((//*[text()[contains(., "Отзывы о проекте")]])[2]/parent::div//ul/li)[1]').click()
                rew_video = driver.find_element(by=By.XPATH, value='//iframe[@class="uk-lightbox-iframe"]')
                driver.switch_to.frame(rew_video)
                rew_video_title = driver.find_element(by=By.CSS_SELECTOR, value='#player a.ytp-title-link')
                if rew_video_title.is_displayed():
                    driver.switch_to.default_content()
                    lb_btn = driver.find_element(by=By.CSS_SELECTOR, value = '.uk-lightbox.uk-overflow-hidden.uk-lightbox-panel.uk-open button')
                    lightbox = driver.find_element(by=By.XPATH, value='//*[@class="uk-lightbox uk-overflow-hidden uk-lightbox-panel uk-open"]')
                    driver.execute_script("arguments[0].setAttribute('class','uk-lightbox uk-overflow-hidden uk-lightbox-panel uk-open uk-active uk-transition-active')", lightbox)
                    lb_btn.click()
                    count_rew_3 = 3
                    print('   OK: видео в 1-й карточке')
                    break
            except:
                driver.refresh()
                count_rew_2 += 1
                if count_rew_2 == 3:
                    print('ERROR: не отображается видео в 1-й карточке')
                else:
                    driver.refresh()
        count_rew_3 = 0 # дотсы
        while count_rew_3 < 3:
            try:
                assert EC.visibility_of_element_located((By.XPATH, '(//*[text()[contains(., "Отзывы о проекте")]])[2]/parent::div//*[(contains(@class, "uk-dotnav"))]'))
                print('     OK: дотсы')
                count_rew_3 = 3
                break
            except:
                count_rew_3 += 1
                if count_rew_3 == 3:
                    print('ERROR: не отображаются дотсы')
                else:
                    driver.refresh()
        count_rew_4 = 0 # переход на стр. отзывов
        while count_rew_4 < 3:
            try:
                main_window = driver.current_window_handle
                driver.find_element(by=By.XPATH, value='(//*[text()[contains(., "Отзывы о проекте")]])[2]/parent::div/div/a').click()
                driver.switch_to.window(driver.window_handles[1])
                rew_url = driver.current_url
                assert rew_url == 'https://moigektar.ru/about/reviews'
                driver.close()
                driver.switch_to.window(main_window)
                print('     OK: выполнен переход на стр. отзывов')
                count_rew_4 = 3
                break
            except:
                count_rew_4 += 1
                if count_rew_4 == 3:
                    driver.get("https://moigektar.ru")
                    print('ERROR: не выполнен переход на стр. отзывов')
                else:
                    driver.refresh()
    except:
        count_rew_1 += 1
        if count_rew_1 == 3:
            print('ERROR: не отображается 1-я карточка')
        else:
            driver.refresh()

# Популярные вопросы / видео / квиз
count_pq_1 = 0
while count_pq_1 < 3:
    try:
        pq_title = driver.find_element(by=By.XPATH, value='//*[text()[contains(., "Популярные вопросы:")]]')
        actions.move_to_element(pq_title).perform()
        main_window = driver.current_window_handle
        pq_video_btn = driver.find_element(by=By.XPATH, value='(//a[@href="https://youtu.be/CsLAIx9EM1k/"])[1]')
        pq_video_btn.click()
        driver.switch_to.window(driver.window_handles[1])
        time.sleep(3)
        pq_url = driver.current_url
        assert pq_url == 'https://www.youtube.com/watch?v=CsLAIx9EM1k'
        driver.close()
        driver.switch_to.window(main_window)
        count_pq_1 = 3
        print('   OK: из "Популярных вопросов" выполнен переход на стр. с видео о законах')
        count_pq_2 = 0 # quiz
        while count_pq_2 < 3:
            try:
                last_q = driver.find_element(by=By.ID, value='uk-accordion-263')
                last_q.click()
                time.sleep(3)
                pq_q_btn = driver.find_element(by=By.XPATH, value='(//*[@class="w-faq"]//a[(contains(@class, "uk-button-danger"))])[1]')
                actions.click(pq_q_btn).perform()
                m_iframe = driver.find_element(by=By.XPATH, value='//iframe[@class="marquiz__frame marquiz__frame_open"]')
                driver.switch_to.frame(m_iframe)
                pq_title_q = wait(driver,20).until(EC.visibility_of_element_located((By.XPATH, '//button[text()[contains(., "Настроить фильтр")]]')))
                if pq_title_q:
                    driver.switch_to.default_content()
                    driver.find_element(by=By.XPATH, value="//button[@id='marquiz__close']").click()
                    print('     OK: квиз')
                    break
            except:
                count_pq_2 += 1
                if count_pq_2 == 3:
                    print('ERROR: не отображается квиз в "Популярных вопросах"')
                else:
                    driver.refresh()
    except:
        count_pq_1 += 1
        if count_pq_1 == 3:
            print('ERROR: не выполнен переход на стр. с видео о законах')
            driver.get("https://moigektar.ru")
        else:
            driver.refresh()
            pq_url = driver.current_url
            assert pq_url == 'https://www.youtube.com/watch?v=CsLAIx9EM1k'
            driver.close()
            driver.switch_to.window(main_window)

# "Видео, которые вам ..." - 1-я карточка / видео / дотсы
count_vw_1 = 0
while count_vw_1 < 3:
    try:
        vw_title = driver.find_element(by=By.XPATH, value='//*[text()[contains(., "Видео, которые")]]')
        actions.move_to_element(vw_title).perform()
        assert EC.visibility_of_element_located((By.XPATH, '(//*[@id="b-video"]//*[@class="uk-object-cover"])[1]'))
        count_vw_1 = 3
        print('   OK: 1-я карточка в "Видео, которые вам ..."')
        count_vw_2 = 0 # видео
        while count_vw_2 < 3:
            try:
                driver.find_element(by=By.XPATH, value='(//*[@id="b-video"]//*[@class="uk-object-cover"])[1]').click()
                vw_video = driver.find_element(by=By.XPATH, value='//iframe[@class="uk-lightbox-iframe"]')
                driver.switch_to.frame(vw_video)
                vw_video_title = driver.find_element(by=By.CSS_SELECTOR, value='#player a.ytp-title-link')
                if vw_video_title.is_displayed():
                    driver.switch_to.default_content()
                    lb_btn = driver.find_element(by=By.CSS_SELECTOR, value = '.uk-lightbox.uk-overflow-hidden.uk-lightbox-panel.uk-open button')
                    lightbox = driver.find_element(by=By.XPATH, value='//*[@class="uk-lightbox uk-overflow-hidden uk-lightbox-panel uk-open"]')
                    driver.execute_script("arguments[0].setAttribute('class','uk-lightbox uk-overflow-hidden uk-lightbox-panel uk-open uk-active uk-transition-active')", lightbox)
                    lb_btn.click()
                    count_vw_2 = 3
                    print('     OK: видео в 1-й карточке')
                    break
            except:
                driver.refresh()
                count_vw_2 += 1
                if count_vw_2 == 3:
                    print('ERROR: не отображается видео в 1-й карточке')
                else:
                    driver.refresh()
        count_vw_3 = 0 # дотсы
        while count_vw_3 < 3:
            try:
                assert EC.visibility_of_element_located((By.XPATH, '(//*[@id="b-video"]//*[(contains(@class, "uk-dotnav"))]/li)[1]'))
                count_vw_3 = 3
                print('     OK: дотсы')
                break
            except:
                count_vw_3 += 1
                if count_vw_3 == 3:
                    print('ERROR: не отображаются дотсы в "Видео, которые вам ..."')
                else:
                    driver.refresh()
    except:
        count_vw_1 += 1
        if count_vw_1 == 3:
            print('ERROR: не отображается 1-я карточка в "Видео, которые вам ..."')
        else:
            driver.refresh()

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

# форма со Снежанной 3-я - поле ввода / кнопка / фото
count_sf_1 = 0
while count_sf_1 < 3:
    try:
        assert EC.visibility_of_element_located((By.XPATH, '(//*[(contains(@class, "snezh"))]//*[@id="consultationform-name"])[3]'))
        count_sf_1 = 3
        print('   OK: поле ввода в 3-й форме со Снежанной')
        count_sf_2 = 0 # кнопка
        while count_sf_2 < 3:
            try:
                assert EC.visibility_of_element_located((By.XPATH, '(//*[(contains(@class, "snezh"))]//button)[5]'))
                count_sf_2 = 3
                print('     OK: кнопка в форме')
                break
            except:
                count_sf_2 += 1
                if count_sf_2 == 3:
                    print('ERROR: не отображается кнопка в форме со Снежанной')
                else:
                    driver.refresh()
        count_sf_3 = 0 # фото
        while count_sf_3 < 3:
            try:
                assert EC.visibility_of_element_located((By.XPATH, '(//*[@data-src="/img/form/snezhana.png"])[3]'))
                count_sf_3 = 3
                print('     OK: отображается фото')
                break
            except:
                count_sf_3 += 1
                if count_sf_3 == 3:
                    print('ERROR: не отображается фото в форме со Снежанной')
                else:
                    driver.refresh()
    except:
        count_sf_1 += 1
        if count_sf_1 == 3:
            print('ERROR: не отображается поле ввода в 3-й форме со Снежанной')
        else:
            driver.refresh()

# 2. Каталог посёлков
# driver.get('https://moigektar.ru/catalogue')
# print("Каталог поселков")





time.sleep(1)
driver.quit()

