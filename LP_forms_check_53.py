import chromedriver_binary
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
from selenium.webdriver.common.keys import Keys
import time
import json
driver.set_window_size(1660, 1000)
driver.implicitly_wait(10)

with open('data.json', 'r') as file:
    data = json.load(file)

driver.get("https://syn53.lp.moigektar.ru/")

# модалка в баннере над хедером
# try:
#     bnr = wait(driver, 14).until(EC.element_to_be_clickable((By.XPATH, "//body/a/picture/img[@alt='Баннер']")))
#     bnr.click()
#     name = wait(driver, 14).until(EC.element_to_be_clickable((By.XPATH, '//*[@class="uk-modal w-modal-callback uk-open"]//*[@id="consultationform-name"]')))
#     name.send_keys(str(data["test_data_valid"]["name"]))
#     driver.find_element(by=By.XPATH, value='//*[@class="uk-modal w-modal-callback uk-open"]//*[@id="consultationform-phone"]').send_keys(str(data["test_data_valid"]["phone"]))
#     driver.find_element(by=By.XPATH, value='//*[@class="uk-modal w-modal-callback uk-open"]//*[@id="consultationform-email"]').send_keys(str(data["test_data_valid"]["email"]))
#     driver.find_element(by=By.XPATH, value='//*[@class="uk-modal w-modal-callback uk-open"]//*[@type="submit"]').click()
#     wait(driver, 14).until(EC.visibility_of_element_located((By.XPATH, '//*[@class="uk-modal w-modal-callback uk-open"]//*[text()[contains(., "Заявка отправлена")]]')))
#     driver.find_element(by=By.XPATH, value='//*[@class="uk-modal w-modal-callback uk-open"]/div/div/div/button').click()
#     print('   OK: syn_53 модалка в 1-м баннере')
# except:
#     print('ERROR: что-то не так с модалкой в 1-м баннере на син_53')

# квиз в хедере
try:
    wait(driver, 10).until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
    btn_1 = wait(driver, 14).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "nav > div > div > .btn-mquiz")))
    btn_1.click()
    m_frame = driver.find_element(by=By.XPATH, value='//iframe[@class="marquiz__frame marquiz__frame_open"]')
    driver.switch_to.frame(m_frame)
    btn_2 = wait(driver, 14).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='start']// button")))
    btn_2.click()
    wait(driver, 14).until(EC.visibility_of_element_located((By.XPATH, "//span[text()[contains(., 'Выберите цели')]]")))
    print('   OK: syn_53 квиз в хедере')
except:
    try:
        driver.refresh()
        wait(driver, 10).until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
        btn_1 = wait(driver, 14).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "nav > div > div > .btn-mquiz")))
        btn_1.click()
        m_frame = driver.find_element(by=By.XPATH, value='//iframe[@class="marquiz__frame marquiz__frame_open"]')
        driver.switch_to.frame(m_frame)
        btn_2 = wait(driver, 14).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='start']// button")))
        btn_2.click()
        wait(driver, 14).until(EC.visibility_of_element_located((By.XPATH, "//span[text()[contains(., 'Выберите цели')]]")))
        print('   OK: syn_53 квиз в хедере')
    except:
        print('ERROR: что-то не так с квизом в хедере на син_53')

