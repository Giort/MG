from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import json
import time
import os


# МГ: проверка доступности и атрибутов модальных окон

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

config = ENV_CONFIG[ENV]
BASE_URL = config["base_url"]

start_time = time.time()


class ModalChecker:
    def __init__(self):
        ch_options = Options()
        ch_options.add_argument('--headless')
        ch_options.page_load_strategy = 'eager'
        ch_options.add_argument('--no-sandbox')
        ch_options.add_argument('--disable-dev-shm-usage')

        service = ChromeService(executable_path=ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=ch_options)
        self.driver.set_window_size(1660, 1000)
        self.wait = WebDriverWait(self.driver, 10)
        self.actions = ActionChains(self.driver)

        self.results = {'success': [], 'failed': []}

    # ------------------------------------------------------------------
    # Вспомогательные методы
    # ------------------------------------------------------------------

    def _set_mobile_viewport(self):
        self.driver.set_window_size(390, 844)

    def _set_desktop_viewport(self):
        self.driver.set_window_size(1660, 1000)

    def _remove_popup(self):
        """Закрывает попап посетителей если он появился"""
        try:
            popup_close = self.driver.find_element(
                By.XPATH, '//*[contains(@class,"js-visitor-popup-close")]'
            )
            popup_close.click()
            time.sleep(0.5)
        except NoSuchElementException:
            pass

    def _navigate(self, url: str) -> bool:
        """Переходит на страницу и убирает попап"""
        try:
            self.driver.get(url)
            time.sleep(1)
            self._remove_popup()
            return True
        except Exception as e:
            print(f"     ERROR: Не удалось открыть {url} — {e}")
            return False

    def _scroll_to_element(self, selector: str) -> object | None:
        """Находит элемент и скроллит к нему"""
        from selenium.common.exceptions import MoveTargetOutOfBoundsException
        try:
            btn = self.driver.find_element(By.XPATH, selector)
            try:
                self.actions.move_to_element(btn).perform()
            except MoveTargetOutOfBoundsException:
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", btn)
            time.sleep(0.5)
            return btn
        except NoSuchElementException:
            return None

    def _click_button(self, btn) -> bool:
        """Кликает по кнопке"""
        try:
            btn.click()
            return True
        except Exception:
            try:
                self.driver.execute_script("arguments[0].click();", btn)
                return True
            except Exception as e:
                print(f"     ERROR: Не удалось кликнуть — {e}")
                return False

    def _wait_modal_open(self, modal_id: str, timeout: int = 8) -> bool:
        """Ждёт появления модалки с классом uk-open"""
        try:
            self.wait.until(
                EC.presence_of_element_located((
                    By.XPATH,
                    f'//*[@id="{modal_id}" and contains(@class,"uk-open")]'
                ))
            )
            return True
        except TimeoutException:
            return False

    def _check_phone_clickable(self, modal_id: str, phone_selector: str = None) -> bool:
        """Проверяет что телефонный инпут внутри модалки кликабелен"""
        try:
            xpath = phone_selector if phone_selector else \
                f'(//*[@id="{modal_id}"]//input[@id="consultationform-phone"])'
            phone_input = WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, xpath))
            )
            return phone_input.is_displayed() and phone_input.is_enabled()
        except TimeoutException:
            return False

    def _get_lgform_value(self, modal_id: str, lgform_selector: str = None) -> str | None:
        """Читает значение скрытого поля lgForm внутри открытой модалки"""
        try:
            xpath = lgform_selector if lgform_selector else \
                f'//*[@id="{modal_id}"]//input[@id="consultationform-lgform"]'
            lgform_input = self.driver.find_element(By.XPATH, xpath)
            return lgform_input.get_attribute('value')
        except NoSuchElementException:
            return None

    def _close_modal(self, modal_id: str):
        """Закрывает модалку нажатием Escape"""
        try:
            from selenium.webdriver.common.keys import Keys
            self.driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.ESCAPE)
            time.sleep(0.5)
        except Exception:
            pass

    # ------------------------------------------------------------------
    # Основная проверка одной модалки
    # ------------------------------------------------------------------

    def check_modal(self, modal_config: dict) -> bool:
        """
        Полный цикл проверки одной модалки:
        1. Переход на страницу
        2. Скролл к кнопке
        3. Клик по кнопке
        4. Ожидание открытия модалки
        5. Проверка кликабельности инпута (видимость для пользователя)
        6. Проверка значения lgForm
        """
        name = modal_config['name']
        url_name = modal_config['url_name']
        url = BASE_URL + modal_config['url']
        btn_selector = modal_config['btn_selector']
        modal_id = modal_config['modal_id']
        expected_lgform = modal_config['lgform']
        phone_selector = modal_config.get('phone_selector', None) # у большинства мод. одинаковые селекторы инпута
        # телефона, но у некоторых нужно задавать другой
        lgform_selector = modal_config.get('lgform_selector', None) # у большинства мод. одинаковые селекторы lgForm,
        # но у некоторых нужно задавать другой

        label = f'[{url_name}] {name}'

        is_mobile = modal_config.get('mobile', False)
        if is_mobile:
            self._set_mobile_viewport()
        else:
            self._set_desktop_viewport()

        # 1. Переход на страницу
        if not self._navigate(url):
            self._record_result(label, False, 'не удалось открыть страницу')
            return False

        # 2. Скролл к кнопке
        btn = self._scroll_to_element(btn_selector)
        if btn is None:
            self._record_result(label, False, 'кнопка не найдена')
            return False

        # 3. Клик
        if not self._click_button(btn):
            self._record_result(label, False, 'не удалось кликнуть по кнопке')
            return False

        # 4. Ожидание открытия модалки
        if not self._wait_modal_open(modal_id):
            self._record_result(label, False, 'модалка не открылась (нет класса uk-open)')
            return False

        # 5. Проверка видимости инпута
        if not self._check_phone_clickable(modal_id, phone_selector):
            self._record_result(label, False, 'телефонный инпут не кликабелен')
            return False

        # 6. Проверка lgForm
        actual_lgform = self._get_lgform_value(modal_id, lgform_selector)
        if actual_lgform != expected_lgform:
            msg = f'lgForm: ожидалось "{expected_lgform}", получено "{actual_lgform}"'
            self._record_result(label, False, msg)
            return False

        self._record_result(label, True)
        self._close_modal(modal_id)
        return True

    def _record_result(self, label: str, success: bool, error: str = ''):
        if success:
            print(f"     OK: {label}")
            self.results['success'].append(label)
        else:
            print(f" ERROR: {label} — {error}")
            self.results['failed'].append(f"{label} ({error})")

    # ------------------------------------------------------------------
    # Запуск всех проверок
    # ------------------------------------------------------------------

    def run(self, modals_config: list):
        print(f"\n     Проверка модальных окон МГ [{ENV.upper()}]  {BASE_URL}\n")

        for modal_config in modals_config:
            self.check_modal(modal_config)

        self._print_summary()

    def _print_summary(self):
        total = len(self.results['success']) + len(self.results['failed'])
        success = len(self.results['success'])
        failed = len(self.results['failed'])

        print(f"\n     {'=' * 50}")
        print(f"     Итого: {total}  |  OK: {success}  |  Ошибок: {failed}")

        if self.results['failed']:
            print(f"\n     Проблемные модалки:")
            for item in self.results['failed']:
                print(f"       - {item}")
        else:
            print(f"\n     ОШИБОК НЕТ")

    def close(self):
        if self.driver:
            self.driver.quit()


def load_modals_config(config_file: str) -> list:
    try:
        if not os.path.exists(config_file):
            raise FileNotFoundError(f"Файл конфигурации не найден: {config_file}")
        with open(config_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data['modals']
    except Exception as e:
        print(f" ERROR: Ошибка загрузки конфигурации: {e}")
        raise


def main():
    modals_config = load_modals_config('../data/modal_mg_list_test.json')

    checker = ModalChecker()
    try:
        checker.run(modals_config)
    finally:
        checker.close()


if __name__ == "__main__":
    main()

# Время выполнения
end_time = time.time()
elapsed_time = end_time - start_time
minutes = int(elapsed_time // 60)
seconds = int(elapsed_time % 60)

if minutes > 0:
    print(f'\n     Время выполнения теста: {minutes} мин {seconds} сек ({elapsed_time:.2f} сек)')
else:
    print(f'\n     Время выполнения теста: {seconds} сек ({elapsed_time:.2f} сек)')

