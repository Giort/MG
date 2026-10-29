from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException, InvalidArgumentException
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time
import json
import os
import socket

# Проверка доступности веб-интерфейсов сервисов по наличию на страницах ключевых элементов

# Засекаем время начала теста
start_time = time.time()

# Подстроки URL, ошибки по которым не учитываются при проверке консоли
# (например, сторонние счётчики). Пример: ['mc.yandex.ru', 'google-analytics.com']
CONSOLE_IGNORE_URLS = []

# Сколько ошибок консоли выводить по одному сайту
CONSOLE_ERRORS_PRINT_LIMIT = 5


def init_driver():
    """Инициализация драйвера Chrome"""
    ch_options = Options()
    ch_options.add_argument('--headless')
    ch_options.page_load_strategy = 'eager'

    # Журнал сетевых событий - из него берутся HTTP-статусы всех запросов страницы
    ch_options.set_capability('goog:loggingPrefs', {'performance': 'ALL'})

    service = ChromeService(executable_path=ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=ch_options)
    driver.set_window_size(1680, 1000)
    driver.implicitly_wait(10)
    driver.set_page_load_timeout(30)
    return driver


def check_domain(url, max_attempts=3, wait_time=2):
    """Проверка доступности домена с несколькими попытками"""
    try:
        domain = url.split('//')[1].split('/')[0]
    except:
        print(f'ERROR: Не удалось извлечь домен из URL: {url}')
        return False

    for attempt in range(max_attempts):
        try:
            socket.gethostbyname(domain)
            if attempt > 0:
                print(f'     == Домен {domain} доступен после {attempt + 1} попытки')
            return True
        except socket.gaierror:
            if attempt == max_attempts - 1:
                return False
            else:
                time.sleep(wait_time)
        except Exception as e:
            print(f'ERROR: Неожиданная ошибка при проверке домена {domain}: {str(e)}')
            return False
    return False


def flush_network_log(driver):
    """
    Очистка накопленного журнала сети.
    Вызывается перед каждой загрузкой страницы, чтобы ошибки
    предыдущего сайта не попали в отчёт по следующему.
    """
    try:
        driver.get_log('performance')
    except Exception:
        pass


def collect_http_errors(driver, ignore_urls=None):
    """
    Сбор запросов страницы, вернувших 4xx/5xx (то, что в консоли браузера
    выглядит как "Failed to load resource: the server responded with a status of ...").

    Returns:
        list: [{'status': 404, 'url': '...', 'count': 1}, ...]
    """
    ignore_urls = ignore_urls if ignore_urls is not None else CONSOLE_IGNORE_URLS
    errors = {}

    try:
        logs = driver.get_log('performance')
    except Exception as e:
        print(f'WARNING: Не удалось получить журнал сети: {str(e)[:100]}')
        return []

    for entry in logs:
        try:
            message = json.loads(entry['message'])['message']
        except Exception:
            continue

        if message.get('method') != 'Network.responseReceived':
            continue

        response = message.get('params', {}).get('response', {})
        url = response.get('url', '')
        try:
            status = int(response.get('status'))
        except (TypeError, ValueError):
            continue

        if not 400 <= status < 600:
            continue
        if any(pattern in url for pattern in ignore_urls):
            continue

        # Один и тот же запрос может повторяться - считаем, а не дублируем
        key = (status, url)
        if key in errors:
            errors[key]['count'] += 1
        else:
            errors[key] = {'status': status, 'url': url, 'count': 1}

    return sorted(errors.values(), key=lambda e: (e['status'], e['url']))


def print_http_errors(errors, indent='       ', limit=CONSOLE_ERRORS_PRINT_LIMIT):
    """Вывод списка ошибок консоли"""
    for error in errors[:limit]:
        count = f" (x{error['count']})" if error['count'] > 1 else ''
        print(f"{indent}[{error['status']}] {error['url'][:150]}{count}")
    if len(errors) > limit:
        print(f'{indent}... и ещё {len(errors) - limit}')


def check_console(driver, display_name, url, console_report, skip=False):
    """
    Проверка ошибок 4xx/5xx в консоли после загрузки страницы.
    Найденные ошибки выводятся сразу и сохраняются в console_report для итогового отчёта.
    skip=True - проверка консоли для сайта отключена
    Ключ skip_console_check в конфиге. Для одиночного сайта: ключ добавляется в список
    остальных ключей. Для проекта с несколькими доменами ключ можно поставить на весь проект
    или на отдельный домен. Флаг домена важнее флага проекта, поэтому можно, например,
    отключить проверку для всего проекта, а для одного домена включить обратно через
    "skip_console_check": false
    """
    if skip:
        return []

    # Даём странице время выполнить фоновые запросы
    time.sleep(1)

    errors = collect_http_errors(driver)
    if errors:
        print(f'WARNING: {display_name} - ошибки в консоли: {len(errors)} ({url})')
        print_http_errors(errors)
        console_report.append({'name': display_name, 'url': url, 'errors': errors})

    return errors


