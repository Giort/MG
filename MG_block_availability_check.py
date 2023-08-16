from selenium import webdriver
from selenium.webdriver.chrome.options import Options
ch_options = Options()
ch_options.add_argument('--headless')
ch_options.page_load_strategy = 'eager'
driver = webdriver.Chrome(options= ch_options)
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
driver.get("https://moigektar.ru/")
print('Главная')

# баннер над хедером
try:
    assert driver.find_element(by=By.CLASS_NAME, value='w-banner').is_displayed()
    print('   баннер над хедером: OK')
except:
    print('ERROR: проблема с баннером над хедером на главной МГ')

# хедер + квиз!!!
try:
    wait(driver, 10).until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
    wait(driver,14).until(EC.presence_of_element_located((By.XPATH, "//li[@class='uk-active']/a[@href='/']")))
    print('   хедер: OK')
    # отключил, так как сейчас там модалка
    try:
        m2_btn = driver.find_element(by=By.XPATH, value="//li/div/*[text()[contains(., 'Подобрать участок')]]")
        actions.move_to_element(m2_btn).click().perform()
        try:
            m_iframe = driver.find_element(by=By.XPATH, value="//iframe[@class='marquiz__frame marquiz__frame_open']")
            driver.switch_to.frame(m_iframe)
            wait(driver,20).until(EC.visibility_of_element_located((By.XPATH, "//*[@id='start']/div/div[2]/div[1]/button")))
            print('   квиз в хедере на главной МГ: OK')
            driver.switch_to.default_content()
            driver.find_element(by=By.XPATH, value="//*[@id='marquiz__close']").click()
        except:
            print('ERROR: не загрузился квиз в хедере на главной МГ')
    except:
        print('ERROR: что-то с кнопкой квиз в хедере на главной МГ')
except:
    print('ERROR: проблема с хедером на главной МГ')

# блок первый баннер (первый экран)
try:
    wait(driver,14).until(EC.presence_of_element_located((By.CLASS_NAME, "w-main-bg")))
    print('   первый экран, фото: OK')
except:
    print('ERROR: проблема с первым экраном МГ')

# блок первый баннер (первый экран) + квиз
try:
    m2_btn = driver.find_element(by=By.CSS_SELECTOR, value=".uk-first-column .btn-mquiz")
    actions.move_to_element(m2_btn).click().perform()
    try:
        m_iframe = driver.find_element(by=By.XPATH, value="//iframe[@class='marquiz__frame marquiz__frame_open']")
        driver.switch_to.frame(m_iframe)
        wait(driver,20).until(EC.visibility_of_element_located((By.CLASS_NAME, "start-page__button")))
        print('   квиз в баннере под хедером на главной МГ: OK')
        driver.switch_to.default_content()
        driver.find_element(by=By.XPATH, value="//*[@id='marquiz__close']").click()
    except:
        print('ERROR: не загрузился квиз в баннере под хедером на главной МГ')
except:
    print('ERROR: что-то с кнопкой квиза в баннере под хедером на главной МГ')

# блок первый баннер (первый экран) + видео
try:
    driver.refresh()
    wait(driver, 10).until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
    video_btn = driver.find_element(by=By.CLASS_NAME, value="w-main__video-wrapper")
    actions.move_to_element(video_btn).click().perform()
    try:
        v_iframe = driver.find_element(by=By.XPATH, value="//iframe[@src='https://www.youtube.com/embed/HYCRL4TCeCA']")
        driver.switch_to.frame(v_iframe)
        wait(driver,20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'button[aria-label="Смотреть"]')))
        print('   видео на первом экране на главной МГ: OK')
    except:
        print('ERROR: не загрузилось видео на первом экране на главной МГ')
except:
    print('ERROR: что-то с кнопкой видео на первом экране на главной МГ')

# блок "Проект МГ - это"
try:
    driver.refresh()
    assert driver.find_element(by=By.XPATH, value='//*[@id="w-descr"]/div/div[1]//div[@class="w-descr__img"]//ul[@class="uk-slider-items"]').is_displayed()
    print('   блок "Проект МГ - это": OK')
except:
    print('ERROR: проблема с блоком "Проект МГ - это" на главной МГ')

