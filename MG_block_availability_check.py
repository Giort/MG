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
#driver.get("https://moigektar.ru")
driver.get("https://moigektar.ru" + str(data['mg_loc']['mg_cur_release_1']))
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
        header_q_btn = driver.find_element(by=By.XPATH, value='(//*[@id="mquiz-btn"])[1]')
        actions.click(header_q_btn).perform()
        m_iframe = driver.find_element(by=By.XPATH, value="//iframe[@class='marquiz__frame marquiz__frame_open']")
        driver.switch_to.frame(m_iframe)
        header_quiz = wait(driver,20).until(EC.visibility_of_element_located((By.XPATH, '//button[text()[contains(., "Настроить фильтр")]]')))
        if header_quiz:
            driver.switch_to.default_content()
            driver.find_element(by=By.XPATH, value="//button[@id='marquiz__close']").click()
            print('   OK: хедер и квиз в нём')
            count_h_1 = 3
    except:
        count_h_1 += 1
        if count_h_1 == 3:
            print('ERROR: что-то не так в хедере')
        else:
            driver.refresh()

# 1-й экран - картинка / квиз
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
    except:
        count_f_1 += 1
        if count_f_1 == 3:
            print('ERROR: не отображается бэкграунд на 1-м экране')
        else:
            driver.refresh()

# блок "Описание проекта "МГ"" - квиз
count_mg_1 = 0
while count_mg_1 < 3:
    try:
        mg_q_btn = driver.find_element(by=By.XPATH, value='(//*[@id="mquiz-btn"])[2]')
        actions.move_to_element(mg_q_btn).perform()
        actions.send_keys(Keys.ARROW_DOWN).perform()
        actions.click(mg_q_btn).perform()
        mg_q = driver.find_element(by=By.XPATH, value='//iframe[@class="marquiz__frame marquiz__frame_open"]')
        driver.switch_to.frame(mg_q)
        mg_elem = wait(driver,20).until(EC.visibility_of_element_located((By.XPATH, '//button[text()[contains(., "Настроить фильтр")]]')))
        if mg_elem.is_displayed():
            driver.switch_to.default_content()
            driver.find_element(by=By.XPATH, value='//button[@id="marquiz__close"]').click()
            print('   OK: квиз в блоке "Описание проекта"')
            count_mg_1 = 3
    except:
        count_mg_1 += 1
        if count_mg_1 == 3:
            print('ERROR: не отображается содержимое квиза в блоке "Описание проекта"')
        else:
            driver.refresh()

# блок "Господдержка" - фото в 1-й карточке / видео во 2-й карточке
count_g_1 = 0
while count_g_1 < 3:
    try: # фото
        g_title = driver.find_element(by=By.XPATH, value='//h2[text()[contains(., "Государственная поддержка")]]')
        actions.move_to_element(g_title).perform()
        assert EC.visibility_of_element_located((By.XPATH, '(//h2[text()[contains(., "Государственная поддержка")]]/parent::div//img)[1]'))
        print('   OK: 1-е фото в "Господдержке"')
        count_g_1 = 3
    except:
        count_g_1 += 1
        if count_g_1 == 3:
            print('ERROR: не отображается фото в "Господдержке"')
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