def load_resources():
    """Загрузка конфигурации ресурсов из JSON файла"""
    try:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        json_path = os.path.join(os.path.dirname(current_dir), 'data', 'project_list.json')

        with open(json_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            return data.get('resources', [])
    except FileNotFoundError:
        print(f"ERROR: Файл project_list.json не найден")
        return []
    except json.JSONDecodeError as e:
        print(f"ERROR: Ошибка парсинга JSON: {e}")
        return []
    except Exception as e:
        print(f"ERROR: Неожиданная ошибка при загрузке ресурсов: {e}")
        return []


def load_auth_data():
    """Загрузка данных для авторизации"""
    try:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        json_path = os.path.join(os.path.dirname(current_dir), 'data', 'data.json')

        with open(json_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        print("WARNING: файл data.json не найден, авторизация будет пропущена")
        return {}
    except Exception as e:
        print(f"WARNING: Ошибка загрузки data.json: {e}")
        return {}


def get_auth_credentials(auth_config, project_name):
    """
    Получить данные для авторизации на основе конфига auth

    Args:
        auth_config: значение поля auth из project_list.json
        project_name: имя проекта

    Returns:
        tuple: (нужна_ли_авторизация, ключ_для_credentials)
    """
    if not auth_config:
        return False, None

    if isinstance(auth_config, str):
        # Если строка - используем её как ключ
        return True, auth_config
    elif isinstance(auth_config, bool) and auth_config is True:
        # Если True - используем project_name как ключ
        return True, project_name
    else:
        return False, None


def perform_auth(driver, auth_config, project_name, auth_data):
    """
    Универсальная авторизация на странице

    Args:
        driver: WebDriver
        auth_config: значение поля auth из конфига
        project_name: имя проекта
        auth_data: словарь с данными авторизации

    Returns:
        bool: успешность авторизации
    """
    need_auth, credentials_key = get_auth_credentials(auth_config, project_name)

    if not need_auth or not auth_data:
        return True

    # Отдельно пробуем найти форму логина. Если её нет на странице — это не ошибка авторизации
    # (возможно, сессия уже авторизованаили форма логина не требуется на этой странице), поэтому не
    # считаем это провалом и не пишем ложное предупреждение.
    try:
        login_input = wait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'loginconfig-username'))
        )
    except TimeoutException:
        return True

    # Форма логина найдена — вот тут уже реальная попытка авторизации,
    # и любая ошибка на этом этапе действительно является ошибкой авторизации
    try:
        password_input = driver.find_element(By.ID, 'loginconfig-password')
        submit_btn = driver.find_element(By.CSS_SELECTOR, 'div button, button[type]')

        creds = auth_data.get(credentials_key, {})
        login = str(creds.get("login", ""))
        password = str(creds.get("password", ""))

        login_input.send_keys(login)
        password_input.send_keys(password)
        submit_btn.click()
        time.sleep(2)

        # Запросы до входа (например, 401 от API) не считаем ошибками сайта
        flush_network_log(driver)

        return True
    except Exception as e:
        print(f'WARNING: Ошибка авторизации - {str(e)[:100]}')
        return False


def check_single_resource(driver, resource, auth_data, console_report):
    """Проверка одного ресурса (одиночный URL)"""
    url = resource['url']
    name = resource['name']
    selector = resource['selector']
    auth_config = resource.get('auth', False)
    clear_cookies = resource.get('clear_cookies', False)
    skip_console = resource.get('skip_console_check', False) is True
    max_attempts = 3
    wait_timeout = 14

    # Проверка доступности домена
    if not check_domain(url):
        print(f'ERROR: {name} - домен недоступен ({url})')
        return False

    # Загрузка страницы
    try:
        flush_network_log(driver)
        driver.get(url)
        time.sleep(1)
    except InvalidArgumentException:
        print(f'ERROR: {name} - некорректный URL ({url})')
        return False
    except Exception as e:
        print(f'ERROR: {name} - ошибка загрузки: {str(e)[:100]} ({url})')
        return False

    # Авторизация, если нужна
    perform_auth(driver, auth_config, name, auth_data)

    # Проверка элемента
    for attempt in range(max_attempts):
        try:
            elem = wait(driver, wait_timeout).until(
                EC.visibility_of_element_located((By.XPATH, selector))
            )
            if elem:
                print(f'     OK: {name}')
                check_console(driver, name, url, console_report, skip_console)

                if clear_cookies:
                    driver.delete_all_cookies()
                    time.sleep(5)

                return True
        except Exception as e:
            if attempt == max_attempts - 1:
                print(f'ERROR: {name}: {str(e)[:100]} ({url})')
                check_console(driver, name, url, console_report, skip_console)

                if clear_cookies:
                    driver.delete_all_cookies()
                    time.sleep(0.5)

                return False
            else:
                try:
                    flush_network_log(driver)
                    driver.refresh()
                    time.sleep(2)

                    # Повторная авторизация после обновления
                    perform_auth(driver, auth_config, name, auth_data)
                except:
                    pass

    return False


