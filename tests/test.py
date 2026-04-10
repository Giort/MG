from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import time
import json
import socket

start_time = time.time()


class VirtourChecker:
    """Класс для проверки загрузки виртуальных туров на сайтах посёлков"""

    def __init__(self, projects_path='../data/project_list.json',
                 virtour_config_path='../data/virtour_config.json'):
        self.driver = self._init_driver()
        self.actions = ActionChains(self.driver)
        self.creds_data = self._load_json('../data/data.json')
        self.projects = self._load_json(projects_path)
        self.virtour_config = self._load_json(virtour_config_path)
        self.current_url = None
        self.is_authenticated = False

    def _init_driver(self):
        """Инициализация драйвера Chrome"""
        service = ChromeService(executable_path=ChromeDriverManager().install())
        ch_options = Options()
        ch_options.add_argument('--headless')
        ch_options.page_load_strategy = 'eager'

        driver = webdriver.Chrome(service=service, options=ch_options)
        driver.set_window_size(1600, 1000)
        driver.implicitly_wait(10)
        driver.set_page_load_timeout(30)
        return driver

    def _load_json(self, path):
        """Загрузка JSON файла"""
        try:
            with open(path, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            print(f'WARNING: Файл {path} не найден')
            return {}
        except json.JSONDecodeError as e:
            print(f'ERROR: Ошибка парсинга JSON {path}: {e}')
            return {}

    def _get_project_url(self, project_name):
        """Получить первый URL проекта по имени"""
        for resource in self.projects.get('resources', []):
            # Проверяем поле project_name
            if resource.get('project_name') == project_name:
                domains = resource.get('domains', [])
                if domains:
                    return domains[0].get('url')
            # Проверяем поле name (для обычных ресурсов)
            if resource.get('name') == project_name:
                return resource.get('url')
        return None

    def _check_domain(self, url, max_attempts=3, wait_time=2):
        """Проверка доступности домена"""
        try:
            domain = url.split('//')[1].split('/')[0]
        except:
            print(f'ERROR: Не удалось извлечь домен из URL: {url}')
            return False

        for attempt in range(max_attempts):
            try:
                socket.gethostbyname(domain)
                return True
            except socket.gaierror as e:
                if attempt == max_attempts - 1:
                    print(f'ERROR: Домен {domain} недоступен - {str(e)}')
                    return False
                time.sleep(wait_time)
            except Exception as e:
                print(f'ERROR: Ошибка проверки домена {domain}: {str(e)}')
                return False
        return False

    def _authenticate(self, credentials_key):
        """Авторизация на текущей странице"""
        if not self._check_domain(self.driver.current_url):
            return False

        try:
            creds = self.creds_data.get(credentials_key, {})
            login_input = wait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, 'loginconfig-username'))
            )
            password_input = self.driver.find_element(By.ID, 'loginconfig-password')
            submit_btn = self.driver.find_element(By.CSS_SELECTOR, 'div button')

            login_input.send_keys(str(creds.get("login", "")))
            password_input.send_keys(str(creds.get("password", "")))
            submit_btn.click()
            time.sleep(2)
            self.is_authenticated = True
            return True
        except Exception as e:
            print(f'ERROR: Ошибка авторизации - {str(e)}')
            return False

    def _load_page(self, url, auth=False, credentials_key=None):
        """Загрузка страницы с возможной авторизацией"""
        if not self._check_domain(url):
            return False

        # Если страница уже загружена и авторизована, не перезагружаем
        if self.current_url == url and self.is_authenticated:
            return True

        try:
            self.driver.get(url)
            self.current_url = url
            self.is_authenticated = False
        except Exception as e:
            print(f'ERROR: Ошибка загрузки {url}: {str(e)}')
            return False

        # Авторизация, если нужно
        if auth and credentials_key:
            return self._authenticate(credentials_key)

        return True

    def _parse_locator(self, locator):
        """
        Преобразует locator из формата JSON в формат Selenium

        Формат JSON: ["by_type", "value"]
        Поддерживаемые by_type: xpath, css_selector, id, class_name, name, tag_name

        Returns:
            tuple (By, value)
        """
        if not locator or len(locator) != 2:
            raise ValueError(f"Неверный формат локатора: {locator}")

        by_type, value = locator

        by_mapping = {
            'xpath': By.XPATH,
            'css_selector': By.CSS_SELECTOR,
            'id': By.ID,
            'class_name': By.CLASS_NAME,
            'name': By.NAME,
            'tag_name': By.TAG_NAME
        }

        if by_type not in by_mapping:
            raise ValueError(f"Неподдерживаемый тип локатора: {by_type}")

        return (by_mapping[by_type], value)

    def check_tour(self, config):
        """
        Проверка виртуального тура

        Args:
            config: Словарь с параметрами:
                - name: название для логов
                - project_name: имя проекта в project_list.json
                - url: URL страницы (опционально, если не указан, берется из project_list)
                - title_locator: ["by_type", "value"] для поиска заголовка/секции
                - btn_locator: ["by_type", "value"] для поиска кнопки тура
                - elem_xpath: ожидаемый эелемент
                - auth: нужно ли авторизоваться (True/False)
                - credentials_key: ключ для данных авторизации
                - scroll: нужно ли скроллить (опционально, по умолчанию False)
                - wait_time: время ожидания перед кликом (опционально, по умолчанию 1)
                - max_attempts: максимальное количество попыток (опционально, по умолчанию 3)
                - iframe_class: класс iframe (опционально, по умолчанию "uk-lightbox-iframe")

        Returns:
            True если проверка успешна, False если нет
        """
        name = config.get('name')
        project_name = config.get('project_name')
        url = config.get('url')

        # Если URL не указан явно, берем из project_list
        if not url and project_name:
            url = self._get_project_url(project_name)

        if not url:
            print(f'ERROR: Не найден URL для {name or project_name}')
            return False

        # Получаем параметры
        title_locator = self._parse_locator(config.get('title_locator'))
        btn_locator = self._parse_locator(config.get('btn_locator'))
        elem_xpath = str(config.get('elem_xpath'))
        auth = config.get('auth', False)
        credentials_key = config.get('credentials_key')
        scroll = config.get('scroll', False)
        wait_time = config.get('wait_time', 1)
        max_attempts = config.get('max_attempts', 3)
        iframe_class = config.get('iframe_class', 'uk-lightbox-iframe')

        # Загружаем страницу
        if not self._load_page(url, auth, credentials_key):
            return False

        count = 0
        while count < max_attempts:
            try:
                # Находим заголовок/секцию и перемещаемся к ней
                title = wait(self.driver, 10).until(
                    EC.presence_of_element_located(title_locator)
                )
                self.actions.move_to_element(title).perform()

                # Скроллим, если нужно
                if scroll:
                    self.actions.send_keys(Keys.PAGE_DOWN).perform()

                time.sleep(wait_time)

                # Находим и кликаем кнопку тура
                btn = wait(self.driver, 10).until(
                    EC.element_to_be_clickable(btn_locator)
                )
                self.actions.click(btn).perform()

                # Переключаемся на iframe
                iframe = wait(self.driver, 20).until(
                    EC.presence_of_element_located((By.CLASS_NAME, iframe_class))
                )
                self.driver.switch_to.frame(iframe)

                # Проверяем наличие элемента с нужным z-index
                elem = wait(self.driver, 30).until(
                    EC.visibility_of_element_located(
                        (By.XPATH, elem_xpath)
                    )
                )

                if elem:
                    print(f'     OK: {name}')
                    self.driver.switch_to.default_content()
                    return True

            except Exception as e:
                self.driver.switch_to.default_content()
                count += 1
                if count == max_attempts:
                    print(f'ERROR: не загрузился виртуальный тур на {name} - {str(e)[:400]}')
                    return False
                else:
                    self.driver.refresh()
                    time.sleep(2)

        return False


    def run_checks(self):
        """Запуск всех проверок из конфига"""
        print(f"\n     Проверка доступности виртуальных туров на сайтах \n")

        # Проверка тура на странице актива
        if 'asset_tour' in self.virtour_config:
            self.check_tour(self.virtour_config['asset_tour'])
            time.sleep(1)

        # Проверка туров на лендингах по конфигу
        for tour in self.virtour_config.get('tours', []):
            self.check_tour(tour)
            time.sleep(1)

    def cleanup(self):
        """Закрытие драйвера"""
        time.sleep(5)
        self.driver.quit()


def main():
    """Основная функция запуска проверок"""
    checker = VirtourChecker()
    try:
        checker.run_checks()
    finally:
        checker.cleanup()


if __name__ == '__main__':
    main()

    end_time = time.time()
    elapsed_time = end_time - start_time
    minutes = int(elapsed_time // 60)
    seconds = int(elapsed_time % 60)

    if minutes > 0:
        print(f'\n     Время выполнения теста: {minutes} мин {seconds} сек ({elapsed_time:.2f} сек)')
    else:
        print(f'\n     Время выполнения теста: {seconds} сек ({elapsed_time:.2f} сек)')