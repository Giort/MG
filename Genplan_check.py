from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time
import json


class GenplanChecker:
    """Класс для проверки загрузки генпланов на сайтах посёлков"""

    def __init__(self):
        self.driver = self._init_driver()
        self.actions = ActionChains(self.driver)
        self.data = self._load_data()

    def _init_driver(self):
        """Инициализация драйвера Chrome"""
        service = ChromeService(executable_path=ChromeDriverManager().install())
        ch_options = Options()
        ch_options.add_argument('--headless')
        ch_options.page_load_strategy = 'eager'

        driver = webdriver.Chrome(service=service, options=ch_options)
        driver.set_window_size(1920, 1080)
        driver.implicitly_wait(10)
        return driver

    def _load_data(self):
        """Загрузка конфигурации из JSON"""
        try:
            with open('data.json', 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            return {}

    def check_genplan(self, url, name, title_xpath='(//*[text()[contains(.,"Генеральный")]])[3]',
                      genplan_css='ymaps.ymaps-2-1-79-inner-panes',
                      max_attempts=3, wait_time=14):
        """
        Проверка загрузки генплана на странице

        Args:
            url: URL страницы
            name: Название посёлка для логов
            title_xpath: XPath для кликабельного элемента открытия генплана
            genplan_css: CSS селектор для элемента генплана
            max_attempts: Максимальное количество попыток
            wait_time: Время ожидания элементов
        """
        self.driver.get(url)

        for attempt in range(max_attempts):
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
                    print(f'   OK: {name}')
                    return True

            except Exception as e:
                if attempt == max_attempts - 1:
                    print(f'ERROR: генплан на {name}')
                    return False
                else:
                    self.driver.refresh()

        return False

    def check_with_auth(self, url, name, credentials_key,
                        title_xpath='(//*[text()[contains(.,"Генеральный")]])[3]',
                        genplan_css='ymaps.ymaps-2-1-79-inner-panes'):
        """
        Проверка генплана с авторизацией

        Args:
            url: URL страницы
            name: Название посёлка для логов
            credentials_key: Ключ для получения креденшелов из data.json
            title_xpath: XPath для кликабельного элемента открытия генплана
            genplan_css: CSS селектор для элемента генплана
        """
        self.driver.get(url)

        # Авторизация
        creds = self.data.get(credentials_key, {})
        login_input = self.driver.find_element(By.ID, 'loginconfig-username')
        password_input = self.driver.find_element(By.ID, 'loginconfig-password')
        submit_btn = self.driver.find_element(By.CSS_SELECTOR, 'div button')

        login_input.send_keys(str(creds.get("login", "")))
        password_input.send_keys(str(creds.get("password", "")))
        submit_btn.click()
        time.sleep(2)

        # Проверка генплана
        self.check_genplan(self.driver.current_url, name, title_xpath, genplan_css)

    def run_checks(self):
        """Запуск всех проверок"""

        # Сайты с одинаковыми селекторами
        standard_sites = [
            ('https://syn9.lp.moigektar.ru', 'syn_9'),
            ('https://syn33.lp.moigektar.ru', 'syn_33'),
            ('https://syn34.lp.moigektar.ru', 'syn_34'),
            ('https://syn35.lp.moigektar.ru', 'syn_35'),
            ('https://syn39.lp.moigektar.ru', 'syn_39'),
            ('https://syn42.lp.moigektar.ru', 'syn_42'),
            ('https://syn48.lp.moigektar.ru', 'syn_48'),
            ('https://syn52.lp.moigektar.ru', 'syn_52'),
            ('https://syn53.lp.moigektar.ru', 'syn_53'),
            ('https://syn56.lp.moigektar.ru', 'syn_56'),
            ('https://syn67.lp.moigektar.ru', 'syn_67'),
            ('https://syn73.lp.moigektar.ru', 'syn_73'),
            ('https://syn74.lp.moigektar.ru', 'syn_74'),
            ('https://syn84.lp.moigektar.ru', 'syn_84'),
            ('https://syn85.lp.moigektar.ru', 'syn_85'),
            ('https://syn87.lp.moigektar.ru', 'syn_87'),
            ('https://syn89.lp.moigektar.ru', 'syn_89'),
            ('https://syn92.lp.moigektar.ru', 'syn_92'),
            ('https://syn95.lp.moigektar.ru', 'syn_95'),
            ('https://syn99.lp.moigektar.ru', 'syn_99'),
            ('https://synergycountryclub.ru', 'syn_103'),
            ('https://syn447.lp.moigektar.ru', 'syn_447'),
        ]

        for url, name in standard_sites:
            self.check_genplan(url, name)

        # vazuza2 (другой селектор)
        self.check_genplan(
            'https://vazuza2.lp.moigektar.ru',
            'Вазуза',
            title_xpath='(//*[text()[contains(.,"Генеральный")]])[1]'
        )

        # syn_111 - с авторизацией
        self.check_with_auth(
            'https://syn111.lp.moigektar.ru',
            'syn_111',
            '111_cred'
        )

        # турпортал Едем на Вазузу - с авторизацией и особым селектором
        self.check_with_auth(
            'https://едемнавазузу.рф',
            'ТурПортал',
            'turporlal_cred',
            title_xpath='(//*[text()[contains(.,"Интерактивная")]])[1]'
        )

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