def check_project_with_domains(driver, project, auth_data, console_report):
    """
    Проверка проекта с несколькими доменами.

    Returns:
        tuple: (успешных доменов, доменов с ошибкой)
    """
    project_name = project['project_name']
    domains = project['domains']
    selector = project['selector']
    auth_config = project.get('auth', False)
    clear_cookies = project.get('clear_cookies', False)

    successful = 0
    failed = 0

    for domain in domains:
        url = domain['url']
        domain_name = domain['name']

        # Флаг домена важнее флага проекта
        skip_console = domain.get(
            'skip_console_check', project.get('skip_console_check', False)
        ) is True

        # Для логов используем короткое имя
        display_name = f"[{project_name}] {domain_name}"

        # Проверка доступности домена
        if not check_domain(url):
            print(f'ERROR: {display_name} - домен недоступен ({url})')
            failed += 1
            continue

        # Загрузка страницы
        try:
            flush_network_log(driver)
            driver.get(url)
            time.sleep(2)
        except Exception as e:
            print(f'ERROR: {display_name} - ошибка загрузки: {str(e)[:100]} ({url})')
            failed += 1
            continue

        # Авторизация, если нужна (универсальный метод)
        perform_auth(driver, auth_config, project_name, auth_data)

        # Проверка элемента
        success = False
        for attempt in range(3):
            try:
                elem = wait(driver, 14).until(
                    EC.visibility_of_element_located((By.XPATH, selector))
                )
                if elem:
                    print(f'     OK: {display_name}')
                    check_console(driver, display_name, url, console_report, skip_console)
                    success = True

                    if clear_cookies:
                        driver.delete_all_cookies()
                        time.sleep(5)

                    break
            except Exception as e:
                if attempt == 2:
                    print(f'ERROR: {display_name} - {str(e)[:100]} ({url})')
                    check_console(driver, display_name, url, console_report, skip_console)

                    if clear_cookies:
                        driver.delete_all_cookies()
                        time.sleep(0.5)

                else:
                    try:
                        flush_network_log(driver)
                        driver.refresh()
                        time.sleep(2)
                        # Повторная авторизация после обновления
                        perform_auth(driver, auth_config, project_name, auth_data)
                    except:
                        pass

        if success:
            successful += 1
        else:
            failed += 1

        time.sleep(0.5)  # Пауза между доменами

    return successful, failed


def main():
    """Основная функция запуска проверок"""
    print(f"\n     Проверка доступности сайтов \n")

    # Загрузка данных
    resources = load_resources()
    if not resources:
        print("ERROR: Нет ресурсов для проверки")
        return

    auth_data = load_auth_data()

    # Инициализация драйвера
    driver = init_driver()

    try:
        total_resources = 0
        successful = 0
        failed = 0
        console_report = []  # Сайты с ошибками 4xx/5xx в консоли

        # Сайты, у которых проверка консоли отключена (для итогов)
        skipped_console = []
        for resource in resources:
            if 'domains' in resource:
                for domain in resource['domains']:
                    if domain.get('skip_console_check',
                                  resource.get('skip_console_check', False)) is True:
                        skipped_console.append(f"[{resource['project_name']}] {domain['name']}")
            elif resource.get('skip_console_check', False) is True:
                skipped_console.append(resource['name'])

        # Проходим по всем ресурсам
        for resource in resources:
            # Проверка типа ресурса
            if 'domains' in resource:
                # Это проект с несколькими доменами
                ok, fail = check_project_with_domains(driver, resource, auth_data, console_report)
                successful += ok
                failed += fail
                total_resources += len(resource['domains'])
            else:
                # Это одиночный ресурс
                if check_single_resource(driver, resource, auth_data, console_report):
                    successful += 1
                else:
                    failed += 1
                total_resources += 1

            time.sleep(0.5)  # Пауза между проверками

        # Итоговая статистика
        print(f"\n     Итоги проверки:")
        print(f"     Всего ресурсов: {total_resources}")
        print(f"     Успешно: {successful}")
        print(f"     Ошибок: {failed}")
        if total_resources > 0:
            print(f"     Доступность: {successful / total_resources * 100:.1f}%")
        print(f"     С ошибками в консоли: {len(console_report)}")
        if skipped_console:
            print(f"     Без проверки консоли: {len(skipped_console)} ({', '.join(skipped_console)})")

        # Отчёт по ошибкам консоли
        if console_report:
            print(f"\n     Ошибки 4xx/5xx в консоли:")
            for site in console_report:
                print(f"\n       {site['name']} ({site['url']})")
                print_http_errors(site['errors'], indent='         ')

    finally:
        time.sleep(2)
        driver.quit()


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