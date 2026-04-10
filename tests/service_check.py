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


def init_driver():
    """Инициализация драйвера Chrome"""
    ch_options = Options()
    ch_options.add_argument('--headless')
    ch_options.page_load_strategy = 'eager'
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

    try:
        # Пробуем найти поля авторизации
        login_input = wait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'loginconfig-username'))
        )
        password_input = driver.find_element(By.ID, 'loginconfig-password')
        submit_btn = driver.find_element(By.CSS_SELECTOR, 'div button, button[type]')

        # Получаем credentials
        creds = auth_data.get(credentials_key, {})
        login = str(creds.get("login", ""))
        password = str(creds.get("password", ""))

        login_input.send_keys(login)
        password_input.send_keys(password)
        submit_btn.click()
        time.sleep(2)

        return True
    except Exception as e:
        print(f'WARNING: Ошибка авторизации - {str(e)[:100]}')
        return False


def check_single_resource(driver, resource, auth_data):
    """Проверка одного ресурса (одиночный URL)"""
    url = resource['url']
    name = resource['name']
    selector = resource['selector']
    auth_config = resource.get('auth', False)
    clear_cookies = resource.get('clear_cookies', False)
    max_attempts = 3
    wait_timeout = 14

    # Проверка доступности домена
    if not check_domain(url):
        print(f'ERROR: {name} - домен недоступен')
        return False

    # Загрузка страницы
    try:
        driver.get(url)
        time.sleep(1)
    except InvalidArgumentException:
        print(f'ERROR: {name} - некорректный URL')
        return False
    except Exception as e:
        print(f'ERROR: {name} - ошибка загрузки: {str(e)[:100]}')
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

                if clear_cookies:
                    driver.delete_all_cookies()
                    time.sleep(5)

                return True
        except Exception as e:
            if attempt == max_attempts - 1:
                print(f'ERROR: {name}: {str(e)[:100]}')

                if clear_cookies:
                    driver.delete_all_cookies()
                    time.sleep(0.5)

                return False
            else:
                try:
                    driver.refresh()
                    time.sleep(2)

                    # Повторная авторизация после обновления
                    perform_auth(driver, auth_config, name, auth_data)
                except:
                    pass

    return False


def check_project_with_domains(driver, project, auth_data):
    """Проверка проекта с несколькими доменами"""
    project_name = project['project_name']
    domains = project['domains']
    selector = project['selector']
    auth_config = project.get('auth', False)
    clear_cookies = project.get('clear_cookies', False)

    all_success = True

    for domain in domains:
        url = domain['url']
        domain_name = domain['name']

        # Для логов используем короткое имя
        display_name = f"[{project_name}] {domain_name}"

        # Проверка доступности домена
        if not check_domain(url):
            print(f'ERROR: {display_name} - домен недоступен')
            all_success = False
            continue

        # Загрузка страницы
        try:
            driver.get(url)
            time.sleep(2)
        except Exception as e:
            print(f'ERROR: {display_name} - ошибка загрузки: {str(e)[:100]}')
            all_success = False
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
                    success = True

                    if clear_cookies:
                        driver.delete_all_cookies()
                        time.sleep(5)

                    break
            except Exception as e:
                if attempt == 2:
                    print(f'ERROR: {display_name} - {str(e)[:100]}')

                    if clear_cookies:
                        driver.delete_all_cookies()
                        time.sleep(0.5)

                    all_success = False
                else:
                    try:
                        driver.refresh()
                        time.sleep(2)
                        # Повторная авторизация после обновления
                        perform_auth(driver, auth_config, project_name, auth_data)
                    except:
                        pass

        time.sleep(0.5)  # Пауза между доменами

    return all_success


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

        # Проходим по всем ресурсам
        for resource in resources:
            # Проверка типа ресурса
            if 'domains' in resource:
                # Это проект с несколькими доменами
                if check_project_with_domains(driver, resource, auth_data):
                    successful += len(resource['domains'])
                else:
                    failed += len(resource['domains'])
                total_resources += len(resource['domains'])
            else:
                # Это одиночный ресурс
                if check_single_resource(driver, resource, auth_data):
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