from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time
import json
import socket

start_time = time.time()


class GenplanChecker:
    """Класс для проверки загрузки генпланов на сайтах посёлков"""

    def __init__(self, projects_path='../data/project_list.json',
                 genplan_config_path='../data/genplan_config.json'):
        self.driver = self._init_driver()
        self.actions = ActionChains(self.driver)
        self.creds_data = self._load_json('../data/data.json')
        self.projects = self._load_json(projects_path)
        self.genplan_config = self._load_json(genplan_config_path)
        self.current_url = None
        self.is_authenticated = False

    def _init_driver(self):
        """Инициализация драйвера Chrome"""
        service = ChromeService(executable_path=ChromeDriverManager().install())
        ch_options = Options()
        ch_options.add_argument('--headless')
        ch_options.page_load_strategy = 'eager'

        driver = webdriver.Chrome(service=service, options=ch_options)
        driver.set_window_size(1920, 1080)
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

    def check_genplan_old(self, name, title_xpath, genplan_css, wait_time=14):
        """Проверка генплана старого типа (с кликом)"""
        try:
            # Ожидание и скролл к элементу
            title = wait(self.driver, wait_time).until(
                EC.presence_of_element_located((By.XPATH, title_xpath))
            )
            self.actions.move_to_element(title).perform()

            # Клик для открытия генплана
            title.click()

            # Проверка загрузки генплана
            genplan_elem = wait(self.driver, wait_time).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, genplan_css))
            )

            if genplan_elem:
                print(f'     OK: {name}')
                return True

        except Exception as e:
            print(f'ERROR: генплан на {name}')
            return False

        return False

    def check_genplan_new(self, name, title_xpath, check_css, wait_time=14):
        """Проверка генплана нового типа (без клика)"""
        try:
            # Ожидание появления элемента
            title = wait(self.driver, wait_time).until(
                EC.presence_of_element_located((By.XPATH, title_xpath))
            )

            # Скролл к элементу
            self.actions.move_to_element(title).perform()
            time.sleep(1)

            # Проверка видимости целевого элемента
            check_element = wait(self.driver, wait_time).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, check_css))
            )

            if check_element:
                print(f'     OK: {name}')
                return True

        except Exception as e:
            print(f'ERROR: {name} (проверка нового генплана) - {str(e)[:100]}')
            return False

        return False

    def check_catalogue_map(self, config):
        """Проверка загрузки карты в каталоге"""
        url = config.get('url', 'https://moigektar.ru/catalogue-no-auth')
        name = config.get('name', 'Каталог МГ')
        max_attempts = 3
        wait_time = 14

        if not self._load_page(url):
            return False

        self.actions.send_keys(Keys.PAGE_DOWN).perform()

        for attempt in range(max_attempts):
            try:
                map_button = wait(self.driver, wait_time).until(
                    EC.element_to_be_clickable((By.XPATH, '(//*[text()[contains(., "На карте")]])[1]'))
                )
                map_button.click()

                tour_element = wait(self.driver, wait_time).until(
                    EC.visibility_of_element_located((By.XPATH, '//*[text()[contains(., "Слои")]]'))
                )

                if tour_element:
                    print(f'     OK: {name}')
                    return True

            except Exception as e:
                if attempt == max_attempts - 1:
                    print(f'ERROR: {name} - {str(e)}')
                    return False
                else:
                    try:
                        time.sleep(1)
                        self.driver.refresh()
                    except:
                        pass
                    time.sleep(2)

        return False

    def check_asset_genplan(self, config):
        """Проверка загрузки генплана на странице актива"""
        url = config.get('url', 'https://moigektar.ru/batches-no-auth/60786')
        name = config.get('name', 'Страница участка')
        max_attempts = 3
        wait_time = 14

        if not self._load_page(url):
            return False

        for attempt in range(max_attempts):
            try:
                genplan_button = wait(self.driver, wait_time).until(
                    EC.element_to_be_clickable((By.XPATH, '//*[text()[contains(.,"Генеральный")]]'))
                )

                if attempt == 0:
                    self.actions.move_to_element(genplan_button).perform()

                genplan_button.click()

                to_plot_element = wait(self.driver, wait_time).until(
                    EC.visibility_of_element_located((By.XPATH, '//*[text()[contains(.,"На участок")]]'))
                )

                if to_plot_element:
                    print(f'     OK: {name}')
                    return True

            except Exception as e:
                if attempt == max_attempts - 1:
                    print(f'ERROR: {name} - {str(e)}')
                    return False
                else:
                    try:
                        time.sleep(1)
                        self.driver.refresh()
                    except:
                        pass
                    time.sleep(2)

        return False

    def run_checks(self):
        """Запуск всех проверок из конфига"""
        print(f"\n     Проверка доступности блока генплана на сайтах \n")

        # Проверка каталога
        if 'catalogue' in self.genplan_config:
            self.check_catalogue_map(self.genplan_config['catalogue'])
            time.sleep(1)

        # Проверка страницы актива
        if 'asset' in self.genplan_config:
            self.check_asset_genplan(self.genplan_config['asset'])
            time.sleep(1)

        # Проверка лендингов по конфигу генпланов
        for genplan in self.genplan_config.get('genplans', []):
            project_name = genplan.get('project_name')
            url = self._get_project_url(project_name)

            if not url:
                print(f'WARNING: Не найден URL для проекта {project_name}')
                continue

            # Формируем название для вывода
            plan_name = genplan.get('name')
            if plan_name:
                # Если есть name, выводим project_name - name
                display_name = f"{project_name} - {plan_name}"
            else:
                # Если нет name, выводим только project_name
                display_name = project_name

            auth = genplan.get('auth', False)
            credentials_key = genplan.get('credentials_key')
            genplan_type = genplan.get('type')

            # Загружаем страницу
            if not self._load_page(url, auth, credentials_key):
                continue

            # Проверяем в зависимости от типа
            if genplan_type == 'old':
                self.check_genplan_old(
                    display_name,
                    genplan.get('title_xpath'),
                    genplan.get('genplan_css', 'ymaps.ymaps-2-1-79-inner-panes')
                )
            elif genplan_type == 'new':
                self.check_genplan_new(
                    display_name,
                    genplan.get('title_xpath'),
                    genplan.get('check_css')
                )

            time.sleep(1)

    def cleanup(self):
        """Закрытие драйвера"""
        time.sleep(5)
        self.driver.quit()


def main():
    """Основная функция запуска проверок"""
    checker = GenplanChecker()
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