# модалка "Обратная связь" в блоке "Новая жизнь - это"
try:
    driver.refresh()
    wait(driver, 10).until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
    btn_1 = wait(driver, 14).until(EC.element_to_be_clickable((By.XPATH, "//*[text()[contains(., 'Показать еще')]]")))
    actions.move_to_element(btn_1).perform()
    btn_1.click()
    actions.send_keys(Keys.PAGE_DOWN).send_keys(Keys.PAGE_DOWN).perform()
    btn_2 = wait(driver, 14).until(EC.element_to_be_clickable((By.XPATH, "//div[@class='uk-visible@m uk-width-1-1']/*[text()[contains(., 'Узнать подробности')]]")))
    btn_2.click()
    name = wait(driver, 14).until(EC.element_to_be_clickable((By.XPATH, '//*[@class="uk-modal w-modal-callback uk-open"]//*[@id="consultationform-name"]')))
    name.send_keys(str(data["test_data_valid"]["name"]))
    driver.find_element(by=By.XPATH, value='//*[@class="uk-modal w-modal-callback uk-open"]//*[@id="consultationform-phone"]').send_keys(str(data["test_data_valid"]["phone"]))
    driver.find_element(by=By.XPATH, value='//*[@class="uk-modal w-modal-callback uk-open"]//*[@id="consultationform-email"]').send_keys(str(data["test_data_valid"]["email"]))
    driver.find_element(by=By.XPATH, value='//*[@class="uk-modal w-modal-callback uk-open"]//*[@type="submit"]').click()
    wait(driver, 14).until(EC.visibility_of_element_located((By.XPATH, '//*[@class="uk-modal w-modal-callback uk-open"]//*[text()[contains(., "Заявка отправлена")]]')))
    print('   OK: syn_53 модалка в блоке "НЖ - это"')
    driver.find_element(by=By.XPATH, value='//*[@class="uk-modal w-modal-callback uk-open"]/div/div/button').click()
except:
    print('ERROR: что-то не так с модалкой в блоке "НЖ - это" на син_53')

# модалка "Подобрать участок" в блоке "Категории участков"
try:
    time.sleep(2)
    btn = driver.find_element(by=By.XPATH, value='//li[1]//button[text()[contains(., "Подобрать участок")]]')
    actions.move_to_element(btn).perform()
    btn.click()
    name = wait(driver, 14).until(EC.element_to_be_clickable((By.XPATH, '//*[@class="w-modal-description uk-modal uk-open"]//*[@id="consultationform-name"]')))
    name.send_keys(str(data["test_data_valid"]["name"]))
    driver.find_element(by=By.XPATH, value='//*[@class="w-modal-description uk-modal uk-open"]//*[@id="consultationform-phone"]').send_keys(str(data["test_data_valid"]["phone"]))
    driver.find_element(by=By.XPATH, value='//*[@class="w-modal-description uk-modal uk-open"]//*[@id="consultationform-email"]').send_keys(str(data["test_data_valid"]["email"]))
    driver.find_element(by=By.XPATH, value='//*[@class="w-modal-description uk-modal uk-open"]//*[@type="submit"]').click()
    wait(driver, 14).until(EC.visibility_of_element_located((By.XPATH, '//*[@class="w-modal-description uk-modal uk-open"]//*[text()[contains(., "Заявка отправлена")]]')))
    print('   OK: syn_53 модалка в блоке "Категории участков"')
    driver.find_element(by=By.XPATH, value='//*[@class="w-modal-description uk-modal uk-open"]/div/div/button').click()
except:
    print('ERROR: что-то не так с модалкой в блоке "Категории участков" на син_53')

# модалка "Узнать подробнее" в блоке "Посетите усадьбу"
try:
    time.sleep(2)
    btn = driver.find_element(by=By.XPATH, value='//div[@class="uk-first-column"]/button[@uk-toggle="target: #modal-stay"]')
    actions.move_to_element(btn).perform()
    btn.click()
    name = wait(driver, 14).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="modal-stay"]//*[@id="consultationform-name"]')))
    name.send_keys(str(data["test_data_valid"]["name"]))
    driver.find_element(by=By.XPATH, value='//*[@id="modal-stay"]//*[@id="consultationform-phone"]').send_keys(str(data["test_data_valid"]["phone"]))
    driver.find_element(by=By.XPATH, value='//*[@id="modal-stay"]//*[@id="consultationform-email"]').send_keys(str(data["test_data_valid"]["email"]))
    driver.find_element(by=By.XPATH, value='//*[@id="modal-stay"]//*[@type="submit"]').click()
    wait(driver, 14).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="modal-stay"]//*[text()[contains(., "Заявка отправлена")]]')))
    print('   OK: syn_53 модалка в блоке "Посетите усадьбу"')
    driver.find_element(by=By.XPATH, value='//*[@id="modal-stay"]/div/div/button').click()
