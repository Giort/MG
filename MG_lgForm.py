from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
ch_options = Options()
ch_options.add_argument('--headless')
ch_options.page_load_strategy = 'eager'
driver = webdriver.Chrome(service = Service(ChromeDriverManager().install()), options = ch_options)
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
actions = ActionChains(driver)
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import ElementNotVisibleException
from selenium.webdriver.common.keys import Keys
import time
import json
import unittest
driver.set_window_size(1680, 1000)
driver.implicitly_wait(10)


class FeedbackFormTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Инициализация драйвера (укажите путь к вашему драйверу)
        cls.driver = webdriver.Chrome()
        cls.driver.maximize_window()

        # URL тестируемой страницы
        cls.test_url = "https://moigektar.ru"

        # Открытие страницы
        cls.driver.get(cls.test_url)

    def test_form_attributes(self):
        # Заполнение формы тестовыми данными
        phone_input = self.driver.find_element(By.XPATH, '(//*[@id="consultationform-phone"])[14]')  # замените на актуальный селектор

        phone_input.send_keys("9127777777")

        # Нажатие кнопки отправки
        submit_button = self.driver.find_element(By.XPATH, '(//*[@type="submit"])[12]')
        submit_button.click()

        # # Проверка атрибутов формы перед отправкой
        # form = self.driver.find_element(By.TAG_NAME, "form")
        # form_method = form.get_attribute("method")  # GET или POST
        # form_action = form.get_attribute("action")  # URL обработчика формы
        #
        # print(f"\nФорма отправляется методом: {form_method}")
        # print(f"Обработчик формы: {form_action}")

        # Проверка скрытых полей (hidden inputs)
        hidden_inputs = self.driver.find_elements(By.XPATH, "//input[@type='hidden']")
        print(f"\nОбнаружено скрытых полей: {len(hidden_inputs)}")

        for input_field in hidden_inputs:
            name = input_field.get_attribute("name")
            value = input_field.get_attribute("value")
            print(f"Скрытое поле: name='{name}', value='{value}'")
        #
        # # Проверка дополнительных атрибутов (data-атрибуты)
        # data_attrs = form.get_property("attributes")
        # print("\nДополнительные атрибуты формы:")
        # for attr in data_attrs:
        #     if attr['name'].startswith('data-'):
        #         print(f"{attr['name']}: {attr['value']}")

    @classmethod
    def tearDownClass(cls):
        # Закрытие браузера
        cls.driver.quit()


if __name__ == "__main__":
    unittest.main()

time.sleep(5)
driver.quit()