# блок "Успешные примеры" - фото / переключение кейсов
count_sc_1 = 0
while count_sc_1 < 3:
    try: # 1-е фото
        sc_title = driver.find_element(by=By.XPATH, value='//*[text()[contains(., "Успешные примеры")]]')
        actions.move_to_element(sc_title).perform()
        assert EC.visibility_of_element_located((By.XPATH, '(//*[@id="best-example"]//img[(contains(@class, "uk-visible@s"))])[1]'))
        print('   OK: блок "Успешные примеры ..." фото в 1-м кейсе')
        count_sc_1 = 3
        count_sc_2 = 0 # переключение на 2-й кейс
        while count_sc_2 < 3:
            try:
                sc_2_btn = driver.find_element(by=By.XPATH, value='//div[text()="Усадьба в Завидово"]')
                actions.move_to_element(sc_2_btn).perform()
                actions.send_keys(Keys.PAGE_DOWN).perform()
                sc_2_btn.click()
                sc_t = driver.find_element(by=By.XPATH, value='//*[text()[contains(., "Собственник участка в поселке «Усадьба в Завидово»")]]')
                sc_t.click()
                print('     OK: выполнено переключение на 3-й кейс')
                count_sc_2 = 3
                break
            except:
                count_sc_2 += 1
                if count_sc_2 == 3:
                    print('ERROR: не выполнено переключение на 3-й кейс в "Успешных примерах"')
                else:
                    driver.refresh()
    except:
        count_sc_1 += 1
        if count_sc_1 == 3:
            print('ERROR: не отображается фото в "Успешных примерах')
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
        count_rew_2 = 0 # дотсы
        while count_rew_2 < 3:
            try:
                assert EC.visibility_of_element_located((By.XPATH, '(//*[text()[contains(., "Отзывы о проекте")]])[2]/parent::div//*[(contains(@class, "uk-dotnav"))]'))
                print('     OK: дотсы')
                count_rew_2 = 3
                break
            except:
                count_rew_2 += 1
                if count_rew_2 == 3:
                    print('ERROR: не отображаются дотсы')
                else:
                    driver.refresh()
        count_rew_3 = 0 # переход на стр. отзывов
        while count_rew_3 < 3:
            try:
                main_window = driver.current_window_handle
                driver.find_element(by=By.XPATH, value='(//*[text()[contains(., "Отзывы о проекте")]])[2]/parent::div/div/a').click()
                driver.switch_to.window(driver.window_handles[1])
                rew_url = driver.current_url
                assert rew_url == 'https://moigektar.ru/about/reviews'
                driver.close()
                driver.switch_to.window(main_window)
                print('     OK: выполнен переход на стр. отзывов')
                count_rew_3 = 3
                break
            except:
                count_rew_3 += 1
                if count_rew_3 == 3:
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
    except:
        count_gg_1 += 1
        if count_gg_1 == 3:
            print('ERROR: не отображается 1-я карточка в "Гектар под ваши цели"')
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
                    cat_title = driver.find_element(By.XPATH, value='//h4[text()="Подобрать участок"]')
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

# инлайн-форма 1-я - поле ввода / кнопка / фото
count_if_1_1 = 0
while count_if_1_1 < 3:
    try:
        f_i_1 = wait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '(//*[(contains(@class, "snezh"))]//*[@id="consultationform-phone"])[1]')))
        if f_i_1:
            count_if_1_1 = 3
            print('   OK: поле ввода в 1-й инлайн-форме')
            count_if_1_2 = 0 # кнопка
            while count_if_1_2 < 3:
                try:
                    f_b_1 = wait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '(//*[(contains(@class, "snezh"))]//button)[1]')))
                    actions.move_to_element(f_b_1).perform()
                    if f_b_1:
                        count_if_1_2 = 3
                        print('     OK: кнопка в форме')
                        break
                except:
                    count_if_1_2 += 1
                    if count_if_1_2 == 3:
                        print('ERROR: не отображается кнопка в 1-й инлайн-форме')
                    else:
                        driver.refresh()
            count_if_1_3 = 0 # фото
            while count_if_1_3 < 3:
                try:
                    f_p_1 = wait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, '(//*[@src="/img/form/arina.png"])[1]')))
                    if f_p_1:
                        count_if_1_3 = 3
                        print('     OK: отображается фото')
                        break
                except:
                    count_if_1_3 += 1
                    if count_if_1_3 == 3:
                        print('ERROR: не отображается фото в 1-й инлайн-форме')
                    else:
                        driver.refresh()
    except:
        count_if_1_1 += 1
        if count_if_1_1 == 3:
            print('ERROR: не отображается поле ввода в 1-й инлайн-форме')
        else:
            driver.refresh()

