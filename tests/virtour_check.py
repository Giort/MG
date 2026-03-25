from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import time
import json


# Проверка работы виртуальных туров на сайтах


# Засекаем время начала теста
start_time = time.time()


def init_driver():
    """Инициализация драйвера"""
    ch_options = Options()
    ch_options.add_argument('--headless')
    ch_options.page_load_strategy = 'eager'
    service = ChromeService(executable_path=ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=ch_options)
    driver.set_window_size(1600, 1000)
    driver.implicitly_wait(10)
    return driver

print(f"\n     Проверка доступности виртуальных туров на сайтах \n")


def check_tour(driver, actions, config):
    """
    Универсальная функция проверки виртуального тура

    Args:
        driver: WebDriver экземпляр
        actions: ActionChains экземпляр
        config: Словарь с параметрами:
            - name: название проекта для логов
            - url: URL страницы
            - title_locator: кортеж (By, value) для поиска заголовка/секции
            - btn_locator: кортеж (By, value) для поиска кнопки тура
            - z_index: ожидаемое значение z-index
            - scroll: нужно ли скроллить (опционально, по умолчанию False)
            - wait_time: время ожидания перед кликом (опционально, по умолчанию 1)
            - max_attempts: максимальное количество попыток (опционально, по умолчанию 3)
            - auth: словарь с данными авторизации (опционально)

    Returns:
        True если проверка успешна, False если нет
    """
    name = config['name']
    url = config['url']
    title_locator = config['title_locator']
    btn_locator = config['btn_locator']
    z_index = config['z_index']
    scroll = config.get('scroll', False)
    wait_time = config.get('wait_time', 1)
    max_attempts = config.get('max_attempts', 3)
    auth = config.get('auth', None)

    driver.get(url)

    # Авторизация, если нужна
    if auth:
        try:
            login = driver.find_element(By.XPATH, '//*[@id="loginconfig-username"]')
            password = driver.find_element(By.XPATH, '//*[@id="loginconfig-password"]')
            submit = driver.find_element(By.CSS_SELECTOR, 'div button')
            login.send_keys(str(auth["login"]))
            password.send_keys(str(auth["password"]))
            submit.click()
            time.sleep(2)
        except Exception as e:
            print(f'WARNING: Ошибка авторизации на {name}: {e}')

    count = 0
    while count < max_attempts:
        try:
            # Находим заголовок/секцию и перемещаемся к ней
            title = driver.find_element(*title_locator)
            actions.move_to_element(title).perform()

            # Скроллим, если нужно
            if scroll:
                actions.send_keys(Keys.PAGE_DOWN).perform()

            time.sleep(wait_time)

            # Находим и кликаем кнопку тура
            btn = driver.find_element(*btn_locator)
            actions.click(btn).perform()

            # Переключаемся на iframe
            iframe = driver.find_element(By.CLASS_NAME, "uk-lightbox-iframe")
            driver.switch_to.frame(iframe)

            # Проверяем наличие элемента с нужным z-index
            elem = wait(driver, 30).until(
                EC.visibility_of_element_located((By.XPATH, f"//div[(contains(@style, 'z-index: {z_index}'))]"))
            )

            if elem:
                print(f'     OK: {name}')
                driver.switch_to.default_content()
                return True

        except Exception:
            driver.switch_to.default_content()
            count += 1
            if count == max_attempts:
                print(f'ERROR: не загрузился виртур на {name}')
                return False
            else:
                driver.refresh()

    return False


# =============================================================================
# КОНФИГУРАЦИИ ПРОВЕРОК
# =============================================================================

