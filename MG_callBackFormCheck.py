import json
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager


class FormChecker:
    """Класс для проверки форм обратной связи на сайте МойГектар"""

    # Базовый URL сайта - можно легко переключаться между prod и local
    BASE_URL = "https://moigektar.ru"

    # BASE_URL = "http://moigektar.localhost"

    def __init__(self, headless=False):
        self.driver = self._init_driver(headless)
        self.actions = ActionChains(self.driver)
        self.test_data = self._load_test_data()

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

    def _load_test_data(self):
        """Загрузка тестовых данных из JSON"""
        with open('data.json', 'r') as file:
            return json.load(file)

    def check_element(self, xpath, page_name, form_name, element_type, max_attempts=3):
        """
        Универсальная проверка элемента на странице с повторными попытками

        Args:
            xpath: XPath селектор элемента
            page_name: Название страницы для логирования
            form_name: Название формы для логирования
            element_type: Тип элемента (lgForm, заголовок и т.д.)
            max_attempts: Максимальное количество попыток (по умолчанию 3)
        """
        for attempt in range(1, max_attempts + 1):
            try:
                self.driver.find_element(by=By.XPATH, value=xpath)
                print(f"     ОК: {page_name}, {form_name}, {element_type}")
                return True
            except Exception as e:
                if attempt < max_attempts:
                    self.driver.refresh()
                    time.sleep(2)
                else:
                    error_msg = str(e).split('\n')[0]
                    print(f"ОШИБКА: {page_name}, {form_name}, {element_type} — {error_msg}")
                    return False

    def remove_popup(self):
        """Удаление всплывающего окна, которое может перекрывать элементы"""
        try:
            self.driver.get(self.BASE_URL)
            time.sleep(1)
            popup_w = self.driver.find_element(by=By.XPATH, value="//div[@id='visitors-popup']")
            self.driver.execute_script("arguments[0].remove();", popup_w)
        except:
            print("Popup not found")

    def scroll_page(self):
        """Прокрутка страницы вниз для каталога"""
        for _ in range(8):
            self.actions.send_keys(Keys.PAGE_DOWN).perform()
            time.sleep(1)

    def check_sofia_form_1_with_submit(self):
        """Проверка формы с Софией №1 на главной странице с отправкой данных"""
        try:
            title = self.driver.find_element(by=By.XPATH, value="/descendant::*[text()[contains(.,'София')]][2]")
            form_id = self.driver.find_element(
                by=By.XPATH,
                value="(//*[text()[contains(.,'София')]]/ancestor::div[contains(@id, 'cfw')])[1]"
            ).get_attribute("id")
            self.actions.move_to_element(title).perform()

            # Проверка lgForm
            self.check_element(
                f"(//div[@id='{form_id}']//*[@value='mg_main_page_sofia2_callback'])[2]",
                "главная", "форма с Софией №1", "lgForm"
            )

            # Проверка заголовка
            self.check_element(
                f"//div[@id='{form_id}']//div[@class='uk-visible@s']//*[text()[contains(.,'проконсультирую')]]",
                "главная", "форма с Софией №1", "заголовок"
            )

            # Проверка отправки данных
            try:
                self.driver.find_element(
                    by=By.XPATH,
                    value=f"(//div[@id='{form_id}']//*[@id='consultationform-phone'])[1]"
                ).send_keys(str(self.test_data["test_data_valid"]["phone"]))

                self.driver.find_element(
                    by=By.XPATH,
                    value=f"(//div[@id='{form_id}']//*[text()[contains(.,'Отправить')]])[1]"
                ).click()

                name_input = self.driver.find_element(
                    by=By.XPATH,
                    value=f"(//div[@id='{form_id}']//*[@id='consultationform-name'])[2]"
                )
                name_input.click()
                print("     ОК: главная, форма с Софией №1, отправка через форму")
            except Exception as e:
                error_msg = str(e).split('\n')[0]
                print(f"Ошибка: главная, форма с Софией №1, отправка через форму — {error_msg}")

        except Exception as e:
            error_msg = str(e).split('\n')[0]
            print(f"Ошибка: главная, форма с Софией №1 — {error_msg}")

    def check_main_page_forms(self):
        """Проверка всех форм на главной странице"""
        self.driver.get(self.BASE_URL)
        self.remove_popup()

        # София №1 с отправкой
        self.check_sofia_form_1_with_submit()

        # Арина #1
        self.check_element(
            "(//*[text()[contains(.,'Арина')]]/ancestor::div[contains(@id, 'cfw')]//*[@value='mg_main_page_arina_callback'])[1]",
            "главная", "форма с Ариной #1", "lgForm"
        )
        self.check_element(
            "(//*[text()[contains(.,'Арина')]]/ancestor::div[contains(@id, 'cfw')]//div[text()[contains(., 'Напишу вам в WhatsApp,')]])[2]",
            "главная", "форма с Ариной #1", "заголовок"
        )

        # Арина #2
        self.check_element(
            "(//*[text()[contains(.,'Арина')]]/ancestor::div[contains(@id, 'cfw')]//*[@value='mg_main_page_arina2_callback'])[1]",
            "главная", "форма с Ариной #2", "lgForm"
        )
        self.check_element(
            "(//*[text()[contains(.,'Арина')]]/ancestor::*[contains(@id, 'cfw')]//*[text()[contains(., 'Расскажу подробнее об акциях')]])[2]",
            "главная", "форма с Ариной #2", "заголовок"
        )

        # Анастасия
        self.check_element(
            "(//*[text()[contains(.,'Анастасия')]]/ancestor::div[contains(@id, 'cfw')]//*[@value='mg_main_page_anastasiya_callback'])[1]",
            "главная", "форма с Анастасией", "lgForm"
        )
        self.check_element(
            "(//*[text()[contains(.,'Анастасия')]]/ancestor::*[contains(@id, 'cfw')]//*[text()[contains(., 'Закажите развитие участка')]])[3]",
            "главная", "форма с Анастасией", "заголовок"
        )

        # София №2
        self.check_element(
            "(//*[text()[contains(.,'София')]]/ancestor::div[contains(@id, 'cfw')]//*[@value='mg_main_page_sofia_callback'])[1]",
            "главная", "форма с Софией №2", "lgForm"
        )
        self.check_element(
            "(//*[text()[contains(.,'София')]]/ancestor::*[contains(@id, 'cfw')]//*[text()[contains(., 'Расскажу про развитие участка')]])[2]",
            "главная", "форма с Софией №2", "заголовок"
        )

        # Максим
        self.check_element(
            "(//*[text()[contains(.,'Максим')]]/ancestor::div[contains(@id, 'cfw')]//*[@value='mg_main_page_max_callback'])[1]",
            "главная", "форма с Максимом", "lgForm"
        )
        self.check_element(
            "(//*[text()[contains(.,'София')]]/ancestor::*[contains(@id, 'cfw')]//*[text()[contains(., 'Расскажу про развитие участка')]])[2]",
            "главная", "форма с Максимом", "заголовок"
        )

    def check_catalog_forms(self):
        """Проверка форм в каталоге"""
        # Каталог - Арина
        self.driver.get(f"{self.BASE_URL}/catalogue-no-auth")
        self.scroll_page()

        self.check_element(
            "(//*[text()[contains(.,'Арина')]]/ancestor::div[contains(@id, 'cfw')]//*[@value='mg_catalog_arina_callback'])[1]",
            "каталог", "форма с Ариной", "lgForm"
        )
        self.check_element(
            "(//*[text()[contains(.,'Арина')]]/ancestor::*[contains(@id, 'cfw')]//*[text()[contains(., 'оставьте свой номер')]])[2]",
            "каталог", "форма с Ариной", "заголовок"
        )

        # Страница актива - Арина
        self.driver.get(f"{self.BASE_URL}/batches/44607")

        self.check_element(
            "(//*[text()[contains(.,'Арина')]]/ancestor::div[contains(@id, 'cfw')]//*[@value='mg_batch_page_arina_callback'])[1]",
            "стр. актива", "форма с Ариной", "lgForm"
        )
        self.check_element(
            "(//*[text()[contains(.,'Арина')]]/ancestor::*[contains(@id, 'cfw')]//div[text()[contains(., 'Напишу вам в WhatsApp,')]])[2]",
            "стр. актива", "форма с Ариной", "заголовок"
        )

    def check_about_section(self):
        """Проверка раздела 'О проекте'"""
        pages = [
            ("/about", "О проекте", "mg_about_page_callback"),
            ("/about/advantages", "О проекте - Партнеры", "mg_about_partners_page_callback"),
            ("/about/union", "О проекте - Союз садоводов", "mg_about_union_page_callback"),
            ("/about/reviews", "О проекте - Отзывы", "mg_about_reviews_page_callback"),
        ]

        for path, page_name, lg_form_value in pages:
            self.driver.get(f"{self.BASE_URL}{path}")
            self.check_element(
                f"(//*[text()[contains(.,'Арина')]]/ancestor::div[contains(@id, 'cfw')]//*[@value='{lg_form_value}'])[1]",
                f'"{page_name}"', "форма с Ариной", "lgForm"
            )
            self.check_element(
                "(//*[text()[contains(.,'Арина')]]/ancestor::*[contains(@id, 'cfw')]//div[text()[contains(., 'Напишу вам в WhatsApp,')]])[2]",
                f"'{page_name}'", "форма с Ариной", "заголовок"
            )

    def check_growth_section(self):
        """Проверка раздела 'Развитие'"""
        pages = [
            ("/growth", "Развитие - Развитие поселков", "mg_growth_page_callback"),
            ("/investment", "Развитие - Глазами инвестора", "mg_investment_page_callback"),
            ("/investment/capitalization", "Развитие - Капитализация", "mg_capitalization_page_callback"),
            ("/investment/basic", "Развитие - Базовая стратегия", "mg_invest_basic_page_callback"),
            ("/investment/businessman", "Развитие - Предприниматель", "mg_invest_businessman_page_callback"),
            ("/investment/farmer", "Развитие - Садовод", "mg_invest_farmer_page_callback"),
            ("/investment/family", "Развитие - Усадьба", "mg_invest_family_page_callback"),
        ]

        for path, page_name, lg_form_value in pages:
            self.driver.get(f"{self.BASE_URL}{path}")
            self.check_element(
                f"(//*[text()[contains(.,'Арина')]]/ancestor::div[contains(@id, 'cfw')]//*[@value='{lg_form_value}'])[1]",
                f'"{page_name}"', "форма с Ариной", "lgForm"
            )
            self.check_element(
                "(//*[text()[contains(.,'Арина')]]/ancestor::*[contains(@id, 'cfw')]//div[text()[contains(., 'Напишу вам в WhatsApp,')]])[2]",
                f"'{page_name}'", "форма с Ариной", "заголовок"
            )

    def check_support_section(self):
        """Проверка раздела 'Меры поддержки'"""
        pages = [
            ("/documents/gos", "Меры поддержки - основная"),
            ("/documents", "Меры поддержки - Для владельцев земли"),
            ("/documents/farmer", "Меры поддержки - Начинающий фермер"),
            ("/documents/startup", "Меры поддержки - Агростартап"),
            ("/documents/family", "Меры поддержки - Семейная ферма"),
            ("/documents/ipoteka", "Меры поддержки - Сельская ипотека"),
        ]

        for path, page_name in pages:
            self.driver.get(f"{self.BASE_URL}{path}")
            self.check_element(
                "(//*[text()[contains(.,'Арина')]]/ancestor::div[contains(@id, 'cfw')]//*[@value='mg_gos_page_callback'])[1]",
                f'"{page_name}"', "форма с Ариной", "lgForm"
            )
            self.check_element(
                "(//*[text()[contains(.,'Арина')]]/ancestor::*[contains(@id, 'cfw')]//div[text()[contains(., 'Напишу вам в WhatsApp,')]])[2]",
                f"'{page_name}'", "форма с Ариной", "заголовок"
            )

    def check_faq_page(self):
        """Проверка страницы 'Вопрос-ответ'"""
        self.driver.get(f"{self.BASE_URL}/faq")

        self.check_element(
            "(//*[text()[contains(.,'Юлия')]]/ancestor::div[contains(@id, 'cfw')]//*[@value='mg_question_page_adamova_callback'])[1]",
            '"Вопрос-ответ"', "форма с Юлией", "lgForm"
        )
        self.check_element(
            "(//*[text()[contains(.,'Юлия')]]/ancestor::*[contains(@id, 'cfw')]//div[text()[contains(., 'я вас проконсультирую')]])[1]",
            '"Вопрос-ответ"', "форма с Юлией", "заголовок"
        )

    def check_news_page(self):
        """Проверка детальной страницы новости"""
        self.driver.get(
            f"{self.BASE_URL}/news/keys-statya-proekta-moy-gektar-dom-nikity-lovicha-usadba-v-zavidovo-W2fdhFEXcn")

        self.check_element(
            "(//*[text()[contains(.,'Арина')]]/ancestor::div[contains(@id, 'cfw')]//*[@value='mg_news_page_callback'])[1]",
            "детальная страница новости", "форма с Ариной", "lgForm"
        )
        self.check_element(
            "(//*[text()[contains(.,'Арина')]]/ancestor::*[contains(@id, 'cfw')]//div[text()[contains(., 'Напишу вам в WhatsApp,')]])[2]",
            "детальная страница новости", "форма с Ариной", "заголовок"
        )

    def check_actions_section(self):
        """Проверка раздела 'Акции'"""
        actions = [
            ("/actions", "Акции - Основная", "Максим", "mg_action_main_page_max_callback", "Максимом"),
            ("/actions/1", "Акции - страница 1", "Арина", "mg_action_page_large_family_callback", "Ариной"),
            ("/actions/2", "Акции - страница 2", "Максим", "mg_action_page_svo_callback", "Максимом"),
            ("/actions/3", "Акции - страница 3", "Андрей", "mg_action_page_veteran_callback", "Андреем"),
            ("/actions/4", "Акции - страница 4", "София", "mg_action_page_facilities_callback", "Софией"),
            ("/actions/5", "Акции - страница 5", "Арина", "mg_action_page_certificate_friend_callback", "Ариной"),
            ("/actions/6", "Акции - страница 6", "Андрей", "mg_action_page_refugees_callback", "Андреем"),
            ("/actions/7", "Акции - страница 7", "Максим", "mg_action_page_certificate_self_callback", "Максимом"),
        ]

        for path, page_name, consultant_keyword, lg_form_value, consultant_name_instrumental in actions:
            self.driver.get(f"{self.BASE_URL}{path}")
            self.check_element(
                f"(//*[text()[contains(.,'{consultant_keyword}')]]/ancestor::div[contains(@id, 'cfw')]//*[@value='{lg_form_value}'])[1]",
                page_name, f"форма с {consultant_name_instrumental}", "lgForm"
            )
            self.check_element(
                f"(//*[text()[contains(.,'{consultant_keyword}')]]/ancestor::*[contains(@id, 'cfw')]//div[text()[contains(., 'я вас проконсультирую')]])[1]",
                page_name, f"форма с {consultant_name_instrumental}", "заголовок"
            )

    def check_other_pages(self):
        """Проверка остальных страниц"""
        pages = [
            ("/good-fund", "Фонд добра", "гораздо", "mg_fond_dobra_callback", "Юлией"),
            ("/hr", "Вакансии", "Юлия", "callback_hr_form", "Юлией"),
            ("/contacts", "Контакты", "Арина", "mg_contact_page_callback", "Ариной"),
            ("/goal/glamping", "Глэмпинг", "Андрей", "mg_glamping_page_andrey_callback", "Андреем"),
            ("/goal/farm", "Фермы и агробизнес", "Андрей", "mg_farm_page_andrey_callback", "Андреем"),
            ("/goal/settlements", "Родовые поселения", "Андрей", "mg_settlements_page_andrey_callback", "Андреем"),
            ("/gift", "Подарочный сертификат", "Арина", "mg_gift_page_callback", "Ариной"),
            ("/cabinet", "раздел личного кабинета", "Арина", "mg_lk_page_page_arina_callback", "Ариной"),
            ("/invest-batch", "страница про инвестиции", "Максим", "mg_invest_batch_page_callback", "Максимом"),
        ]

        for path, page_name, consultant_keyword, lg_form_value, consultant_name_instrumental in pages:
            self.driver.get(f"{self.BASE_URL}{path}")
            self.check_element(
                f"(//*[text()[contains(.,'{consultant_keyword}')]]/ancestor::div[contains(@id, 'cfw')]//*[@value='{lg_form_value}'])[1]",
                page_name, f"форма с {consultant_name_instrumental}", "lgForm"
            )

            # Специальная проверка заголовков для разных страниц
            if page_name == "Контакты" or page_name == "Подарочный сертификат":
                header_text = "оставьте свой номер"
                index = "[2]"
            else:
                header_text = "я вас проконсультирую"
                index = "[1]"

            self.check_element(
                f"(//*[text()[contains(.,'{consultant_keyword}')]]/ancestor::*[contains(@id, 'cfw')]//div[text()[contains(., '{header_text}')]]){index}",
                page_name, f"форма с {consultant_name_instrumental}", "заголовок"
            )

        # Дополнительная форма с Игорем в личном кабинете
        self.driver.get(f"{self.BASE_URL}/cabinet")
        self.check_element(
            "(//*[text()[contains(.,'Игорь')]]/ancestor::div[contains(@id, 'cfw')]//*[@value='mg_lk_page_kalinin_callback'])[1]",
            "раздел личного кабинета", "форма с Игорем", "lgForm"
        )
        self.check_element(
            "(//*[text()[contains(.,'Игорь')]]/ancestor::*[contains(@id, 'cfw')]//div[text()[contains(., 'к личному кабинету')]])[1]",
            "раздел личного кабинета", "форма с Игорем", "заголовок"
        )

    def check_webinar_page(self):
        """Проверка страниц вебинаров"""
        self.driver.get(f"{self.BASE_URL}/webinar/invest")
        self.check_element(
            "(//*[text()[contains(.,'вебинара')]]/ancestor::div[contains(@id, 'cfw')]//*[@value='mg_webinar'])[1]",
            'Вебинар "Как заработать на гектаре"', "1-я инлайн-форма", "lgForm"
        )

        self.driver.get(f"{self.BASE_URL}/webinar/gos-support")
        self.check_element(
            "(//*[text()[contains(.,'вебинара')]]/ancestor::div[contains(@id, 'cfw')]//*[@value='mg_webinar'])[1]",
            'Вебинар "Гранты и господдержка"', "1-я инлайн-форма", "lgForm"
        )

        self.driver.get(f"{self.BASE_URL}/webinar/what-to-do")
        self.check_element(
            "(//*[text()[contains(.,'вебинара')]]/ancestor::div[contains(@id, 'cfw')]//*[@value='mg_webinar'])[1]",
            'Вебинар "Что делать на гектаре"', "1-я инлайн-форма", "lgForm"
        )

        self.driver.get(f"{self.BASE_URL}/webinar/how-to-choose")
        self.check_element(
            "(//*[text()[contains(.,'вебинара')]]/ancestor::div[contains(@id, 'cfw')]//*[@value='mg_webinar'])[1]",
            'Вебинар "Как выбрать участок"', "1-я инлайн-форма", "lgForm"
        )

        self.driver.get(f"{self.BASE_URL}/webinar/income-property")
        self.check_element(
            "(//*[text()[contains(.,'вебинара')]]/ancestor::div[contains(@id, 'cfw')]//*[@value='mg_webinar'])[1]",
            'Вебинар "Доходная недвижимость"', "1-я инлайн-форма", "lgForm"
        )

        self.driver.get(f"{self.BASE_URL}/webinar/answers-to-questions")
        self.check_element(
            "(//*[text()[contains(.,'вебинара')]]/ancestor::div[contains(@id, 'cfw')]//*[@value='mg_webinar'])[1]",
            'Вебинар "Ответы на вопросы"', "1-я инлайн-форма", "lgForm"
        )

        self.driver.get(f"{self.BASE_URL}/webinar/glamping")
        self.check_element(
            "(//*[text()[contains(.,'вебинара')]]/ancestor::div[contains(@id, 'cfw')]//*[@value='mg_webinar'])[1]",
            'Вебинар "Глэмпинг"', "1-я инлайн-форма", "lgForm"
        )

    def check_public_event_page(self):
        """Проверка раздела регистрации от стойки"""
        self.driver.get(f"{self.BASE_URL}/public-event")
        self.check_element(
            "(//*[text()[contains(.,'Оставьте')]]/ancestor::div[contains(@id, 'cfw')]//*[@value='public-event'])[1]",
            "раздел регистрации от стойки", "инлайн-форма", "lgForm"
        )

    def check_closed_offer_page(self):
        """Проверка раздела закрытого предложения"""
        self.driver.get(f"{self.BASE_URL}/closed-offer")
        self.check_element(
            "//*[text()[contains(.,'закрытом')]]/ancestor::div//*[@value='lg_closed_offer']",
            "раздел закрытого предложения", "инлайн-форма", "lgForm"
        )

    def run_all_checks(self):
        """Запуск всех проверок"""
        print("\n Начало проверки форм на сайте МойГектар")

        self.check_main_page_forms()
        self.check_catalog_forms()
        self.check_about_section()
        self.check_growth_section()
        self.check_support_section()
        self.check_faq_page()
        self.check_news_page()
        self.check_actions_section()
        self.check_other_pages()
        self.check_webinar_page()
        self.check_public_event_page()
        self.check_closed_offer_page()

        print("\n Проверка завершена")

    def close(self):
        """Закрытие браузера"""
        time.sleep(3)
        self.driver.quit()


if __name__ == "__main__":
    checker = FormChecker(headless=False)
    try:
        checker.run_all_checks()
    finally:
        checker.close()