# блок "МГ - это" + видео в нём
try:
    play_btn = driver.find_element(by=By.XPATH, value="//*[@id='w-descr']//a/div[1]/img")
    actions.move_to_element(play_btn).perform()
    play_btn.click()
    try:
        mg_iframe = driver.find_element(by=By.XPATH, value="//iframe[@class='uk-lightbox-iframe']")
        driver.switch_to.frame(mg_iframe)
        wait(driver,14).until(EC.presence_of_element_located((By.XPATH, '//*[@id="movie_player"]/div[4]/button')))
        print('   видео в 1-й секции блока МГ - это: OK')
    except:
        print('ERROR: проблема с видео в 1-й секции блока "МГ - это" на главной МГ')
except:
    print('ERROR: проблема с кнопкой видео в 1-й секции блока "МГ - это" на главной МГ')

# блок "Специальная цена"
try:
    title = wait(driver,14).until(EC.presence_of_element_located((By.XPATH, "" + str(data["mg_loc"]["mg_main_sow_title"]))))
    print('   блок "Специальная цена": OK')
    try:
        actions.move_to_element(title).pause(2).send_keys(Keys.PAGE_DOWN).perform()
        wait(driver,14).until(EC.visibility_of_element_located((By.XPATH, "" + str(data["mg_loc"]["mg_main_sow_btn"]))))
        print('   карточки в СП на главной: OK')
    except:
        print('ERROR: проблема с карточками СП на главной МГ')
except (TimeoutException, NoSuchElementException, ElementNotVisibleException):
    print('ERROR: проблема с блоком "Специальная цена" на главной МГ')

# блок "Специальная цена", переход в Каталог участков
try:
    driver.find_element(by=By.XPATH, value='//*[@id="catalogueSpecial"]//div[3]/a[contains(text(), "Перейти в каталог")]').click()
    assert driver.find_element(by=By.CSS_SELECTOR, value='.uk-breadcrumb a[href="/batches"]')
    driver.execute_script("window.history.go(-1)")
    print('   блок Спеццена, переход в Каталог: OK')
except:
    print('ERROR: проблема с переходом в Каталог из блока "Специальная цена" на главной МГ')

# блок "Лучшие посёлки"
try:
    driver.refresh()
    wait(driver, 10).until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
    l_title = driver.find_element(by=By.XPATH, value='//h1[text()[contains(.,"Лучшие поселки")]]')
    ActionChains(driver).move_to_element(l_title).send_keys(Keys.PAGE_DOWN).perform()
    assert EC.visibility_of_element_located((By.XPATH, "//h1[text()[contains(.,'Лучшие поселки')]]"))
    print('   блок "Лучшие поселки": OK')
    try:
        wait(driver,14).until(EC.visibility_of_element_located((By.XPATH, "//*[@id='catalogue']//div[1]/div/div[1]//li[1]//button")))
        print('   карточки в Лучших посёлках на главной: OK')
    except:
        print('ERROR: проблема с карточками Лучшие посёлки на главной МГ')
except:
    print('ERROR: проблема с блоком "Лучшие поселки проекта" на главной МГ')

# блок "Виртуальный тур"
try:
    wait(driver,14).until(EC.visibility_of_element_located((By.XPATH, "//h1[text()[contains(.,'Виртуальный тур')]]")))
    print('   блок "Виртуальный тур": есть')
    try:
        t_btn = driver.find_element(by=By.XPATH, value="//*[@id='w-select-map-preview']/div[3]//img")
        actions.move_to_element(t_btn).pause(3).click(t_btn).perform()
        try:
            iframe = driver.find_element(by=By.XPATH, value="//iframe[@class='embed-responsive-item']")
            driver.switch_to.frame(iframe)
            wait(driver,20).until(EC.visibility_of_element_located((By.XPATH, "//*[@id='krpanoSWFObject']//div[(contains(@style, 'z-index: 205'))]")))
            print('   блок "Виртуальный тур": тур загрузился, OK')
            driver.switch_to.default_content()
        except:
            driver.switch_to.default_content()
            print('ERROR: не загрузился "Виртуальный тур" на главной МГ')
    except:
        print('ERROR: что-то с кнопкой в блоке "Виртуальный тур" на главной МГ')
except:
    print('ERROR: проблема с блоком "Виртуальный тур" на главной МГ')

# блок "Лучшее время"
try:
    wait(driver,14).until(EC.presence_of_element_located((By.XPATH, "//h1[text()[contains(.,'Лучшее время')]]")))
    print('   блок "Лучшее время для покупки": OK')
except:
    print('ERROR: проблема с блоком "Лучшее время для покупки" на главной МГ')

