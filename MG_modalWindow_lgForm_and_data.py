from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import json
import time
from typing import Dict, List, Tuple


class ModalWindowChecker:
    def __init__(self, headless: bool = True):
        """Инициализация драйвера с настройками"""
        self.options = Options()
        if headless:
            self.options.add_argument('--headless')
        self.options.page_load_strategy = 'eager'
        self.options.add_argument('--no-sandbox')
        self.options.add_argument('--disable-dev-shm-usage')

        self.driver = webdriver.Chrome(options=self.options)
        self.driver.set_window_size(1660, 1000)
        self.wait = WebDriverWait(self.driver, 10)
        self.actions = ActionChains(self.driver)

        # Загрузка тестовых данных
        self.data = self._load_test_data()

    def _load_test_data(self) -> dict:
        """Загружает тестовые данные из JSON файла"""
        try:
            with open('data.json', 'r', encoding='utf-8') as file:
                return json.load(file)
        except FileNotFoundError:
            print("Предупреждение: файл data.json не найден")
            return {}

    def _remove_popup(self) -> None:
        """Удаляет всплывающее окно, если оно есть"""
        try:
            popup = self.driver.find_element(By.ID, 'visitors-popup')
            self.driver.execute_script("arguments[0].remove();", popup)
            print("   Popup удален")
        except NoSuchElementException:
            pass  # Popup не найден, это нормально

    def _format_error_message(self, error: Exception) -> str:
        """Форматирует сообщение об ошибке для вывода"""
        error_str = str(error).strip()

        # Если строка пустая или содержит только "Message: ", берем название класса исключения
        if not error_str or error_str == "Message:" or error_str == "Message: ":
            return f"{type(error).__name__}: элемент не найден"

        # Разделяем по строкам и берем первую информативную строку
        lines = error_str.split('\n')
        for line in lines:
            line = line.strip()
            if line and line != "Message:" and not line.startswith("Stacktrace:"):
                # Удаляем лишний префикс "Message: " если он есть
                if line.startswith("Message: "):
                    line = line[9:]  # убираем "Message: "
                return line if line else f"{type(error).__name__}: элемент не найден"

        # Если все строки пустые или содержат только служебную информацию
        return f"{type(error).__name__}: элемент не найден"

    def _check_element(self, xpath: str, description: str) -> bool:
        """Проверяет наличие элемента по XPath"""
        try:
            self.driver.find_element(By.XPATH, xpath)
            print(f'   ОК: {description}')
            return True
        except NoSuchElementException as e:
            error_msg = self._format_error_message(e)
            print(f'ОШИБКА: {description} — {error_msg}')
            return False

    def _safe_navigate(self, url: str, max_retries: int = 3) -> bool:
        """Безопасная навигация с повторными попытками"""
        for attempt in range(max_retries):
            try:
                self.driver.get(url)
                # Ждем загрузки страницы
                self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
                return True
            except TimeoutException:
                print(f"Попытка {attempt + 1}/{max_retries} загрузки {url} не удалась")
                if attempt == max_retries - 1:
                    print(f"Не удалось загрузить {url}")
                    return False
        return False

    def check_main_page(self) -> List[bool]:
        """Проверяет модальные окна на главной странице"""
        print("\n   Проверка главной страницы 'МГ'")

        if not self._safe_navigate("https://moigektar.ru"):
            return [False] * 8

        time.sleep(1)
        self._remove_popup()

        results = []

        # Список проверок для главной страницы
        checks = [
            ('(//*[@id="modal-auth-lk"]//*[@value="catalog_auth_request"])[1]',
             'главная, модалка "Доступ в личный кабинет", lgForm'),
            ('(//*[@id="promo-modal1-3"]//*[@value="callback_main_promo_volga"])[1]',
             'главная, модалка в блоке "Распродажа на Волге", lgForm'),
            ('(//*[@id="modal_syn-73"]//*[@value="lg_main_catalog_yasnie_zori"])[1]',
             'главная, модалка син_73 в блоке "Лучшие поселения", lgForm'),
            ('(//*[@id="modal_syn-53"]//*[@value="lg_main_catalog_new_gizn"])[1]',
             'главная, модалка син_53 в блоке "Лучшие поселения", lgForm'),
            ('(//*[@id="modal_syn-29"]//*[@value="lg_main_catalog_usadba_na_volge"])[1]',
             'главная, модалка син_29 в блоке "Лучшие поселения", lgForm'),
            ('(//*[@id="modal-descr-invest-batch-1"]//*[@value="mg_main_page_business_area"])[1]',
             'главная, модалка на карточке 1 в блоке "Зарабатывайте на гектаре", lgForm'),
            ('(//*[@id="modal-descr-invest-batch-2"]//*[@value="mg_main_page_business_area"])[1]',
             'главная, модалка на карточке 2 в блоке "Зарабатывайте на гектаре", lgForm'),
            ('(//*[@id="modal-descr-invest-batch-3"]//*[@value="mg_main_page_business_area"])[1]',
             'главная, модалка на карточке 3 в блоке "Зарабатывайте на гектаре", lgForm'),
            ('(//*[@id="modal-descr-invest-batch"]//*[@value="mg_invest_batch_page"])[1]',
             'главная, модалка на красной кнопке в блоке "Зарабатывайте на гектаре", lgForm'),
            ('(//*[@id="modal-main-consultation"]//*[@value="callback_main"])[1]',
             'главная, модалка "Получить консультацию" в футере, lgForm'),
            ('(//*[@id="modal-fixed"]//*[@value="callback_fixed_btn"])[1]',
             'главная, модалка "Получить консультацию" на фикс. кнопке, lgForm'),
            ('(//*[@id="modal-meeting-meeting"]//*[@value="meeting_book"])[1]',
             'главная, модалка "Записаться на встречу", lgForm')
        ]

        for xpath, description in checks:
            results.append(self._check_element(xpath, description))

        # Проверка модалки "Записаться на встречу" с заполнением формы
        results.append(self._check_meeting_modal())

        return results

    def _check_meeting_modal(self) -> bool:
        """Проверяет модалку 'Записаться на встречу' с заполнением формы"""
        try:
            # Находим и нажимаем кнопку "Записаться на встречу"
            btn = self.driver.find_element(By.XPATH, "(//*[text()[contains(.,'Записаться на встречу')]])[2]")
            self.actions.move_to_element(btn).perform()
            self.actions.send_keys(Keys.ARROW_DOWN).perform()
            btn.click()

            # Ждем появления модального окна и заполняем телефон
            phone_field = self.wait.until(
                EC.presence_of_element_located(
                    (By.XPATH, '(//*[@id="modal-meeting-meeting"]//*[@id="consultationform-phone"])[1]'))
            )
            phone_field.click()
            phone_number = str(self.data["test_data_valid"]["phone"])
            time.sleep(2)
            phone_field.send_keys(phone_number)
            time.sleep(2)

            # Нажимаем кнопку отправки
            submit_btn = self.driver.find_element(By.XPATH,
                                                  '(//*[@id="modal-meeting-meeting"]//*[text()[contains(.,"Отправить заявку")]])[1]')
            submit_btn.click()

            # Пытаемся найти поле имени - если оно появилось, значит форма успешно отправлена
            try:
                name_input = self.wait.until(EC.element_to_be_clickable(
                    (By.XPATH, '(//*[@id="modal-meeting-meeting"]//*[@id="consultationform-name"])[2]')))
                name_input.click()
                print('   ОК: главная, модалка "Записаться на встречу", ОТПРАВКА ДАННЫХ через форму (использован номер ' + phone_number + ')')
                return True  # Возвращаем True при успешной отправке

            except Exception as e:
                error_msg = self._format_error_message(e)
                print(f'ОШИБКА: главная, модалка "Записаться на встречу" — {error_msg}')
                return False  # Возвращаем False при ошибке отправки

        except TimeoutException as e:
            error_msg = f"Таймаут ожидания: {self._format_error_message(e)}"
            print(f'ОШИБКА: главная, модалка "Записаться на встречу" — {error_msg}')
            return False
        except Exception as e:
            error_msg = self._format_error_message(e)
            print(f'ОШИБКА: главная, модалка "Записаться на встречу" — {error_msg}')
            return False

    def check_pages(self) -> Dict[str, List[bool]]:
        """Проверяет все страницы с модальными окнами"""
        results = {}

        # Конфигурация страниц для проверки
        page_configs = {
            'catalog': {
                'url': 'https://moigektar.ru/catalogue',
                'checks': [
                    ('(//*[@id="modal-auth"]//*[@value="catalog_auth_request"])[1]',
                     'стр. каталога, модалка "Доступ в каталог", lgForm')
                ]
            },
            'batch_detail': {
                'url': 'https://moigektar.ru/batches/55302',
                'checks': [
                    ('(//*[@id="modal-batch-detail"]//*[@value="buy-batch-modal"])[1]',
                     'стр. актива, модалка "Заявка на консультацию", lgForm'),
                    ('(//*[@id="modal-cashback-banner"]//*[@value="batch_cashback"])[1]',
                     'стр. актива, модалка "Оставьте заявку" на кешбэке, lgForm'),
                    ('(//*[@id="modal-batch-installment"]//*[@value="batch_installment_special_offer"])[1]',
                     'стр. актива, модалка "Рассчитайте рассрочку", lgForm')
                ]
            },
            'investment_basic': {
                'url': 'https://moigektar.ru/investment/basic',
                'checks': [
                    ('(//*[@id="modal-select"]//*[@value="mg_invest_basic_page_callback"])[1]',
                     'стр. "Базовая стратегия", модалка "Заказать услугу", lgForm')
                ]
            },
            'investment_businessman': {
                'url': 'https://moigektar.ru/investment/businessman',
                'checks': [
                    ('(//*[@id="modal-select"]//*[@value="capitalization_count"])[1]',
                     'стр. "Предприниматель", модалка "Заказать услугу", lgForm')
                ]
            },
            'business_plans': {
                'url': 'https://moigektar.ru/business-plans',
                'checks': [
                    ('(//*[@id="modal-main"]//*[@value="callback_business"])[1]',
                     'стр. "Бизнес-планы", модалка "Получить консультацию", lgForm')
                ]
            },
            'gift': {
                'url': 'https://moigektar.ru/gift',
                'checks': [
                    ('(//*[@id="gift-main-modal"]//*[@value="lg_cert"])[1]',
                     'стр. "Подарочный сертификат", модалка "Оставьте заявку!", lgForm')
                ]
            },
            'hr': {
                'url': 'https://moigektar.ru/hr',
                'checks': [
                    ('(//*[@id="hr-main-modal"]//*[@value="callback_hr"])[1]',
                     'стр. "Вакансии", модалка "Оставьте анкету ...", lgForm')
                ]
            },
            'settlements': {
                'url': 'http://moigektar.ru/goal/settlements',
                'checks': [
                    ('(//*[@id="settlements-main-modal"]//*[@value="callback_main_settlements"])[1]',
                     'стр. "Родовые поселения", 1-й экран, модалка "Оставьте заявку!", lgForm'),
                    ('(//*[@id="settlements-descr-modal"]//*[@value="callback_descr_settlements"])[1]',
                     'стр. "Родовые поселения", описание, модалка "Оставьте заявку!", lgForm')
                ]
            }
        }

        # Проверяем каждую страницу
        for page_name, config in page_configs.items():
            print(f"\n   Проверка страницы: {page_name}")
            page_results = []

            if self._safe_navigate(config['url']):
                for xpath, description in config['checks']:
                    page_results.append(self._check_element(xpath, description))
            else:
                page_results = [False] * len(config['checks'])

            results[page_name] = page_results

        return results

    def run_all_checks(self) -> Dict[str, any]:
        """Запускает все проверки"""
        print("Начинаем проверку модальных окон...")

        results = {
            'main_page': self.check_main_page(),
            'other_pages': self.check_pages()
        }

        # Подсчет статистики
        total_checks = 0
        passed_checks = 0

        for page_results in results.values():
            if isinstance(page_results, list):
                # Фильтруем None значения и считаем только bool
                valid_results = [result for result in page_results if isinstance(result, bool)]
                total_checks += len(valid_results)
                passed_checks += sum(valid_results)
            elif isinstance(page_results, dict):
                for page_list in page_results.values():
                    if isinstance(page_list, list):
                        # Фильтруем None значения и считаем только bool
                        valid_results = [result for result in page_list if isinstance(result, bool)]
                        total_checks += len(valid_results)
                        passed_checks += sum(valid_results)

        print(f"\nИтого: {passed_checks}/{total_checks} проверок прошли успешно")
        print(f"Процент успешных проверок: {(passed_checks / total_checks * 100):.1f}%")

        return results

    def __del__(self):
        """Закрывает драйвер при уничтожении объекта"""
        if hasattr(self, 'driver'):
            self.driver.quit()


def main():
    """Основная функция"""
    checker = ModalWindowChecker(headless=True)
    try:
        results = checker.run_all_checks()
        return results
    finally:
        checker.driver.quit()


if __name__ == "__main__":
    main()