except:
    print('ERROR: что-то не так с модалкой в блоке "Посетите усадьбу" на син_53')

# модалка "Получить консультацию" в блоке "Зона интенсивного развития"
try:
    time.sleep(2)
    btn = driver.find_element(by=By.XPATH, value='//button[@uk-toggle="target: #modal-zir"]')
    actions.move_to_element(btn).perform()
    btn.click()
    name = wait(driver, 14).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="modal-zir"]//*[@id="consultationform-name"]')))
    name.send_keys(str(data["test_data_valid"]["name"]))
    driver.find_element(by=By.XPATH, value='//*[@id="modal-zir"]//*[@id="consultationform-phone"]').send_keys(str(data["test_data_valid"]["phone"]))
    driver.find_element(by=By.XPATH, value='//*[@id="modal-zir"]//*[@id="consultationform-email"]').send_keys(str(data["test_data_valid"]["email"]))
    driver.find_element(by=By.XPATH, value='//*[@id="modal-zir"]//*[@type="submit"]').click()
    wait(driver, 14).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="modal-zir"]//*[text()[contains(., "Заявка отправлена")]]')))
    print('   OK: syn_53 модалка в блоке "Зона интенсивного развития"')
    driver.find_element(by=By.XPATH, value='//*[@id="modal-zir"]/div/div/button').click()
except:
    print('ERROR: что-то не так с модалкой в блоке "Зона интенсивного развития" на син_53')

# форма "Получите схему проезда"
try:
    time.sleep(2)
    name = driver.find_element(by=By.XPATH, value='//div[text()[contains(., "Получите схему")]]//parent::div//*[@id="consultationform-name"]')
    actions.move_to_element(name).perform()
    name.send_keys(str(data["test_data_valid"]["name"]))
    driver.find_element(by=By.XPATH, value='//div[text()[contains(., "Получите схему")]]//parent::div//*[@id="consultationform-phone"]').send_keys(str(data["test_data_valid"]["phone"]))
    driver.find_element(by=By.XPATH, value='//div[text()[contains(., "Получите схему")]]//parent::div//*[@id="consultationform-email"]').send_keys(str(data["test_data_valid"]["email"]))
    driver.find_element(by=By.XPATH, value='//div[text()[contains(., "Получите схему")]]//parent::div//*[text()[contains(., "Отправить заявку")]]').click()
    wait(driver, 14).until(EC.visibility_of_element_located((By.XPATH, '//div[text()[contains(., "Получите схему")]]//parent::div//*[text()[contains(., "Заявка отправлена")]]')))
    print('   OK: syn_53 форма "Получите схему проезда"')
except:
    print('ERROR: что-то не так с формой "Получите схему проезда" на син_53')

# модалка в "Бизнес-планах"
try:
    driver.refresh()
    wait(driver, 10).until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
    btn = driver.find_element(by=By.XPATH, value='//*[text()[contains(., "Бизнес-планы")]]//parent::div//li[1]//*[text()[contains(., "Подробнее")]]')
    actions.move_to_element(btn).perform()
    btn.click()
    name = wait(driver, 14).until(EC.element_to_be_clickable((By.XPATH, '//*[@class="uk-modal w-modal-callback uk-open"]//*[@id="consultationform-name"]')))
    name.send_keys(str(data["test_data_valid"]["name"]))
    driver.find_element(by=By.XPATH, value='//*[@class="uk-modal w-modal-callback uk-open"]//*[@id="consultationform-phone"]').send_keys(str(data["test_data_valid"]["phone"]))
    driver.find_element(by=By.XPATH, value='//*[@class="uk-modal w-modal-callback uk-open"]//*[@id="consultationform-email"]').send_keys(str(data["test_data_valid"]["email"]))
    driver.find_element(by=By.XPATH, value='//*[@class="uk-modal w-modal-callback uk-open"]//*[@type="submit"]').click()
    wait(driver, 14).until(EC.visibility_of_element_located((By.XPATH, '//*[@class="uk-modal w-modal-callback uk-open"]//*[text()[contains(., "Заявка отправлена")]]')))
    print('   OK: syn_53 модалка в "Бизнес-планах"')
    driver.find_element(by=By.XPATH, value='//*[@class="uk-modal w-modal-callback uk-open"]/div/div/button').click()
