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




# Проверка наличия блоков на главной МГ

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
        ch_options.add_argument('--headless')
        ch_options.page_load_strategy = 'eager'
        service = ChromeService(executable_path=ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=ch_options)
        self.driver.set_window_size(1680, 1000)
        self.driver.implicitly_wait(10)
        return self.driver

    def remove_popup(driver):
        """Удаление попапа посетителей"""
        try:
            # Удаляем попап посетителей
            popup_visitors = driver.find_element(by=By.XPATH, value="//div[@id='visitors-popup']")
            driver.execute_script("arguments[0].remove();", popup_visitors)
        except Exception:
            pass

        try:
            # Удаляем попап вебинара
            popup_webinar = driver.find_element(by=By.XPATH,
                                                value="//*[contains(@class, 'js-webinar-running-event-modal')]")
            driver.execute_script("arguments[0].remove();", popup_webinar)
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

        total = len(results)
        visible = sum(1 for r in results.values() if r['visible'])
        not_visible = total - visible

        # print(f"Всего блоков: {total}")
        # print(f"Полностью видимых: {visible} ({visible / total * 100:.1f}%)")
        # print(f"С ошибками: {not_visible} ({not_visible / total * 100:.1f}%)")

        print(f"\n{'=' * 60}")
        print("     Результат")

        if not_visible > 0:
            print(f"\n     БЛОКИ С ПРОБЛЕМАМИ:")
            for name, info in results.items():
                if not info['visible']:
                    print(f"     {name}")
        else:
            print(f"\n     ОШИБОК НЕТ")

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
        'name': 'Главный экран',
        'elements': [
            {
                'name': 'Заголовок "Гектар"',
                'xpath': '//div[contains (@class, "w-main") and contains (@id, "main")]//p/span[contains(text(), "Гектар")]'
            },
            {
                'name': 'Подзаголовок с текстом о поселениях',
                'xpath': '//div[contains (@class, "w-main") and contains (@id, "main")]//div[contains(@class, "w-main-bg")]//p[contains(text(), "нового типа")]'
            },
            {
                'name': 'Кнопка "Каталог участков"',
                'xpath': '//div[contains (@class, "w-main") and contains (@id, "main")]//a[contains(text(), "Каталог участков")]'
            }
        ]
    },
    {
        'name': 'Блок "Гектар для реализации всех идей"',
        'elements': [
            {
                'name': 'Заголовок',
                'xpath': '//div[@id="w-gektar-idea"]/h2[contains(text(), "Гектар для реализации всех идей")]'
            },
            {
                'name': '1-й блок: кнопка запуска видео',
                'xpath': '(//div[@id="w-gektar-idea"]//a[contains(@data-type, "iframe")])[1]'
            },
            {
                'name': '1-й блок: кнопка вызова квиза',
                'xpath': '(//div[@id="w-gektar-idea"]//a[contains(text(), "Подобрать участок")])[1]'
            }
        ]
    },
    {
        'name': 'Блок "Преимущества проекта"',
        'elements': [
            {
                'name': 'Заголовок',
                'xpath': '//div[@id="project_advantages"]//h2[contains(text(), "Преимущества проекта")]'
            },
            {
                'name': '1-я ячейка сетки, картинка',
                'xpath': '(//div[@id="project_advantages"]//div[contains(@class, "uk-grid")]//img[@src="img/project-advantages/1.svg"])[1]'
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
                'name': '1-я секция: кнопка видео',
                'xpath': '(//div[@id="w-descr"]//div[contains(text(), "Смотреть ")])[1]'
            },
            {
                'name': '1-я секция: фото',
                'xpath': '(//div[@id="w-descr"]//img[contains(@class, "uk-visible@l")])[1]'
            }
        ]
    },
    {
        'name': 'Блок СП',
        'elements': [
            {
                'name': '1-я карточка СП, фото',
                'xpath': '(//div[@id="catalogueSpecial"]//a//div/img)[1]'
            },
            {
                'name': '1-я карточка СП, бейдж скидки',
                'xpath': '(//div[@id="catalogueSpecial"]//div[@data-src="/img/catalogue/label-sale.svg"])[1]'
            },
            {
                'name': '1-я карточка СП, бейдж СП',
                'xpath': '(//div[@id="catalogueSpecial"]//span[contains(text(), "Спецпредложение")])[1]'
            },
            {
                'name': 'Кнопка перехода в каталог',
                'xpath': '//div[@id="catalogueSpecial"]//a[contains(@href, "https://moigektar.ru/catalogue?popularChoiceIds%5B0%5D=1&clusterIds%5B0%5D=93&clusterIds%5B1%5D=33&clusterIds%5B2%5D=26") and contains(text(), "Перейти в каталог")]'
            }
        ]
    },
    {
        'name': 'Блок "Лучшие поселения"',
        'elements': [
            {
                'name': 'Заголовок',
                'xpath': '//*[@id="catalogue"]//h2[contains(text(), "Лучшие поселения месяца")]'
            },
            {
                'name': 'Кнопка запуска тура',
                'xpath': '(//*[@id="catalogue"]//lord-icon[@src="/dist/icons/air-balloon.json"])[1]'
            },
            {
                'name': '1-я карточка: вызов модалки',
                'xpath': '(//*[@id="catalogue"]//a[@href="#modal_syn-376"])[1]'
            }
        ]
    },
    {
        'name': 'Блок "Распродажа инвестпроектов"',
        'elements': [
            {
                'name': 'Заголовок',
                'xpath': '//div[@id="catalogueSpecial11"]//h2[contains (text(), "Распродажа инвестпроектов")]'
            },
            {
                'name': '1-я карточка СП, фото',
                'xpath': '(//div[@id="catalogueSpecial11"]//a//div/img)[1]'
            },
            {
                'name': '1-я карточка СП, бейдж скидки',
                'xpath': '(//div[@id="catalogueSpecial11"]//div[@data-src="/img/catalogue/label-sale.svg"])[1]'
            },
            {
                'name': '1-я карточка СП, бейдж СП',
                'xpath': '(//div[@id="catalogueSpecial11"]//span[contains(text(), "Спецпредложение")])[1]'
            },
            {
                'name': 'Кнопка перехода в каталог',
                'xpath': '//div[@id="catalogueSpecial11"]//a[contains(@href, "/catalogue?popularChoiceIds%5B%5D=11") and contains(text(), "Перейти в каталог")]'
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