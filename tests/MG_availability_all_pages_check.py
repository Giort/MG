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
import os
from pathlib import Path

# Проверка доступности страниц на МГ


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


class PageChecker:
    def __init__(self, mg_base_url):
        self.mg_base_url = mg_base_url.rstrip('/')
        self.driver = None

    def set_auth_data(self, auth_data):
        """Устанавливает данные для авторизации"""
        self.auth_data = auth_data

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
        """ Авторизация """
        if not self.auth_data:
            print(" ERROR: Данные для авторизации не установлены")
            return False

        try:
            self.driver.get("https://moigektar.ru//")
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


def load_pages_config(config_file='mg_pages.json'):
    """
    Загружает конфигурацию страниц из JSON файла
    """
    try:
        # Проверяем существование файла
        if not os.path.exists(config_file):
            raise FileNotFoundError(f" ERROR: Файл конфигурации не найден: {config_file}")

        with open(config_file, 'r', encoding='utf-8') as f:
            config = json.load(f)

        return config

    except json.JSONDecodeError as e:
        print(f" ERROR: Ошибка в формате JSON файла {config_file}: {e}")
        raise
    except Exception as e:
        print(f" ERROR: Ошибка загрузки конфигурации: {e}")
        # Возвращаем конфигурацию по умолчанию
        return get_default_pages_config()


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
    # Проверяем наличие необходимых файлов
    if not check_data_files():
        return  # Прерываем выполнение, если файлы не найдены

    # Загружаем данные
    try:
        data = load_data()
    except Exception as e:
        print(f" ERROR: Не удалось загрузить данные: {e}")
        return

    checker = PageChecker(MG_BASE_URL)

    try:
        # Передаем данные в checker (можно через конструктор или отдельно)
        checker.set_auth_data(data["LK_cred"])

        pages_config = load_pages_config('../data/mg_pages.json')
        checker.init_driver()
        results = checker.check_all_pages(pages_config, delay=1)

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