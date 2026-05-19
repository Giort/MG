import json
import time
import sys
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager

sys.path.insert(0, os.path.dirname(__file__))
from helpers.popups import remove_popups


# Проверка форм обратной связи.
# Находим форму по подзаголовку, проверяем, что установлен правильный lgForm и правильный заголовок


# Засекаем время начала теста
start_time = time.time()


class FormChecker:
    """Класс для проверки форм обратной связи на сайте МойГектар"""

    # ============================================================
    #  Переключение окружения: "prod" или "local"
    # ============================================================
    ENV = "prod"
    # ============================================================

    ENV_CONFIG = {
        "prod": {
            "base_url": "https://moigektar.ru",
        },
        "local": {
            "base_url": "http://moigektar.localhost",
        },
    }

    BASE_URL = ENV_CONFIG[ENV]["base_url"]

    def __init__(self, headless=False):
        self.driver = self._init_driver(headless)
        self.actions = ActionChains(self.driver)
        self.errors = []
        self.success_count = 0

    def _init_driver(self, headless):
        """Инициализация Chrome WebDriver"""
        ch_options = Options()
        if headless:
            ch_options.add_argument('--headless')
        ch_options.page_load_strategy = 'eager'

        driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=ch_options
        )
        driver.implicitly_wait(10)
        driver.set_window_size(1660, 1000)
        return driver

    def _load_config(self, config_path='../data/mg_callback_form_config.json'):
        """Загрузка конфигурации форм"""
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def _scroll_page(self):
        """Прокрутка страницы вниз"""
        for _ in range(8):
            self.actions.send_keys(Keys.PAGE_DOWN).perform()
            time.sleep(1)

    def check_element(self, xpath, page_name, form_name, check_type, max_attempts=3):
        """
        Универсальная проверка элемента на странице с повторными попытками

        Args:
            xpath:        XPath селектор элемента
            page_name:    название страницы для логирования
            form_name:    название формы для логирования
            check_type:   тип проверки (lgForm / заголовок)
            max_attempts: максимальное количество попыток
        """
        for attempt in range(1, max_attempts + 1):
            try:
                self.driver.find_element(By.XPATH, xpath)
                print(f"     ОК: {page_name}: {form_name} — {check_type}")
                self.success_count += 1
                return True
            except Exception as e:
                if attempt < max_attempts:
                    self.driver.refresh()
                    time.sleep(2)
                else:
                    error_msg = str(e).split('\n')[0]
                    error_text = f" ERROR: {page_name}, {form_name} — {check_type} — {error_msg}"
                    print(error_text)
                    self.errors.append(error_text)
                    return False

    def check_phone_clickable(self, lgform_xpath, page_name, form_name, max_attempts=3):
        """
        Проверяет кликабельность инпута телефона внутри формы.
        Поднимается от lgform_xpath до контейнера cfw и ищет инпут внутри него.
        """
        phone_xpath = f"({lgform_xpath}/ancestor::div[contains(@id, 'cfw')]//input[contains(@class, 'js-phone') and @type='tel'])[1]"

        for attempt in range(1, max_attempts + 1):
            try:
                from selenium.webdriver.support.ui import WebDriverWait
                from selenium.webdriver.support import expected_conditions as EC
                phone_input = WebDriverWait(self.driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, phone_xpath))
                )
                if phone_input.is_displayed() and phone_input.is_enabled():
                    print(f"     ОК: {page_name}: {form_name} — инпут телефона кликабелен")
                    self.success_count += 1
                    return True
                else:
                    raise Exception("инпут не отображается или недоступен")
            except Exception as e:
                if attempt < max_attempts:
                    self.driver.refresh()
                    time.sleep(2)
                else:
                    error_msg = f"инпут телефона не кликабелен"
                    error_text = f" ERROR: {page_name}, {form_name} — {error_msg}"
                    print(error_text)
                    self.errors.append(error_text)
                    return False

    def check_form(self, form_config):
        """
        Проверка одной формы из конфига:
        - загружает страницу
        - при необходимости прокручивает
        - проверяет lgForm, заголовок и кликабельность инпута телефона
        """
        page_name = form_config['page_name']
        form_name = form_config.get('form_name', '')
        url       = self.BASE_URL + form_config['url']
        scroll    = form_config.get('scroll', False)

        self.driver.get(url)
        remove_popups(self.driver)

        if scroll:
            self._scroll_page()

        self.check_element(form_config['lgform_xpath'], page_name, form_name, 'lgForm')

        if form_config.get('header_xpath'):
            self.check_element(form_config['header_xpath'], page_name, form_name, 'заголовок')

        self.check_phone_clickable(form_config['lgform_xpath'], page_name, form_name)

    def run_all_checks(self, config_path='../data/mg_callback_form_config.json'):
        """Запуск всех проверок из конфига"""
        print(f"\n     Проверка форм обратной связи на сайте МойГектар на домене {self.BASE_URL} | [{self.ENV.upper()}]\n")

        forms = self._load_config(config_path)
        for form_config in forms:
            self.check_form(form_config)

        self.print_report(total=len(forms))

    def print_report(self, total):
        """Вывод отчёта о результатах"""
        print(f"\n     {'=' * 50}")
        print(f"     Итого форм: {total}  |  OK: {self.success_count}  |  Ошибок: {len(self.errors)}")

        if self.errors:
            print(f"\n     Список ошибок:")
            for i, error in enumerate(self.errors, 1):
                print(f"     {i}. {error}")
        else:
            print(f"\n     ОШИБОК НЕТ")

    def close(self):
        """Закрытие браузера"""
        time.sleep(3)
        self.driver.quit()


if __name__ == "__main__":
    checker = FormChecker(headless=True)
    try:
        checker.run_all_checks()
    finally:
        checker.close()

# Вычисляем и выводим время выполнения теста
end_time = time.time()
elapsed_time = end_time - start_time
minutes = int(elapsed_time // 60)
seconds = int(elapsed_time % 60)

if minutes > 0:
    print(f'\n     Время выполнения теста: {minutes} мин {seconds} сек ({elapsed_time:.2f} сек)')
else:
    print(f'\n     Время выполнения теста: {seconds} сек ({elapsed_time:.2f} сек)')