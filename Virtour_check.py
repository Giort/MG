from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
ch_options = Options()
ch_options.add_argument('--headless')
ch_options.page_load_strategy = 'eager'
service = ChromeService(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=ch_options)
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
actions = ActionChains(driver)
from selenium.webdriver.common.keys import Keys
import time
import json
driver.set_window_size(1600, 1000)
driver.implicitly_wait(10)

with open('data.json', 'r') as file:
    data = json.load(file)


# Скрипт заходит на сайты посёлков, запускает загрузку Виртуального тура
# и проверяет, что элемент на нём прогрузился
#
# В лог выводится сообщение "ОК", если этот элемент загрузился
# В лог выводится сообщение "ERROR", если элемент не загрузился
#


# МГ, главная, туры в блоке "Лучшие поселения"
def check_tour(tour_number, balloon_index, z_index_value, max_attempts=3):
    """
    Args:
        tour_number: номер тура для вывода (1, 2, 3)
        balloon_index: локатор кнопки с шаром
        z_index_value: ожидаемое значение z-index для проверки
        max_attempts: максимальное количество попыток (по умолчанию 3)

    Returns:
        True если проверка прошла успешно, False если не прошла после всех попыток
    """
    for attempt in range(1, max_attempts + 1):
        try:
            # Находим и кликаем на кнопку
            btn = wait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, f'(//span[@uk-icon="balloon"])[{balloon_index}]'))
            )
            actions.move_to_element(btn).perform()
            time.sleep(1)
            actions.click(btn).perform()

            # Переключаемся на iframe
            iframe = wait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'uk-lightbox-iframe'))
            )
            driver.switch_to.frame(iframe)

            # Проверяем наличие элемента с нужным z-index
            elem = wait(driver, 20).until(
                EC.visibility_of_element_located((By.XPATH, f"//div[(contains(@style, 'z-index: {z_index_value}'))]"))
            )

            if elem:
                print(f'   OK: МГ, тур{tour_number} на главной')
                driver.switch_to.default_content()
                return True

        except Exception as e:
            driver.switch_to.default_content()

            if attempt < max_attempts:
                driver.refresh()
                time.sleep(2)
            else:
                print(f'ERROR: МГ, тур{tour_number} на главной')
                return False

    return False

# Основной код
try:
    driver.get("https://moigektar.ru/")
    time.sleep(3)  # Даем странице время загрузиться

    # Выполняем все три проверки независимо друг от друга
    # Тур 1 - z-index: 3101
    check_tour(tour_number=1, balloon_index=1, z_index_value='3101', max_attempts=3)

    # Тур 2 - z-index: 308
    check_tour(tour_number=2, balloon_index=2, z_index_value='308', max_attempts=3)

    # Тур 3 - z-index: 230
    check_tour(tour_number=3, balloon_index=3, z_index_value='230', max_attempts=3)

finally:
    driver.refresh()


# Мой гектар, тур на странице актива
count = 0
driver.get("https://moigektar.ru/batches-no-auth/29305")
while count < 3:
    try:
        btn = driver.find_element(by=By.XPATH, value='(//a[@data-type="iframe"])[6]')
        actions.click(btn).perform()
        iframe = driver.find_element(by=By.CLASS_NAME, value='uk-lightbox-iframe')
        driver.switch_to.frame(iframe)
        elem = wait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, "//div[(contains(@style, 'z-index: 3101'))]")))
        if elem:
            print('   OK: тур на странице актива')
            break
    except:
        count += 1
        if count == 3:
            print('ERROR: не загрузился виртур на странице актива')
        else:
            driver.refresh()

# syn_9
count = 0
driver.get("https://syn9.lp.moigektar.ru/")
while count < 3:
    try:
        title = driver.find_element(by=By.ID, value='tour')
        actions.move_to_element(title).perform()
        time.sleep(1)
        btn = driver.find_element(by=By.XPATH, value='//*[(contains(@class, "w-tour__btn"))]')
        actions.click(btn).perform()
        iframe = driver.find_element(by=By.CLASS_NAME, value="uk-lightbox-iframe")
        driver.switch_to.frame(iframe)
        elem = wait(driver, 14).until(EC.visibility_of_element_located((By.XPATH, "//div[(contains(@style, 'z-index: 3056'))]")))
        if elem:
            print('   OK: syn_9')
            break
    except:
        count += 1
        if count == 3:
            print('ERROR: не загрузился виртур на син_9')
        else:
            driver.refresh()