# Общие локаторы
TITLE_MG_MAIN_PAGE = (By.XPATH, '//*[text()[contains(., "Лучшие поселения месяца")]]')
TITLE_BY_ID_TOUR = (By.ID, 'tour')
TITLE_34_1 = (By.XPATH, '(//*[text()[contains(., "в Подмосковье»")]])[7]')
TITLE_34_2 = (By.XPATH, '(//*[text()[contains(., "«Экополис»")]])[1]')
TITLE_89_1 = (By.XPATH, '(//h5[text()[contains(., "Оазис на Осуге")]])[1]')
TITLE_89_2 = (By.XPATH, '(//h5[text()[contains(., "на озере Шитовское")]])[1]')
TITLE_89_3 = (By.XPATH, '(//h5[text()[contains(., "на Большом озере")]])[1]')
TITLE_98 = (By.XPATH, '(//h5[text()[contains(., "Оазис в Завидово")]])[1]')
BTN_TOUR_CLASS = (By.XPATH, '//*[(contains(@class, "w-tour__btn"))]')
BTN_TOUR_ICON = (By.XPATH, '//*[(contains(@class, "w-tour__icon"))]')
BTN_PLAN_CLASS = (By.XPATH, '(//*[(contains(@class, "w-plan__btn"))])[1]')
BTN_34_1 = (By.XPATH, '(//img[@src="/img/360.svg"])[1]')
BTN_34_2 = (By.XPATH, '(//img[@src="/img/360.svg"])[2]')
BTN_89_1 = (By.XPATH, '(//img[@src="/img/360.svg"])[1]')
BTN_89_2 = (By.XPATH, '(//img[@src="/img/360.svg"])[2]')
BTN_89_3 = (By.XPATH, '(//img[@src="/img/360.svg"])[3]')
BTN_98 = (By.XPATH, '(//img[@src="/img/360.svg"])[1]')