# блок "Лучшие поселки ..." - фото / кнопка "Еще"
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
            print('ERROR: не отображается фото в 1-й секции в "Лучших поселках"')
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

# инлайн-форма 2-я - поле ввода / кнопка / фото
count_if_2_1 = 0
while count_if_2_1 < 3:
    try:
        f_i_2 = wait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '(//*[(contains(@class, "snezh"))]//*[@id="consultationform-phone"])[3]')))
        if f_i_2:
            count_if_2_1 = 3
            print('   OK: поле ввода во 2-й инлайн-форме')
            count_if_2_2 = 0 # кнопка
            while count_if_2_2 < 3:
                try:
                    f_b_2 = wait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '(//*[(contains(@class, "snezh"))]//button)[4]')))
                    actions.move_to_element(f_b_2).perform()
                    if f_b_2:
                        count_if_2_2 = 3
                        print('     OK: кнопка в форме')
                        break
                except:
                    count_if_2_2 += 1
                    if count_if_2_2 == 3:
                        print('ERROR: не отображается кнопка во 2-й инлайн-форме')
                    else:
                        driver.refresh()
            count_if_2_3 = 0 # фото
            while count_if_2_3 < 3:
                try:
                    f_p_2 = wait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, '(//*[@src="/img/form/ny-andr.png"])[1]')))
                    if f_p_2:
                        count_if_2_3 = 3
                        print('     OK: отображается фото')
                        break
                except:
                    count_if_2_3 += 1
                    if count_if_2_3 == 3:
                        print('ERROR: не отображается фото во 2-й инлайн-форме')
                    else:
                        driver.refresh()
    except:
        count_if_2_1 += 1
        if count_if_2_1 == 3:
            print('ERROR: не отображается поле ввода во 2-й инлайн-форме')
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

# Популярные вопросы - видео / квиз
count_pq_1 = 0
while count_pq_1 < 3:
    try:
        pq_title = driver.find_element(by=By.XPATH, value='//*[text()[contains(., "Популярные вопросы:")]]')
        actions.move_to_element(pq_title).perform()
        second_q = driver.find_element(by=By.ID, value='uk-accordion-261')
        second_q.click()
        time.sleep(2)
        main_window = driver.current_window_handle
        pq_video_btn = driver.find_element(by=By.XPATH, value='(//a[@href="https://youtu.be/CsLAIx9EM1k/"])[1]')
        pq_video_btn.click()
        driver.switch_to.window(driver.window_handles[1])
        time.sleep(3)
        pq_title = driver.title
        assert pq_title == '«Мой гектар» Какие законы разрешают строительство на сельхозземлях - YouTube'
        driver.close()
        driver.switch_to.window(main_window)
        count_pq_1 = 3
        print('   OK: из "Популярных вопросов" выполнен переход на стр. с видео о законах')
        count_pq_2 = 0 # quiz
        while count_pq_2 < 3:
            try:
                last_q = driver.find_element(by=By.ID, value='uk-accordion-287')
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
                    wait(driver, 20).until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
    except:
        count_pq_1 = 3
        break