# блок "Видео, которые"
try:
    wait(driver,14).until(EC.visibility_of_element_located((By.XPATH, "//h1[text()[contains(.,'Видео, которые')]]")))
    print('   блок "Видео, которые": OK')
except:
    print('ERROR: проблема с блоком "Видео, которые вам стоит увидеть" на главной МГ')

# блок "Награды проекта"
try:
    wait(driver,14).until(EC.visibility_of_element_located((By.XPATH, "//div[text()[contains(.,'Награды проекта')]]")))
    print('   блок "Награды проекта": OK')
except:
    print('ERROR: проблема с блоком "Награды проекта" на главной МГ')

# блок "СМИ о проекте"
try:
    smi = driver.find_element(by=By.XPATH, value="//div[text()[contains(.,'СМИ о проекте')]]")
    ActionChains(driver).move_to_element(smi).send_keys(Keys.PAGE_DOWN).perform()
    assert EC.visibility_of_element_located((By.XPATH, '//div[text()[contains(.,"СМИ о проекте")]]//parent::div[1]//*[@class="uk-first-column"]'))
    print('   блок "СМИ о проекте": OK')
except:
    print('ERROR: проблема с блоком "СМИ о проекте" на главной МГ')

# блок "Развитие вашего участка"
try:
    driver.refresh()
    wait(driver, 10).until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
    growth = driver.find_element(by=By.XPATH, value="//h1[text()[contains(.,'Развитие вашего участка')]]")
    ActionChains(driver).move_to_element(growth).send_keys(Keys.PAGE_DOWN).perform()
    assert EC.visibility_of_element_located((By.XPATH, "//h1[text()[contains(.,'Развитие вашего участка')]]"))
    print('   блок "Развитие вашего участка": OK')
except:
    print('ERROR: проблема с блоком "Развитие вашего участка" на главной МГ')

# блок "Сохраните свои"
try:
    driver.refresh()
    wait(driver, 10).until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
    save = driver.find_element(by=By.XPATH, value="//h1[text()[contains(.,'Сохраните свои')]]")
    ActionChains(driver).move_to_element(save).send_keys(Keys.PAGE_DOWN).perform()
    wait(driver,14).until(EC.visibility_of_element_located((By.XPATH, "//h1[text()[contains(.,'Сохраните свои')]]")))
    print('   блок "Сохраните свои": OK')
except:
    print('ERROR: проблема с блоком "Сохраните свои" на главной МГ')

# блок "Почему нам доверяют"
try:
    why = driver.find_element(by=By.XPATH, value="//div[text()[contains(.,'Почему нам')]]")
    ActionChains(driver).move_to_element(why).send_keys(Keys.PAGE_DOWN).perform()
    assert EC.visibility_of_element_located((By.XPATH, "//div[text()[contains(.,'Почему нам')]]"))
    print('   блок "Почему нам доверяют": OK')
    try:
        time.sleep(3)
        driver.find_element(by=By.XPATH, value="//*[text()[contains(.,'Почему нам доверяют')]]//parent::div//a[text()[contains(., 'Подобрать участок')]]").click()
        m_iframe = driver.find_element(by=By.XPATH, value="//iframe[@class='marquiz__frame marquiz__frame_open']")
        driver.switch_to.frame(m_iframe)
        wait(driver,20).until(EC.visibility_of_element_located((By.XPATH, "//*[@id='start']/div/div[2]/div[1]/button")))
        print('   квиз в "Почему нам доверяют": OK')
    except:
        print('ERROR: не загрузился квиз в "почему нам доверяют" на главной"')
except:
    print('ERROR: проблема с блоком "Почему нам доверяют" на главной МГ')

# блок "Господдержка"
try:
    driver.refresh()
    wait(driver, 10).until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
    gos = driver.find_element(by=By.XPATH, value="//h1[text()[contains(.,'Государственная поддержка')]]")
    ActionChains(driver).move_to_element(gos).send_keys(Keys.PAGE_DOWN).perform()
    wait(driver,14).until(EC.visibility_of_element_located((By.XPATH, "//h1[text()[contains(.,'Государственная поддержка')]]")))
    print('   блок "Государственная поддержка": OK')
except:
    print('ERROR: проблема с блоком "Государственная поддержка" на главной МГ')

# форма "Узнайте все подробности"
try:
    wait(driver,14).until(EC.visibility_of_element_located((By.XPATH, "//b[text()[contains(.,'Узнайте все подробности')]]")))
    print('   форма "Узнайте все подробности": OK')
