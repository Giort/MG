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

# Засекаем время начала теста
start_time = time.time()

# Загрузка данных авторизации
with open('../data/data.json', 'r') as file:
    data = json.load(file)

# Базовые URL
MG_BASE_URL = "https://moigektar.ru"
LK_BASE_URL = "https://cabinet.moigektar.ru"

# Конфигурация страниц
PAGES = {
    'catalogue': {
        'name': 'каталог',
        'path': 'catalogue',
        'xpath_unauth': '//*[text()[contains(.,"Доступ в каталог")]]',
        'xpath_noauth': '(//*[(contains(@class, "js-batch-name"))])[1]',
        'xpath_auth': '(//*[(contains(@class, "js-batch-name"))])[1]',
    },
    'asset': {
        'name': 'страница актива',
        'path': 'batches/30608',
        'xpath_unauth': '//*[text()[contains(.,"Доступ в каталог")]]',
        'xpath_noauth': '(//*[@uk-toggle="target: #modal-batch-detail"])[2]',
        'xpath_auth': '(//*[@uk-toggle="target: #modal-batch-detail"])[2]',
    },
    'wishlist': {
        'name': 'избранное',
        'path': 'catalogue/wishlist',
        'xpath_unauth': '//*[text()[contains(.,"для авторизованных пользователей.")]]',
        'xpath_noauth': '//*[text()[contains(.,"для авторизованных пользователей.")]]',
        'xpath_auth': '//*[text()[contains(.,"Мои подборки")]]',
    },
    'compare': {
        'name': 'сравнения',
        'path': 'catalogue/compare',
        'xpath_unauth': '//*[text()[contains(.,"для авторизованных пользователей.")]]',
        'xpath_noauth': '//*[text()[contains(.,"для авторизованных пользователей.")]]',
        'xpath_auth': '//*[text()[contains(.,"Выбранные участки")]]',
    }
}

# Специальные страницы с нестандартными путями
SPECIAL_PAGES = {
    'catalogue_noauth': {
        'name': 'каталог',
        'path': 'catalogue-no-auth',
        'xpath_unauth': None,  # не используется
        'xpath_noauth': '(//*[(contains(@class, "js-batch-name"))])[1]',
        'xpath_auth': '(//*[(contains(@class, "js-batch-name"))])[1]',
    }
}


