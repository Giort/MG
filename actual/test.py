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

# Засекаем время начала теста
start_time = time.time()

# Проверяемый урл
MG_BASE_URL = "https://moigektar.ru"


# MG_BASE_URL = "http://moigektar.localhost"


class PageBlocksChecker:
    def __init__(self, mg_base_url):
        self.mg_base_url = mg_base_url.rstrip('/')
        self.driver = None

    def init_driver(self):
        ch_options = Options()
        # ch_options.add_argument('--headless')
        ch_options.page_load_strategy = 'eager'
        service = ChromeService(executable_path=ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=ch_options)
        self.driver.set_window_size(1680, 1000)
        self.driver.implicitly_wait(10)
        return self.driver

    def remove_popup(self):
        """Удаление попапа посетителей"""
        try:
            popup_w = self.driver.find_element(by=By.XPATH, value="//div[@id='visitors-popup']")
            self.driver.execute_script("arguments[0].remove();", popup_w)
        except Exception:
            pass

    def check_block_visibility(self, block_config, timeout=10):
        """Проверка видимости конкретного блока по его конфигурации"""
        block_name = block_config['name']

        try:
            # Проверяем каждый элемент в блоке
            all_visible = True
            element_results = []

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

                    # Дополнительная проверка видимости
                    if element.is_displayed():
                        element_results.append(f"{element_name}")
                    else:
                        element_results.append(f"✗ {element_name}")
                        all_visible = False

                except TimeoutException:
                    element_results.append(f"✗ {element_name}")
                    all_visible = False
                except Exception as e:
                    element_results.append(f"✗ {element_name}")
                    all_visible = False

            # Формируем результат
            elements_info = " | ".join(element_results)

            if all_visible:
                print(f"     OK: {block_name}")
            else:
                print(f" ERROR: {block_name} - {elements_info}")

            return all_visible

        except Exception as e:
            print(f" ERROR: {block_name} - Критическая ошибка: {str(e)[:100]}")
            return False

    def check_all_blocks(self, blocks_config, delay=1):
        """Проверка всех блоков из конфигурации"""
        print(f"\n     Проверка видимости блоков на странице: {self.mg_base_url}/ \n")

        results = {}

        for block_config in blocks_config:
            result = self.check_block_visibility(block_config)
            results[block_config['name']] = {
                'visible': result,
                'elements': block_config['elements']
            }
            time.sleep(delay)

        return results

    def print_summary(self, results):
        """Вывод сводки результатов"""
        print(f"\n{'=' * 60}")
        print("СВОДКА РЕЗУЛЬТАТОВ")
        print(f"{'=' * 60}")

        total = len(results)
        visible = sum(1 for r in results.values() if r['visible'])
        not_visible = total - visible

        print(f"Всего блоков: {total}")
        print(f"Полностью видимых: {visible} ({visible / total * 100:.1f}%)")
        print(f"С ошибками: {not_visible} ({not_visible / total * 100:.1f}%)")

        if not_visible > 0:
            print(f"\nБЛОКИ С ПРОБЛЕМАМИ:")
            for name, info in results.items():
                if not info['visible']:
                    print(f"  ✗ {name}")

        print(f"\nУСПЕШНО ПРОВЕРЕНЫ:")
        for name, info in results.items():
            if info['visible']:
                print(f"  ✓ {name}")

    def close(self):
        if self.driver:
            self.driver.quit()


# КОНФИГУРАЦИЯ БЛОКОВ ДЛЯ ПРОВЕРКИ
BLOCKS_CONFIG = [
    {
        'name': 'Хедер',
        'elements': [
            {
                'name': 'Логотип',
                'xpath': '(//div[contains(@class, "w-navbar")]//img[@src="/img/logo.svg"])[1]'
            },
            {
                'name': 'Ссылка на каталог',
                'xpath': '(//div[contains(@class, "w-navbar")]//a[@href="/catalogue"])[1]'
            },
            {
                'name': 'Кнопка "Каталог участков" (квиз)',
                'xpath': '//div[contains(@class, "w-navbar")]//a[contains(@role, "button") and contains(., "Каталог участков")]'
            },
            {
                'name': 'Кнопка авторизации',
                'xpath': '(//div[contains(@class, "w-navbar")]//a[@href="#modal-auth-lk"])[1]'
            }
        ]
    },
    {
        'name': 'Главный экран (герой)',
        'elements': [
            {
                'name': 'Заголовок "Свой участок"',
                'xpath': '//h1[contains(text(), "Свой участок")]'
            },
            {
                'name': 'Подзаголовок с текстом о гектаре',
                'xpath': '//div[contains(@class, "hero")]//p[contains(text(), "гектар")]'
            },
            {
                'name': 'Кнопка "Найти участок"',
                'xpath': '//div[contains(@class, "hero")]//button[contains(text(), "Найти участок")]'
            }
        ]
    },
    {
        'name': 'Блок "Описание проекта"',
        'elements': [
            {
                'name': 'Заголовок "Описание проекта"',
                'xpath': '//h2[contains(text(), "Описание проекта")]'
            },
            {
                'name': 'Карточка с преимуществами',
                'xpath': '//div[contains(@class, "uk-card") and contains(@class, "uk-card-body")]//h3[contains(text(), "Участки")]'
            }
        ]
    },
    {
        'name': 'Карта участков',
        'elements': [
            {
                'name': 'Заголовок карты',
                'xpath': '//h2[contains(text(), "Участки на карте") or contains(text(), "Карта участков")]'
            },
            {
                'name': 'Контейнер карты',
                'xpath': '//div[contains(@class, "map-container") or contains(@id, "map")]'
            },
            {
                'name': 'Фильтры на карте',
                'xpath': '//div[contains(@class, "map-filter") or contains(@class, "map-controls")]'
            }
        ]
    },
    {
        'name': 'Блок "Отзывы"',
        'elements': [
            {
                'name': 'Заголовок "Отзывы"',
                'xpath': '//h2[contains(text(), "Отзывы")]'
            },
            {
                'name': 'Слайдер отзывов',
                'xpath': '//div[contains(@class, "reviews-slider") or contains(@class, "testimonials-slider")]'
            },
            {
                'name': 'Карточка отзыва',
                'xpath': '//div[contains(@class, "review-card") or contains(@class, "testimonial-card")]'
            }
        ]
    },
    {
        'name': 'Футер (подвал)',
        'elements': [
            {
                'name': 'Блок контактов',
                'xpath': '//footer//div[contains(text(), "Контакты")]'
            },
            {
                'name': 'Телефон',
                'xpath': '//footer//a[contains(@href, "tel:")]'
            },
            {
                'name': 'Социальные сети',
                'xpath': '//footer//div[contains(@class, "social-links")]'
            }
        ]
    }
]


def main():
    checker = PageBlocksChecker(MG_BASE_URL)

    try:
        checker.init_driver()

        # Загружаем главную страницу
        checker.driver.get(f"{MG_BASE_URL}/")
        time.sleep(3)
        checker.remove_popup()

        # Проверяем все блоки
        results = checker.check_all_blocks(BLOCKS_CONFIG)

        # Выводим сводку
        checker.print_summary(results)

        # Сохраняем результаты в файл
        with open('blocks_visibility_report.json', 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        print(f"\nПодробный отчет сохранен в файл: blocks_visibility_report.json")

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