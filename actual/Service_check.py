from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException, InvalidArgumentException
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time
from datetime import datetime
import json


# Засекаем время начала теста
start_time = time.time()

# Инициализация драйвера
def init_driver():
    ch_options = Options()
    ch_options.add_argument('--headless')
    ch_options.page_load_strategy = 'eager'
    service = ChromeService(executable_path=ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=ch_options)
    driver.set_window_size(1680, 1000)
    driver.implicitly_wait(10)
    return driver

print(f"\n     Проверка доступности сайтов \n")

# Универсальный метод проверки сервиса
def check_service(driver, config, data=None):
    """
    Проверяет доступность сервиса по заданной конфигурации

    Args:
        driver: WebDriver экземпляр
        config: Словарь с параметрами проверки
        data: Данные для авторизации (если нужны)
    """
    url = config['url']
    name = config['name']
    xpath = config['xpath']
    auth = config.get('auth', None)
    max_attempts = config.get('max_attempts', 3)
    wait_timeout = config.get('wait_timeout', 14)
    project = config.get('_project', None)  # Название проекта (если есть)

    try:
        driver.get(url)
        time.sleep(1)
    except InvalidArgumentException:
        if project:
            print(f'ERROR: [{project}] {name}')
        else:
            print(f'ERROR: {name}')
        return False

    # Авторизация, если нужна
    if auth and data:
        try:
            if auth == 'turportal':
                driver.find_element(By.CSS_SELECTOR, 'input[id=loginconfig-username]').send_keys(
                    str(data["turporlal_cred"]["login"]))
                driver.find_element(By.CSS_SELECTOR, 'input[id=loginconfig-password]').send_keys(
                    str(data["turporlal_cred"]["password"]))
                driver.find_element(By.CSS_SELECTOR, 'button[type]').click()
                time.sleep(5)
            elif auth == 'syn111':
                driver.find_element(By.ID, 'loginconfig-username').send_keys(str(data["111_cred"]["login"]))
                driver.find_element(By.ID, 'loginconfig-password').send_keys(str(data["111_cred"]["password"]))
                driver.find_element(By.CSS_SELECTOR, 'div button').click()
                time.sleep(2)
        except Exception as e:
            print(f'WARNING: Ошибка авторизации на {name}: {e}')

    # Проверка элемента
    count = 0
    while count < max_attempts:
        try:
            elem = wait(driver, wait_timeout).until(EC.visibility_of_element_located((By.XPATH, xpath)))
            if elem:
                if project:
                    print(f'     OK: [{project}] {name}')
                else:
                    print(f'     OK: {name}')

                # Удаляем куки только если указан флаг clear_cookies (это для того, чтобы вход в ЛК под демо не влиял на
                # отображение интерфейса на зависящих сайтах)
                if config.get('clear_cookies', False):
                    driver.delete_all_cookies()
                    time.sleep(10)  # Даём время на применение удаления кук

                return True
        except:
            count += 1
            if count == max_attempts:
                if project:
                    print(f'ERROR: [{project}] {name}')
                else:
                    print(f'ERROR: {name}')

                # Удаляем куки только если указан флаг clear_cookies
                if config.get('clear_cookies', False):
                    driver.delete_all_cookies()
                    time.sleep(0.5)  # Даём время на применение удаления кук

                return False
            else:
                driver.refresh()
                # Повторная авторизация после обновления страницы
                if auth and data:
                    try:
                        if auth == 'turportal':
                            driver.find_element(By.CSS_SELECTOR, 'input[id=loginconfig-username]').send_keys(
                                str(data["turportal_cred"]["login"]))
                            driver.find_element(By.CSS_SELECTOR, 'input[id=loginconfig-password]').send_keys(
                                str(data["turportal_cred"]["password"]))
                            driver.find_element(By.CSS_SELECTOR, 'button[type]').click()
                            time.sleep(5)
                        elif auth == 'syn111':
                            driver.find_element(By.ID, 'loginconfig-username').send_keys(str(data["111_cred"]["login"]))
                            driver.find_element(By.ID, 'loginconfig-password').send_keys(
                                str(data["111_cred"]["password"]))
                            driver.find_element(By.CSS_SELECTOR, 'div button').click()
                    except:
                        pass
    return False