# инлайн-форма 3-я - поле ввода / кнопка / фото
count_if_3_1 = 0
while count_if_3_1 < 3:
    try:
        f_i_3 = wait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '(//*[(contains(@class, "snezh"))]//*[@id="consultationform-phone"])[5]')))
        if f_i_3:
            count_if_3_1 = 3
            print('   OK: поле ввода в 3-й инлайн-форме')
            count_if_3_2 = 0 # кнопка
            while count_if_3_2 < 3:
                try:
                    f_b_3 = wait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '(//*[(contains(@class, "snezh"))]//button)[7]')))
                    actions.move_to_element(f_b_3).perform()
                    if f_b_3:
                        count_if_3_2 = 3
                        print('     OK: кнопка в форме')
                        break
                except:
                    count_if_3_2 += 1
                    if count_if_3_2 == 3:
                        print('ERROR: не отображается кнопка в 3-й инлайн-форме')
                    else:
                        driver.refresh()
            count_if_3_3 = 0 # фото
            while count_if_3_3 < 3:
                try:
                    f_p_3 = wait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, '(//*[@src="/img/form/sof.png"])[1]')))
                    if f_p_3:
                        count_if_3_3 = 3
                        print('     OK: отображается фото')
                        break
                except:
                    count_if_3_3 += 1
                    if count_if_3_3 == 3:
                        print('ERROR: не отображается фото в 3-й инлайн-форме')
                    else:
                        driver.refresh()
    except:
        count_if_3_1 += 1
        if count_if_3_1 == 3:
            print('ERROR: не отображается поле ввода в 3-й инлайн-форме')
        else:
            driver.refresh()

# "Видео, которые вам ..." - 1-я карточка / видео / дотсы
count_vw_1 = 0
while count_vw_1 < 3:
    try:
        vw_title = driver.find_element(by=By.XPATH, value='//*[text()[contains(., "Видео, которые")]]')
        actions.move_to_element(vw_title).perform()
        assert EC.visibility_of_element_located((By.XPATH, '(//*[@id="b-video"]//*[@class="uk-object-cover"])[1]'))
        count_vw_1 = 3
        print('   OK: 1-я карточка в "Видео, которые вам ..."')
        count_vw_2 = 0 # дотсы
        while count_vw_2 < 3:
            try:
                assert EC.visibility_of_element_located((By.XPATH, '(//*[@id="b-video"]//*[(contains(@class, "uk-dotnav"))]/li)[1]'))
                count_vw_2 = 3
                print('     OK: дотсы')
                break
            except:
                count_vw_2 += 1
                if count_vw_2 == 3:
                    print('ERROR: не отображаются дотсы в "Видео, которые вам ..."')
                else:
                    driver.refresh()
    except:
        count_vw_1 += 1
        if count_vw_1 == 3:
            print('ERROR: не отображается 1-я карточка в "Видео, которые вам ..."')
        else:
            driver.refresh()

# блок "Варианты строительства ..." - модалка / видео
count_ob_1 = 0 # скрытый текст
while count_ob_1 < 3:
    try:
        ob_title = wait(driver,14).until(EC.presence_of_element_located((By.XPATH, '//*[text()[contains(., "Варианты строительства")]]')))
        actions.move_to_element(ob_title).perform()
        ob_accord = driver.find_element(by=By.XPATH, value='(//*[@class="uk-accordion"])[1]')
        ob_accord.click()
        ob_button = wait(driver,14).until(EC.element_to_be_clickable((By.XPATH, '(//*[@class="uk-accordion"]/li/div/a)[1]')))
        ob_button.click()
        ob_mod = wait(driver,14).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="build-1-1"]/div/div/button')))
        if ob_mod:
            driver.find_element(by=By.XPATH, value='//*[@id="build-1-1"]/div/div/button').click()
            count_ob_1 = 3
            print('   OK: в "Вариантах строительства" открывается модалка')
            count_ob_2 = 0 # видео
            while count_ob_2 < 3:
                try:
                    ob_v_btn = driver.find_element(by=By.XPATH, value='(//*[text()[contains(., "Варианты строительства")]]//parent::div//img)[2]')
                    ob_v_btn.click()
                    ob_video = driver.find_element(by=By.XPATH, value='//iframe[@class="uk-lightbox-iframe"]')
                    driver.switch_to.frame(ob_video)
                    ob_video_title = driver.find_element(by=By.CSS_SELECTOR, value='#player a.ytp-title-link')
                    if ob_video_title.is_displayed():
                        driver.switch_to.default_content()
                        lb_btn = driver.find_element(by=By.CSS_SELECTOR, value = '.uk-lightbox.uk-overflow-hidden.uk-lightbox-panel.uk-open button')
                        lightbox = driver.find_element(by=By.XPATH, value='//*[@class="uk-lightbox uk-overflow-hidden uk-lightbox-panel uk-open"]')
                        driver.execute_script("arguments[0].setAttribute('class','uk-lightbox uk-overflow-hidden uk-lightbox-panel uk-open uk-active uk-transition-active')", lightbox)
                        lb_btn.click()
                        count_ob_2 = 3
                        print('     OK: видео')
                        break
                except:
                    driver.refresh()
                    count_ob_2 += 1
                    if count_ob_2 == 3:
                        print('ERROR: не отображается видео')
                    else:
                        driver.refresh()
    except:
        count_ob_1 += 1
        if count_ob_1 == 3:
            print('ERROR: в "Вариантах строительства" не открывается модалка')
        else:
            driver.refresh()

