from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json
from pathlib import Path


# Проверка доступности пользовательских страниц при разных состояниях
#
# Состояния:
# - не авторизован
# - зашёл по no-auth
# - авторизован как демо
# - авторизован как зарегистрированный пользователь
# -- хорошо бы проверять доступность с офисных айпи

# Проверяемый урл
MG_BASE_URL = "https://moigektar.ru"
LK_BASE_URL = "https://cabinet.moigektar.ru"
# MG_BASE_URL = "http://moigektar.localhost"
# LK_BASE_URL = "http://cabinet.moigektar.localhost"


# Определяем пути
BASE_DIR = Path(__file__).parent.parent  # Поднимаемся на уровень выше tests
TESTS_DIR = BASE_DIR / 'tests'
DATA_DIR = BASE_DIR / 'data'

# Создаем необходимые папки, если их нет
DATA_DIR.mkdir(exist_ok=True)

# Файлы с данными
DATA_JSON = DATA_DIR / 'data.json'           # файл с учетными данными


def check_data_files():
    """Проверяет наличие необходимых файлов с данными"""
    missing_files = []

    if not DATA_JSON.exists():
        missing_files.append(f"data/{DATA_JSON.name}")

    if missing_files:
        print(f"\n ERROR: Отсутствуют необходимые файлы:")
        for file in missing_files:
            print(f"   - {file}")
        print(f"\nСоздайте папку 'data' на одном уровне с 'tests' и поместите туда файлы:")
        return False

    return True


def load_data():
    """Загружает данные из data.json"""
    try:
        with open(DATA_JSON, 'r', encoding='utf-8') as file:
            data = json.load(file)
        return data
    except FileNotFoundError:
        print(f" ERROR: Файл не найден: {DATA_JSON}")
        raise
    except json.JSONDecodeError as e:
        print(f" ERROR: Ошибка в формате JSON файла {DATA_JSON}: {e}")
        raise
    except Exception as e:
        print(f" ERROR: Ошибка загрузки данных: {e}")
        raise

# Засекаем время начала теста
start_time = time.time()


class UnauthChecker:
    def __init__(self, mg_base_url):
        self.mg_base_url = mg_base_url.rstrip('/')
        self.driver = None

    def init_driver(self):
        """Инициализация драйвера"""
        ch_options = Options()
        ch_options.add_argument('--headless')
        ch_options.page_load_strategy = 'eager'
        service = ChromeService(executable_path=ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=ch_options)
        self.driver.set_window_size(1680, 1000)
        self.driver.implicitly_wait(10)
        return self.driver

    def check_page(self, page_config, timeout=20):
        """
        Проверяет доступность страницы и наличие элемента

        Args:
            page_config: словарь с конфигурацией страницы
            timeout: время ожидания элемента
        """
        page_path = page_config['path']
        page_name = page_config['name']
        xpath_selector = page_config['xpath']

        full_url = f"{self.mg_base_url}/{page_path.lstrip('/')}"

        # Выполняем три попытки
        for attempt in range(3):
            try:
                self.driver.get(full_url)

                # Ждем появления элемента
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
        """
        Проверяет все страницы из конфигурации

        Args:
            pages_config: список словарей с конфигурациями страниц
            delay: задержка между проверками
        """
        print(f"\n     Проверка страниц для _неавторизованного пользователя_ на домене {self.mg_base_url}")

        results = {}
        for page_config in pages_config:
            result = self.check_page(page_config)
            results[page_config['name']] = result
            time.sleep(delay)

        return results

    def close(self):
        """Закрывает драйвер"""
        if self.driver:
            self.driver.quit()

# Конфигурация страниц и элементов
PAGES_CONFIG = [
    {
        'name': 'каталог',
        'path': 'catalogue',
        'xpath': '//*[text()[contains(.,"Доступ в каталог")]]',
    },
    {
        'name': 'страница актива',
        'path': 'batches/30608',
        'xpath': '//*[text()[contains(.,"Доступ в каталог")]]',
    },
    {
        'name': 'избранное',
        'path': 'catalogue/wishlist',
        'xpath': '//*[text()[contains(.,"для авторизованных пользователей.")]]',
    },
    {
        'name': 'сравнения',
        'path': 'catalogue/compare',
        'xpath': '//*[text()[contains(.,"для авторизованных пользователей.")]]',
    },
]