except:
    print('ERROR: проблема с формой "Узнайте все подробности" на главной МГ')

# блок "Получите каталог"
try:
    wait(driver,14).until(EC.visibility_of_element_located((By.XPATH, "//b[text()[contains(.,'Получите каталог')]]")))
    print('   форма "Получите каталог": OK')
except:
    print('ERROR: проблема с формой "Получите каталог" на главной МГ')

# блок "Отзывы о проекте"
try:
    wait(driver,14).until(EC.visibility_of_element_located((By.XPATH, "//div[text()[contains(.,'Отзывы о проекте')]]")))
    print('   блок "Отзывы о проекте": OK')
except:
    print('ERROR: проблема с блоком "Отзывы о проекте" на главной МГ')

# блок "Бизнес-планы"
try:
    wait(driver,14).until(EC.visibility_of_element_located((By.XPATH, "//h1[text()[contains(.,'Бизнес-планы')]]")))
    print('   блок "Бизнес-планы": OK')
except:
    print('ERROR: проблема с блоком "Бизнес-планы" на главной МГ')

# блок "Личный кабинет"
try:
    wait(driver,14).until(EC.visibility_of_element_located((By.XPATH, '//*[@class="w-community-content"]/div[text()[contains(.,"Личный кабинет")]]')))
    print('   блок "Личный кабинет": OK')
except:
    print('ERROR: проблема с блоком "Личный кабинет" на главной МГ')

# блок "Подпишитесь в соцсетях"
try:
    sMedia = driver.find_element(by=By.XPATH, value="//div[text()[contains(.,'в соцсетях')]]")
    ActionChains(driver).move_to_element(sMedia).send_keys(Keys.PAGE_DOWN).perform()
    assert EC.visibility_of_element_located((By.XPATH, '//*[@id="elfsight_social_container"]//*[@data-elfsight-app-lazy=""]/div/div/div/div/div'))
    print('   блок "Подпишитесь в соцсетях": OK')
except:
    print('ERROR: проблема с блоком "Подпишитесь в соцсетях" на главной МГ')

# форма "Подпишитесь на рассылку"
try:
    wait(driver,14).until(EC.visibility_of_element_located((By.XPATH, "//*[text()[contains(.,'Подпишитесь на рассылку')]]")))
    print('   форма "Подпишитесь на рассылку": OK')
except:
    print('ERROR: проблема с формой "Подпишитесь на рассылку" на главной МГ')

# блок "Подпишитесь на новости развития"
try:
    title_r = driver.find_element(by=By.XPATH, value="//h1[text()[contains(.,'на новости развития')]]")
    print('   блок "Подпишитесь на новости развития": OK')
    try:
        actions.move_to_element(title_r).perform()
        time.sleep(5)
        wait(driver,14).until(EC.visibility_of_element_located((By.XPATH, "//div[@class='w-news-wrapper']/div/ul/li[1]/a/div[1]/div/div[1]")))
        print('   блок "Подпишитесь на новости развития": карточки отображаются, ОК')
    except:
        print('ERROR: проблема с блоком "Подпишитесь на новости развития" на главной МГ')
except:
    print('ERROR: проблема с блоком "Подпишитесь на новости развития" на главной МГ')

# блок "Проект от сохи до сохи"
try:
    title_n = driver.find_element(by=By.XPATH, value="//h1[text()[contains(.,'От сохи')]]")
    print('   блок "От сохи до сохи": OK')
    try:
        actions.move_to_element(title_n).perform()
        actions.send_keys(Keys.PAGE_DOWN).perform()
        time.sleep(5)
        wait(driver,14).until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".yottie-widget-inner div:nth-of-type(1) > div:nth-of-type(1) > a span img")))
        print('   блок "От сохи до сохи": карточки отображаются, ОК')
    except:
        print('ERROR: проблема с блоком "От сохи до сохи" на главной МГ')
except:
    print('ERROR: проблема с блоком "От сохи до сохи" на главной МГ')

# форма "Действуйте"
try:
    wait(driver,14).until(EC.visibility_of_element_located((By.XPATH, "//b[text()[contains(.,'Узнайте все')]]")))
    print('   форма "Действуйте": OK')
except:
    print('ERROR: проблема с формой "Действуйте" на главной МГ')