# syn_33
count = 0
driver.get("https://syn33.lp.moigektar.ru/")
while count < 3:
    try:
        title = driver.find_element(by=By.ID, value='tour')
        actions.move_to_element(title).perform()
        time.sleep(1)
        btn = driver.find_element(by=By.XPATH, value='(//*[(contains(@class, "w-plan__btn"))])[1]')
        actions.click(btn).perform()
        iframe = driver.find_element(by=By.CLASS_NAME, value="uk-lightbox-iframe")
        driver.switch_to.frame(iframe)
        elem = wait(driver, 14).until(EC.visibility_of_element_located((By.XPATH, "//div[(contains(@style, 'z-index: 3101'))]")))
        if elem:
            print('   OK: syn_33')
            break
    except:
        count += 1
        if count == 3:
            print('ERROR: не загрузился виртур на син_33')
        else:
            driver.refresh()

# syn_34
count = 0
driver.get("https://syn34.lp.moigektar.ru/")
while count < 3:
    try:
        title = driver.find_element(by=By.ID, value='tour')
        actions.move_to_element(title).perform()
        time.sleep(1)
        btn = driver.find_element(by=By.XPATH, value='//*[(contains(@class, "w-tour__btn"))]')
        actions.click(btn).perform()
        iframe = driver.find_element(by=By.CLASS_NAME, value="uk-lightbox-iframe")
        driver.switch_to.frame(iframe)
        elem = wait(driver, 14).until(EC.visibility_of_element_located((By.XPATH, "//div[(contains(@style, 'z-index: 350'))]")))
        if elem:
            print('   OK: syn_34')
            break
    except:
        count += 1
        if count == 3:
            print('ERROR: не загрузился виртур на син_34')
        else:
            driver.refresh()

# syn_39
count = 0
driver.get("https://syn39.lp.moigektar.ru/")
while count < 3:
    try:
        title = driver.find_element(by=By.XPATH, value='//div[text()[contains(., "Виртуальный тур")]]')
        actions.move_to_element(title).send_keys(Keys.PAGE_DOWN).perform()
        time.sleep(1)
        btn = driver.find_element(by=By.XPATH, value='//*[(contains(@class, "w-tour__btn"))]')
        actions.click(btn).perform()
        iframe = driver.find_element(by=By.CLASS_NAME, value="uk-lightbox-iframe")
        driver.switch_to.frame(iframe)
        elem = wait(driver, 14).until(EC.visibility_of_element_located((By.XPATH, '//div[(contains(@style, "z-index: 155"))]')))
        if elem:
            print('   OK: syn_39')
            break
    except:
        count += 1
        if count == 3:
            print('ERROR: не загрузился виртур на син_39')
        else:
            driver.refresh()

# syn_42
count = 0
driver.get("https://syn42.lp.moigektar.ru/")
while count < 3:
    try:
        title = driver.find_element(by=By.XPATH, value='//div[text()[contains(., "Виртуальный тур")]]')
        actions.move_to_element(title).send_keys(Keys.PAGE_DOWN).perform()
        time.sleep(1)
        btn = driver.find_element(by=By.XPATH, value='//*[(contains(@class, "w-tour__btn"))]')
        actions.click(btn).perform()
        iframe = driver.find_element(by=By.CLASS_NAME, value="uk-lightbox-iframe")
        driver.switch_to.frame(iframe)
        elem = wait(driver, 14).until(EC.visibility_of_element_located((By.XPATH, "//div[(contains(@style, 'z-index: 239'))]")))
        if elem:
            print('   OK: syn_42')
            break
    except:
        count += 1
        if count == 3:
            print('ERROR: не загрузился виртур на син_42')
        else:
            driver.refresh()

# syn_47
driver.get("https://syn47.lp.moigektar.ru/")
count = 0
while count < 3:
    try:
        title = driver.find_element(by=By.ID, value='tour')
        actions.move_to_element(title).perform()
        time.sleep(1)
        btn = driver.find_element(by=By.XPATH, value='//*[(contains(@class, "w-tour__btn"))]')
        actions.click(btn).perform()
        iframe = driver.find_element(by=By.CLASS_NAME, value="uk-lightbox-iframe")
        driver.switch_to.frame(iframe)
        elem = wait(driver, 14).until(EC.visibility_of_element_located((By.XPATH, "//div[(contains(@style, 'z-index: 159'))]")))
        if elem:
            print('   OK: syn_47')
            break
    except:
        count += 1
        if count == 3:
            print('ERROR: не загрузился виртур на син_47')
        else:
            driver.refresh()