def main():
    checker = UnauthChecker(MG_BASE_URL)

    try:
        checker.init_driver()
        results = checker.check_all_pages(PAGES_CONFIG)

    except Exception as e:
        print(f" Критическая ошибка: {e}")
    finally:
        checker.close()


if __name__ == "__main__":
    main()




class DemoChecker:
    def __init__(self, mg_base_url):
        self.mg_base_url = mg_base_url.rstrip('/')
        self.driver = None

    def init_driver(self):

        ch_options = Options()
        ch_options.add_argument('--headless')
        ch_options.page_load_strategy = 'eager'
        service = ChromeService(executable_path=ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=ch_options)
        self.driver.set_window_size(1680, 1000)
        self.driver.implicitly_wait(10)
        return self.driver

    def open_cabinet(self):
        """Открываем ЛК для того, чтобы произошла авторизация от лица демо-пользователя"""
        try:
            self.driver.get(LK_BASE_URL)
            return True
        except Exception as e:
            print(f" ERROR: Не удалось открыть cabinet - {str(e)}")
            return False

    def check_page(self, page_config, timeout=20):

        page_path = page_config['path']
        page_name = page_config['name']
        xpath_selector = page_config['xpath']

        full_url = f"{self.mg_base_url}/{page_path.lstrip('/')}"

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
        """
        Проверяет все страницы из конфигурации

        Args:
            pages_config: список словарей с конфигурациями страниц
            delay: задержка между проверками
        """
        print(f"\n     Проверка страниц для _демо-пользователя_")

        # сначала заходим в кабинет

        self.open_cabinet()
        time.sleep(6)

        results = {}
        for page_config in pages_config:
            result = self.check_page(page_config)
            results[page_config['name']] = result
            time.sleep(delay)

        return results

    def close(self):
        """Закрывает драйвер"""
        if self.driver:
            self.driver.quit()


# Конфигурация страниц и элементов
PAGES_CONFIG = [
    {
        'name': 'каталог',
        'path': 'catalogue',
        'xpath': '//*[text()[contains(.,"Доступ в каталог")]]',
    },
    {
        'name': 'страница актива',
        'path': 'batches/30608',
        'xpath': '//*[text()[contains(.,"Доступ в каталог")]]',
    },
    {
        'name': 'избранное',
        'path': 'catalogue/wishlist',
        'xpath': '//*[text()[contains(.,"для авторизованных пользователей.")]]',
    },
    {
        'name': 'сравнения',
        'path': 'catalogue/compare',
        'xpath': '//*[text()[contains(.,"для авторизованных пользователей.")]]',
    },
]


def main():
    checker = DemoChecker(MG_BASE_URL)

    try:
        checker.init_driver()
        results = checker.check_all_pages(PAGES_CONFIG)

    except Exception as e:
        print(f" Критическая ошибка: {e}")
    finally:
        checker.close()


if __name__ == "__main__":
    main()


