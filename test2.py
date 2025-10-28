from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
ch_options = Options()
# ch_options.add_argument('--headless')
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


def check_tour(tour_number, balloon_index, z_index_value, max_attempts=3):
    """
    Проверяет виртуальный тур на главной странице МГ

    Args:
        tour_number: номер тура для вывода (1, 2, 3)
        balloon_index: индекс кнопки с баллоном в XPath (1, 2, 3)
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
    # Закрываем драйвер
    driver.quit()