# syn_48
count = 0
driver.get("https://syn48.lp.moigektar.ru/")
while count < 3:
    try:
        title = driver.find_element(by=By.ID, value='tour')
        actions.move_to_element(title).perform()
        time.sleep(1)
        btn = driver.find_element(by=By.XPATH, value='//*[(contains(@class, "w-tour__btn"))]')
        actions.click(btn).perform()
        iframe = driver.find_element(by=By.CLASS_NAME, value="uk-lightbox-iframe")
        driver.switch_to.frame(iframe)
        elem = wait(driver, 14).until(EC.visibility_of_element_located((By.XPATH, "//div[(contains(@style, 'z-index: 207'))]")))
        if elem:
            print('   OK: syn_48')
            break
    except:
        count += 1
        if count == 3:
            print('ERROR: не загрузился виртур на син_48')
        else:
            driver.refresh()

# syn_52
count = 0
driver.get("https://syn52.lp.moigektar.ru/")
while count < 3:
    try:
        title = driver.find_element(by=By.ID, value='tour')
        actions.move_to_element(title).perform()
        time.sleep(1)
        btn = driver.find_element(by=By.XPATH, value='//*[(contains(@class, "w-tour__btn"))]')
        actions.click(btn).perform()
        iframe = driver.find_element(by=By.CLASS_NAME, value="uk-lightbox-iframe")
        driver.switch_to.frame(iframe)
        elem = wait(driver, 14).until(EC.visibility_of_element_located((By.XPATH, "//div[(contains(@style, 'z-index: 245'))]")))
        if elem:
            print('   OK: syn_52')
            break
    except:
        count += 1
        if count == 3:
            print('ERROR: не загрузился виртур на син_52')
        else:
            driver.refresh()

# syn_53
count = 0
driver.get("https://syn53.lp.moigektar.ru/")
while count < 3:
    try:
        title = driver.find_element(by=By.XPATH, value='//*[@id="tour"]')
        actions.move_to_element(title).perform()
        time.sleep(1)
        btn = driver.find_element(by=By.XPATH, value='//*[(contains(@class, "w-tour__btn"))]')
        actions.click(btn).perform()
        iframe = driver.find_element(by=By.CLASS_NAME, value="uk-lightbox-iframe")
        driver.switch_to.frame(iframe)
        elem = wait(driver, 14).until(EC.visibility_of_element_located((By.XPATH, "//div[(contains(@style, 'z-index: 306'))]")))
        if elem:
            print('   OK: syn_53')
            break
    except:
        count += 1
        if count == 3:
            print('ERROR: не загрузился виртур на син_53')
        else:
            driver.refresh()

# syn_56
count = 0
driver.get("https://syn56.lp.moigektar.ru/")
while count < 3:
    try:
        title = driver.find_element(by=By.ID, value='tour')
        actions.move_to_element(title).perform()
        time.sleep(1)
        btn = driver.find_element(by=By.XPATH, value='//*[(contains(@class, "w-tour__btn"))]')
        actions.click(btn).perform()
        iframe = driver.find_element(by=By.CLASS_NAME, value="uk-lightbox-iframe")
        driver.switch_to.frame(iframe)
        elem = wait(driver, 14).until(EC.visibility_of_element_located((By.XPATH, "//div[(contains(@style, 'z-index: 230'))]")))
        if elem:
            print('   OK: syn_56')
            break
    except:
        count += 1
        if count == 3:
            print('ERROR: не загрузился виртур на син_56')
        else:
            driver.refresh()

# syn_67
count = 0
driver.get("https://syn67.lp.moigektar.ru/")
while count < 3:
    try:
        title = driver.find_element(by=By.ID, value='tour')
        actions.move_to_element(title).perform()
        time.sleep(1)
        btn = driver.find_element(by=By.XPATH, value='//*[(contains(@class, "w-tour__btn"))]')
        actions.click(btn).perform()
        iframe = driver.find_element(by=By.CLASS_NAME, value="uk-lightbox-iframe")
        driver.switch_to.frame(iframe)
        elem = wait(driver, 14).until(EC.visibility_of_element_located((By.XPATH, "//div[(contains(@style, 'z-index: 3101'))]")))
        if elem:
            print('   OK: syn_67')
            break
    except:
        count += 1
        if count == 3:
            print('ERROR: не загрузился виртур на син_67')
        else:
            driver.refresh()

