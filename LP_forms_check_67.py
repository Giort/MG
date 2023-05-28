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
import time
import json
driver.set_window_size(1660, 1080)
driver.implicitly_wait(10)

with open('data.json', 'r') as file:
    data = json.load(file)




driver.get("https://syn67.lp.moigektar.ru/")

# quiz в баннере над хедером
try:
    wait(driver, 10).until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
    bnr = wait(driver, 14).until(EC.element_to_be_clickable((By.XPATH, "//body/a/picture/img[@alt='Баннер']")))
    bnr.click()
    m_frame = driver.find_element(by=By.XPATH, value='//iframe[@class="marquiz__frame marquiz__frame_open"]')
    driver.switch_to.frame(m_frame)
    wait(driver, 14).until(EC.visibility_of_element_located((By.XPATH, "//h1[text()[contains(., 'Ответьте на несколько')]]")))
    print('   OK: син_67 квиз в баннере над хедером')
except:
    print('ERROR: что-то не так: квиз в баннере над хедером на син_67')

# квиз в хедере
try:
    driver.refresh()
    wait(driver, 10).until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
    btn_1 = wait(driver, 14).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "nav > div > div > .btn-mquiz")))
    btn_1.click()
    m_frame = driver.find_element(by=By.XPATH, value='//iframe[@class="marquiz__frame marquiz__frame_open"]')
    driver.switch_to.frame(m_frame)
    btn_2 = wait(driver, 14).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='start']// button")))
    btn_2.click()
    wait(driver, 14).until(EC.visibility_of_element_located((By.XPATH, "//span[text()[contains(., 'Площадь участка')]]")))
    print('   OK: syn_67 квиз в хедере')
except:
    print('ERROR: что-то не так с квизом в хедере на син_67')

# модалка "Подобрать участок" в блоке "Категории участков"
try:
    driver.refresh()
    wait(driver, 10).until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
    btn = driver.find_element(by=By.XPATH, value='//li[1]//button[text()[contains(., "Подобрать участок")]]')
    actions.move_to_element(btn).perform()
    btn.click()
    name = wait(driver, 14).until(EC.element_to_be_clickable((By.XPATH, '//*[@class="w-modal-description uk-modal uk-open"]//*[@id="consultationform-name"]')))
    name.send_keys(str(data["test_data_valid"]["name"]))
    driver.find_element(by=By.XPATH, value='//*[@class="w-modal-description uk-modal uk-open"]//*[@id="consultationform-phone"]').send_keys(str(data["test_data_valid"]["phone"]))
    driver.find_element(by=By.XPATH, value='//*[@class="w-modal-description uk-modal uk-open"]//*[@id="consultationform-email"]').send_keys(str(data["test_data_valid"]["email"]))
    driver.find_element(by=By.XPATH, value='//*[@class="w-modal-description uk-modal uk-open"]//*[@type="submit"]').click()
    wait(driver, 14).until(EC.visibility_of_element_located((By.XPATH, '//*[@class="w-modal-description uk-modal uk-open"]//*[text()[contains(., "Заявка отправлена")]]')))
    driver.find_element(by=By.XPATH, value='//*[@class="w-modal-description uk-modal uk-open"]/div/div/button').click()
    print('   OK: syn_67 модалка в блоке "Категории участков"')
except:
    print('ERROR: что-то не так с модалкой в блоке "Категории участков" на син_67')

# форма "Получите схему проезда"
try:
    driver.refresh()
    wait(driver, 10).until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
    name = driver.find_element(by=By.XPATH, value='//div[text()[contains(., "Получите схему")]]//parent::div//*[@id="consultationform-name"]')
    actions.move_to_element(name).perform()
    name.send_keys(str(data["test_data_valid"]["name"]))
    driver.find_element(by=By.XPATH, value='//div[text()[contains(., "Получите схему")]]//parent::div//*[@id="consultationform-phone"]').send_keys(str(data["test_data_valid"]["phone"]))
    driver.find_element(by=By.XPATH, value='//div[text()[contains(., "Получите схему")]]//parent::div//*[@id="consultationform-email"]').send_keys(str(data["test_data_valid"]["email"]))
    driver.find_element(by=By.XPATH, value='//div[text()[contains(., "Получите схему")]]//parent::div//*[text()[contains(., "Отправить заявку")]]').click()
    wait(driver, 14).until(EC.visibility_of_element_located((By.XPATH, '//div[text()[contains(., "Получите схему")]]//parent::div//*[text()[contains(., "Заявка отправлена")]]')))
    print('   OK: syn_67 форма "Получите схему проезда"')
except:
    print('ERROR: что-то не так с формой "Получите схему проезда" на син_67')

# модалка в "Бизнес-планах"
try:
    time.sleep(2)
    btn = driver.find_element(by=By.XPATH, value='//*[text()[contains(., "Бизнес-планы")]]//parent::div//li[1]//*[text()[contains(., "Подробнее")]]')
    actions.move_to_element(btn).perform()
    btn.click()
    name = wait(driver, 14).until(EC.element_to_be_clickable((By.XPATH, '//*[@class="uk-modal w-modal-callback uk-open"]//*[@id="consultationform-name"]')))
    name.send_keys(str(data["test_data_valid"]["name"]))
    driver.find_element(by=By.XPATH, value='//*[@class="uk-modal w-modal-callback uk-open"]//*[@id="consultationform-phone"]').send_keys(str(data["test_data_valid"]["phone"]))
    driver.find_element(by=By.XPATH, value='//*[@class="uk-modal w-modal-callback uk-open"]//*[@id="consultationform-email"]').send_keys(str(data["test_data_valid"]["email"]))
    driver.find_element(by=By.XPATH, value='//*[@class="uk-modal w-modal-callback uk-open"]//*[@type="submit"]').click()
    wait(driver, 14).until(EC.visibility_of_element_located((By.XPATH, '//*[@class="uk-modal w-modal-callback uk-open"]//*[text()[contains(., "Заявка отправлена")]]')))
    driver.find_element(by=By.XPATH, value='//*[@class="uk-modal w-modal-callback uk-open"]/div/div/div/button').click()
    print('   OK: syn_67 модалка в "Бизнес-планах"')
except:
    print('ERROR: что-то не так с модалкой в "Бизнес-планах" на син_67')

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
    print('   OK: syn_67 форма "Получите презентацию"')
except:
    print('ERROR: что-то не так с формой "Получите презентацию" на син_67')

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
    driver.find_element(by=By.XPATH, value='//*[@class="uk-modal w-modal-callback uk-open"]/div/div/div/button').click()
    print('   OK: syn_67 модалка в "Господдержке"')
except:
    print('ERROR: что-то не так с модалкой в "Господдержке" на син_67')

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
    driver.find_element(by=By.XPATH, value='//*[@class="uk-modal uk-open"]/div/div/div/button').click()
    print('   OK: syn_67 модалка в "Сохраните сбережения"')
except:
    print('ERROR: что-то не так с модалкой в "Сохраните сбережения" на син_67')

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
    driver.find_element(by=By.XPATH, value='//*[@class="uk-modal w-uk-form uk-open"]/div/div/div/button').click()
    print('   OK: syn_67 модалка в "Не упусти свой шанс"')
except:
    print('ERROR: что-то не так с модалкой в "Не упусти свой шанс" на син_67')

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
    print('   OK: syn_67 форма "Действуйте"')
except:
    print('ERROR: что-то не так с формой "Действуйте" на син_67')


time.sleep(5)
driver.quit()