# Вспомогательная функция для создания конфигураций проектов с несколькими доменами
def create_project_configs(project_name, domains, xpath, auth=None):
    """
    Создает список конфигураций для одного проекта с несколькими доменами

    Args:
        project_name: Название проекта (отображается в логах)
        domains: Список кортежей (название, url)
        xpath: Общий xpath для всех доменов проекта
        auth: Тип авторизации (если нужна)

    Returns:
        Список конфигураций для всех доменов проекта

    Пример использования:
        *create_project_configs(
            'syn_67',
            [
                ('syn_67', 'https://syn67.lp.moigektar.ru'),
                ('me.lp.moigektar.ru', 'https://me.lp.moigektar.ru'),
                ('моепоместье.рф', 'https://моепоместье.рф'),
            ],
            XPATH_W_DESCR
        )

    При ошибке выведет:
        ERROR: [syn_67] me.lp.moigektar.ru
    """
    configs = []
    for name, url in domains:
        config = {
            'name': name,
            'url': url,
            'xpath': xpath,
            '_project': project_name  # Метка проекта для группировки в логах
        }
        if auth:
            config['auth'] = auth
        configs.append(config)
    return configs


# =============================================================================
# КОНФИГУРАЦИИ XPATH ДЛЯ ГРУПП ПРОЕКТОВ
# =============================================================================
# Все повторяющиеся xpath вынесены в константы для удобства изменения

XPATH_CHOOSE_PLOT = '//h2[text()[contains(.,"Выбрать участок")]]'
XPATH_W_DESCR = '//a[@href="#w-descr"]'
XPATH_INTERACTIVE = '//span[text()[contains(.,"Интерактивный")]]'
XPATH_GENPLAN = '//span[text()[contains(.,"Генеральный")]]'
XPATH_VIRTUAL_TOURS = '//span[text()[contains(.,"Виртуальные")]]'
XPATH_UNIQUE_ECORESORT = '//h3[text()[contains(., "Уникальный экокурорт")]]'
XPATH_20_SOTOK = '//*[text()[contains(.,"20 соток ИЖС")]]'
XPATH_W_MAIN = '(//a[@href="#w-main"])[1]'
XPATH_CLUB_VILLAGE = '//*[text()[contains(., "Клубный поселок")]]'
XPATH_BOOK = '//h3[text()[contains(.,"Забронировать")]]'
XPATH_CONCEPT = '//*[text()[contains(., "Концепция")]]'
XPATH_LAKE_REGION = '//*[text()[contains(.,"Озерный край: ")]]'
XPATH_EMPRESS_ESTATE = '//*[text()[contains(., "«Усадьба Императрицы»")]]'
XPATH_CLUB_SETTLEMENT = '(//*[text()[contains(.,"Клубный посёлок")]])[1]'
XPATH_BAIKAL_ESTATE = '//*[text()[contains(., "Усадьба на Байкале» — это:")]]'

# =============================================================================
# МАССИВ КОНФИГУРАЦИЙ ДЛЯ ВСЕХ СЕРВИСОВ
# =============================================================================

