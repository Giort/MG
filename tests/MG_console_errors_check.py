from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json
import os
import sys
from pathlib import Path
import requests
import logging
logging.getLogger('WDM').setLevel(logging.WARNING)
logging.getLogger('webdriver_manager').setLevel(logging.WARNING)


# Проверка страниц МГ на ошибки в консоли

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('page_checker.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Засекаем время начала теста
start_time = time.time()

# Проверяемый урл
MG_BASE_URL = "https://moigektar.ru"
# MG_BASE_URL = "http://moigektar.localhost"

# Определяем пути
BASE_DIR = Path(__file__).parent.parent  # Поднимаемся на уровень выше tests
TESTS_DIR = BASE_DIR / 'tests'
LOGS_DIR = BASE_DIR / 'logs'
DATA_DIR = BASE_DIR / 'data'
SCREENSHOTS_DIR = LOGS_DIR / 'screenshots'

# Создаем необходимые папки, если их нет
for directory in [LOGS_DIR, DATA_DIR, SCREENSHOTS_DIR]:
    directory.mkdir(exist_ok=True)

# Файлы с данными
DATA_JSON = DATA_DIR / 'data.json'           # файл с учетными данными
MG_PAGES_JSON = DATA_DIR / 'mg_pages.json'   # файл с конфигурацией страниц


def check_data_files():
    """Проверяет наличие необходимых файлов с данными"""
    missing_files = []

    if not DATA_JSON.exists():
        missing_files.append(f"data/{DATA_JSON.name}")

    if not MG_PAGES_JSON.exists():
        missing_files.append(f"data/{MG_PAGES_JSON.name}")

    if missing_files:
        print(f"\n ERROR: Отсутствуют необходимые файлы:")
        for file in missing_files:
            print(f"   - {file}")
        print(f"\nСоздайте папку 'data' на одном уровне с 'tests' и поместите туда файлы:")
        return False

    return True

# НАСТРОЙКА ЛОГИРОВАНИЯ
logging.getLogger('WDM').setLevel(logging.WARNING)
logging.getLogger('webdriver_manager').setLevel(logging.WARNING)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOGS_DIR / 'page_checker.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def load_data():
    """Загружает данные из data.json"""
    try:
        with open(DATA_JSON, 'r', encoding='utf-8') as file:
            data = json.load(file)
        return data
    except FileNotFoundError:
        logger.error(f" ERROR: Файл не найден: {DATA_JSON}")
        raise
    except json.JSONDecodeError as e:
        logger.error(f" ERROR: Ошибка в формате JSON файла {DATA_JSON}: {e}")
        raise
    except Exception as e:
        logger.error(f" ERROR: Ошибка загрузки данных: {e}")
        raise

class PageChecker:
    def __init__(self, base_url):
        self.base_url = base_url.rstrip('/')
        self.driver = None
        self.session = requests.Session()

        # Определяем пути для логов и скриншотов
        self.base_dir = Path(__file__).parent.parent
        self.logs_dir = self.base_dir / 'logs'
        self.screenshots_dir = self.logs_dir / 'screenshots'

        # Создаем папки при инициализации
        self.screenshots_dir.mkdir(exist_ok=True, parents=True)

        # Добавляем временную метку для группировки файлов текущего запуска
        self.run_timestamp = time.strftime('%Y%m%d_%H%M%S')

        # Настраиваем сессию для проверки HTTP
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        })
        self.session.timeout = 15
        self.results = {
            'success': [],
            'errors': []
        }

    def init_driver(self):
        """Инициализация WebDriver"""
        try:
            ch_options = Options()
            ch_options.add_argument('--headless')
            ch_options.add_argument('--no-sandbox')
            ch_options.add_argument('--disable-dev-shm-usage')
            ch_options.add_argument('--disable-gpu')
            ch_options.page_load_strategy = 'eager'

            # Включаем логирование консоли
            ch_options.set_capability('goog:loggingPrefs', {
                'browser': 'ALL',
                'performance': 'ALL'
            })

            service = ChromeService(executable_path=ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=ch_options)
            self.driver.set_window_size(1680, 1000)
            self.driver.implicitly_wait(5)

            # Включаем мониторинг сети через CDP
            self.driver.execute_cdp_cmd('Network.enable', {})

            # Регистрируем обработчик для перехвата консольных ошибок
            self._setup_console_monitoring()

            print("\n     Проверка всех страниц МГ на ошибки в консоли\n")
            return True
        except Exception as e:
            logger.error(f"Ошибка инициализации WebDriver: {e}")
            return False

    def _setup_console_monitoring(self):
        """Настройка мониторинга консоли и сети"""
        # Скрипт для перехвата ошибок в JavaScript
        js_script = """
        // Сохраняем оригинальные методы
        const originalError = console.error;
        const originalWarn = console.warn;

        // Массивы для хранения ошибок
        window._capturedConsoleErrors = [];
        window._capturedNetworkErrors = [];

        // Перехватываем console.error
        console.error = function(...args) {
            const message = args.join(' ');
            window._capturedConsoleErrors.push({
                type: 'console.error',
                message: message,
                timestamp: Date.now(),
                stack: new Error().stack
            });
            return originalError.apply(console, args);
        };

        // Перехватываем console.warn
        console.warn = function(...args) {
            const message = args.join(' ');
            if (message.includes('403') || message.includes('404') || 
                message.includes('500') || message.includes('Failed')) {
                window._capturedConsoleErrors.push({
                    type: 'console.warn',
                    message: message,
                    timestamp: Date.now()
                });
            }
            return originalWarn.apply(console, args);
        };

        // Перехватываем ошибки загрузки ресурсов
        window.addEventListener('error', function(e) {
            if (e.target && (e.target.tagName === 'SCRIPT' || 
                             e.target.tagName === 'LINK' || 
                             e.target.tagName === 'IMG')) {
                window._capturedNetworkErrors.push({
                    type: 'resource_error',
                    url: e.target.src || e.target.href,
                    tag: e.target.tagName,
                    message: 'Failed to load resource'
                });
            }
        }, true);
        """

        self.driver.execute_script(js_script)

    def capture_browser_errors(self):
        """Сбор ошибок из консоли браузера"""
        critical_errors = []  # Критические (4xx, 5xx)
        non_critical_errors = []  # Некритические (предупреждения и т.д.)

        try:
            # Собираем логи из консоли браузера
            browser_logs = self.driver.get_log('browser')

            for entry in browser_logs:
                message = entry.get('message', '')
                level = entry.get('level', '').upper()

                # Пропускаем информационные сообщения
                if level not in ['SEVERE', 'ERROR', 'WARNING']:
                    continue

                # Определяем, критическая ли ошибка
                is_critical = False
                status_code = None
                url = 'unknown'

                # Проверяем на сетевые ошибки (403, 404, 500 и т.д.)
                if any(error_code in message for error_code in
                       [' 403 ', ' 404 ', ' 500 ', ' 502 ', ' 503 ', ' 504 ']):
                    # Это сетевая ошибка - критическая
                    is_critical = True
                    status_code = self._extract_status_code(message)

                    # Извлекаем URL
                    import re
                    url_pattern = r'https?://[^\s\'"]+'
                    urls = re.findall(url_pattern, message)
                    url = urls[0][:150] if urls else 'unknown'

                # Также считаем критические JS ошибки
                elif level == 'SEVERE' and any(phrase in message for phrase in
                                               ['Uncaught', 'SyntaxError', 'TypeError']):
                    is_critical = True

                error_data = {
                    'level': level,
                    'message': message[:250],
                    'url': url,
                    'status': status_code,
                    'source': 'browser_console'
                }

                if is_critical:
                    critical_errors.append(error_data)
                else:
                    non_critical_errors.append(error_data)

        except Exception as e:
            logger.warning(f"Ошибка при сборе ошибок из браузера: {e}")

        return critical_errors, non_critical_errors

    def _extract_status_code(self, message):
        """Извлекает статус код и определяет, критический ли он"""
        import re

        # Ищем статус коды
        patterns = [
            r'\s(\d{3})\s+\([^)]+\)',  # " 403 (Forbidden)"
            r'status[=:]\s*(\d{3})',  # "status=403"
            r'\"status\":\s*(\d{3})',  # "status": 403
        ]

        for pattern in patterns:
            match = re.search(pattern, message)
            if match:
                status = int(match.group(1))
                # Критические только 4xx и 5xx
                if 400 <= status < 600:
                    return status

        return None

    def _extract_url_from_message(self, message):
        """Извлекает URL из сообщения об ошибке"""
        import re
        url_pattern = r'https?://[^\s\']+'
        match = re.search(url_pattern, message)
        return match.group(0)[:200] if match else 'unknown'

    def check_http_status(self, url, timeout=15):
        """
        Проверка HTTP статуса страницы
        Возвращает (status_code, error_message, response_time)
        """
        try:
            start = time.time()
            response = self.session.get(
                url,
                timeout=timeout,
                allow_redirects=True
            )
            response_time = time.time() - start

            status_code = response.status_code

            # Классификация ошибок
            if 400 <= status_code < 500:
                error_type = f"Клиентская ошибка {status_code}"
                return status_code, error_type, response_time
            elif 500 <= status_code < 600:
                error_type = f"Серверная ошибка {status_code}"
                return status_code, error_type, response_time
            else:
                return status_code, None, response_time

        except requests.exceptions.Timeout:
            return None, f"Таймаут ({timeout} секунд)", None
        except requests.exceptions.ConnectionError as e:
            return None, f"Ошибка подключения: {str(e)}", None
        except requests.exceptions.TooManyRedirects:
            return None, "Слишком много перенаправлений", None
        except requests.exceptions.RequestException as e:
            return None, f"Ошибка запроса: {str(e)}", None
        except Exception as e:
            return None, f"Неизвестная ошибка: {str(e)}", None

    def _log_error(self, page_name, url, error_type, error_message,
                   http_status, response_time, critical_errors=None, non_critical_errors=None):
        """Логирование ошибки"""

        # Сохраняем скриншот для ошибок
        screenshot_path = None
        if self.driver and error_type not in ['HTTP_ERROR']:
            screenshot_path = self.save_screenshot("error", page_name)

        error_info = {
            'page': page_name,
            'url': url,
            'error_type': error_type,
            'error_message': error_message,
            'http_status': http_status,
            'response_time': response_time,
            'critical_errors': critical_errors or [],
            'non_critical_errors': non_critical_errors or [],
            'screenshot': screenshot_path,
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
        }
        self.results['errors'].append(error_info)

    def _log_success(self, page_name, url, http_status, response_time, non_critical_errors=None):
        """Логирование успешной проверки"""
        success_info = {
            'page': page_name,
            'url': url,
            'http_status': http_status,
            'response_time': response_time,
            'non_critical_errors': non_critical_errors or [],
            'has_non_critical_errors': bool(non_critical_errors),
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
        }
        self.results['success'].append(success_info)

    def quick_image_health_check(self):
        """Быстрая проверка здоровья сервера картинок"""

        test_urls = [
            "https://i.bigland.ru/images/f64bad331de9d257296fee7ee50966a8173a91c9d3c37434120a2de378dadd0a/2xl",
        ]

        all_ok = True
        for url in test_urls:
            try:
                response = self.session.head(url, timeout=10)

                if response.status_code != 200:
                    all_ok = False

            except Exception as e:
                print(f"  \033[31m✗\033[0m {url[:50]}... - ERROR: {str(e)[:30]}")
                all_ok = False

        if all_ok:
            print("\n     ОК: Все критичные изображения доступны")
        else:
            print("  \033[31m⚠ Есть проблемы с изображениями!\033[0m")

        return all_ok

    def check_page_elements(self, url, xpath_selector, timeout=20):
        """
        Проверка наличия элементов на странице
        """
        try:
            self.driver.get(url)

            # Проверяем, что страница загрузилась (заголовок не пустой)
            if self.driver.title is None or self.driver.title.strip() == "":
                logger.warning(f"Страница загружена с пустым заголовком: {url}")

            # Ждем появления элемента
            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((By.XPATH, xpath_selector))
            )

            # Дополнительная проверка, что элемент видим
            if element.is_displayed():
                print(f"     ОК: Элемент найден и видим")
                return True, None
            else:
                # Если элемент не видим, прокручиваем к нему
                self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});",
                                           element)
                time.sleep(0.5)

                if element.is_displayed():
                    logger.debug(f"     ОК: Элемент найден и стал видимым после прокрутки")
                    return True, None
                else:
                    return False, f"     Элемент найден, но не видим"

        except TimeoutException:
            error_msg = f"Таймаут ({timeout} сек) при ожидании элемента: {xpath_selector[:50]}..."

            # Пытаемся сделать скриншот при ошибке
            try:
                # Генерируем имя файла с timestamp
                page_name = url.split('/')[-1] if url.split('/')[-1] else 'home'
                screenshot_name = f"error_{self.run_timestamp}_{page_name}.png"
                screenshot_path = self.screenshots_dir / screenshot_name

                self.driver.save_screenshot(str(screenshot_path))
                error_msg += f" (скриншот: logs/screenshots/{screenshot_name})"
            except Exception as screenshot_error:
                error_msg += f" (не удалось сохранить скриншот: {screenshot_error})"

            return False, error_msg
        except NoSuchElementException:
            return False, f"Элемент не найден: {xpath_selector[:50]}..."
        except Exception as e:
            return False, f"Ошибка Selenium: {str(e)[:100]}"

    def save_screenshot(self, prefix="screenshot", page_name=None):
        """
        Сохраняет скриншот текущей страницы в папку logs/screenshots

        Args:
            prefix: префикс имени файла
            page_name: имя страницы (будет использовано в имени файла)

        Returns:
            Путь к сохраненному файлу или None при ошибке
        """
        try:
            if not self.driver:
                return None

            # Формируем имя файла
            if page_name:
                # Убираем недопустимые символы для имени файла
                safe_page_name = ''.join(c for c in page_name if c.isalnum() or c in (' ', '-', '_')).strip()
                safe_page_name = safe_page_name.replace(' ', '_')
                filename = f"{prefix}_{self.run_timestamp}_{safe_page_name}.png"
            else:
                filename = f"{prefix}_{self.run_timestamp}.png"

            screenshot_path = self.screenshots_dir / filename
            self.driver.save_screenshot(str(screenshot_path))

            logger.debug(f"Скриншот сохранен: {screenshot_path}")
            return str(screenshot_path)

        except Exception as e:
            logger.error(f"Ошибка сохранения скриншота: {e}")
            return None

    def check_page(self, page_config, delay=1):
        """
        Полная проверка одной страницы
        """
        page_name = page_config['name']
        page_path = page_config['path']
        xpath_selector = page_config['xpath']

        full_url = f"{self.base_url}/{page_path.lstrip('/')}"

        # Исключение для страницы ошибки 404
        is_error_page = page_path == '123'

        # Шаг 1: Проверка HTTP статуса
        http_status, http_error, response_time = self.check_http_status(full_url)

        if http_error and not is_error_page:
            # Обычная страница - ошибка критическая
            print(f"HTTP ошибка: {http_error}")
            return False
        elif http_error and is_error_page:
            # Страница ошибки - проверяем что это именно 404
            if http_status == 404:
                print(f"     Ожидаемая ошибка 404 (страница не найдена)")
            else:
                print(f"HTTP ошибка: {http_error} (неожиданный статус)")
                return False
        elif not http_error and is_error_page:
            # Если страница ошибки вернула не 404 - это проблема
            if http_status != 404:
                print(f"ОШИБКА: страница ошибки вернула {http_status} вместо 404")
                return False

        print(f"     HTTP статус: {http_status} (время ответа: {response_time:.2f} сек)")

        # Шаг 2: Проверка элементов на странице
        elements_ok, elements_error = self.check_page_elements(
            full_url,
            xpath_selector
        )

        if not elements_ok:
            # Отсутствие элемента - критическая ошибка
            print(f"Ошибка элемента: {elements_error}")
            self._log_error(page_name, full_url, 'ELEMENT_ERROR', elements_error, http_status, response_time)
            return False

        # Шаг 3: Сбор ошибок из консоли браузера
        time.sleep(1)  # Даем время для выполнения запросов
        critical_errors, non_critical_errors = self.capture_browser_errors()

        # Логируем некритические ошибки (только если их много)
        if non_critical_errors:
            # print(f"Найдено некритических ошибок: {len(non_critical_errors)} (не мешают работе)")
            # Можно залогировать в файл, но не выводить в консоль
            logger.debug(f"Некритические ошибки на {page_name}: {len(non_critical_errors)}")

        # Проверяем критические ошибки
        if critical_errors:
            if not is_error_page:
                logger.warning(f"ERROR:  Найдено критических ошибок: {len(critical_errors)}")
                for error in critical_errors[:3]:  # Показываем первые 3
                    status = f"[{error.get('status', '?')}] " if error.get('status') else ""
                    url_display = error.get('url', '')[:50] if error.get('url') != 'unknown' else ''
                    print(f"  - {status}{url_display}")

                # Логируем детали критической ошибки
                error_message = f"Найдено {len(critical_errors)} критических ошибок в консоли"
                self._log_error(
                    page_name, full_url, 'CONSOLE_ERRORS', error_message,
                    http_status, response_time, critical_errors, non_critical_errors
                )
                return False

        # Успешная проверка
        self._log_success(
            page_name, full_url, http_status, response_time,
            non_critical_errors  # Сохраняем некритические ошибки для отчета
        )

        # Пауза между проверками
        time.sleep(delay)

        return True

    def check_all_pages(self, pages_config, delay=1):

        # Быстрая проверка картинок перед тестами
        self.quick_image_health_check()

        """
        Проверка всех страниц из конфигурации
        """
        print(f"\n     Начинаем проверку страниц")

        total_pages = len(pages_config)
        successful = 0
        failed = 0

        for i, page_config in enumerate(pages_config, 1):
            print(f"\n     Страница {i}/{total_pages}: {page_config['name']}")

            try:
                if self.check_page(page_config, delay):
                    successful += 1
                else:
                    failed += 1

            except Exception as e:
                logger.error(f" Критическая ошибка при проверке страницы: {e}")
                failed += 1
                error_info = {
                    'page': page_config['name'],
                    'url': f"{self.base_url}/{page_config['path'].lstrip('/')}",
                    'error_type': 'CRITICAL_ERROR',
                    'error_message': str(e),
                    'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
                }
                self.results['errors'].append(error_info)

        # Вывод итогового отчета
        self.print_summary(total_pages, successful, failed)

        return self.results

    def print_summary(self, total, successful, failed):
        """
        Вывод отчета
        """

        print(f"\n {' #' * 80}")
        print("     ОТЧЕТ")

        print(f"\n     Статистика:")
        print(f"       Всего проверено страниц: {total}")
        print(f"       Успешно: {successful} ({successful / total * 100:.1f}%)")
        print(f"       С ошибками: {failed} ({failed / total * 100:.1f}%)")

        # Собираем все критические ошибки
        all_critical_errors = []
        for error in self.results['errors']:
            if 'critical_errors' in error:
                all_critical_errors.extend(error['critical_errors'])

        # Группируем критические ошибки по типу
        if all_critical_errors:
            print(f"\n     КРИТИЧЕСКИЕ ОШИБКИ ПО ТИПАМ:")

            # Сетевые ошибки (4xx, 5xx)
            network_errors = [e for e in all_critical_errors if e.get('status')]
            if network_errors:
                print(f"\n       Сетевые ошибки:")
                error_counts = {}
                for error in network_errors:
                    status = error.get('status', 'unknown')
                    error_counts[status] = error_counts.get(status, 0) + 1

                for status, count in sorted(error_counts.items()):
                    print(f"     {status}: {count} ошибок")

            # JS ошибки
            js_errors = [e for e in all_critical_errors if not e.get('status')]
            if js_errors:
                print(f"       JavaScript ошибки: {len(js_errors)}")

        # Выводим детали по страницам с критическими ошибками
        if self.results['errors']:
            print(f"\n     СТРАНИЦЫ С КРИТИЧЕСКИМИ ОШИБКАМИ:")
            for error in self.results['errors']:
                print(f"\n       Страница: {error['page']}")
                print(f"         URL: {error['url']}")
                print(f"         Тип ошибки: {error['error_type']}")
                print(f"         Сообщение: {error['error_message']}")

                # Выводим только критические ошибки
                if 'critical_errors' in error and error['critical_errors']:
                    print(f"         Критические ошибки:")
                    for crit_err in error['critical_errors'][:3]:  # Первые 3
                        if crit_err.get('status'):
                            status = crit_err.get('status', '?')
                            url_display = crit_err.get('url', '')[:60]
                            print(f"         [{status}] {url_display}...")
                        else:
                            msg = crit_err.get('message', '')[:80]
                            print(f"         JS: {msg}...")

    def auth(self):
        """Авторизация в системе"""
        try:
            print("     Выполняем авторизацию...")
            self.driver.get(f"{self.base_url}/")
            auth_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '(//*[@href="#modal-auth-lk"])[1]'))
            )
            auth_button.click()
            time.sleep(1)

            # Переключаемся на вход по паролю
            password_tab = self.driver.find_element(By.XPATH, '//*[text()="По паролю"]')
            password_tab.click()
            time.sleep(0.5)

            # Заполняем форму
            name_field = self.driver.find_element(By.XPATH, '//*[@id="authform-login"]')
            password_field = self.driver.find_element(By.XPATH, '//*[@id="authform-password"]')
            submit_button = self.driver.find_element(By.XPATH, '//*[text()="Войти"]')

            name_field.send_keys(str(data["LK_cred"]["login"]))
            password_field.send_keys(str(data["LK_cred"]["password"]))
            submit_button.click()

            # Ждем успешной авторизации
            time.sleep(3)

            # Проверяем, что авторизация прошла успешно
            try:
                self.driver.find_element(By.XPATH, '(//a[@href="https://moigektar.ru/catalogue/compare"])[1]')
                print("     Авторизация успешна")
                return True
            except:
                logger.warning("Авторизация возможно не удалась")
                return True  # Все равно продолжаем проверку

        except Exception as e:
            logger.error(f"Ошибка авторизации: {e}")
            return False

    def close(self):
        """Закрытие ресурсов"""
        if self.driver:
            self.driver.quit()
        self.session.close()