# syn_73
count = 0
driver.get("https://syn73.lp.moigektar.ru/")
while count < 3:
    try:
        title = driver.find_element(by=By.ID, value='tour')
        actions.move_to_element(title).perform()
        time.sleep(3)
        btn = driver.find_element(by=By.XPATH, value='//*[(contains(@class, "w-tour__btn"))]')
        actions.click(btn).perform()
        iframe = driver.find_element(by=By.CLASS_NAME, value="uk-lightbox-iframe")
        driver.switch_to.frame(iframe)
        elem = wait(driver, 14).until(EC.visibility_of_element_located((By.XPATH, "//div[(contains(@style, 'z-index: 173'))]")))
        if elem:
            print('   OK: syn_73')
            break
    except:
        count += 1
        if count == 3:
            print('ERROR: не загрузился виртур на син_73')
        else:
            driver.refresh()

# syn_74
count = 0
driver.get("https://syn74.lp.moigektar.ru/")
while count < 3:
    try:
        title = driver.find_element(by=By.ID, value='tour')
        actions.move_to_element(title).perform()
        time.sleep(3)
        btn = driver.find_element(by=By.XPATH, value='//*[(contains(@class, "w-tour__icon"))]')
        actions.click(btn).perform()
        iframe = driver.find_element(by=By.CLASS_NAME, value="uk-lightbox-iframe")
        driver.switch_to.frame(iframe)
        elem = wait(driver, 14).until(EC.visibility_of_element_located((By.XPATH, "//div[(contains(@style, 'z-index: 176'))]")))
        if elem:
            print('   OK: syn_74')
            break
    except:
        count += 1
        if count == 3:
            print('ERROR: не загрузился виртур на син_74')
        else:
            driver.refresh()

# syn_84
count = 0
driver.get("https://syn84.lp.moigektar.ru/")
while count < 3:
    try:
        title = driver.find_element(by=By.ID, value='tour')
        actions.move_to_element(title).perform()
        time.sleep(3)
        btn = driver.find_element(by=By.XPATH, value='//*[(contains(@class, "w-tour__btn"))]')
        actions.click(btn).perform()
        iframe = driver.find_element(by=By.CLASS_NAME, value="uk-lightbox-iframe")
        driver.switch_to.frame(iframe)
        elem = wait(driver, 14).until(EC.visibility_of_element_located((By.XPATH, "//div[(contains(@style, 'z-index: 182'))]")))
        if elem:
            print('   OK: syn_84')
            break
    except:
        count += 1
        if count == 3:
            print('ERROR: не загрузился виртур на син_84')
        else:
            driver.refresh()

# syn_85
count = 0
driver.get("https://syn85.lp.moigektar.ru/")
while count < 3:
    try:
        title = driver.find_element(by=By.ID, value='tour')
        actions.move_to_element(title).perform()
        time.sleep(1)
        btn = driver.find_element(by=By.XPATH, value='//*[(contains(@class, "w-tour__btn"))]')
        actions.click(btn).perform()
        iframe = driver.find_element(by=By.CLASS_NAME, value="uk-lightbox-iframe")
        driver.switch_to.frame(iframe)
        elem = wait(driver, 14).until(EC.visibility_of_element_located((By.XPATH, "//div[(contains(@style, 'z-index: 3101'))]")))
        if elem:
            print('   OK: syn_85')
            break
    except:
        count += 1
        if count == 3:
            print('ERROR: не загрузился виртур на син_85')
        else:
            driver.refresh()

# syn_87
count = 0
driver.get("https://syn87.lp.moigektar.ru/")
while count < 3:
    try:
        title = driver.find_element(by=By.ID, value='tour')
        actions.move_to_element(title).perform()
        time.sleep(1)
        btn = driver.find_element(by=By.XPATH, value='//*[(contains(@class, "w-tour__btn"))]')
        actions.click(btn).perform()
        iframe = driver.find_element(by=By.CLASS_NAME, value="uk-lightbox-iframe")
        driver.switch_to.frame(iframe)
        elem = wait(driver, 14).until(EC.visibility_of_element_located((By.XPATH, "//div[(contains(@style, 'z-index: 230'))]")))
        if elem:
            print('   OK: syn_87')
            break
    except:
        count += 1
        if count == 3:
            print('ERROR: не загрузился виртур на син_87')
        else:
            driver.refresh()

