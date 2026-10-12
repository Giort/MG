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
from helpers.popups import remove_popups
from helpers.auth import auth_mg

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
        self.results = {'success': [], 'failed': []}

    def _init_driver(self):
        """Инициализация драйвера Chrome"""
        service = ChromeService(executable_path=ChromeDriverManager().install())
        ch_options = Options()
        ch_options.add_argument('--headless')
        ch_options.page_load_strategy = 'eager'

        driver = webdriver.Chrome(service=service, options=ch_options)
        driver.set_window_size(1920, 1080)
        driver.implicitly_wait(10)
        driver.set_page_load_timeout(60)
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

    def _get_auth_from_project_list(self, project_name):
        """
        Получить настройки авторизации для проекта из project_list.json

        Returns:
            tuple: (нужна_ли_авторизация, ключ_для_credentials)
        """
        for resource in self.projects.get('resources', []):
            if resource.get('project_name') == project_name:
                auth_config = resource.get('auth', False)

                if not auth_config:
                    return False, None
                elif isinstance(auth_config, str):
                    return True, auth_config
                elif isinstance(auth_config, bool) and auth_config is True:
                    return True, project_name
                else:
                    return False, None

        return False, None

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

    def _load_page(self, url, auth=False, credentials_key=None, max_attempts=3, retry_delay=5):
        """Загрузка страницы с повторными попытками и возможной авторизацией"""
        if not self._check_domain(url):
            return False

        # Если страница уже загружена и авторизована, не перезагружаем
        if self.current_url == url and self.is_authenticated:
            return True

        for attempt in range(1, max_attempts + 1):
            try:
                self.driver.get(url)
                self.current_url = url
                self.is_authenticated = False
                break
            except Exception as e:
                # Страница не загрузилась - сбрасываем состояние
                self.current_url = None
                self.is_authenticated = False

                if attempt == max_attempts:
                    print(f'ERROR: Ошибка загрузки {url} (попыток: {max_attempts}): {str(e)[:200]}')
                    return False

                # Останавливаем зависшую загрузку, чтобы следующий get() не упал сразу
                try:
                    self.driver.execute_script('window.stop();')
                except Exception:
                    pass
                time.sleep(retry_delay)

        # Авторизация, если нужно
        if auth and credentials_key:
            return self._authenticate(credentials_key)

        return True

    @staticmethod
    def _is_true(value):
        """Приведение значения флага из конфига к bool (true / "true" / 1 / "1" / "да")"""
        if isinstance(value, bool):
            return value
        if isinstance(value, (int, float)):
            return value == 1
        if isinstance(value, str):
            return value.strip().lower() in ('true', '1', 'yes', 'да')
        return False

    def _click_element(self, element):
        """
        Нажатие на элемент, запускающий генплан (постер или тайтл).
        Если обычный клик перехвачен другим элементом - кликаем через JS.
        """
        self.actions.move_to_element(element).perform()
        try:
            element.click()
        except Exception:
            self.driver.execute_script("arguments[0].click();", element)

        # Даём генплану время начать загрузку
        time.sleep(1)

    def _scroll_to_anchor(self, anchor_xpath, wait_time=14):
        """
        Прокрутка к якорю перед поиском тайтла - для блоков с ленивой загрузкой,
        которые появляются в DOM только когда до них доскроллили.
        Используется JS scrollIntoView: якорь может быть пустым элементом
        без размеров, и move_to_element на нём не сработает.
        """
        anchor = wait(self.driver, wait_time).until(
            EC.presence_of_element_located((By.XPATH, anchor_xpath))
        )
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'start'});", anchor
        )
        # Даём блоку время подгрузиться
        time.sleep(2)

    def _get_poster_xpath(self, config):
        """
        Локатор постера из конфига.
        Постер нажимается, если указан poster_xpath; poster_click: false
        позволяет временно отключить нажатие, не удаляя локатор.
        Возвращает (xpath или None, ошибка конфига или None).
        """
        poster_xpath = config.get('poster_xpath')
        poster_click = config.get('poster_click')

        if poster_click is not None and not self._is_true(poster_click):
            return None, None
        if self._is_true(poster_click) and not poster_xpath:
            return None, 'включён poster_click, но не указан poster_xpath'
        return poster_xpath, None

    def check_genplan(self, name, config, url=None, wait_time=14):
        """
        Единая проверка генплана для обоих типов:
          1. прокрутка к якорю (anchor_xpath, если блок грузится лениво);
          2. перемещение к тайтлу (title_xpath);
          3. нажатие на постер, запускающий генплан:
             - poster_xpath, если указан;
             - иначе для type "old" постером считается сам тайтл;
             - иначе для type "new" ничего не нажимается;
          4. проверка загрузки:
             - type "old": видимость genplan_css;
             - type "new": видимость check_xpath.
        """
        genplan_type = config.get('type')
        if genplan_type == 'old':
            check_locator = (By.CSS_SELECTOR, config.get('genplan_css'))
        elif genplan_type == 'new':
            check_locator = (By.XPATH, config.get('check_xpath'))
        else:
            print(f'WARNING: Неизвестный type "{genplan_type}" для {name}')
            self._record_result(name, False, url)
            return False

        poster_xpath, config_error = self._get_poster_xpath(config)
        if config_error:
            print(f'WARNING: Для {name} {config_error}')
            self._record_result(name, False, url)
            return False

        try:
            # 1. Прокрутка к якорю (если блок грузится лениво)
            anchor_xpath = config.get('anchor_xpath')
            if anchor_xpath:
                self._scroll_to_anchor(anchor_xpath, wait_time)

            # 2. Перемещение к тайтлу
            title = wait(self.driver, wait_time).until(
                EC.presence_of_element_located((By.XPATH, config.get('title_xpath')))
            )
            self.actions.move_to_element(title).perform()
            time.sleep(1)

            # 3. Нажатие на постер
            if poster_xpath:
                poster = wait(self.driver, wait_time).until(
                    EC.element_to_be_clickable((By.XPATH, poster_xpath))
                )
                self._click_element(poster)
            elif genplan_type == 'old':
                self._click_element(title)

            # 4. Проверка загрузки генплана
            wait(self.driver, wait_time).until(
                EC.visibility_of_element_located(check_locator)
            )
            print(f'     OK: {name}')
            self._record_result(name, True, url)
            return True

        except Exception as e:
            print(f'ERROR: генплан на {name} - {str(e)[:100]} ({url})')
            self._record_result(name, False, url)
            return False

    def check_moigektar_genplan(self, config):
        """
        Проверка генплана на отдельных страницах сайта Мой Гектар
        (в отличие от check_asset/catalogue, URL берётся напрямую из
        конфига, а не через project_list.json; поддерживает и старый,
        и новый тип генплана через поле 'type')
        """
        url = config.get('url')
        name = config.get('name', url)

        if not url:
            print(f'WARNING: Не указан url для {name}')
            self._record_result(name, False, None)
            return False

        if not self._load_page(url):
            self._record_result(name, False, url)
            return False

        remove_popups(self.driver)

        # Для страниц МГ тип по умолчанию - новый (как и раньше)
        return self.check_genplan(name, {'type': 'new', **config}, url=url)

    def _authenticate_mg(self):
        """
        Авторизация на сайте Мой Гектар через модальное окно (helpers.auth.auth_mg).
        Вызывается один раз перед проверками МГ - куки сессии затем
        действуют для всех последующих страниц этого домена.
        Логика повторяет mg_availability_uspages_check.py.
        """
        auth_config = self.genplan_config.get('auth')
        if not auth_config:
            return True

        credentials_key = auth_config.get('credentials_key', 'LK_cred')
        creds = self.creds_data.get(credentials_key, {})

        if not creds:
            print(f'WARNING: Не найдены credentials по ключу "{credentials_key}" в data.json')
            return False

        auth_url = auth_config.get('auth_url', 'https://moigektar.ru/12345')

        try:
            if not auth_mg(self.driver, auth_url=auth_url, creds=creds):
                print('ERROR: Не удалось авторизоваться на Мой Гектар')
                return False

            time.sleep(6)
            self.current_url = auth_url
            self.is_authenticated = True
            return True
        except Exception as e:
            print(f'ERROR: Ошибка авторизации на Мой Гектар - {str(e)}')
            return False

    def check_catalogue_map(self, config):
        """Проверка загрузки карты в каталоге"""
        url = config.get('url', 'https://moigektar.ru/catalogue-no-auth')
        name = config.get('name', 'Каталог МГ')
        max_attempts = 3
        wait_time = 14

        if not self._load_page(url):
            self._record_result(name, False, url)
            return False

        remove_popups(self.driver)

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
                    self._record_result(name, True, url)
                    return True

            except Exception as e:
                if attempt == max_attempts - 1:
                    print(f'ERROR: {name} - {str(e)} ({url})')
                    self._record_result(name, False, url)
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
        wait_time = 30

        if not self._load_page(url):
            self._record_result(name, False, url)
            return False

        remove_popups(self.driver)

        for attempt in range(max_attempts):
            try:
                genplan_button = wait(self.driver, wait_time).until(
                    EC.element_to_be_clickable((By.XPATH, '(//*[text()[contains(.,"Генеральный")]])[2]'))
                )

                if attempt == 0:
                    self.actions.move_to_element(genplan_button).perform()

                genplan_button.click()

                to_plot_element = wait(self.driver, wait_time).until(
                    EC.visibility_of_element_located((By.XPATH, '//*[text()[contains(.,"На участок")]]'))
                )

                if to_plot_element:
                    print(f'     OK: {name}')
                    self._record_result(name, True, url)
                    return True

            except Exception as e:
                if attempt == max_attempts - 1:
                    print(f'ERROR: {name} - {str(e)} ({url})')
                    self._record_result(name, False, url)
                    return False
                else:
                    try:
                        time.sleep(1)
                        self.driver.refresh()
                    except:
                        pass
                    time.sleep(2)

        return False

    def _record_result(self, name: str, success: bool, url: str = None):
        if success:
            self.results['success'].append(name)
        else:
            self.results['failed'].append((name, url))

    def _print_summary(self):
        total   = len(self.results['success']) + len(self.results['failed'])
        success = len(self.results['success'])
        failed  = len(self.results['failed'])

        print(f"\n     {'=' * 50}")
        print(f"     Итого: {total}  |  OK: {success}  |  Ошибок: {failed}")

        if self.results['failed']:
            print(f"\n     Недоступные генпланы:")
            for name, url in self.results['failed']:
                if url:
                    print(f"       - {name} {url}")
                else:
                    print(f"       - {name}")
        else:
            print(f"\n     ОШИБОК НЕТ")

    def run_checks(self):
        """Запуск всех проверок из конфига"""
        print(f"\n     Проверка доступности блока генплана на сайтах \n")

        # Авторизация на Мой Гектар (теперь требуется для доступа к генпланам)
        self._authenticate_mg()

        # Проверка каталога
        if 'catalogue' in self.genplan_config:
            self.check_catalogue_map(self.genplan_config['catalogue'])
            time.sleep(1)

        # Проверка страницы актива
        if 'asset' in self.genplan_config:
            self.check_asset_genplan(self.genplan_config['asset'])
            time.sleep(1)

        # Проверка генпланов на прочих страницах Мой Гектар
        # (старого и/или нового типа, URL задаётся прямо в конфиге)
        for genplan in self.genplan_config.get('moigektar_genplans', []):
            self.check_moigektar_genplan(genplan)
            time.sleep(1)

        # Проверка лендингов по конфигу генпланов
        for genplan in self.genplan_config.get('genplans', []):
            project_name = genplan.get('project_name')

            # Формируем название для вывода
            plan_name = genplan.get('name')
            if plan_name:
                display_name = f"{project_name} - {plan_name}"
            else:
                display_name = project_name

            url = self._get_project_url(project_name)

            if not url:
                print(f'WARNING: Не найден URL для проекта {project_name}')
                self._record_result(display_name, False, None)
                continue

            # ПОЛУЧАЕМ АВТОРИЗАЦИЮ ИЗ PROJECT_LIST
            auth, credentials_key = self._get_auth_from_project_list(project_name)

            # Загружаем страницу
            if not self._load_page(url, auth, credentials_key):
                self._record_result(display_name, False, url)
                continue

            self.check_genplan(display_name, genplan, url=url)

            time.sleep(1)

        self._print_summary()

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