except:
    print('ERROR: что-то не так с модалкой в "Бизнес-планах" на син_53')

# форма "Получите презентацию"
try:
    time.sleep(2)
    name = driver.find_element(by=By.XPATH, value='//div[text()[contains(., "Получите презентацию")]]//parent::div//*[@id="consultationform-name"]')
    actions.move_to_element(name).perform()
    name.send_keys(str(data["test_data_valid"]["name"]))
    driver.find_element(by=By.XPATH, value='//div[text()[contains(., "Получите презентацию")]]//parent::div//*[@id="consultationform-phone"]').send_keys(str(data["test_data_valid"]["phone"]))
    driver.find_element(by=By.XPATH, value='//div[text()[contains(., "Получите презентацию")]]//parent::div//*[@id="consultationform-email"]').send_keys(str(data["test_data_valid"]["email"]))
    driver.find_element(by=By.XPATH, value='//div[text()[contains(., "Получите презентацию")]]//parent::div//*[text()[contains(., "Отправить")]]').click()
    wait(driver, 14).until(EC.visibility_of_element_located((By.XPATH, '//div[text()[contains(., "Получите презентацию")]]//parent::div//*[text()[contains(., "Заявка отправлена")]]')))
    print('   OK: syn_53 форма "Получите презентацию"')
except:
    print('ERROR: что-то не так с формой "Получите презентацию" на син_53')

# модалка в "Господдержке"
try:
    driver.refresh()
    wait(driver, 10).until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
    btn = driver.find_element(by=By.XPATH, value='//*[text()[contains(., "Господдержка для")]]//parent::div//*[text()[contains(., "подробнее")]]')
    actions.move_to_element(btn).perform()
    btn.click()
    name = wait(driver, 14).until(EC.element_to_be_clickable((By.XPATH, '//*[@class="uk-modal w-modal-callback uk-open"]//*[@id="consultationform-name"]')))
    name.send_keys(str(data["test_data_valid"]["name"]))
    driver.find_element(by=By.XPATH, value='//*[@class="uk-modal w-modal-callback uk-open"]//*[@id="consultationform-phone"]').send_keys(str(data["test_data_valid"]["phone"]))
    driver.find_element(by=By.XPATH, value='//*[@class="uk-modal w-modal-callback uk-open"]//*[@id="consultationform-email"]').send_keys(str(data["test_data_valid"]["email"]))
    driver.find_element(by=By.XPATH, value='//*[@class="uk-modal w-modal-callback uk-open"]//*[@type="submit"]').click()
    wait(driver, 14).until(EC.visibility_of_element_located((By.XPATH, '//*[@class="uk-modal w-modal-callback uk-open"]//*[text()[contains(., "Заявка отправлена")]]')))
    print('   OK: syn_53 модалка в "Господдержке"')
    driver.find_element(by=By.XPATH, value='//*[@class="uk-modal w-modal-callback uk-open"]/div/div/button').click()
except:
    print('ERROR: что-то не так с модалкой в "Господдержке" на син_53')