# Конфигурации проверок
tour_configs = [
    # МГ - туры на главной
    {
        'name': 'МГ, тур1 на главной',
        'url': 'https://moigektar.ru',
        'title_locator': TITLE_MG_MAIN_PAGE,
        'btn_locator': (By.XPATH, '(//*[@class="w-lord"])[1]'),
        'z_index': '188',
    },
    {
        'name': 'МГ, тур2 на главной',
        'url': 'https://moigektar.ru',
        'title_locator': TITLE_MG_MAIN_PAGE,
        'btn_locator': (By.XPATH, '(//*[@class="w-lord"])[2]'),
        'z_index': '332',
    },
    {
        'name': 'МГ, тур3 на главной',
        'url': 'https://moigektar.ru',
        'title_locator': TITLE_MG_MAIN_PAGE,
        'btn_locator': (By.XPATH, '(//*[@class="w-lord"])[3]'),
        'z_index': '176',
    },

    # МГ - тур на странице актива
    {
        'name': 'МГ, тур на странице актива',
        'url': 'https://moigektar.ru/batches-no-auth/29305',
        'title_locator': (By.XPATH, '(//a[@data-type="iframe"])[6]'),
        'btn_locator': (By.XPATH, '(//a[@data-type="iframe"])[6]'),
        'z_index': '182',
    },

    # Проекты с ID tour и кнопкой w-tour__btn
    {
        'name': 'syn_9',
        'url': 'https://syn9.lp.moigektar.ru/',
        'title_locator': TITLE_BY_ID_TOUR,
        'btn_locator': BTN_TOUR_CLASS,
        'z_index': '3056',
    },
    {
        'name': 'syn_33',
        'url': 'https://syn33.lp.moigektar.ru/',
        'title_locator': TITLE_BY_ID_TOUR,
        'btn_locator': BTN_PLAN_CLASS,
        'z_index': '3101',
    },
    {
        'name': 'syn_34_1',
        'url': 'https://syn34.lp.moigektar.ru/',
        'title_locator': TITLE_34_1,
        'btn_locator': BTN_34_1,
        'z_index': '350',
    },
    {
        'name': 'syn_34_2',
        'url': 'https://syn34.lp.moigektar.ru/',
        'title_locator': TITLE_34_2,
        'btn_locator': BTN_34_2,
        'z_index': '176',
    },
    {
        'name': 'syn_35',
        'url': 'https://syn35.lp.moigektar.ru/',
        'title_locator': TITLE_BY_ID_TOUR,
        'btn_locator': BTN_TOUR_CLASS,
        'z_index': '3101',
    },
    {
        'name': 'syn_39',
        'url': 'https://syn39.lp.moigektar.ru/',
        'title_locator': TITLE_BY_ID_TOUR,
        'btn_locator': BTN_TOUR_CLASS,
        'z_index': '155',
        'scroll': True,
    },
    {
        'name': 'syn_42',
        'url': 'https://syn42.lp.moigektar.ru/',
        'title_locator': TITLE_BY_ID_TOUR,
        'btn_locator': BTN_TOUR_CLASS,
        'z_index': '239',
        'scroll': True,
    },
    {
        'name': 'syn_47',
        'url': 'https://syn47.lp.moigektar.ru/',
        'title_locator': TITLE_BY_ID_TOUR,
        'btn_locator': BTN_TOUR_CLASS,
        'z_index': '173',
    },
    {
        'name': 'syn_48',
        'url': 'https://syn48.lp.moigektar.ru/',
        'title_locator': TITLE_BY_ID_TOUR,
        'btn_locator': BTN_TOUR_CLASS,
        'z_index': '207',
    },
    {
        'name': 'syn_52',
        'url': 'https://syn52.lp.moigektar.ru/',
        'title_locator': TITLE_BY_ID_TOUR,
        'btn_locator': BTN_TOUR_CLASS,
        'z_index': '245',
    },
    {
        'name': 'syn_53',
        'url': 'https://syn53.lp.moigektar.ru/',
        'title_locator': TITLE_BY_ID_TOUR,
        'btn_locator': BTN_TOUR_CLASS,
        'z_index': '332',
    },
    {
        'name': 'syn_56',
        'url': 'https://syn56.lp.moigektar.ru/',
        'title_locator': TITLE_BY_ID_TOUR,
        'btn_locator': BTN_TOUR_CLASS,
        'z_index': '230',
    },
    {
        'name': 'syn_67',
        'url': 'https://syn67.lp.moigektar.ru/',
        'title_locator': TITLE_BY_ID_TOUR,
        'btn_locator': BTN_TOUR_CLASS,
        'z_index': '3101',
    },
    {
        'name': 'syn_73',
        'url': 'https://syn73.lp.moigektar.ru/',
        'title_locator': TITLE_BY_ID_TOUR,
        'btn_locator': BTN_TOUR_CLASS,
        'z_index': '173',
        'wait_time': 3,
    },
    {
        'name': 'syn_74',
        'url': 'https://syn74.lp.moigektar.ru/',
        'title_locator': TITLE_BY_ID_TOUR,
        'btn_locator': BTN_TOUR_ICON,
        'z_index': '188',
        'wait_time': 3,
    },
    {
        'name': 'syn_84',
        'url': 'https://syn84.lp.moigektar.ru/',
        'title_locator': TITLE_BY_ID_TOUR,
        'btn_locator': BTN_TOUR_CLASS,
        'z_index': '182',
        'wait_time': 3,
    },
    {
        'name': 'syn_85',
        'url': 'https://syn85.lp.moigektar.ru/',
        'title_locator': TITLE_BY_ID_TOUR,
        'btn_locator': BTN_TOUR_CLASS,
        'z_index': '3101',
    },
    {
        'name': 'syn_87',
        'url': 'https://syn87.lp.moigektar.ru/',
        'title_locator': TITLE_BY_ID_TOUR,
        'btn_locator': BTN_TOUR_CLASS,
        'z_index': '230',
    },
    {
        'name': 'syn_89_1',
        'url': 'https://syn89.lp.moigektar.ru/',
        'title_locator': TITLE_89_1,
        'btn_locator': BTN_89_1,
        'z_index': '161',
    },
    {
        'name': 'syn_89_2',
        'url': 'https://syn89.lp.moigektar.ru/',
        'title_locator': TITLE_89_2,
        'btn_locator': BTN_89_2,
        'z_index': '155',
    },
    {
        'name': 'syn_89_3',
        'url': 'https://syn89.lp.moigektar.ru/',
        'title_locator': TITLE_89_3,
        'btn_locator': BTN_89_3,
        'z_index': '176',
    },
    {
        'name': 'syn_92',
        'url': 'https://syn92.lp.moigektar.ru/',
        'title_locator': TITLE_BY_ID_TOUR,
        'btn_locator': BTN_TOUR_CLASS,
        'z_index': '189',
    },
    {
        'name': 'syn_95',
        'url': 'https://syn95.lp.moigektar.ru/',
        'title_locator': TITLE_BY_ID_TOUR,
        'btn_locator': BTN_TOUR_CLASS,
        'z_index': '275',
    },
    {
        'name': 'syn_99',
        'url': 'https://syn99.lp.moigektar.ru/',
        'title_locator': TITLE_BY_ID_TOUR,
        'btn_locator': BTN_TOUR_CLASS,
        'z_index': '181',
    },
    {
        'name': 'syn_447',
        'url': 'https://syn447.lp.moigektar.ru/',
        'title_locator': TITLE_BY_ID_TOUR,
        'btn_locator': BTN_TOUR_CLASS,
        'z_index': '263',
    },

    # Проекты с другими локаторами
    {
        'name': 'syn_74',
        'url': 'https://syn74.lp.moigektar.ru/',
        'title_locator': TITLE_BY_ID_TOUR,
        'btn_locator': BTN_TOUR_ICON,
        'z_index': '188',
        'wait_time': 3,
    },
    {
        'name': 'syn_33',
        'url': 'https://syn33.lp.moigektar.ru/',
        'title_locator': TITLE_BY_ID_TOUR,
        'btn_locator': BTN_PLAN_CLASS,
        'z_index': '3101',
    },
    {
        'name': 'syn_34_1',
        'url': 'https://syn34.lp.moigektar.ru/',
        'title_locator': TITLE_34_1,
        'btn_locator': BTN_34_1,
        'z_index': '350',
    },
    {
        'name': 'syn_34_2',
        'url': 'https://syn34.lp.moigektar.ru/',
        'title_locator': TITLE_34_2,
        'btn_locator': BTN_34_2,
        'z_index': '176',
    },
    {
        'name': 'syn_89_1',
        'url': 'https://syn89.lp.moigektar.ru/',
        'title_locator': TITLE_89_1,
        'btn_locator': BTN_89_1,
        'z_index': '161',
    },
    {
        'name': 'syn_89_2',
        'url': 'https://syn89.lp.moigektar.ru/',
        'title_locator': TITLE_89_2,
        'btn_locator': BTN_89_2,
        'z_index': '155',
    },
    {
        'name': 'syn_89_3',
        'url': 'https://syn89.lp.moigektar.ru/',
        'title_locator': TITLE_89_3,
        'btn_locator': BTN_89_3,
        'z_index': '176',
    },
]