# блок "Приглашаем ..." - модалка / фото / модалка
count_iy_1 = 0 # модалка
while count_iy_1 < 3:
    try:
        iy_title = wait(driver, 7).until(EC.presence_of_element_located((By.XPATH, '//*[text()[contains(., "Приглашаем ")]]')))
        actions.move_to_element(iy_title).perform()
        iy_btn_1 = driver.find_element(by=By.XPATH, value='(//*[@uk-toggle="target: #modal-meeting-meeting"])[1]')
        iy_btn_1.click()
        iy_mod_1 = wait(driver,14).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="modal-meeting-meeting"]/div/div/button')))
        if iy_mod_1:
            driver.find_element(by=By.XPATH, value='//*[@id="modal-meeting-meeting"]/div/div/button').click()
            count_iy_1 = 3
            print('   OK: в "Приглашаем ..." открывается 1-я модалка')
            count_iy_2 = 0 # фото
            while count_iy_2 < 3:
                try:
                    time.sleep(5)
                    iy_img = wait(driver, 7).until(EC.element_to_be_clickable((By.XPATH, '(//*[@id="meeting"]//img)[1]')))
                    count_iy_2 = 3
                    print('     OK: фото')
                    break
                except:
                    driver.refresh()
                    count_iy_2 += 1
                    if count_iy_2 == 3:
                        driver.save_screenshot('visible-part-of-screen_1.png')
                        print('ERROR: не отображается фото')
                    else:
                        driver.refresh()
            count_iy_3 = 0 # 2-я модалка
            while count_iy_3 < 3:
                try:
                    iy_btn_2 = driver.find_element(by=By.XPATH, value='(//*[@uk-toggle="target: #modal-meeting-meeting"])[2]')
                    iy_btn_2.click()
                    iy_mod_2 = wait(driver,14).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="modal-meeting-meeting"]/div/div/button')))
                    if iy_mod_2:
                        driver.find_element(by=By.XPATH, value='//*[@id="modal-meeting-meeting"]/div/div/button').click()
                        count_iy_3 = 3
                        print('     OK: 2-я модалка')
                        break
                except:
                    driver.refresh()
                    count_iy_3 += 1
                    if count_iy_3 == 3:
                        driver.save_screenshot('visible-part-of-screen_2.png')
                        print('ERROR: не открылась 2-я модалка')
                    else:
                        driver.refresh()
    except:
        count_iy_1 += 1
        if count_iy_1 == 3:
            print('ERROR: в "Приглашаем ..." не открывается 1-я модалка')
        else:
            driver.refresh()