# модалка в "Сохраните сбережения"
try:
    time.sleep(2)
    btn = driver.find_element(by=By.XPATH, value='//*[text()[contains(., "Получить альманах")]]')
    actions.move_to_element(btn).perform()
    time.sleep(2)
    btn.click()
    name = wait(driver, 14).until(EC.element_to_be_clickable((By.XPATH, '//*[@class="uk-modal uk-open"]//*[@id="consultationform-name"]')))
    name.send_keys(str(data["test_data_valid"]["name"]))
    driver.find_element(by=By.XPATH, value='//*[@class="uk-modal uk-open"]//*[@id="consultationform-phone"]').send_keys(str(data["test_data_valid"]["phone"]))
    driver.find_element(by=By.XPATH, value='//*[@class="uk-modal uk-open"]//*[@id="consultationform-email"]').send_keys(str(data["test_data_valid"]["email"]))
    driver.find_element(by=By.XPATH, value='//*[@class="uk-modal uk-open"]//*[@type="submit"]').click()
    wait(driver, 14).until(EC.visibility_of_element_located((By.XPATH, '//*[@class="uk-modal uk-open"]//*[text()[contains(., "Заявка отправлена")]]')))
    print('   OK: syn_53 модалка в "Сохраните сбережения"')
    driver.find_element(by=By.XPATH, value='//*[@class="uk-modal uk-open"]/div/div/button').click()
except:
    print('ERROR: что-то не так с модалкой в "Сохраните сбережения" на син_53')

# модалка в "Не упусти свой шанс"
try:
    time.sleep(2)
    btn = driver.find_element(by=By.XPATH, value='//*[text()[contains(., "Рассчитайте рассрочку")]]//parent::div//*[text()[contains(., "Отправить заявку")]]')
    actions.move_to_element(btn).perform()
    btn.click()
    name = wait(driver, 14).until(EC.element_to_be_clickable((By.XPATH, '//*[@class="uk-modal w-uk-form uk-open"]//*[@id="consultationform-name"]')))
    name.send_keys(str(data["test_data_valid"]["name"]))
    driver.find_element(by=By.XPATH, value='//*[@class="uk-modal w-uk-form uk-open"]//*[@id="consultationform-phone"]').send_keys(str(data["test_data_valid"]["phone"]))
    driver.find_element(by=By.XPATH, value='//*[@class="uk-modal w-uk-form uk-open"]//*[@id="consultationform-email"]').send_keys(str(data["test_data_valid"]["email"]))
    driver.find_element(by=By.XPATH, value='//*[@class="uk-modal w-uk-form uk-open"]//*[@type="submit"]').click()
    wait(driver, 14).until(EC.visibility_of_element_located((By.XPATH, '//*[@class="uk-modal w-uk-form uk-open"]//*[text()[contains(., "Заявка отправлена")]]')))
    print('   OK: syn_53 модалка в "Не упусти свой шанс"')
    driver.find_element(by=By.XPATH, value='//*[@class="uk-modal w-uk-form uk-open"]/div/div/button').click()
except:
    print('ERROR: что-то не так с модалкой в "Не упусти свой шанс" на син_53')

# форма "Действуйте"
try:
    time.sleep(2)
    name = driver.find_element(by=By.XPATH, value='//div[text()[contains(., "Действуйте")]]//parent::div//*[@id="consultationform-name"]')
    actions.move_to_element(name).perform()
    name.send_keys(str(data["test_data_valid"]["name"]))
    driver.find_element(by=By.XPATH, value='//div[text()[contains(., "Действуйте")]]//parent::div//*[@id="consultationform-phone"]').send_keys(str(data["test_data_valid"]["phone"]))
    driver.find_element(by=By.XPATH, value='//div[text()[contains(., "Действуйте")]]//parent::div//*[@id="consultationform-email"]').send_keys(str(data["test_data_valid"]["email"]))
    driver.find_element(by=By.XPATH, value='//div[text()[contains(., "Действуйте")]]//parent::div//*[text()[contains(., "Отправить")]]').click()
    wait(driver, 14).until(EC.visibility_of_element_located((By.XPATH, '//div[text()[contains(., "Действуйте")]]//parent::div//*[text()[contains(., "Заявка отправлена")]]')))
    print('   OK: syn_53 форма "Действуйте"')
except:
    print('ERROR: что-то не так с формой "Действуйте" на син_53')


time.sleep(5)
driver.quit()
