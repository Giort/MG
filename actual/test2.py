from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import time
import json
import requests
from urllib.parse import urljoin

# расширенная версия кода проверки всех страниц. Сейчас проверяет http-статус страницы при входе.



with open('data.json', 'r') as file:
    data = json.load(file)

# Засекаем время начала теста
start_time = time.time()

# Проверка доступности страниц МГ

# Проверяемый урл
MG_BASE_URL = "https://moigektar.ru"
LK_BASE_URL = "https://cabinet.moigektar.ru"
# MG_BASE_URL = "http://moigektar.localhost"
# LK_BASE_URL = "http://cabinet.moigektar.localhost"


class PageChecker:
    def __init__(self, mg_base_url):
        self.driver = self.init_driver()
        self.actions = ActionChains(self.driver)
        self.mg_base_url = mg_base_url.rstrip('/')
        self.session = requests.Session()
        # Устанавливаем заголовки, чтобы имитировать браузер
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        })

    def init_driver(self):
        ch_options = Options()
        ch_options.add_argument('--headless')
        ch_options.page_load_strategy = 'eager'
        service = ChromeService(executable_path=ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=ch_options)
        driver.set_window_size(1680, 1000)
        driver.implicitly_wait(10)
        return driver

    def auth(self):
        """ Авторизация """
        try:
            self.driver.get("https://moigektar.ru//")
            self.driver.find_element(By.XPATH, '(//*[@href="#modal-auth-lk"])[1]').click()
            time.sleep(2)
            tab = self.driver.find_element(By.XPATH, '//*[text()="По паролю"]')
            name = self.driver.find_element(By.XPATH, '//*[@id="authform-login"]')
            password = self.driver.find_element(By.XPATH, '//*[@id="authform-password"]')
            btn = self.driver.find_element(By.XPATH, '//*[text()="Войти"]')
            tab.click()
            name.send_keys(str(data["LK_cred"]["login"]))
            password.send_keys(str(data["LK_cred"]["password"]))
            btn.click()
            time.sleep(5)
            return True
        except Exception as e:
            print(f" ERROR: Не удалось авторизоваться - {str(e)}")
            return False

    def check_http_status(self, url, timeout=10):
        """
        Проверяет HTTP-статус страницы
        Возвращает (status_code, error_message)
        """
        try:
            response = self.session.get(url, timeout=timeout, allow_redirects=True)

            # Проверяем статус код
            status_code = response.status_code

            if status_code >= 400:
                if 400 <= status_code < 500:
                    error_type = "Клиентская ошибка"
                elif status_code >= 500:
                    error_type = "Серверная ошибка"
                else:
                    error_type = "Ошибка"

                return status_code, f"{error_type} {status_code}"
            else:
                return status_code, None

        except requests.exceptions.Timeout:
            return None, "Таймаут при проверке HTTP-статуса"
        except requests.exceptions.ConnectionError:
            return None, "Ошибка подключения"
        except Exception as e:
            return None, f"Ошибка при проверке HTTP: {str(e)}"

    def check_page(self, page_config, timeout=20):
        page_path = page_config['path']
        page_name = page_config['name']
        xpath_selector = page_config['xpath']

        full_url = f"{self.mg_base_url}/{page_path.lstrip('/')}"
        self.actions.send_keys(Keys.PAGE_DOWN).perform()
        time.sleep(2)

        # Сначала проверяем HTTP-статус
        status_code, http_error = self.check_http_status(full_url)

        if http_error:
            print(f" ERROR: {page_name} - {http_error}")
            return False

        # Затем проверяем через Selenium
        for attempt in range(3):
            try:
                self.driver.get(full_url)

                element = WebDriverWait(self.driver, timeout).until(
                    EC.visibility_of_element_located((By.XPATH, xpath_selector))
                )

                print(f"     OK: {page_name}")
                return True

            except TimeoutException:
                if attempt < 2:
                    time.sleep(1)
                else:
                    print(f" ERROR: {page_name} - элемент не найден")
                    return False
            except Exception as e:
                if attempt < 2:
                    time.sleep(1)
                else:
                    print(f" ERROR: {page_name} - {str(e)}")
                    return False

    def check_all_pages(self, pages_config, delay=1):
        print(f"\n     Проверка всех страниц МГ \n")

        # сначала авторизуемся
        self.auth()
        time.sleep(6)

        results = {}
        for page_config in pages_config:
            result = self.check_page(page_config)
            results[page_config['name']] = result
            time.sleep(delay)

        return results

    def close(self):
        if self.driver:
            self.driver.quit()