services_config = [
    # === ОСНОВНЫЕ СЕРВИСЫ ===
    {
        'name': 'МГ',
        'url': 'https://moigektar.ru',
        'xpath': '//h2[text()[contains(.,"Описание проекта")]]'
    },
    {
        'name': 'ЛК',
        'url': 'https://cabinet.moigektar.ru',
        'xpath': '(//*[text()[contains(.,"Вы находитесь в демо-версии личного кабинета")]])[2]',
        'clear_cookies': True  # Удаляем куку _identity после проверки
    },
    {
        'name': 'YouTrack',
        'url': 'https://youtrack.bug.land',
        'xpath': '(//*[text()[contains(.,"Вы находитесь в демо-версии личного кабинета")]])[2]'
    },

    # === ПРОЕКТ: syn_6 Почурино ===
    *create_project_configs(
        'syn_6 Почурино',
        [
            ('syn_6', 'https://syn6.lp.moigektar.ru'),
            ('pochurino.moigektar.ru', 'https://pochurino.moigektar.ru'),
        ],
        XPATH_CHOOSE_PLOT
    ),

    # === ПРОЕКТ: syn_8 Долина Селигера ===
    {
        'name': '[syn_8 Долина Селигера]',
        'url': 'https://syn8.lp.moigektar.ru',
        'xpath': XPATH_GENPLAN
    },

    # === ПРОЕКТ: syn_9 Бологое ===
    *create_project_configs(
        'syn_9 Бологое',
        [
            ('syn_9', 'https://syn9.lp.moigektar.ru'),
            ('синергия-бологое.рф', 'https://xn----btbecgepc3aoqbbtl4u.xn--p1ai'),
            ('усадьба-бологое.рф', 'https://xn----7sbadcmcn6c3abb2a1a2l.xn--p1ai'),
        ],
        XPATH_W_DESCR
    ),

    # === ПРОЕКТ: syn_11 Синергия-Мирный ===
    *create_project_configs(
        'syn_11 Синергия-Мирный',
        [
            ('syn_11', 'https://syn11.lp.moigektar.ru'),
            ('синергия-мирный.рф', 'http://синергия-мирный.рф'),
        ],
        XPATH_INTERACTIVE
    ),

    # === ПРОЕКТ: syn_12 Синергия-Волга ===
    *create_project_configs(
        'syn_12 Синергия-Волга',
        [
            ('syn_12', 'https://syn12.lp.moigektar.ru'),
            ('синергия-волга.рф', 'http://синергия-волга.рф'),
            ('1za-100.ru', 'http://1za-100.ru'),
        ],
        XPATH_INTERACTIVE
    ),

    # === ПРОЕКТ: syn_14 Русская Венеция ===
    *create_project_configs(
        'syn_14 Русская Венеция',
        [
            ('syn_14', 'https://syn14.lp.moigektar.ru'),
            ('1ga100.ru', 'http://1ga100.ru'),
        ],
        XPATH_INTERACTIVE
    ),

    # === ПРОЕКТ: syn_15 Агро-Усадьба ===
    {
        'name': '[syn_15 Агро-Усадьба]',
        'url': 'https://syn15.lp.moigektar.ru',
        'xpath': '//span[text()[contains(.,"Виртуальные туры")]]'
    },

    # === ПРОЕКТ: syn_16 Синергия-Митино ===
    *create_project_configs(
        'syn_16 Синергия-Митино',
        [
            ('syn_16', 'https://syn16.lp.moigektar.ru'),
            ('синергия-митино.рф', 'http://синергия-митино.рф'),
        ],
        XPATH_INTERACTIVE
    ),

    # === ПРОЕКТ: syn_17 Агро-Мирный ===
    {
        'name': '[syn_17 Агро-Мирный]',
        'url': 'https://syn17.lp.moigektar.ru',
        'xpath': XPATH_VIRTUAL_TOURS
    },

    # === ПРОЕКТ: syn_18 Почурино 2 ===
    *create_project_configs(
        'Почурино 2',
        [
            ('syn_18', 'https://syn18.lp.moigektar.ru'),
            ('почурино.рф', 'https://почурино.рф'),
            ('почурино-ижс.рф', 'https://почурино-ижс.рф'),
        ],
        XPATH_INTERACTIVE
    ),

    # === ПРОЕКТ: syn_23 Долина Вазузы ===
    {
        'name': '[syn_23 Долина Вазузы]',
        'url': 'https://syn23.lp.moigektar.ru',
        'xpath': XPATH_UNIQUE_ECORESORT
    },

    # === ПРОЕКТ: syn_24 Княжьи Горы ===
    *create_project_configs(
        'syn_24 Княжьи Горы',
        [
            ('syn_24', 'https://syn24.lp.moigektar.ru'),
            ('княжьигоры.рф', 'https://княжьигоры.рф'),
        ],
        XPATH_GENPLAN
    ),

    # === ПРОЕКТ: syn_29-56 Усадьба на Волге 1 и 6 ===
    *create_project_configs(
        'syn_29-56 Усадьба на Волге 1 и 6',
        [
            ('syn_29', 'https://syn29.lp.moigektar.ru'),
            ('syn_37', 'https://syn37.lp.moigektar.ru'),
            ('syn_56', 'https://syn56.lp.moigektar.ru'),
            ('усадьба-на-волге.рф', 'https://усадьба-на-волге.рф'),
        ],
        XPATH_W_DESCR
    ),

    # === ПРОЕКТ: syn_33 ===
    *create_project_configs(
        'syn_33',
        [
            ('syn_33', 'https://syn33.lp.moigektar.ru'),
            ('syn33v2.lp.moigektar.ru', 'https://syn33v2.lp.moigektar.ru'),
            ('лисицыно.рф', 'http://лисицыно.рф'),
            ('поселок-лисицино.рф', 'http://поселок-лисицино.рф'),
            ('лисицино.рф', 'https://лисицино.рф'),
        ],
        XPATH_W_DESCR
    ),

    # === ПРОЕКТ: syn_34 ===
    *create_project_configs(
        'syn_34',
        [
            ('syn_34', 'https://syn34.lp.moigektar.ru'),
            ('syn63.lp.moigektar.ru', 'https://syn63.lp.moigektar.ru'),
            ('усадьба-в-подмосковье.рф', 'https://усадьба-в-подмосковье.рф'),
        ],
        XPATH_20_SOTOK
    ),

    # === ПРОЕКТ: syn_35 Усадьба подо Ржевом===
    *create_project_configs(
        'syn_35 Усадьба подо Ржевом',
        [
            ('syn_35', 'https://syn35.lp.moigektar.ru'),
            ('усадьба-ржев.рф', 'https://усадьба-ржев.рф'),
        ],
        XPATH_W_MAIN
    ),

    # === ПРОЕКТ: syn_25-26-28-31-32-36-64 Победа ===
    *create_project_configs(
        'syn_25-26-28-31-32-36-64 Победа',
        [
            ('syn_25', 'https://syn25.lp.moigektar.ru'),
            ('syn_26', 'https://syn26.lp.moigektar.ru'),
            ('syn_28', 'https://syn28.lp.moigektar.ru'),
            ('syn_31', 'https://syn31.lp.moigektar.ru'),
            ('syn_32', 'https://syn32.lp.moigektar.ru'),
            ('syn_36', 'https://syn36.lp.moigektar.ru'),
            ('syn_64', 'https://syn64.lp.moigektar.ru'),
            ('pobeda.lp.moigektar.ru', 'https://pobeda.lp.moigektar.ru'),
            ('поселок-победа.рф', 'https://поселок-победа.рф'),
        ],
        XPATH_GENPLAN
    ),

    # === ПРОЕКТ: syn_39 Лесная Усадьба ===
    *create_project_configs(
        'syn_39 Лесная Усадьба',
        [
            ('syn_39', 'https://syn39.lp.moigektar.ru'),
            ('syn39-v2.lp.moigektar.ru', 'https://syn39-v2.lp.moigektar.ru'),
            ('лесная-усадьба.рф', 'https://лесная-усадьба.рф'),
        ],
        XPATH_W_DESCR
    ),

    # === ПРОЕКТ: syn_42 Усадьба в Завидово ===
    *create_project_configs(
        'syn_42 Усадьба в Завидово',
        [
            ('syn_42', 'https://syn42.lp.moigektar.ru'),
            ('усадьба-в-завидово.рф', 'https://усадьба-в-завидово.рф'),
        ],
        XPATH_W_DESCR
    ),

    # === ПРОЕКТ: syn_47 Synergy Island (активы 62) ===
    {
        'name': '[syn_47 Synergy Island] (активы 62)',
        'url': 'https://syn47.lp.moigektar.ru',
        'xpath': XPATH_CLUB_VILLAGE
    },

    # === ПРОЕКТ: syn_48-97-105 Парк Патриот ===
    *create_project_configs(
        'syn_48-97-105 Парк Патриот',
        [
            ('syn_48', 'https://syn48.lp.moigektar.ru'),
            ('syn48-v2.lp.moigektar.ru', 'https://syn48-v2.lp.moigektar.ru'),
            ('парк-патриот.рф', 'https://парк-патриот.рф'),
        ],
        XPATH_W_DESCR
    ),

    # === ПРОЕКТ: syn_52 Долина Волги ===
    *create_project_configs(
        'syn_52 Долина Волги',
        [
            ('syn_52', 'https://syn52.lp.moigektar.ru'),
            ('долина-волги.рф', 'https://долина-волги.рф'),
            ('долинаволги.рф', 'https://долинаволги.рф'),
        ],
        XPATH_W_MAIN
    ),

    # === ПРОЕКТ: syn_53 Новая Жизнь ===
    *create_project_configs(
        'syn_53 Новая Жизнь',
        [
            ('syn_53', 'https://syn53.lp.moigektar.ru'),
            ('новая-жизнь.рф', 'https://новая-жизнь.рф'),
        ],
        XPATH_W_DESCR
    ),

    # === ПРОЕКТ: syn_58 Волга-Путилово ===
    *create_project_configs(
        'syn_58 Волга-Путилово',
        [
            ('syn_58', 'https://syn58.lp.moigektar.ru'),
            ('волга-путилово.рф', 'https://волга-путилово.рф'),
        ],
        XPATH_BOOK
    ),

    # === ПРОЕКТ: vazuza2 Долина Вазузы ===
    *create_project_configs(
        'vazuza2 Долина Вазузы',
        [
            ('vazuza2.lp.moigektar.ru', 'https://vazuza2.lp.moigektar.ru'),
            ('dolina-vazuza.ru', 'https://dolina-vazuza.ru'),
            ('долина-вазузы.рф', 'https://долина-вазузы.рф'),
            ('долина-вазуза.рф', 'https://долина-вазуза.рф'),
        ],
        XPATH_UNIQUE_ECORESORT
    ),

    # === ПРОЕКТ: syn_61 Долина Селигера (Антоново) ===
    *create_project_configs(
        'syn_61 Долина Селигера (Антоново)',
        [
            ('syn_61', 'https://syn61.lp.moigektar.ru'),
            ('долина-селигера.рф', 'https://долина-селигера.рф'),
        ],
        XPATH_GENPLAN
    ),

    # === ПРОЕКТ: syn_67 Моё Поместье ===
    *create_project_configs(
        'syn_67 Моё Поместье',
        [
            ('syn_67', 'https://syn67.lp.moigektar.ru'),
            ('me.lp.moigektar.ru', 'https://me.lp.moigektar.ru'),
            ('me-v2.lp.moigektar.ru', 'https://me-v2.lp.moigektar.ru'),
            ('моепоместье.рф', 'https://моепоместье.рф'),
        ],
        XPATH_W_DESCR
    ),

    # === ПРОЕКТ: syn_73 Ясные Зори===
    *create_project_configs(
        'syn_73 Ясные Зори',
        [
            ('syn_73', 'https://syn73.lp.moigektar.ru'),
            ('ясные-зори.рф', 'https://ясные-зори.рф'),
        ],
        XPATH_W_DESCR
    ),

    # === ПРОЕКТ: syn_74 Междуречье syn_75 Устье ===
    *create_project_configs(
        'syn_74 Междуречье syn_75 Устье',
        [
            ('syn_74', 'https://syn74.lp.moigektar.ru'),
            ('междуречье-волги.рф', 'https://междуречье-волги.рф'),
        ],
        XPATH_CONCEPT
    ),

    # === ПРОЕКТ: syn_83-84 Малая Родина ===
    *create_project_configs(
        'syn_83-84 Малая Родина',
        [
            ('syn_83', 'https://syn83.lp.moigektar.ru'),
            ('syn_84', 'https://syn84.lp.moigektar.ru'),
            ('малая-родина.рф', 'https://малая-родина.рф'),
        ],
        XPATH_W_DESCR
    ),

    # === ПРОЕКТ: syn_85 Междуречье на Валдае ===
    *create_project_configs(
        'syn_85 Междуречье на Валдае',
        [
            ('syn_85', 'https://syn85.lp.moigektar.ru'),
            ('междуречье-на-валдае.рф', 'https://междуречье-на-валдае.рф'),
            ('междуречье-валдай.рф', 'https://междуречье-валдай.рф'),
            ('синергия-междуречье.рф', 'https://синергия-междуречье.рф'),
        ],
        XPATH_W_DESCR
    ),

    # === ПРОЕКТ: syn_19-44-87 Москва-Тверская ===
    *create_project_configs(
        'syn_19-44-87 Москва-Тверская',
        [
            ('syn_19', 'https://syn19.lp.moigektar.ru'),
            ('syn_87', 'https://syn87.lp.moigektar.ru'),
            ('mt.lp.moigektar.ru', 'https://mt.lp.moigektar.ru'),
            ('москва-тверская.рф', 'https://москва-тверская.рф'),
        ],
        XPATH_W_DESCR
    ),

    # === ПРОЕКТ: syn_89 Долина Озёр===
    *create_project_configs(
        'syn_89 Долина Озёр',
        [
            ('syn_89', 'https://syn89.lp.moigektar.ru'),
            ('lakes-valley.lp.moigektar.ru', 'https://lakes-valley.lp.moigektar.ru'),
            ('долина-озер.рф', 'https://долина-озер.рф'),
        ],
        XPATH_LAKE_REGION
    ),

    # === ПРОЕКТ: syn_92 Усадьба в Дубровке ===
    *create_project_configs(
        'syn_92 Усадьба в Дубровке',
        [
            ('syn_92', 'https://syn92.lp.moigektar.ru'),
            ('усадьба-дубровка.рф', 'https://усадьба-дубровка.рф'),
            ('усадба-дубровка.рф', 'https://усадба-дубровка.рф'),
            ('усадьба-на-дубровке.рф', 'https://усадьба-на-дубровке.рф'),
            ('дубровка-усадьба.рф', 'https://дубровка-усадьба.рф'),
        ],
        XPATH_W_DESCR
    ),

    # === ПРОЕКТ: syn_95 Усадьба Императрицы ===
    *create_project_configs(
        'syn_95 Усадьба Императрицы',
        [
            ('syn_95', 'https://syn95.lp.moigektar.ru'),
            ('екатериновка2.рф', 'https://екатериновка2.рф'),
        ],
        XPATH_EMPRESS_ESTATE
    ),

    # === ПРОЕКТ: syn_99 Лесные Озёра ===
    *create_project_configs(
        'syn_99 Лесные Озёра',
        [
            ('syn_99', 'https://syn99.lp.moigektar.ru'),
            ('лесныеозера.рф', 'https://лесныеозера.рф'),
            ('озера-лесные.рф', 'https://озера-лесные.рф'),
        ],
        XPATH_W_DESCR
    ),

    # === ПРОЕКТ: syn_103 Synergy Country Club ===
    {
        'name': 'synergycountryclub.ru (103)',
        'url': 'https://synergycountryclub.ru',
        'xpath': XPATH_CLUB_SETTLEMENT
    },

    # === ПРОЕКТ: syn_111 Технопарк - С АВТОРИЗАЦИЕЙ ===
    *create_project_configs(
        'syn_111 Технопарк',
        [
            ('syn_111', 'https://syn111.lp.moigektar.ru'),
            ('technopark.lp.moigektar.ru', 'https://technopark.lp.moigektar.ru'),
            ('технопарк-завидово.рф', 'https://технопарк-завидово.рф'),
        ],
        XPATH_W_DESCR,
        auth='syn111'
    ),

    # === ПРОЕКТ: syn_447 Усадьба на Байкале ===
    *create_project_configs(
        'syn_447 Усадьба на Байкале',
        [
            ('syn_447', 'https://syn447.lp.moigektar.ru'),
            ('усадьба-на-байкале.рф', 'https://усадьба-на-байкале.рф'),
        ],
        XPATH_BAIKAL_ESTATE
    ),

    # === ДОПОЛНИТЕЛЬНЫЕ СЕРВИСЫ ===
    {
        'name': 'сервис генерации опросов',
        'url': 'https://polls.moigektar.ru',
        'xpath': '//*[text()[contains(.,"Заполните поля")]]'
    },
    {
        'name': 'pay.moigektar',
        'url': 'https://pay.moigektar.ru',
        'xpath': '//h3[text()[contains(.,"Платежные сервисы")]]'
    },
    {
        'name': 'Вынос границ',
        'url': 'https://points.lp.moigektar.ru',
        'xpath': '//p[text()[contains(.,"ВЫНОС ГРАНИЦ")]]'
    },
    {
        'name': 'Инвестиции',
        'url': 'https://investment.lp.moigektar.ru',
        'xpath': '//h1[text()[contains(.,"Инвестиции")]]'
    },
    {
        'name': 'Комплекс услуг',
        'url': 'https://complex.lp.moigektar.ru',
        'xpath': '//h1[text()[contains(.,"Комплекс услуг")]]'
    },
    {
        'name': 'Кооперативы',
        'url': 'https://cooperative.lp.moigektar.ru',
        'xpath': '//h1[text()[contains(.,"Кооператив собственников")]]'
    },
    {
        'name': 'сайт "Онлайн-показ"',
        'url': 'https://presentation.lp.moigektar.ru',
        'xpath': '//span[text()[contains(., "онлайн-показ")]]'
    },
    {
        'name': 'Правовая поддержка',
        'url': 'https://law.lp.moigektar.ru',
        'xpath': '//h1[text()[contains(.,"центр правовой поддержки")]]'
    },
    {
        'name': 'Разработка проекта',
        'url': 'https://planning.moigektar.ru',
        'xpath': '//p[text()[contains(.,"ЭТАПЫ РАБОТЫ")]]'
    },
    {
        'name': 'Расчистка участка',
        'url': 'https://clearance.lp.moigektar.ru',
        'xpath': '//*[text()[contains(.,"для чего нужна расчистка")]]'
    },
    {
        'name': 'Строительство въездной группы',
        'url': 'http://syn9.entrance.lp.moigektar.ru',
        'xpath': '//h1[text()[contains(.,"Коллективное")]]'
    },
    {
        'name': 'Строительство дорог',
        'url': 'https://syn23.roads.moigektar.ru',
        'xpath': '//p[text()[contains(.,"КОЛЛЕКТИВНОЕ")]]'
    },
    {
        'name': 'Строительство центрального дома',
        'url': 'https://house.lp.moigektar.ru',
        'xpath': '//h1[text()[contains(.,"коллективное строительство")]]'
    },
    {
        'name': 'Установка видеонаблюдения',
        'url': 'https://barrier.lp.moigektar.ru',
        'xpath': '//h1[text()[contains(.,"установка видеонаблюдения")]]'
    },
    {
        'name': 'Электрификация',
        'url': 'https://syn9.electrification.lp.moigektar.ru',
        'xpath': '//h1[text()[contains(.,"коллективное")]]'
    },
    {
        'name': 'Барская усадьба',
        'url': 'https://xn--80aacl7dl0e.xn--p1ai',
        'xpath': '//*[text()[contains(., "Эксклюзивный отдых")]]'
    },
    {
        'name': 'Бронницы',
        'url': 'https://здание-бронницы.рф',
        'xpath': '(//*[text()[contains(., "Отдельно стоящее здание")]])[1]'
    },
    {
        'name': 'сайт турпортала',
        'url': 'https://турпортал-вазуза.рф',
        'xpath': XPATH_UNIQUE_ECORESORT,
        'auth': 'turportal'
    },
    {
        'name': '"Родовые поселения"',
        'url': 'https://settlements.lp.moigektar.ru',
        'xpath': '//*[text()[contains(., "участником")]]'
    },
    {
        'name': 'сайт Бутовецкого',
        'url': 'https://книга-садоводов.рф',
        'xpath': '//*[text()[contains(., "Заказать книгу")]]'
    },
    {
        'name': 'GIS',
        'url': 'https://gis.bigland.ru/site/login',
        'xpath': '//h1[text()[contains(.,"Login")]]'
    },
    {
        'name': 'Сервис генерации КП',
        'url': 'https://offers.bigland.ru',
        'xpath': '//h1[text()[contains(.,"Сервис генерации КП")]]'
    },
    {
        'name': 'Полевые работы',
        'url': 'https://fields.bigland.ru/site/login',
        'xpath': '//*[text()[contains(.,"Запомнить")]]'
    },
    {
        'name': 'Сервис дорог',
        'url': 'https://editor.roads.bigland.ru/site/login',
        'xpath': '//h1[text()[contains(.,"Login")]]'
    },
    {
        'name': 'сервис по работе с портал ТП',
        'url': 'https://electrification.bigland.ru/site/login',
        'xpath': '//*[@id="loginparams-username"]'
    },
    {
        'name': 'сервис статей',
        'url': 'https://a.bigland.ru',
        'xpath': '//*[@id="loginform-username"]'
    },
    {
        'name': 'сайт "mail.bug.land"',
        'url': 'https://mail.bug.land',
        'xpath': '//*[@id="userNameLabel"]'
    },
    {
        'name': 'vault.dmz.bug.land',
        'url': 'https://vault.dmz.bug.land',
        'xpath': '//*[text()[contains(., "Sign in to Vault")]]'
    },
    {
        'name': 'compliance.bug.land',
        'url': 'https://compliance.bug.land',
        'xpath': '(//*[text()[contains(.,"Авторизация")]])[3]'
    }
]


def main():
    # Загрузка данных для авторизации
    try:
        with open('../actual/data.json', 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        data = None
        print("WARNING: файл data.json не найден, авторизация будет пропущена")

    # Инициализация драйвера
    driver = init_driver()

    try:
        # Проверка всех сервисов
        for config in services_config:
            check_service(driver, config, data)
            time.sleep(0.5)  # Небольшая пауза между проверками

    finally:
        time.sleep(2)
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
