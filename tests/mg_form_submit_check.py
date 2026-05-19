import json
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
from helpers.popups import remove_popups

# Засекаем время начала теста
start_time = time.time()

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


class FormSubmitChecker:
    """Проверка реальной отправки данных из формы обратной связи"""

    def __init__(self, headless=True):
        self.driver = self._init_driver(headless)
        self.actions = ActionChains(self.driver)
        self.test_data = self._load_test_data()

    def _init_driver(self, headless):
        ch_options = Options()
        ch_options.add_argument('--headless')
        ch_options.page_load_strategy = 'eager'
        driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=ch_options
        )
        driver.implicitly_wait(10)
        driver.set_window_size(1660, 1000)
        return driver

    def _load_test_data(self):
        with open('../data/data.json', 'r') as file:
            return json.load(file)

    def check_form_submit(self):
        """
        Проверка отправки данных через форму с Софией №1 на главной странице.
        Все формы идентичны — достаточно одной проверки.
        """
        print(f"\n     Проверка отправки данных из формы на домене {BASE_URL} | [{ENV.upper()}]\n")

        try:
            self.driver.get(BASE_URL)

            remove_popups(self.driver)

            # Находим форму с Софией
            title = self.driver.find_element(
                by=By.XPATH,
                value="/descendant::*[text()[contains(.,'София')]][2]"
            )
            form_id = self.driver.find_element(
                by=By.XPATH,
                value="(//*[text()[contains(.,'София')]]/ancestor::div[contains(@id, 'cfw')])[1]"
            ).get_attribute("id")

            self.actions.move_to_element(title).perform()

            # Берём тестовые данные для текущего окружения
            submit_data = self.test_data[f"submit_data_{ENV.lower()}"]

            # Вводим телефон и отправляем
            self.driver.find_element(
                by=By.XPATH,
                value=f"(//div[@id='{form_id}']//*[@id='consultationform-phone'])[1]"
            ).send_keys(str(submit_data["phone"]))

            self.driver.find_element(
                by=By.XPATH,
                value=f"(//div[@id='{form_id}']//*[text()[contains(.,'Отправить')]])[1]"
            ).click()

            # Проверяем что форма перешла на следующий шаг
            self.driver.find_element(
                by=By.XPATH,
                value=f"(//div[@id='{form_id}']//*[@id='consultationform-name'])[2]"
            ).click()

            print("     OK: форма отправлена успешно")

        except Exception as e:
            error_msg = str(e).split('\n')[0]
            print(f" ERROR: не удалось отправить форму — {error_msg}")

    def close(self):
        time.sleep(3)
        self.driver.quit()


if __name__ == "__main__":
    checker = FormSubmitChecker(headless=True)
    try:
        checker.check_form_submit()
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