def load_pages_config(config_file='mg_pages.json'):
    """
    Загружает конфигурацию страниц из JSON файла
    """
    try:
        # Определяем путь к файлу конфигурации
        config_path = DATA_DIR / config_file

        if not config_path.exists():
            # Пробуем найти в текущей директории (для обратной совместимости)
            alt_path = Path(config_file)
            if alt_path.exists():
                config_path = alt_path
                logger.warning(
                    f"⚠ Файл найден в текущей директории, а не в data/. Рекомендуется переместить его в data/")
            else:
                raise FileNotFoundError(f"Файл конфигурации не найден: {config_path}")

        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)

        return config

    except json.JSONDecodeError as e:
        logger.error(f"❌ Ошибка в формате JSON файла {config_path}: {e}")
        raise
    except Exception as e:
        logger.error(f"❌ Ошибка загрузки конфигурации: {e}")
        raise

# Загружаем данные
try:
    data = load_data()
except Exception as e:
    print(f"\n ERROR: Не удалось загрузить данные. Тест остановлен.")
    sys.exit(1)


def get_default_pages_config():
    """
    Возвращает конфигурацию по умолчанию
    (на случай, если файл не найден)
    """
    return [
        {
            'name': 'Главная страница',
            'path': '',
            'xpath': "//h1[contains(., 'Мой гекатар')]",
        },
        {
            'name': 'Страница актива',
            'path': 'batches/30608',
            'xpath': "(//*[@uk-toggle='target: #modal-batch-detail'])[2]",
        },
        {
            'name': 'Страница для брокеров',
            'path': 'broker',
            'xpath': "(//*[contains(@class, 'uk-inline-clip') and contains(.,'Усадьба Императрицы')])[1]",
        }
    ]

def main():
    """Основная функция"""
    checker = PageChecker(MG_BASE_URL)

    try:

        pages_config = load_pages_config('../data/mg_pages.json')

        # Инициализируем драйвер
        if not checker.init_driver():
            logger.error("Не удалось инициализировать WebDriver")
            return

        # Выполняем авторизацию (если нужно)
        checker.auth()

        # Проверяем все страницы
        results = checker.check_all_pages(pages_config, delay=1)

    except Exception as e:
        logger.error(f"Критическая ошибка в main: {e}")
        import traceback
        traceback.print_exc()
    finally:
        checker.close()
        print("\n     Ресурсы освобождены")


if __name__ == "__main__":
    main()

# Время выполнения
end_time = time.time()
elapsed_time = end_time - start_time
minutes = int(elapsed_time // 60)
seconds = int(elapsed_time % 60)

print(f"\n{'=' * 80}")
if minutes > 0:
    print(f"     Общее время выполнения: {minutes} мин {seconds} сек")
else:
    print(f"     Общее время выполнения: {seconds:.1f} сек")
print(f"{'=' * 80}")