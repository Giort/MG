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
import requests
from urllib.parse import urljoin
import logging
logging.getLogger('WDM').setLevel(logging.WARNING)
logging.getLogger('webdriver_manager').setLevel(logging.WARNING)


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

with open('data.json', 'r') as file:
    data = json.load(file)

# Засекаем время начала теста
start_time = time.time()

# Проверяемый урл
MG_BASE_URL = "https://moigektar.ru"


# MG_BASE_URL = "http://moigektar.localhost"


class PageChecker:
    def __init__(self, base_url):
        self.base_url = base_url.rstrip('/')
        self.driver = None
        self.session = requests.Session()
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

            service = ChromeService(executable_path=ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=ch_options)
            self.driver.set_window_size(1680, 1000)
            self.driver.implicitly_wait(5)

            print("\n     Проверка всех страниц МГ\n")
            return True
        except Exception as e:
            logger.error(f"Ошибка инициализации WebDriver: {e}")
            return False

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
                print(f"     ОК: Элемент найден и видим: {xpath_selector[:50]}...")
                return True, None
            else:
                # Если элемент не видим, прокручиваем к нему
                self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});",
                                           element)
                time.sleep(0.5)

                if element.is_displayed():
                    logger.debug(f"     ОК: Элемент найден и стал видимым после прокрутки: {xpath_selector[:50]}...")
                    return True, None
                else:
                    return False, f"     Элемент найден, но не видим: {xpath_selector[:50]}..."

        except TimeoutException:
            error_msg = f"Таймаут ({timeout} сек) при ожидании элемента: {xpath_selector[:50]}..."

            # Пытаемся сделать скриншот при ошибке
            try:
                screenshot_name = f"error_{time.strftime('%Y%m%d_%H%M%S')}.png"
                self.driver.save_screenshot(screenshot_name)
                error_msg += f" (скриншот сохранен: {screenshot_name})"
            except:
                pass

            return False, error_msg
        except NoSuchElementException:
            return False, f"Элемент не найден: {xpath_selector[:50]}..."
        except Exception as e:
            return False, f"Ошибка Selenium: {str(e)[:100]}"

    def check_page(self, page_config, delay=1):
        """
        Полная проверка одной страницы
        """
        page_name = page_config['name']
        page_path = page_config['path']
        xpath_selector = page_config['xpath']

        full_url = f"{self.base_url}/{page_path.lstrip('/')}"

        # Шаг 1: Проверка HTTP статуса
        http_status, http_error, response_time = self.check_http_status(full_url)

        if http_error:
            error_info = {
                'page': page_name,
                'url': full_url,
                'error_type': 'HTTP_ERROR',
                'error_message': http_error,
                'http_status': http_status,
                'response_time': response_time,
                'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
            }
            self.results['errors'].append(error_info)
            logger.error(f"❌ HTTP ошибка: {http_error}")
            return False

        print(f"     HTTP статус: {http_status} (время ответа: {response_time:.2f} сек)")

        # Шаг 2: Проверка элементов на странице
        elements_ok, elements_error = self.check_page_elements(
            full_url,
            xpath_selector
        )

        if not elements_ok:
            error_info = {
                'page': page_name,
                'url': full_url,
                'error_type': 'ELEMENT_ERROR',
                'error_message': elements_error,
                'http_status': http_status,
                'response_time': response_time,
                'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
            }
            self.results['errors'].append(error_info)
            logger.error(f"❌ Ошибка элемента: {elements_error}")
            return False

        # Успешная проверка
        success_info = {
            'page': page_name,
            'url': full_url,
            'http_status': http_status,
            'response_time': response_time,
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
        }
        self.results['success'].append(success_info)

        # Пауза между проверками
        time.sleep(delay)

        return True

    def check_all_pages(self, pages_config, delay=1):
        """
        Проверка всех страниц из конфигурации
        """
        print(f"     Начинаем проверку страниц")

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
                logger.error(f"❌ Критическая ошибка при проверке страницы: {e}")
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
        Вывод итогового отчета
        """
        print(f"\n{'#' * 80}")
        print("ОТЧЕТ")

        print(f"\n📊 Статистика:")
        print(f"   Всего проверено страниц: {total}")
        print(f"   Успешно: {successful} ({successful / total * 100:.1f}%)")
        print(f"   С ошибками: {failed} ({failed / total * 100:.1f}%)")

        if failed > 0:
            logger.info(f"\n❌ СТРАНИЦЫ С ОШИБКАМИ:")
            for error in self.results['errors']:
                logger.info(f"\n   Страница: {error['page']}")
                logger.info(f"   URL: {error['url']}")
                logger.info(f"   Тип ошибки: {error['error_type']}")
                logger.info(f"   Сообщение: {error['error_message']}")
                if error.get('http_status'):
                    logger.info(f"   HTTP статус: {error['http_status']}")
                logger.info(f"   Время: {error['timestamp']}")

        # Сохраняем детальный отчет в JSON файл
        try:
            report_file = f"check_report_{time.strftime('%Y%m%d_%H%M%S')}.json"
            with open(report_file, 'w', encoding='utf-8') as f:
                json.dump(self.results, f, ensure_ascii=False, indent=2)
            print(f"\n📄 Детальный отчет сохранен в: {report_file}")
        except Exception as e:
            logger.error(f"Не удалось сохранить отчет: {e}")

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


PAGES_CONFIG = [
    {
        'name': 'главная',
        'path': '/',
        'xpath': '//h2[text()[contains(.,"Описание проекта")]]',
        'scroll_lazy': True
    },
    {
        'name': 'страница актива',
        'path': 'batches/30608',
        'xpath': '(//*[@uk-toggle="target: #modal-batch-detail"])[2]',
        'scroll_lazy': True
    },
    {
        'name': 'онлайн-поселок - голосования и опросы',
        'path': 'polls?list=all',
        'xpath': '(//*[@class="list-view"]//*[contains(@class, "poll-item")])[1]'
    },
    {
        'name': 'о проекте',
        'path': 'about',
        'xpath': '//*[text()[contains(.,"Цель проекта")]]',
    },
    {
        'name': 'страница ошибки',
        'path': '123',
        'xpath': '//img[@data-src="/img/tractor-drift.gif"]',
    },
]


def main():
    """Основная функция"""
    checker = PageChecker(MG_BASE_URL)

    try:
        # Инициализируем драйвер
        if not checker.init_driver():
            logger.error("Не удалось инициализировать WebDriver")
            return

        # Выполняем авторизацию (если нужно)
        checker.auth()

        # Проверяем все страницы
        results = checker.check_all_pages(PAGES_CONFIG, delay=1)

    except Exception as e:
        logger.error(f"Критическая ошибка в main: {e}")
        import traceback
        traceback.print_exc()
    finally:
        checker.close()
        print("Ресурсы освобождены")


if __name__ == "__main__":
    main()

# Время выполнения
end_time = time.time()
elapsed_time = end_time - start_time
minutes = int(elapsed_time // 60)
seconds = int(elapsed_time % 60)

print(f"\n{'=' * 80}")
if minutes > 0:
    print(f"⏱️ Общее время выполнения: {minutes} мин {seconds} сек")
else:
    print(f"⏱️ Общее время выполнения: {seconds:.1f} сек")
print(f"{'=' * 80}")