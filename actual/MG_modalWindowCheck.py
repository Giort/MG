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


# Засекаем время начала теста
start_time = time.time()

class ModalWindowChecker:
    def __init__(self, headless: bool = True, base_url: str = "https://moigektar.ru"):
        """Инициализация драйвера с настройками

        Args:
            headless: Запуск браузера в headless режиме
            base_url: Базовый URL сайта (по умолчанию https://moigektar.ru)
        """
        self.base_url = base_url.rstrip('/')  # Убираем trailing slash если есть

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
            with open('../actual/data.json', 'r', encoding='utf-8') as file:
                return json.load(file)
        except FileNotFoundError:
            print("Предупреждение: файл data.json не найден")
            return {}

    def _remove_popup(self) -> None:
        """Удаляет всплывающее окно, если оно есть"""
        try:
            popup = self.driver.find_element(By.ID, 'visitors-popup')
            self.driver.execute_script("arguments[0].remove();", popup)
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

    def _check_element(self, xpath: str, description: str, max_attempts: int = 3) -> bool:
        """Проверяет наличие элемента по XPath с повторными попытками

        Args:
            xpath: XPath селектор элемента
            description: Описание проверки для логирования
            max_attempts: Максимальное количество попыток (по умолчанию 3)
        """
        for attempt in range(1, max_attempts + 1):
            try:
                self.driver.find_element(By.XPATH, xpath)
                print(f'   ОК: {description}')
                return True
            except NoSuchElementException as e:
                if attempt < max_attempts:
                    self.driver.refresh()
                    time.sleep(2)
                else:
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

        if not self._safe_navigate(self.base_url):
            return [False] * 8

        time.sleep(1)
        self._remove_popup()

        results = []

        # Список проверок для главной страницы
        checks = [
            ('(//*[@id="modal-auth-lk"]//*[@value="catalog_auth_request"])[1]',
             'главная, модалка "Доступ в личный кабинет", lgForm'),
            ('(//*[@id="promo-modal1-3"]//*[@value="lg_promo_modal_newyear"])[1]',
             'главная, модалка в блоке "Лучший новогодний подарок", lgForm'),
            ('(//*[@id="modal_syn-432"]//*[@value="lg_main_catalog_odincovo"])[1]',
             'главная, модалка син_432 в блоке "Лучшие поселения", lgForm'),
            ('(//*[@id="modal_syn-376"]//*[@value="lg_main_catalog_rybackaya"])[1]',
             'главная, модалка син_376 в блоке "Лучшие поселения", lgForm'),
            ('(//*[@id="modal_syn-29"]//*[@value="lg_main_catalog_usadba_na_volge"])[1]',
             'главная, модалка син_29 в блоке "Лучшие поселения", lgForm'),
            ('(//*[@id="product-card-modal"]//*[@value="mg_main_page_product_card_callback"])[1]',
             'главная, модалка в блоке "Реализуйте продукцию ...", lgForm'),
            ('(//*[@id="modal-descr-invest-batch-1"]//*[@value="mg_main_page_business_area"])[1]',
             'главная, модалка на карточке 1 в блоке "Зарабатывайте на гектаре", lgForm'),
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
            time.sleep(2)

            # Пытаемся найти поле имени - если оно появилось, значит форма успешно отправлена
            try:
                name_input = self.wait.until(EC.element_to_be_clickable(
                    (By.XPATH, '(//*[@id="modal-meeting-meeting"]//*[@id="consultationform-name"])[2]')))
                name_input.click()
                print(
                    '   ОК: главная, модалка "Записаться на встречу", ОТПРАВКА ДАННЫХ через форму (использован номер ' + phone_number + ')')
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
                'name': 'Каталог',
                'url': f'{self.base_url}/catalogue',
                'checks': [
                    ('(//*[@id="modal-auth"]//*[@value="catalog_auth_request"])[1]',
                     'стр. каталога, модалка "Доступ в каталог", lgForm')
                ]
            },
            'batch_detail': {
                'name': 'Страница актива',
                'url': f'{self.base_url}/batches/55302',
                'checks': [
                    ('(//*[@id="modal-batch-detail"]//*[@value="buy-batch-modal"])[1]',
                     'стр. актива, модалка "Заявка на консультацию", lgForm'),
                    ('(//*[@id="modal-cashback-banner"]//*[@value="batch_cashback"])[1]',
                     'стр. актива, модалка "Оставьте заявку" на кешбэке, lgForm'),
                    ('(//*[@id="modal-batch-installment"]//*[@value="batch_installment_special_offer"])[1]',
                     'стр. актива, модалка "Рассчитайте рассрочку", lgForm')
                ]
            },
            'service_company': {
                'name': 'Сервисная компания',
                'url': f'{self.base_url}/service-company',
                'checks': [
                    ('(//*[@id="sk-how-interview"]//*[@value="mg_service_company_interview_callback"])[1]',
                     'стр. СК, модалка "Запись на собеседование", lgForm'),
                    ('(//*[@id="sk-how-coach"]//*[@value="mg_service_company_coach_callback"])[1]',
                     'стр. СК, модалка "Запись на коуч-сессию, lgForm'),
                    ('(//*[@id="sk-main-modal"]//*[@value="mg_service_company_page_callback"])[1]',
                     'стр. СК, модалка "Начать развитие", lgForm')
                ]
            },
            'investment_basic': {
                'name': 'Инвестор (базовая)',
                'url': f'{self.base_url}/investment/basic',
                'checks': [
                    ('(//*[@id="modal-select"]//*[@value="mg_invest_basic_page_callback"])[1]',
                     'стр. "Базовая стратегия", модалка "Заказать услугу", lgForm')
                ]
            },
            'investment_businessman': {
                'name': 'Инвестор (предприниматель)',
                'url': f'{self.base_url}/investment/businessman',
                'checks': [
                    ('(//*[@id="modal-select"]//*[@value="capitalization_count"])[1]',
                     'стр. "Предприниматель", модалка "Заказать услугу", lgForm')
                ]
            },
            'business_plans': {
                'name': 'Бизнес-планы',
                'url': f'{self.base_url}/business-plans',
                'checks': [
                    ('(//*[@id="modal-main"]//*[@value="callback_business"])[1]',
                     'стр. "Бизнес-планы", модалка "Получить консультацию", lgForm')
                ]
            },
            'gift': {
                'name': 'Подарочный сертификат',
                'url': f'{self.base_url}/gift',
                'checks': [
                    ('(//*[@id="gift-main-modal"]//*[@value="lg_cert"])[1]',
                     'стр. "Подарочный сертификат", модалка "Оставьте заявку!", lgForm')
                ]
            },
            'hr': {
                'name': 'Вакансии',
                'url': f'{self.base_url}/hr',
                'checks': [
                    ('(//*[@id="hr-main-modal"]//*[@value="callback_hr"])[1]',
                     'стр. "Вакансии", модалка "Оставьте анкету ...", lgForm'),
                    ('(//*[@id="hr-main-modal-2"]//*[@value="callback_hr_partner"])[1]',
                     'стр. "Вакансии", модалка "Станьте партнером ...", lgForm')
                ]
            },
            'settlements': {
                'name': 'Родовые поселения',
                'url': f'{self.base_url}/goal/settlements',
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
        print("\n Проверка модальных окон")

        results = {
            'main_page': self.check_main_page(),
            'other_pages': self.check_pages()
        }

        return results

    def __del__(self):
        """Закрывает драйвер при уничтожении объекта"""
        if hasattr(self, 'driver'):
            self.driver.quit()


def main():
    """Основная функция"""
    # Для быстрого переключения домена измените base_url:
    # Продакшн: base_url="https://moigektar.ru"
    # Локальный: base_url="http://moigektar.localhost"
    checker = ModalWindowChecker(headless=True, base_url="https://moigektar.ru")
    try:
        results = checker.run_all_checks()
        return results
    finally:
        checker.driver.quit()


if __name__ == "__main__":
    main()


# Вычисляем и выводим время выполнения теста
end_time = time.time()
elapsed_time = end_time - start_time
minutes = int(elapsed_time // 60)
seconds = int(elapsed_time % 60)

if minutes > 0:
    print(f'\nВремя выполнения теста: {minutes} мин {seconds} сек ({elapsed_time:.2f} сек)')
else:
    print(f'\nВремя выполнения теста: {seconds} сек ({elapsed_time:.2f} сек)')