def main():
    """
    Скрипт заходит на сайты посёлков, запускает загрузку Виртуального тура
    и проверяет, что элемент на нём прогрузился

    В лог выводится сообщение "ОК", если этот элемент загрузился
    В лог выводится сообщение "ERROR", если элемент не загрузился
    """

    # Загрузка данных для авторизации
    try:
        with open('../data/data.json', 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        data = None
        print("WARNING: файл data.json не найден, авторизация будет пропущена")

    # Инициализация драйвера
    driver = init_driver()
    actions = ActionChains(driver)

    try:

        for config in tour_configs:
            check_tour(driver, actions, config)

        # === syn_111 - С АВТОРИЗАЦИЕЙ ===
        if data:
            syn111_config = {
                'name': 'syn_111',
                'url': 'https://syn111.lp.moigektar.ru/',
                'title_locator': TITLE_BY_ID_TOUR,
                'btn_locator': BTN_TOUR_CLASS,
                'z_index': '215',
                'auth': data.get("111_cred", {}),
            }
            check_tour(driver, actions, syn111_config)

            syn98_config = {
                'name': 'syn_98',
                'url': 'https://syn98.lp.moigektar.ru/',
                'title_locator': TITLE_98,
                'btn_locator': BTN_98,
                'z_index': '158',
                'auth': data.get("98_cred", {}),
            }
            check_tour(driver, actions, syn98_config)

    finally:
        time.sleep(5)
        driver.quit()


if __name__ == "__main__":
    main()


# Вычисляем и выводим время выполнения теста
end_time = time.time()
elapsed_time = end_time - start_time
minutes = int(elapsed_time // 60)
seconds = int(elapsed_time % 60)

if minutes > 0:
    print(f'\n     Время выполнения теста: {minutes} мин {seconds} сек ({elapsed_time:.2f} сек)')
else:
    print(f'\n     Время выполнения теста: {seconds} сек ({elapsed_time:.2f} сек)')