PAGES_CONFIG = [
    {
        'name': 'главная',
        'path': '/',
        'xpath': '//h2[text()[contains(.,"Описание проекта")]]',
    },
#     {
#         'name': 'каталог',
#         'path': 'catalogue',
#         'xpath': '(//*[(contains(@class, "js-batch-name"))])[1]',
#     },
#     {
#         'name': 'каталог чпу - новорижское шоссе',
#         'path': 'catalogue/zemelnye-uchastki-na-novorizhskom-shosse',
#         'xpath': '(//*[(contains(@class, "js-batch-name"))])[1]',
#     },
#     {
#         'name': 'каталог чпу - ленинградское шоссе',
#         'path': 'catalogue/zemelnye-uchastki-na-leningradskom-shosse',
#         'xpath': '(//*[(contains(@class, "js-batch-name"))])[1]',
#     },
#     {
#         'name': 'каталог чпу - минское шоссе',
#         'path': 'catalogue/zemelnye-uchastki-na-minskom-shosse',
#         'xpath': '(//*[(contains(@class, "js-batch-name"))])[1]',
#     },
#     {
#         'name': 'каталог чпу - ярославское шоссе',
#         'path': 'catalogue/uchastki-na-yaroslavskom-shosse',
#         'xpath': '(//*[(contains(@class, "js-batch-name"))])[1]',
#     },
#     {
#         'name': 'каталог чпу - на Волге',
#         'path': 'catalogue/volga',
#         'xpath': '(//*[(contains(@class, "js-batch-name"))])[1]',
#     },
#     {
#         'name': 'каталог чпу - на Валдае',
#         'path': 'catalogue/valday',
#         'xpath': '(//*[(contains(@class, "js-batch-name"))])[1]',
#     },
#     {
#         'name': 'каталог чпу - на Вазузе',
#         'path': 'catalogue/vazuza',
#         'xpath': '(//*[(contains(@class, "js-batch-name"))])[1]',
#     },
#     {
#         'name': 'каталог чпу - на Селигере',
#         'path': 'catalogue/seliger',
#         'xpath': '(//*[(contains(@class, "js-batch-name"))])[1]',
#     },
#     {
#         'name': 'каталог чпу - в Завидово',
#         'path': 'catalogue/uchastki-v-zavidovo',
#         'xpath': '(//*[(contains(@class, "js-batch-name"))])[1]',
#     },
#     {
#         'name': 'каталог чпу - у воды',
#         'path': 'catalogue/zemelnye-uchastki-u-vody',
#         'xpath': '(//*[(contains(@class, "js-batch-name"))])[1]',
#     },
#     {
#         'name': 'каталог чпу - у леса',
#         'path': 'catalogue/zemelnye-uchastki-u-lesa',
#         'xpath': '(//*[(contains(@class, "js-batch-name"))])[1]',
#     },
#     {
#         'name': 'каталог чпу - у реки',
#         'path': 'catalogue/zemelnye-uchastki-u-reki',
#         'xpath': '(//*[(contains(@class, "js-batch-name"))])[1]',
#     },
#     {
#         'name': 'каталог чпу - у озера',
#         'path': 'catalogue/zemelnye-uchastki-u-ozera',
#         'xpath': '(//*[(contains(@class, "js-batch-name"))])[1]',
#     },
#     {
#         'name': 'каталог чпу - на водохранилище',
#         'path': 'catalogue/uchastki-na-vodohranilische',
#         'xpath': '(//*[(contains(@class, "js-batch-name"))])[1]',
#     },
#     {
#         'name': 'каталог чпу - видовые участки',
#         'path': 'catalogue/vidovye-uchastki',
#         'xpath': '(//*[(contains(@class, "js-batch-name"))])[1]',
#     },
#     {
#         'name': 'каталог чпу - до 30 соток',
#         'path': 'catalogue/uchastki-do-30-sotok',
#         'xpath': '(//*[(contains(@class, "js-batch-name"))])[1]',
#     },
#     {
#         'name': 'каталог чпу - под дачу',
#         'path': 'catalogue/dachnye-zemelnye-uchastki',
#         'xpath': '(//*[(contains(@class, "js-batch-name"))])[1]',
#     },
#     {
#         'name': 'каталог чпу - под усадьбу',
#         'path': 'catalogue/zemelnye-uchastki-pod-usadbu',
#         'xpath': '(//*[(contains(@class, "js-batch-name"))])[1]',
#     },
#     {
#         'name': 'каталог чпу - под бизнес',
#         'path': 'catalogue/zemelnye-uchastki-pod-biznes',
#         'xpath': '(//*[(contains(@class, "js-batch-name"))])[1]',
#     },
#     {
#         'name': 'каталог чпу - под базу отдыха',
#         'path': 'catalogue/zemelnye-uchastki-pod-bazu-otdyha',
#         'xpath': '(//*[(contains(@class, "js-batch-name"))])[1]',
#     },
#     {
#         'name': 'каталог чпу - под глэмпинг',
#         'path': 'catalogue/zemelnye-uchastki-pod-glemping',
#         'xpath': '(//*[(contains(@class, "js-batch-name"))])[1]',
#     },
#     {
#         'name': 'каталог чпу - под кемпинг',
#         'path': 'catalogue/zemelnye-uchastki-pod-kemping',
#         'xpath': '(//*[(contains(@class, "js-batch-name"))])[1]',
#     },
#     {
#         'name': 'каталог чпу - под отель, экоотель',
#         'path': 'catalogue/zemelnye-uchastki-pod-otel-eko-otel',
#         'xpath': '(//*[(contains(@class, "js-batch-name"))])[1]',
#     },
#     {
#         'name': 'каталог чпу - под ферму',
#         'path': 'catalogue/zemelnye-uchastki-pod-fermu',
#         'xpath': '(//*[(contains(@class, "js-batch-name"))])[1]',
#     },
#     {
#         'name': 'каталог чпу - под инвестиции',
#         'path': 'catalogue/zemelnye-uchastki-pod-investicii',
#         'xpath': '(//*[(contains(@class, "js-batch-name"))])[1]',
#     },
#     {
#         'name': 'каталог чпу - ижс',
#         'path': 'catalogue/zemelnye-uchastki-pod-izhs-v-moskovskoy-oblasti',
#         'xpath': '(//*[(contains(@class, "js-batch-name"))])[1]',
#     },
#     {
#         'name': 'каталог чпу - под ижс',
#         'path': 'catalogue/uchastki-pod-izhs',
#         'xpath': '(//*[(contains(@class, "js-batch-name"))])[1]',
#     },
#     {
#         'name': 'каталог чпу - под агробизнес',
#         'path': 'catalogue/uchastki-pod-agrobiznes',
#         'xpath': '(//*[(contains(@class, "js-batch-name"))])[1]',
#     },
#     {
#         'name': 'каталог чпу - под туристический бизнес',
#         'path': 'catalogue/uchastki-pod-turistichesky-biznes',
#         'xpath': '(//*[(contains(@class, "js-batch-name"))])[1]',
#     },
#     {
#         'name': 'каталог чпу - для активного отдыха',
#         'path': 'catalogue/uchastki-dlya-aktivnogo-otdyha',
#         'xpath': '(//*[(contains(@class, "js-batch-name"))])[1]',
#     },
#     {
#         'name': 'каталог чпу - под ритейл',
#         'path': 'catalogue/uchastki-pod-riteyl',
#         'xpath': '(//*[(contains(@class, "js-batch-name"))])[1]',
#     },
#     {
#         'name': 'каталог чпу - под производство',
#         'path': 'catalogue/uchastki-pod-proizvodstvo',
#         'xpath': '(//*[(contains(@class, "js-batch-name"))])[1]',
#     },
#     {
#         'name': 'каталог чпу - под придорожный сервис',
#         'path': 'catalogue/uchastki-pod-proidorozhny-servis',
#         'xpath': '(//*[(contains(@class, "js-batch-name"))])[1]',
#     },
#     {
#         'name': 'каталог чпу - под корпоративные посёлки',
#         'path': 'catalogue/uchastki-pod-korporativnye-poselki',
#         'xpath': '(//*[(contains(@class, "js-batch-name"))])[1]',
#     },
#     {
#         'name': 'каталог - регионы - Киевское шоссе',
#         'path': 'catalogue/kiev-highway',
#         'xpath': '(//*[(contains(@class, "js-batch-name"))])[1]',
#     },
#     {
#         'name': 'каталог - регионы - Москва',
#         'path': 'catalogue/moscow-batch',
#         'xpath': '(//*[(contains(@class, "js-batch-name"))])[1]',
#     },
#     {
#         'name': 'каталог - регионы - Московский регион',
#         'path': 'catalogue/moscow-region-batch',
#         'xpath': '(//*[(contains(@class, "js-batch-name"))])[1]',
#     },
#     {
#         'name': 'каталог - регионы - Калужское шоссе',
#         'path': 'catalogue/kaluga-highway',
#         'xpath': '(//*[(contains(@class, "js-batch-name"))])[1]',
#     },
#     {
#         'name': 'каталог - регионы - Ярославское шоссе',
#         'path': 'catalogue/yaroslavl-highway',
#         'xpath': '(//*[(contains(@class, "js-batch-name"))])[1]',
#     },
#     {
#         'name': 'каталог - регионы - Симферопольское шоссе',
#         'path': 'catalogue/simferopol-highway',
#         'xpath': '(//*[(contains(@class, "js-batch-name"))])[1]',
#     },
#     {
#         'name': 'каталог - регионы - Каширское шоссе',
#         'path': 'catalogue/kashirskoe-highway',
#         'xpath': '(//*[(contains(@class, "js-batch-name"))])[1]',
#     },
#     {
#         'name': 'каталог - регионы - Минское шоссе',
#         'path': 'catalogue/minsk-highway',
#         'xpath': '(//*[(contains(@class, "js-batch-name"))])[1]',
#     },
#     {
#         'name': 'каталог - регионы - Рогачёвское шоссе',
#         'path': 'catalogue/rogachevskoe-highway',
#         'xpath': '(//*[(contains(@class, "js-batch-name"))])[1]',
#     },
#     {
#         'name': 'страница актива',
#         'path': 'batches/30608',
#         'xpath': '(//*[@uk-toggle="target: #modal-batch-detail"])[2]',
#     },
#     {
#         'name': 'избранное',
#         'path': 'catalogue/wishlist',
#         'xpath': '//*[text()[contains(.,"Мои подборки")]]',
#     },
#     {
#         'name': 'сравнения',
#         'path': 'catalogue/compare',
#         'xpath': '//*[text()[contains(.,"Выбранные участки")]]',
#     },
#     {
#         'name': 'о проекте',
#         'path': 'about',
#         'xpath': '//*[text()[contains(.,"Цель проекта")]]',
#     },
#     {
#         'name': 'о проекте - сервисная компания',
#         'path': 'service-company',
#         'xpath': '(//*[text()[contains(.,"Анастасия Васехина")]])[2]',
#     },
#     {
#         'name': 'о проекте - личный кабинет',
#         'path': 'cabinet',
#         'xpath': '//*[text()[contains(.,"Для собственников")]]',
#     },
#     {
#         'name': 'о проекте - партнёры',
#         'path': 'about/advantages',
#         'xpath': '(//div[2]/div/picture/img[1])[1]',
#     },
#     {
#         'name': 'о проекте - союз садоводов',
#         'path': 'about/union',
#         'xpath': '(//*[text()[contains(.,"ом садовода - опора семьи")]])[1]',
#     },
#     {
#         'name': 'о проекте - отзывы',
#         'path': 'about/reviews',
#         'xpath': '(//*[@id="w0"]//ul[contains(@class, "uk-grid")]/li)[1]',
#     },
#     {
#         'name': 'миссия проекта',
#         'path': '2.0',
#         'xpath': '//*[text()[contains(.,"Система предоставления")]]',
#     },
#     {
#         'name': 'развитие - развитие гектара',
#         'path': 'growth/construct',
#         'xpath': '//*[text()[contains(.,"Федеральный закон")]]',
#     },
#     {
#         'name': 'развитие - развитие поселков',
#         'path': 'growth',
#         'xpath': '//*[text()[contains(.,"Развитие поселков на карте")]]',
#     },
#     {
#         'name': 'развитие - страница услуги типовая',
#         'path': 'growth/view?uuid=33067acf-f6e7-4579-8a88-237ef05cc9ff',
#         'xpath': '//*[text()[contains(.,"Опубликовано")]]',
#     },
#     {
#         'name': 'развитие - глазами инвестора',
#         'path': 'investment',
#         'xpath': '//*[text()[contains(.,"Приемлемая цена")]]',
#     },
#     {
#         'name': 'развитие - капитализация',
#         'path': 'investment/capitalization',
#         'xpath': '//*[@id="uk-slider-13"]',
#     },
#     {
#         'name': 'развитие - базовая стратегия',
#         'path': 'investment/basic',
#         'xpath': '//h3[text()[contains(.,"Таблица доходности инвестиций")]]',
#     },
#     {
#         'name': 'развитие - предприниматель',
#         'path': 'investment/businessman',
#         'xpath': '//h3[text()[contains(.,"Таблица доходности инвестиций")]]',
#     },
#     {
#         'name': 'развитие - фермер-садовод',
#         'path': 'investment/farmer',
#         'xpath': '//h3[text()[contains(.,"Таблица доходности инвестиций")]]',
#     },
#     {
#         'name': 'развитие - фамильная усадьба',
#         'path': 'investment/family',
#         'xpath': '//h3[text()[contains(.,"Таблица доходности инвестиций")]]',
#     },
#     {
#         'name': 'онлайн-поселок',
#         'path': 'polls/about',
#         'xpath': '//*[text()[contains(.,"Ваша роль в развитии поселка")]]',
#     },
    {
        'name': 'онлайн-поселок - голосования и опросы',
        'path': 'polls?list=all',
        'xpath': '(//*[@class="list-view"]//*[contains(@class, "poll-item")])[1]'
    },
    {
        'name': 'онлайн-поселок - детальная страница голосования',
        'path': 'polls/view?id=19',
        'xpath': '//*[contains(@class, "w-polls-id")]',
    },
    {
        'name': 'онлайн-поселок - результаты работы за 2019 год',
        'path': 'polls/summary-2019',
        'xpath': '(//a[text()[contains(.,"История вопроса")]])[1]',
    },
    {
        'name': 'бизнес-планы',
        'path': 'business-plans',
        'xpath': '(//*[contains(@class, "uk-grid")]//*[contains(@class, "uk-card")])[6]',
    },
    {
        'name': 'меры поддержки - государственная поддержка',
        'path': 'documents/gos',
        'xpath': '(//*[contains(@class, "uk-grid")]//*[contains(@class, "uk-card")])[6]',
    },
    {
        'name': 'меры поддержки - для владельцев земли',
        'path': 'documents',
        'xpath': '//*[text()[contains(.,"Еще 30-40 лет назад")]]',
    },
    {
        'name': 'меры поддержки - начинающий фермер',
        'path': 'documents/farmer',
        'xpath': '//*[text()[contains(.,"Программа “Начинающий фермер” ")]]',
    },
    {
        'name': 'меры поддержки - агростартап',
        'path': 'documents/startup',
        'xpath': '//*[text()[contains(.,"Ещё один из способов")]]',
    },
    {
        'name': 'меры поддержки - грант на семейную ипотеку',
        'path': 'documents/family',
        'xpath': '//*[text()[contains(.,"Грант на развитие семейной")]]',
    },
    {
        'name': 'меры поддержки - сельская ипотека',
        'path': 'documents/ipoteka',
        'xpath': '//*[text()[contains(.,"— это ипотечный кредит")]]',
    },
    {
        'name': 'вопрос-ответ',
        'path': 'faq',
        'xpath': '(//*[contains(@class, "js-faq-15-card")])[1]',
    },
    {
        'name': 'новости - основная страница',
        'path': 'news',
        'xpath': '(//*[contains(@class, "uk-grid")]//*[contains(@class, "uk-card")])[8]',
    },
    {
        'name': 'новости - видео',
        'path': 'news/video',
        'xpath': '(//*[contains(@class, "uk-grid")]//*[contains(@class, "uk-card")])[6]',
    },
    {
        'name': 'новости - страница с фильтром по разделу',
        'path': 'news/list/kredity-granty-subsidii',
        'xpath': '(//*[contains(@class, "uk-grid")]//*[contains(@class, "uk-card")])[8]',
    },
    {
        'name': 'новости - детальная страница новости',
        'path': 'news/k-2030-godu-dlya-vyzhivaniya-lyudey-dopolnitelno-ponadobitsya-80-mln-ga-pahotnyh-zemel-lyhZ51ZoQr',
        'xpath': '(//*[contains(@class, "uk-grid")]//*[contains(@class, "uk-card")])[9]',
    },
    {
        'name': 'акции - основная',
        'path': 'actions',
        'xpath': '(//*[contains(@class, "uk-grid")]//*[contains(@class, "uk-card")])[6]',
    },
    {
        'name': 'акции - участок для многодетной семьи',
        'path': 'actions/1',
        'xpath': '(//*[text()[contains(.,"многодетной семьи")]])[2]',
    },
    {
        'name': 'акции - участок для участников сво',
        'path': 'actions/2',
        'xpath': '(//*[text()[contains(.,"военной операции")]])[2]',
    },
    {
        'name': 'акции - участок для ветеранов ВОВ',
        'path': 'actions/3',
        'xpath': '(//*[text()[contains(.,"Великой Отечественной")]])[2]',
    },
    {
        'name': 'акции - участок для льготных категорий граждан',
        'path': 'actions/4',
        'xpath': '(//*[text()[contains(.,"категорий граждан")]])[2]',
    },
    {
        'name': 'акции - скидка при покупке по сертификату друга',
        'path': 'actions/5',
        'xpath': '(//*[text()[contains(.,"сертификату друга")]])[2]',
    },
    {
        'name': 'акции - скидка для беженцев из Донбасса',
        'path': 'actions/6',
        'xpath': '(//*[text()[contains(.,"беженцев из Донбасса")]])[2]',
    },
    {
        'name': 'акции - скидка при единовременной оплате',
        'path': 'actions/7',
        'xpath': '(//*[text()[contains(.,"единовременной оплате")]])[2]',
    },
    {
        'name': 'фонд добра - основная',
        'path': 'good-fund',
        'xpath': '(//*[text()[contains(.,"своими силами")]])[1]',
    },
    {
        'name': 'фонд добра - фермер восстанавливает храм',
        'path': 'good-fund/farmer',
        'xpath': '(//*[text()[contains(.,"своими силами")]])[1]',
    },
    {
        'name': 'фонд добра - центр помощи "МногоМама"',
        'path': 'good-fund/mama',
        'xpath': '(//*[text()[contains(.,"многодетных семей")]])[1]',
    },
    {
        'name': 'фонд добра - музей "Дорога к Пушкину"',
        'path': 'good-fund/pushkin',
        'xpath': '(//*[text()[contains(.,"Дорога к Пушкину")]])[1]',
    },
    {
        'name': 'фонд добра - храм в Щеколдино',
        'path': 'good-fund/church',
        'xpath': '(//*[text()[contains(.,"местных жителей")]])[1]',
    },
    {
        'name': 'фонд добра - поддержка участников сво',
        'path': 'good-fund/svo',
        'xpath': '(//*[text()[contains(.,"военной операции")]])[1]',
    },
    {
        'name': 'вакансии',
        'path': 'hr',
        'xpath': '//*[text()[contains(.,"направлениях проекта")]]',
    },
    {
        'name': 'контакты',
        'path': 'contacts',
        'xpath': '(//*[text()[contains(.,"Департамент продаж")]])[1]',
    },
    {
        'name': 'подарочный сертификат',
        'path': 'gift',
        'xpath': '//*[text()[contains(.,"преподнести подарок родным")]]',
    },
    {
        'name': 'вебинары - основная',
        'path': 'webinar',
        'xpath': '(//*[text()[contains(.,"мастер-классы")]])[2]',
    },
    {
        'name': 'вебинары - как заработать на участке',
        'path': 'webinar/invest',
        'xpath': '//*[text()[contains(.,"заработать на гектаре")]]',
    },
    {
        'name': 'вебинары - как заработать на участке - видео',
        'path': 'webinar/video/invest',
        'xpath': '//a[text()[contains(.,"землю под инвестиции")]]',
    },
    {
        'name': 'вебинары - глэмпинг',
        'path': 'webinar/glamping',
        'xpath': '//*[text()[contains(.,"организации глэмпинга")]]',
    },
    {
        'name': 'вебинары - глэмпинг - видео',
        'path': 'webinar/video/glamping',
        'xpath': '//a[text()[contains(.,"землю под инвестиции")]]',
    },
    {
        'name': 'вебинары - гранты и господдержка',
        'path': 'webinar/gos-support',
        'xpath': '//*[text()[contains(.,"сфере агробизнеса")]]',
    },
    {
        'name': 'вебинары - гранты и господдержка - видео',
        'path': 'webinar/video/gos-support',
        'xpath': '//a[text()[contains(.,"землю под инвестиции")]]',
    },
    {
        'name': 'вебинары - что делать на гектаре',
        'path': 'webinar/what-to-do',
        'xpath': '//*[text()[contains(.,"построить на своем")]]',
    },
    {
        'name': 'вебинары - что делать на гектаре - видео',
        'path': 'webinar/video/what-to-do',
        'xpath': '//a[text()[contains(.,"землю под инвестиции")]]',
    },
    {
        'name': 'вебинары - как выбрать участок',
        'path': 'webinar/how-to-choose',
        'xpath': '//*[text()[contains(.,"Что можно построить")]]',
    },
    {
        'name': 'вебинары - как выбрать участок - видео',
        'path': 'webinar/video/how-to-choose',
        'xpath': '//a[text()[contains(.,"землю под инвестиции")]]',
    },
    {
        'name': 'вебинары - доходная недвижимость',
        'path': 'webinar/income-property',
        'xpath': '//*[text()[contains(.,"инвестирования в землю")]]',
    },
    {
        'name': 'вебинары - доходная недвижимость - видео',
        'path': 'webinar/video/income-property',
        'xpath': '//a[text()[contains(.,"землю под инвестиции")]]',
    },
    {
        'name': 'вебинары - ответы на вопросы',
        'path': 'webinar/answers-to-questions',
        'xpath': '//*[text()[contains(.,"Какие услуги выполняет")]]',
    },
    {
        'name': 'вебинары - ответы на вопросы - видео',
        'path': 'webinar/video/answers-to-questions',
        'xpath': '//a[text()[contains(.,"землю под инвестиции")]]',
    },
    {
        'name': 'страница заявки на вебинар',
        'path': 'webinar/meeting',
        'xpath': '//*[text()[contains(.,"подогреваемые бассейны")]]',
    },
    {
        'name': 'цели - туризм (глэмпинги)',
        'path': 'goal/glamping',
        'xpath': '//*[contains(@class, "uk-card") and contains(.,"кемпинги")]',
    },
    {
        'name': 'цели - агробизнес',
        'path': 'goal/farm',
        'xpath': '//p[contains(.,"сельскохозяйственной деятельности")]',
    },
    {
        'name': 'цели - родовые поселения',
        'path': 'goal/settlements',
        'xpath': '//h4[contains(.,"Ассортимент участков")]',
    },
    {
        'name': 'страница для брокеров',
        'path': 'broker',
        'xpath': '(//*[contains(@class, "uk-inline-clip") and contains(.,"Усадьба Императрицы")])[1]',
    },
    {
        'name': 'страница про инвестиции',
        'path': 'invest-batch',
        'xpath': '//*[contains(@class, "uk-grid")]/div/div//*[contains(.,"+300")]',
    },
    {
        'name': 'страница регистрации клиента от стойки',
        'path': 'public-event',
        'xpath': '//input[@id="publiceventform-name"]',
    },
    {
        'name': 'страница закрытого предложения',
        'path': 'closed-offer',
        'xpath': '//*[contains(., "закрытом предложении")]//input[@id="consultationform-name"]',
    },
    {
        'name': 'страница благодарности',
        'path': 'thanks',
        'xpath': '//h4[contains(., "Спасибо за отправленную заявку!")]',
    },
    {
        'name': 'страница политики конфиденциальности',
        'path': 'policy',
        'xpath': '//p[contains(., "1. Настоящая Политика конфиденциальности")]',
    },
    {
        'name': 'страница согласия на обработку персональных данных',
        'path': 'policy-personal-data',
        'xpath': '//p[contains(., "Разрешаю Оператору производить")]',
    },
    {
        'name': 'страница согласия на получение рассылки',
        'path': 'policy-marketing',
        'xpath': '//p[contains(., "позволяет подтвердить сторонам")]',
    },
    {
        'name': 'страница правил использования сертификата',
        'path': 'cert',
        'xpath': '//li[contains(., "электронный или бумажный")]',
    },
    {
        'name': 'страница ошибки',
        'path': '123',
        'xpath': '//img[@data-src="/img/tractor-drift.gif"]',
    },
]


def main():
    checker = PageChecker(MG_BASE_URL)

    try:
        checker.init_driver()
        results = checker.check_all_pages(PAGES_CONFIG)

        # Дополнительный анализ результатов
        print("\n" + "=" * 60)
        print("ИТОГОВЫЙ ОТЧЕТ:")
        print("=" * 60)

        successful = sum(1 for result in results.values() if result)
        failed = len(results) - successful

        print(f"Успешно: {successful} страниц")
        print(f"С ошибками: {failed} страниц")

        if failed > 0:
            print("\nСтраницы с ошибками:")
            for page_name, result in results.items():
                if not result:
                    print(f"  - {page_name}")

    except Exception as e:
        print(f" Критическая ошибка: {e}")
    finally:
        checker.close()


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