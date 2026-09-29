import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager


# Засекаем время начала теста
start_time = time.time()

# Проверка виджета ВК на сайтах


# ============================================================
#  Список проверяемых ресурсов
# ============================================================
RESOURCES = [
    {
        "name": "ЛК, главная - блок 'Новости о развитии поселков'",
        "url": "https://cabinet.moigektar.ru",
        "title_xpath": "//*[@class='w-new-uikit']/h6/div[contains(., 'Новости о развитии поселков')]",
        "elem_xpath": "//*[@class='w-new-uikit']/h6/div[contains(., 'Новости о развитии поселков')]/ancestor::div[1]//iframe[@src='https://vk.widgets.cabinet.moigektar.ru/app']",
    },
    {
        "name": "syn_53 Новая жизнь - блок 'Подпишитесь в соцсетях'",
        "url": "https://syn53.lp.moigektar.ru",
        "title_xpath": "//h1[contains(., 'в соцсетях')]/a[contains(@href, 'https://vk.com/mgektar')]",
        "elem_xpath": "//h1[contains(., 'в соцсетях')]/a[contains(@href, 'https://vk.com/mgektar')]/ancestor::div[1]/iframe",
    },
]
# ============================================================


class BlockVisibilityChecker:
    """Проверка видимости заголовка и целевого элемента блока на нескольких ресурсах"""

    def __init__(self):
        self.driver = self._init_driver()
        self.actions = ActionChains(self.driver)
        self.errors = []
        self.success_count = 0

    def _init_driver(self):
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

    def check_resource(self, config, timeout=14):
        """
        Проверка одного ресурса:
        - загружает страницу
        - убеждается, что виден заголовок блока
        - убеждается, что виден целевой элемент блока
        """
        name = config['name']
        url = config['url']
        title_xpath = config['title_xpath']
        elem_xpath = config['elem_xpath']

        try:
            self.driver.get(url)

            try:
                popup = self.driver.find_element(By.XPATH, "//div[@class='login-modal uk-modal uk-flex uk-open']")
                self.driver.execute_script("arguments[0].remove();", popup)
            except Exception:
                pass

            try:
                popup = self.driver.find_element(By.XPATH, "//*[@id='lesson_main']")
                self.driver.execute_script("arguments[0].remove();", popup)
            except Exception:
                pass

            # Заголовок блока
            title =  wait(self.driver, timeout).until(
                EC.visibility_of_element_located((By.XPATH, title_xpath))
            )

            self.actions.move_to_element(title).perform()
            self.actions.send_keys(Keys.PAGE_DOWN).perform()

            # Целевой элемент блока
            elem = wait(self.driver, timeout).until(
                EC.visibility_of_element_located((By.XPATH, elem_xpath))
            )

            if elem:
                print(f"     OK: {name}")
                self.success_count += 1
                return True

        except Exception as e:
            error_msg = str(e).split('\n')[0]
            error_text = f" ERROR: {name} — {error_msg} ({url})"
            print(error_text)
            self.errors.append(error_text)
            return False

    def run_all_checks(self):
        """Запуск проверок по всем ресурсам из RESOURCES"""
        print(f"\n     Проверка видимости виджета ВК на сайтах \n")

        for resource in RESOURCES:
            self.check_resource(resource)
            time.sleep(1)

        self.print_summary(len(RESOURCES))

    def print_summary(self, total):
        """Вывод итогового отчёта"""
        print(f"\n     {'=' * 50}")
        print(f"     Итого: {total}  |  OK: {self.success_count}  |  Ошибок: {len(self.errors)}")

        if self.errors:
            print(f"\n     Список ошибок:")
            for i, error in enumerate(self.errors, 1):
                print(f"     {i}. {error}")
        else:
            print(f"\n     ОШИБОК НЕТ")

    def close(self):
        time.sleep(3)
        self.driver.quit()


if __name__ == "__main__":
    checker = BlockVisibilityChecker()
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