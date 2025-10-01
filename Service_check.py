from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time
import json


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

    driver.get(url)

    # Авторизация, если нужна
    if auth and data:
        try:
            if auth == 'turportal':
                driver.find_element(By.CSS_SELECTOR, 'input[id=loginconfig-username]').send_keys(str(data["turporlal_cred"]["login"]))
                driver.find_element(By.CSS_SELECTOR, 'input[id=loginconfig-password]').send_keys(str(data["turporlal_cred"]["password"]))
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
                print(f'   OK: {name}')
                return True
        except:
            count += 1
            if count == max_attempts:
                print(f'ERROR: {name}')
                return False
            else:
                driver.refresh()
                # Повторная авторизация после обновления страницы
                if auth and data:
                    try:
                        if auth == 'turportal':
                            driver.find_element(By.CSS_SELECTOR, 'input[id=loginconfig-username]').send_keys(str(data["turportal_cred"]["login"]))
                            driver.find_element(By.CSS_SELECTOR, 'input[id=loginconfig-password]').send_keys(str(data["turportal_cred"]["password"]))
                            driver.find_element(By.CSS_SELECTOR, 'button[type]').click()
                            time.sleep(5)
                        elif auth == 'syn111':
                            driver.find_element(By.ID, 'loginconfig-username').send_keys(str(data["111_cred"]["login"]))
                            driver.find_element(By.ID, 'loginconfig-password').send_keys(str(data["111_cred"]["password"]))
                            driver.find_element(By.CSS_SELECTOR, 'div button').click()
                    except:
                        pass
    return False