# блок "Приглашаем на встречу"
try:
    wait(driver,14).until(EC.visibility_of_element_located((By.XPATH, "//div[text()[contains(.,'Приглашаем на встречу')]]")))
    print('   блок "Приглашаем на встречу": OK')
except:
    print('ERROR: проблема с блоком "Приглашаем на встречу" на главной МГ')

# блок Футер
try:
    wait(driver,14).until(EC.presence_of_element_located((By.XPATH, "//div[@class='w-footer']/div/div/div/div/button[text()[contains(.,'Связаться')]]")))
    print('   футер: OK\n')
except:
    print('ERROR: проблема с футером на главной МГ\n')



# 2. Каталог посёлков
driver.get('https://moigektar.ru/catalogue')
print("Каталог поселков")

#блок "Специальное предложение"
try:
    wait(driver,14).until(EC.visibility_of_element_located((By.XPATH, "" + str(data["mg_loc"]["mg_catalog_sow_title"]))))
    print('   блок "Специальное предложение": OK')
    try:
        wait(driver,14).until(EC.visibility_of_element_located((By.XPATH, ""  + str(data["mg_loc"]["mg_catalog_country_sow_btn"]))))
        print('   карточки в СП: OK')
    except:
        print('ERROR: проблема с карточками СП в Каталоге поселков')
except (TimeoutException, NoSuchElementException, ElementNotVisibleException):
    print('ERROR: проблема с блоком "Специальное предложение" в Каталоге поселков')

# блок "Лучшие поселки"
try:
    wait(driver,14).until(EC.presence_of_element_located((By.XPATH, "//h1[text()[contains(.,'Лучшие поселки')]]")))
    print('   блок "Лучшие поселки": OK')
except:
    print('ERROR: проблема с блоком "Лучшие поселки" в Каталоге поселков')

# блок "Поселки в развитии"
try:
    wait(driver,14).until(EC.presence_of_element_located((By.XPATH, "//h1[text()[contains(.,'Поселки в развитии')]]")))
    print('   блок "Поселки в развитии": OK')
except:
    print('ERROR: проблема с блоком "Поселки в развитии" в Каталоге поселков')

# блок "Дачные участки"
try:
    title = wait(driver,14).until(EC.visibility_of_element_located((By.XPATH, "//h1[text()[contains(., 'Дачные участки')]]")))
    print('   блок "Дачные участки": OK')
    try:
        actions.move_to_element(title).send_keys(Keys.PAGE_DOWN).send_keys(Keys.ARROW_DOWN).perform()
        wait(driver,14).until(EC.visibility_of_element_located((By.XPATH, "" + str(data["mg_loc"]['mg_catalog_country_country_btn']))))
        print('   карточки в "Дачных участках": OK')
    except:
        print('ERROR: проблема с карточками в "Дачных участках" в Каталоге поселков')
except (TimeoutException, NoSuchElementException, ElementNotVisibleException):
    print('ERROR: проблема с блоком "Дачные участки" в Каталоге поселков')

# блок "Подберите ваш идеальный"
try:
    wait(driver,14).until(EC.presence_of_element_located((By.XPATH, "//h1[text()[contains(.,'Подберите ваш')]]")))
    print('   баннер "Подберите ваш ...": OK')
except:
    print('ERROR: проблема с баннером "Подберите ваш идеальный гектар" в Каталоге поселков')

# блок "Инвестиционные проекты"
try:
    wait(driver,14).until(EC.presence_of_element_located((By.XPATH, "//h1[text()[contains(.,'Инвестиционные')]]")))
    print('   блок "Инвестпроекты": OK')
except:
    print('ERROR: проблема с блоком "Инвестиционные проекты" в Каталоге поселков')

# блок "Долина Вазузы"
try:
    wait(driver,14).until(EC.presence_of_element_located((By.XPATH, "//h1[text()[contains(.,'Долина')]]")))
    print('   баннер "Долина Вазузы": OK')
except:
    print('ERROR: проблема с баннером "Долина Вазузы" в Каталоге поселков')

# форма "Хотите узнать"
try:
    wait(driver,14).until(EC.visibility_of_element_located((By.XPATH, "//b[text()[contains(.,'Хотите узнать ')]]")))
    print('   форма "Хотите узнать подробнее": OK\n')
except:
    print('ERROR: проблема с формой "Хотите узнать подробнее о проекте?" в Каталоге поселков\n')

time.sleep(1)
driver.quit()