class NoAuthChecker:
    def __init__(self, mg_base_url):
        self.mg_base_url = mg_base_url.rstrip('/')
        self.driver = None

    def init_driver(self):

        ch_options = Options()
        ch_options.add_argument('--headless')
        ch_options.page_load_strategy = 'eager'
        service = ChromeService(executable_path=ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=ch_options)
        self.driver.set_window_size(1680, 1000)
        self.driver.implicitly_wait(10)
        return self.driver

    def check_page(self, page_config, timeout=20):

        page_path = page_config['path']
        page_name = page_config['name']
        xpath_selector = page_config['xpath']

        full_url = f"{self.mg_base_url}/{page_path.lstrip('/')}"

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
                    time.sleep()
                else:
                    print(f" ERROR: {page_name} - {str(e)}")
                    return False

    def check_all_pages(self, pages_config, delay=1):

        print(f"\n     Проверка страниц _при входе по no-auth_")

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
        'name': 'каталог',
        'path': 'catalogue-no-auth',
        'xpath': '(//*[(contains(@class, "js-batch-name"))])[1]',
    },
    {
        'name': 'страница актива',
        'path': 'batches/30608',
        'xpath': '(//*[@uk-toggle="target: #modal-batch-detail"])[2]',
    },
    {
        'name': 'избранное',
        'path': 'catalogue/wishlist',
        'xpath': '//*[text()[contains(.,"для авторизованных пользователей.")]]',
    },
    {
        'name': 'сравнения',
        'path': 'catalogue/compare',
        'xpath': '//*[text()[contains(.,"для авторизованных пользователей.")]]',
    },
]


def main():
    checker = NoAuthChecker(MG_BASE_URL)

    try:
        checker.init_driver()
        results = checker.check_all_pages(PAGES_CONFIG)

    except Exception as e:
        print(f" Критическая ошибка: {e}")
    finally:
        checker.close()


if __name__ == "__main__":
    main()


class AuthChecker:
    def __init__(self, mg_base_url, auth_data):
        self.mg_base_url = mg_base_url.rstrip('/')
        self.driver = None
        self.auth_data = auth_data  # Сохраняем данные для авторизации

    def init_driver(self):

        ch_options = Options()
        ch_options.add_argument('--headless')
        ch_options.page_load_strategy = 'eager'
        service = ChromeService(executable_path=ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=ch_options)
        self.driver.set_window_size(1680, 1000)
        self.driver.implicitly_wait(10)
        return self.driver

    def auth(self):
        if not self.auth_data:
            print(" ERROR: Данные для авторизации не установлены")
            return False

        try:
            self.driver.get("https://moigektar.ru//")
            self.driver.find_element(By.XPATH, '(//*[@href="#modal-auth-lk"])[1]').click()
            time.sleep(2)
            tab = self.driver.find_element(By.XPATH, '//*[text()="По паролю"]')
            name = self.driver.find_element(By.XPATH, '//*[@id="authform-login"]')
            password = self.driver.find_element(By.XPATH, '//*[@id="authform-password"]')
            btn = self.driver.find_element(By.XPATH, '//*[text()="Войти"]')
            tab.click()
            name.send_keys(str(self.auth_data["login"]))
            password.send_keys(str(self.auth_data["password"]))
            btn.click()
            time.sleep(5)
            return True
        except Exception as e:
            print(f" ERROR: Не удалось авторизоваться - {str(e)}")
            return False

    def check_page(self, page_config, timeout=20):

        page_path = page_config['path']
        page_name = page_config['name']
        xpath_selector = page_config['xpath']

        full_url = f"{self.mg_base_url}/{page_path.lstrip('/')}"

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

        print(f"\n     Проверка страниц для _авторизованного пользователя_")

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
        'name': 'каталог',
        'path': 'catalogue-no-auth',
        'xpath': '(//*[(contains(@class, "js-batch-name"))])[1]',
    },
    {
        'name': 'страница актива',
        'path': 'batches/30608',
        'xpath': '(//*[@uk-toggle="target: #modal-batch-detail"])[2]',
    },
    {
        'name': 'избранное',
        'path': 'catalogue/wishlist',
        'xpath': '//*[text()[contains(.,"Мои подборки")]]',
    },
    {
        'name': 'сравнения',
        'path': 'catalogue/compare',
        'xpath': '//*[text()[contains(.,"Выбранные участки")]]',
    },
]


def main():
    if not check_data_files():
        return

    try:
        all_data = load_data()
    except Exception as e:
        print(f" ERROR: Не удалось загрузить данные: {e}")
        return

    checker = AuthChecker(MG_BASE_URL, all_data.get("LK_cred", {}))

    try:
        checker.init_driver()
        results = checker.check_all_pages(PAGES_CONFIG)

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