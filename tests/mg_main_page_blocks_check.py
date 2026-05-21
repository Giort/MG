from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json
from helpers.popups import remove_popups

# Проверка доступности блоков на главной МГ
# В каждом блоке несколько элементов проверяются на видимость

# Хедер
# 1-й экран
# Блок "Гектар для реализации всех идей"
# Блок "Преимущества проекта"
# Блок "Описание проекта"
# Баннер "Распродажа на Волге"
# Блок СП
# Блок "Лучшие поселения месяца"
# Форма №1 с Софией
# Блок "Лучшие участки у воды"
# Блок "Образ будущих поселений"
# Блок "Распродажа инвестпроектов"
# Блок "Успешные примеры проекта"

# Блок "Территория для ваших идей"
# Блок "Ваш доход с гектара"
# Блок "Реализуйте продукцию"
# Блок "Зорабатывайте на гектаре..."
# Блок "Государственная поддержка отрасли"
# Блок "Награды проекта..."
# Форма №1 с Ариной
# Блок "Проект От сохи до сохи"
# Блок "Отзывы о проекте"
# Блок "Сми о проекте"
# Форма №2 с Ариной
# Блок "Выбери участок в лучшей локации"
# Блок "Новости развития поселков"
# Блок "Непрерывное развитие поселков"
# Форма с Анастасией
# Блок "Популярные вопросы"
# Форма №2 с Софией
# Блок "Видео, которое вам стоит увидеть"
# Блок "Строительство на землях сельхозназначения"
# Блок "Рекомендованные фундаменты"
# Блок "Примеры строений"
# Блок "Федеральный закон"
# Блок "Приглашаем на встречу в офис"
# Форма с Максимом
# Футер



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

MG_BASE_URL = ENV_CONFIG[ENV]["base_url"]


class PageBlocksChecker:
    def __init__(self, mg_base_url):
        self.mg_base_url = mg_base_url.rstrip('/')
        self.driver = None

    def init_driver(self):
        ch_options = Options()
        ch_options.add_argument('--headless')
        ch_options.page_load_strategy = 'eager'
        service = ChromeService(executable_path=ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=ch_options)
        self.driver.set_window_size(1680, 1000)
        self.driver.implicitly_wait(10)
        return self.driver


    def check_block_visibility(self, block_config, timeout=10):
        """Проверка видимости конкретного блока по его конфигурации"""
        block_name = block_config['name']

        # Список для сбора отсутствующих элементов
        missing_elements = []

        try:
            # Проверяем каждый элемент в блоке
            for element_config in block_config['elements']:
                element_name = element_config['name']
                xpath = element_config['xpath']

                try:
                    element = WebDriverWait(self.driver, timeout).until(
                        EC.visibility_of_element_located((By.XPATH, xpath))
                    )

                    # Прокручиваем к элементу
                    self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});",
                                               element)
                    time.sleep(0.3)

                    self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});",
                                               element)
                    time.sleep(0.3)

                    # Дополнительная проверка видимости
                    if not element.is_displayed():
                        missing_elements.append(element_name)

                except (TimeoutException, Exception):
                    missing_elements.append(element_name)

            # Формируем результат
            if not missing_elements:
                print(f"     OK: {block_name}")
                return True
            else:
                # Формируем строку только с отсутствующими элементами
                missing_str = " | ".join([f"✗ {elem}" for elem in missing_elements])
                print(f" ERROR: {block_name} - {missing_str}")
                return False

        except Exception as e:
            print(f" ERROR: {block_name} - Критическая ошибка: {str(e)[:100]}")
            return False

    def check_all_blocks(self, blocks_config, delay=1):
        """Проверка всех блоков из конфигурации"""

        results = {}

        for block_config in blocks_config:
            result = self.check_block_visibility(block_config)

            # Собираем информацию о проблемных элементах для сводки
            problematic_elements = []
            if not result:
                for element_config in block_config['elements']:
                    element_name = element_config['name']
                    xpath = element_config['xpath']
                    try:
                        self.driver.find_element(By.XPATH, xpath)
                    except:
                        problematic_elements.append(element_name)

            results[block_config['name']] = {
                'visible': result,
                'problematic_elements': problematic_elements
            }
            time.sleep(delay)

        return results

    def print_summary(self, results):
        """Вывод сводки результатов"""

        total = len(results)
        visible = sum(1 for r in results.values() if r['visible'])
        not_visible = total - visible

        print(f"\n{'=' * 60}")
        print("     Результат")

        if not_visible > 0:
            print(f"\n     БЛОКИ С ПРОБЛЕМАМИ:")
            for name, info in results.items():
                if not info['visible'] and info['problematic_elements']:
                    # Показываем только проблемные элементы для каждого блока
                    elements_str = ", ".join(info['problematic_elements'])
                    print(f"     {name}: {elements_str}")
        else:
            print(f"\n     ОШИБОК НЕТ")

    def check_blocks_order(self, blocks_config):
        """Проверяет что блоки идут сверху вниз в правильном порядке"""
        positions = []

        for block_config in blocks_config:
            if block_config.get('skip_order_check'):
                continue
            anchor_xpath = block_config['elements'][0]['xpath']
            try:
                element = self.driver.find_element(By.XPATH, anchor_xpath)
                y = element.location['y']
                positions.append((block_config['name'], y))
            except Exception:
                pass  # если блок не найден — его уже поймает check_block_visibility

        # Сортируем по фактическому положению на странице
        sorted_by_y = sorted(positions, key=lambda x: x[1])
        expected_order = [name for name, _ in positions]
        actual_order   = [name for name, _ in sorted_by_y]

        order_errors = []
        for i, (expected, actual) in enumerate(zip(expected_order, actual_order)):
            if expected != actual:
                actual_index = actual_order.index(expected)
                order_errors.append(
                    f'«{expected}» ожидается на позиции {i + 1}, фактически на позиции {actual_index + 1}'
                )

        return order_errors

    def close(self):
        if self.driver:
            self.driver.quit()


def main():
    checker = PageBlocksChecker(MG_BASE_URL)

    print(f"\n     Проверка главной страницы на домене {MG_BASE_URL} | [{ENV.upper()}]\n")

    try:
        checker.init_driver()

        with open('../data/mg_main_page_blocks_config_test.json', 'r', encoding='utf-8') as f:
            blocks_config = json.load(f)

        # Загружаем главную страницу
        checker.driver.get(f"{MG_BASE_URL}/")

        time.sleep(3)
        remove_popups(checker.driver)

        # Проверяем все блоки
        results = checker.check_all_blocks(blocks_config)

        # Проверяем порядок блоков
        order_errors = checker.check_blocks_order(blocks_config)

        # Выводим сводку
        checker.print_summary(results)

        if order_errors:
            print(f"\n     НАРУШЕН ПОРЯДОК БЛОКОВ:")
            for err in order_errors:
                print(f"       - {err}")

    except Exception as e:
        print(f" Критическая ошибка: {e}")
    finally:
        checker.close()


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