# Массив конфигураций для всех сервисов
services_config = [
    {
        'name': 'МГ',
        'url': 'https://moigektar.ru/',
        'xpath': '//h2[text()[contains(.,"Описание проекта")]]'
    },
    {
        'name': 'ЛК',
        'url': 'https://cabinet.moigektar.ru',
        'xpath': '(//*[text()[contains(.,"Вы находитесь в демо-версии личного кабинета")]])[2]'
    },
    {
        'name': 'syn_6',
        'url': 'https://syn6.lp.moigektar.ru/',
        'xpath': '//h2[text()[contains(.,"Выбрать участок")]]'
    },
    {
        'name': 'syn_8',
        'url': 'https://syn8.lp.moigektar.ru/',
        'xpath': '//span[text()[contains(.,"Генеральный")]]'
    },
    {
        'name': 'syn_9',
        'url': 'https://syn9.lp.moigektar.ru/',
        'xpath': '//a[@href="#w-descr"]'
    },
    {
        'name': 'syn_11',
        'url': 'https://syn11.lp.moigektar.ru/',
        'xpath': '//span[text()[contains(.,"Интерактивный")]]'
    },
    {
        'name': 'syn_12',
        'url': 'https://syn12.lp.moigektar.ru/',
        'xpath': '//span[text()[contains(.,"Интерактивный")]]'
    },
    {
        'name': 'syn_14',
        'url': 'https://syn14.lp.moigektar.ru/',
        'xpath': '//span[text()[contains(.,"Интерактивный")]]'
    },
    {
        'name': 'syn_15',
        'url': 'https://syn15.lp.moigektar.ru/',
        'xpath': '//span[text()[contains(.,"Виртуальные туры")]]'
    },
    {
        'name': 'syn_16',
        'url': 'https://syn16.lp.moigektar.ru/',
        'xpath': '//span[text()[contains(.,"Интерактивный")]]'
    },
    {
        'name': 'syn_17',
        'url': 'https://syn17.lp.moigektar.ru/',
        'xpath': '//span[text()[contains(.,"Виртуальные")]]'
    },
    {
        'name': 'syn_18',
        'url': 'https://syn18.lp.moigektar.ru/',
        'xpath': '//span[text()[contains(.,"Интерактивный")]]'
    },
    {
        'name': 'syn_19',
        'url': 'https://syn19.lp.moigektar.ru/',
        'xpath': '//a[@href="#w-descr"]'
    },
    {
        'name': 'syn_21',
        'url': 'https://syn21.lp.moigektar.ru/',
        'xpath': '//span[text()[contains(.,"Генеральный")]]'
    },
    {
        'name': 'syn_24',
        'url': 'https://syn24.lp.moigektar.ru/',
        'xpath': '//span[text()[contains(.,"Генеральный")]]'
    },
    {
        'name': 'syn_33',
        'url': 'https://syn33.lp.moigektar.ru/',
        'xpath': '//a[@href="#w-descr"]'
    },
    {
        'name': 'syn_34',
        'url': 'https://syn34.lp.moigektar.ru/',
        'xpath': '//*[text()[contains(.,"10 соток под дачу")]]'
    },
    {
        'name': 'syn_35',
        'url': 'https://syn35.lp.moigektar.ru/',
        'xpath': '//span[text()[contains(.,"Генеральный")]]'
    },
    {
        'name': 'syn_36',
        'url': 'https://syn36.lp.moigektar.ru/',
        'xpath': '//span[text()[contains(.,"Генеральный")]]'
    },
    {
        'name': 'syn_39',
        'url': 'https://syn39.lp.moigektar.ru/',
        'xpath': '//a[@href="#w-descr"]'
    },
    {
        'name': 'syn_42',
        'url': 'https://syn42.lp.moigektar.ru/',
        'xpath': '//a[@href="#w-descr"]'
    },
    {
        'name': 'syn_47',
        'url': 'https://syn47.lp.moigektar.ru/',
        'xpath': '//*[text()[contains(., "Клубный поселок")]]'
    },
    {
        'name': 'syn_48',
        'url': 'https://syn48.lp.moigektar.ru/',
        'xpath': '//a[@href="#w-descr"]'
    },
    {
        'name': 'syn_53',
        'url': 'https://syn53.lp.moigektar.ru/',
        'xpath': '//a[@href="#w-descr"]'
    },
    {
        'name': 'syn_58',
        'url': 'https://syn58.lp.moigektar.ru/',
        'xpath': '//h3[text()[contains(.,"Забронировать")]]'
    },
    {
        'name': 'vazuza',
        'url': 'https://vazuza2.lp.moigektar.ru/',
        'xpath': '//h3[text()[contains(., "Уникальный экокурорт")]]'
    },
    {
        'name': 'syn_61',
        'url': 'https://syn61.lp.moigektar.ru/',
        'xpath': '//span[text()[contains(.,"Генеральный")]]'
    },
    {
        'name': 'syn_67',
        'url': 'https://syn67.lp.moigektar.ru/',
        'xpath': '//a[@href="#w-descr"]'
    },
    {
        'name': 'syn_73',
        'url': 'https://syn73.lp.moigektar.ru/',
        'xpath': '//a[@href="#w-descr"]'
    },
    {
        'name': 'syn_74',
        'url': 'https://syn74.lp.moigektar.ru/',
        'xpath': '//*[text()[contains(., "Концепция")]]'
    },
    {
        'name': 'syn_84',
        'url': 'https://syn84.lp.moigektar.ru/',
        'xpath': '//a[@href="#w-descr"]'
    },
    {
        'name': 'syn_85',
        'url': 'https://syn85.lp.moigektar.ru/',
        'xpath': '//a[@href="#w-descr"]'
    },
    {
        'name': 'syn_89',
        'url': 'https://syn89.lp.moigektar.ru/',
        'xpath': '//*[text()[contains(.,"Озерный край: ")]]'
    },
    {
        'name': 'syn_87',
        'url': 'https://mt.lp.moigektar.ru/',
        'xpath': '//a[@href="#w-descr"]'
    },
    {
        'name': 'syn_92',
        'url': 'https://syn92.lp.moigektar.ru/',
        'xpath': '//a[@href="#w-descr"]'
    },
    {
        'name': 'syn_95',
        'url': 'https://syn95.lp.moigektar.ru/',
        'xpath': '//*[text()[contains(., "«Усадьба Императрицы»")]]'
    },
    {
        'name': 'syn_99',
        'url': 'https://syn99.lp.moigektar.ru/',
        'xpath': '//a[@href="#w-descr"]'
    },
    {
        'name': 'synergycountryclub.ru',
        'url': 'https://synergycountryclub.ru',
        'xpath': '(//*[text()[contains(.,"Клубный посёлок")]])[1]'
    },
    {
        'name': 'syn_111',
        'url': 'https://syn111.lp.moigektar.ru/',
        'xpath': '//a[@href="#w-descr"]',
        'auth': 'syn111'
    },
    {
        'name': 'syn_447',
        'url': 'https://syn447.lp.moigektar.ru',
        'xpath': '//*[text()[contains(., "Усадьба на Байкале» — это:")]]'
    },
    {
        'name': 'сервис генерации опросов',
        'url': 'https://polls.moigektar.ru/',
        'xpath': '//*[text()[contains(.,"Проект «МОЙ ГЕКТАР»")]]'
    },    {
        'name': 'pay.moigektar',
        'url': 'https://pay.moigektar.ru/',
        'xpath': '//h3[text()[contains(.,"Платежные сервисы")]]'
    },
    {
        'name': 'Вынос границ',
        'url': 'https://points.lp.moigektar.ru/',
        'xpath': '//p[text()[contains(.,"ВЫНОС ГРАНИЦ")]]'
    },
    {
        'name': 'Инвестиции',
        'url': 'https://investment.lp.moigektar.ru/',
        'xpath': '//h1[text()[contains(.,"Инвестиции")]]'
    },
    {
        'name': 'Комплекс услуг',
        'url': 'https://complex.lp.moigektar.ru/',
        'xpath': '//h1[text()[contains(.,"Комплекс услуг")]]'
    },
    {
        'name': 'Кооперативы',
        'url': 'https://cooperative.lp.moigektar.ru',
        'xpath': '//h1[text()[contains(.,"Кооператив собственников")]]'
    },
    {
        'name': 'сайт "Онлайн-показ"',
        'url': 'https://presentation.lp.moigektar.ru/',
        'xpath': '//span[text()[contains(., "онлайн-показ")]]'
    },
    {
        'name': 'Правовая поддержка',
        'url': 'https://law.lp.moigektar.ru/',
        'xpath': '//h1[text()[contains(.,"центр правовой поддержки")]]'
    },
    {
        'name': 'Разработка проекта',
        'url': 'https://planning.moigektar.ru/',
        'xpath': '//p[text()[contains(.,"ЭТАПЫ РАБОТЫ")]]'
    },
    {
        'name': 'Расчистка участка',
        'url': 'https://clearance.lp.moigektar.ru/',
        'xpath': '//*[text()[contains(.,"для чего нужна расчистка")]]'
    },
    {
        'name': 'Строительство въездной группы',
        'url': 'http://syn9.entrance.lp.moigektar.ru/',
        'xpath': '//h1[text()[contains(.,"Коллективное")]]'
    },
    {
        'name': 'Строительство дорог',
        'url': 'https://syn23.roads.moigektar.ru/',
        'xpath': '//p[text()[contains(.,"КОЛЛЕКТИВНОЕ")]]'
    },
    {
        'name': 'Строительство центрального дома',
        'url': 'https://house.lp.moigektar.ru/',
        'xpath': '//h1[text()[contains(.,"коллективное строительство")]]'
    },
    {
        'name': 'Установка видеонаблюдения',
        'url': 'https://barrier.lp.moigektar.ru/',
        'xpath': '//h1[text()[contains(.,"установка видеонаблюдения")]]'
    },
    {
        'name': 'Электрификация',
        'url': 'https://syn9.electrification.lp.moigektar.ru/',
        'xpath': '//h1[text()[contains(.,"коллективное")]]'
    },
    {
        'name': 'сайт СК',
        'url': 'https://sc.lp.moigektar.ru/',
        'xpath': '//*[text()[contains(., "Наша цель")]]'
    },
    {
        'name': 'Барская усадьба',
        'url': 'https://xn--80aacl7dl0e.xn--p1ai',
        'xpath': '//h2[text()[contains(., "Ждем вас в гости!")]]'
    },
    {
        'name': 'Бронницы',
        'url': 'https://здание-бронницы.рф',
        'xpath': '(//*[text()[contains(., "Отдельно стоящее здание")]])[1]'
    },
    {
        'name': 'сайт турпортала',
        'url': 'https://турпортал-вазуза.рф',
        'xpath': '//h3[text()[contains(., "Уникальный экокурорт")]]',
        'auth': 'turportal'
    },
    {
        'name': '"Родовые поселения"',
        'url': 'https://settlements.lp.moigektar.ru/',
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
        'url': 'https://offers.bigland.ru/',
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
        'url': 'https://a.bigland.ru/',
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
    }
]


def main():
    # Загрузка данных для авторизации
    try:
        with open('data.json', 'r') as file:
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
            time.sleep(0.5) # Небольшая пауза между проверками

    finally:
        time.sleep(2)
        driver.quit()


if __name__ == "__main__":
    main()