# syn_89
count = 0
driver.get("https://syn89.lp.moigektar.ru/")
while count < 3:
    try:
        title = driver.find_element(by=By.ID, value='tour')
        actions.move_to_element(title).perform()
        time.sleep(1)
        btn = driver.find_element(by=By.XPATH, value='//*[(contains(@class, "w-tour__icon"))]')
        actions.click(btn).perform()
        iframe = driver.find_element(by=By.CLASS_NAME, value="uk-lightbox-iframe")
        driver.switch_to.frame(iframe)
        elem = wait(driver, 14).until(EC.visibility_of_element_located((By.XPATH, "//div[(contains(@style, 'z-index: 3101'))]")))
        if elem:
            print('   OK: syn_89')
            break
    except:
        count += 1
        if count == 3:
            print('ERROR: не загрузился виртур на син_89')
        else:
            driver.refresh()

# syn_92
count = 0
driver.get("https://syn92.lp.moigektar.ru/")
while count < 3:
    try:
        title = driver.find_element(by=By.ID, value='tour')
        actions.move_to_element(title).perform()
        time.sleep(1)
        btn = driver.find_element(by=By.XPATH, value='//*[(contains(@class, "w-tour__btn"))]')
        actions.click(btn).perform()
        iframe = driver.find_element(by=By.CLASS_NAME, value="uk-lightbox-iframe")
        driver.switch_to.frame(iframe)
        elem = wait(driver, 14).until(EC.visibility_of_element_located((By.XPATH, "//div[(contains(@style, 'z-index: 189'))]")))
        if elem:
            print('   OK: syn_92')
            break
    except:
        count += 1
        if count == 3:
            print('ERROR: не загрузился виртур на син_92')
        else:
            driver.refresh()

# syn_95
count = 0
driver.get("https://syn95.lp.moigektar.ru/")
while count < 3:
    try:
        title = driver.find_element(by=By.ID, value='tour')
        actions.move_to_element(title).perform()
        time.sleep(1)
        btn = driver.find_element(by=By.XPATH, value='//*[(contains(@class, "w-tour__btn"))]')
        actions.click(btn).perform()
        iframe = driver.find_element(by=By.CLASS_NAME, value="uk-lightbox-iframe")
        driver.switch_to.frame(iframe)
        elem = wait(driver, 14).until(EC.visibility_of_element_located((By.XPATH, "//div[(contains(@style, 'z-index: 227'))]")))
        if elem:
            print('   OK: syn_95')
            break
    except:
        count += 1
        if count == 3:
            print('ERROR: не загрузился виртур на син_95')
        else:
            driver.refresh()

# syn_99
count = 0
driver.get("https://syn99.lp.moigektar.ru/")
while count < 3:
    try:
        title = driver.find_element(by=By.ID, value='tour')
        actions.move_to_element(title).perform()
        time.sleep(1)
        btn = driver.find_element(by=By.XPATH, value='//*[(contains(@class, "w-tour__btn"))]')
        actions.click(btn).perform()
        iframe = driver.find_element(by=By.CLASS_NAME, value="uk-lightbox-iframe")
        driver.switch_to.frame(iframe)
        elem = wait(driver, 14).until(EC.visibility_of_element_located((By.XPATH, "//div[(contains(@style, 'z-index: 201'))]")))
        if elem:
            print('   OK: syn_99')
            break
    except:
        count += 1
        if count == 3:
            print('ERROR: не загрузился виртур на син_99')
        else:
            driver.refresh()

# syn_111
driver.get("https://syn111.lp.moigektar.ru/")
login = driver.find_element(by=By.ID, value='loginconfig-username')
password = driver.find_element(by=By.ID, value='loginconfig-password')
submit = driver.find_element(by=By.CSS_SELECTOR, value='div button')
login.send_keys(str(data["111_cred"]["login"]))
password.send_keys(str(data["111_cred"]["password"]))
submit.click()
time.sleep(2)
count = 0
while count < 3:
    try:
        title = driver.find_element(by=By.ID, value='tour')
        actions.move_to_element(title).perform()
        time.sleep(1)
        btn = driver.find_element(by=By.XPATH, value='//*[(contains(@class, "w-tour__btn"))]')
        actions.click(btn).perform()
        iframe = driver.find_element(by=By.CLASS_NAME, value="uk-lightbox-iframe")
        driver.switch_to.frame(iframe)
        elem = wait(driver, 14).until(EC.visibility_of_element_located((By.XPATH, "//div[(contains(@style, 'z-index: 215'))]")))
        if elem:
            print('   OK: syn_111')
            break
    except:
        count += 1
        if count == 3:
            print('ERROR: не загрузился виртур на син_111')
        else:
            driver.refresh()

time.sleep(5)
driver.quit()