# инлайн-форма 4-я - поле ввода / кнопка / фото
count_if_4_1 = 0
while count_if_4_1 < 3:
    try:
        f_i_4 = wait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '(//*[(contains(@class, "snezh"))]//*[@id="consultationform-phone"])[7]')))
        if f_i_4:
            count_if_4_1 = 3
            print('   OK: поле ввода в 4-й инлайн-форме')
            count_if_4_2 = 0 # кнопка
            while count_if_4_2 < 3:
                try:
                    f_b_4 = wait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '(//*[(contains(@class, "snezh"))]//button)[10]')))
                    actions.move_to_element(f_b_4).perform()
                    if f_b_4:
                        count_if_4_2 = 3
                        print('     OK: кнопка в форме')
                        break
                except:
                    count_if_4_2 += 1
                    if count_if_4_2 == 3:
                        print('ERROR: не отображается кнопка в 4-й инлайн-форме')
                    else:
                        driver.refresh()
            count_if_4_3 = 0 # фото
            while count_if_4_3 < 3:
                try:
                    f_p_4 = wait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, '(//*[@src="/img/form/max.png"])[1]')))
                    if f_p_4:
                        count_if_4_3 = 3
                        print('     OK: отображается фото')
                        break
                except:
                    count_if_4_3 += 1
                    if count_if_4_3 == 3:
                        print('ERROR: не отображается фото в 4-й инлайн-форме')
                    else:
                        driver.refresh()
    except:
        count_if_4_1 += 1
        if count_if_4_1 == 3:
            print('ERROR: не отображается поле ввода в 4-й инлайн-форме')
        else:
            driver.refresh()

# блок Футер - ссылка "Каталог" / каталог открылся / модалка / рейтинг Яндекса
count_f_1 = 0 # ссылка в футере
while count_f_1 < 3:
    try:
        cat_link = driver.find_element(by=By.XPATH, value='//h5[contains(text(), "Каталог участков")]')
        actions.move_to_element(cat_link).perform()
        assert EC.element_to_be_clickable(cat_link)
        count_f_1 = 3
        print('   OK: футер виден')
        count_f_2 = 0 # переход в каталог
        while count_f_2 < 3:
            try:
                cat_link.click()
                cat_title = driver.find_element(By.XPATH, value='//h4[text()="Подобрать участок"]')
                if cat_title.is_displayed():
                    driver.execute_script("window.history.go(-1)")
                count_f_2 = 3
                print('     OK: переход в каталог')
                break
            except:
                count_f_2 += 1
                if count_f_2 == 3:
                    print('ERROR: не выполняется переход в каталог')
                else:
                    driver.refresh()
        count_f_3 = 0 # модалка
        while count_f_3 < 3:
            try:
                time.sleep(5)
                f_btn = driver.find_element(by=By.XPATH, value='(//*[@uk-toggle="target: #modal-meeting-meeting"])[2]')
                f_btn.click()
                f_mod = wait(driver,14).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="modal-meeting-meeting"]/div/div/button')))
                if f_mod:
                    driver.find_element(by=By.XPATH, value='//*[@id="modal-meeting-meeting"]/div/div/button').click()
                    count_f_3 = 3
                    print('     OK: открылась модалка')
                    break
            except:
                count_f_3 += 1
                if count_f_3 == 3:
                    print('ERROR: не открылась модалка')
                else:
                    driver.refresh()
        count_f_4 = 0 # рейтинг Яндекса
        while count_f_4 < 3:
            try:
                f_ya_frame = ob_video = driver.find_element(by=By.XPATH, value='//iframe[@src="https://yandex.ru/sprav/widget/rating-badge/36705983328"]')
                driver.switch_to.frame(f_ya_frame)
                f_ya_btn = driver.find_element(by=By.CSS_SELECTOR, value='a.RatingBadgeWidget')
                assert f_ya_btn.is_displayed()
                count_f_4 = 3
                driver.switch_to.default_content()
                print('     OK: отображается рейтинг Яндекса')
                break
            except:
                count_f_4 += 1
                if count_f_4 == 3:
                    print('ERROR: не отображается рейтинг Яндекса')
                else:
                    driver.refresh()
    except:
        count_f_1 += 1
        if count_f_1 == 3:
            print('ERROR: что-то с футером')
        else:
            driver.refresh()

# 2. Каталог посёлков
# driver.get('https://moigektar.ru/catalogue')
# print("Каталог поселков")





time.sleep(1)
driver.quit()