class PageChecker:
    """
    Универсальный класс для проверки доступности страниц
    с разными состояниями авторизации
    """

    # Конфигурации состояний
    STATES = {
        'unauth': {
            'page_keys': ['catalogue', 'asset', 'wishlist', 'compare'],
            'page_source': PAGES,
            'xpath_suffix': 'unauth',
            'need_auth': False,
            'need_demo': False,
            'need_noauth_prefix': False,
            'description': 'неавторизованного пользователя'
        },
        'demo': {
            'page_keys': ['catalogue', 'asset', 'wishlist', 'compare'],
            'page_source': PAGES,
            'xpath_suffix': 'unauth',
            'need_auth': False,
            'need_demo': True,
            'need_noauth_prefix': False,
            'description': 'демо-пользователя'
        },
        'noauth': {
            'page_keys': ['catalogue_noauth', 'asset', 'wishlist', 'compare'],
            'page_source': {**PAGES, **SPECIAL_PAGES},
            'xpath_suffix': 'noauth',
            'need_auth': False,
            'need_demo': False,
            'need_noauth_prefix': True,
            'description': 'при входе по no-auth'
        },
        'auth': {
            'page_keys': ['catalogue_noauth', 'asset', 'wishlist', 'compare'],
            'page_source': {**PAGES, **SPECIAL_PAGES},
            'xpath_suffix': 'auth',
            'need_auth': True,
            'need_demo': False,
            'need_noauth_prefix': False,
            'description': 'авторизованного пользователя'
        }
    }

    def __init__(self, mg_base_url=MG_BASE_URL, lk_base_url=LK_BASE_URL):
        self.mg_base_url = mg_base_url.rstrip('/')
        self.lk_base_url = lk_base_url.rstrip('/')
        self.driver = None

    def init_driver(self):
        """Инициализация драйвера Chrome"""
        ch_options = Options()
        # ch_options.add_argument('--headless')
        ch_options.page_load_strategy = 'eager'
        service = ChromeService(executable_path=ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=ch_options)
        self.driver.set_window_size(1680, 1000)
        self.driver.implicitly_wait(10)
        return self.driver

    def _remove_popups(self):
        """Удаление всплывающих окон"""
        popup_selectors = [
            "//div[@id='visitors-popup']",
            "//*[contains(@class, 'js-webinar-running-event-modal')]"
        ]
        for selector in popup_selectors:
            try:
                popup = self.driver.find_element(By.XPATH, selector)
                self.driver.execute_script("arguments[0].remove();", popup)
            except Exception:
                pass

    def _demo_auth(self):
        """Авторизация как демо-пользователь (через открытие ЛК)"""

        try:
            self.driver.get(self.lk_base_url)
            time.sleep(2)
            return True
        except Exception as e:
            print(f" ERROR: Не удалось выполнить демо-авторизацию - {str(e)}")
            return False

    def _full_auth(self):
        """Полноценная авторизация с логином и паролем"""
        try:
            self.driver.get(f"{self.mg_base_url}/")
            time.sleep(1)

            self._remove_popups()

            # Открываем модальное окно авторизации
            self.driver.find_element(By.XPATH, '(//*[@href="#modal-auth-lk"])[1]').click()
            time.sleep(1)

            # Переключаемся на вкладку "По паролю"
            self.driver.find_element(By.XPATH, '//*[text()="По паролю"]').click()
            time.sleep(0.5)

            # Вводим данные
            name_input = self.driver.find_element(By.XPATH, '//*[@id="authform-login"]')
            password_input = self.driver.find_element(By.XPATH, '//*[@id="authform-password"]')
            submit_btn = self.driver.find_element(By.XPATH, '//*[text()="Войти"]')

            name_input.send_keys(str(data.get("LK_cred", {}).get("login", "")))
            password_input.send_keys(str(data.get("LK_cred", {}).get("password", "")))
            submit_btn.click()

            time.sleep(5)

            return True
        except Exception as e:
            print(f" ERROR: Не удалось авторизоваться - {str(e)}")
            return False

    def _get_pages_for_state(self, state):
        """
        Получить список страниц для конкретного состояния

        Args:
            state: ключ состояния ('unauth', 'demo', 'noauth', 'auth')

        Returns:
            list: список словарей с параметрами страниц
        """
        state_config = self.STATES.get(state)
        if not state_config:
            return []

        pages = []
        for page_key in state_config['page_keys']:
            page = state_config['page_source'].get(page_key)
            if page:
                xpath_key = f"xpath_{state_config['xpath_suffix']}"
                xpath = page.get(xpath_key)

                # Пропускаем страницы, для которых нет XPath для этого состояния
                if xpath is None:
                    continue

                pages.append({
                    'name': page['name'],
                    'path': page['path'],
                    'xpath': xpath
                })

        return pages

    def check_page(self, page_config, timeout=20):
        """
        Проверка отдельной страницы

        Args:
            page_config: словарь с параметрами страницы
            timeout: время ожидания элемента
        """
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

        return False

    def run_check(self, state='unauth', delay=1):
        """
        Запуск проверки для определённого состояния

        Args:
            state: состояние ('unauth', 'demo', 'noauth', 'auth')
            delay: задержка между проверками
        """
        state_config = self.STATES.get(state)
        if not state_config:
            print(f" ERROR: Неизвестное состояние '{state}'")
            return {}

        print(f"\n     Проверка страниц для {state_config['description']}")

        # Подготовка перед проверками
        if state_config.get('need_demo'):
            if not self._demo_auth():
                return {}
            time.sleep(6)

        if state_config.get('need_auth'):
            if not self._full_auth():
                return {}
            time.sleep(6)

        # Получаем страницы для этого состояния
        pages = self._get_pages_for_state(state)

        # Проверка страниц
        results = {}
        for page_config in pages:
            result = self.check_page(page_config)
            results[page_config['name']] = result
            time.sleep(delay)

        return results

    def run_all_checks(self, delay=1):
        """Запуск всех проверок последовательно"""
        for state in self.STATES.keys():
            self.init_driver()
            self.run_check(state, delay)
            self.close()
            time.sleep(2)

    def close(self):
        """Закрытие драйвера"""
        if self.driver:
            self.driver.quit()


def main():
    """Основная функция"""

    # Выводим заголовок в самом начале
    print(f"\n     Проверка состояний пользовательских страниц на домене {MG_BASE_URL}")

    checker = PageChecker()

    try:
        checker.run_all_checks()

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