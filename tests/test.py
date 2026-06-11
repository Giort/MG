import time
from seleniumwire import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

ch_options = Options()
# ch_options.add_argument('--headless')
ch_options.add_argument("--window-size=360,900")
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

# Настройка драйвера с Selenium Wire
# Включаем перехват запросов
sw_options = {'disable_capture': False}
import json
from helpers.popups import remove_popups
from datetime import datetime
from helpers.auth import auth_mg


# Засекаем время начала теста
start_time = time.time()

with open('../data/data.json', 'r') as file:
    data = json.load(file)

# ============================================================
#  Переключение окружения: "prod" или "local"
# ============================================================
ENV = "prod"
# ============================================================

ENV_CONFIG = {
    "prod": {
        "base_url": "https://moigektar.ru",
        "cred_key": "LK_cred",
    },
    "local": {
        "base_url": "http://moigektar.localhost",
        "cred_key": "LK_local_cred",
    },
}

config      = ENV_CONFIG[ENV]
MG_BASE_URL = config["base_url"]

print(f"\n     Проверка отправки целей на моб. МГ на домене {MG_BASE_URL} | [{ENV.upper()}]\n")

def init_driver():
    """Инициализация драйвера"""
    driver = webdriver.Chrome(
        seleniumwire_options=sw_options,
        options=ch_options)
    return driver




# кнопки вызова квиза: отправляется цель при нажатии
def check_quiz_btn_goal(tests, max_attempts=3):
    results = {test['place']: {'success': False, 'attempts': 0} for test in tests}

    for test in tests:
        # Для каждого теста выполняем до max_attempts попыток
        for attempt in range(max_attempts):
            driver = None
            try:
                if results[test['place']]['success']:
                    break  # Если тест уже успешен, переходим к следующему

                driver = init_driver()
                actions = ActionChains(driver)

                driver.get(f'{MG_BASE_URL}/?__counters=1')

                time.sleep(2)
                remove_popups(driver)

                btn = driver.find_element(By.XPATH, test['quiz_btn'])
                actions.move_to_element(btn).perform()
                actions.send_keys(Keys.ARROW_DOWN).send_keys(Keys.ARROW_DOWN).send_keys(Keys.ARROW_DOWN).perform()
                btn.click()
                time.sleep(10)

                request_found = False
                for request in driver.requests:
                    if test['goal'] in request.url:
                        results[test['place']]['success'] = True
                        results[test['place']]['attempts'] = attempt + 1
                        request_found = True
                        break

                if request_found:
                    break  # Успешная попытка, выходим из цикла попыток для этого теста

            except Exception as e:
                if attempt == max_attempts - 1:  # Если это последняя попытка
                    print(f"Ошибка в тесте '{test['place']}': {e}")
            finally:
                if driver:
                    driver.quit()

                if attempt < max_attempts - 1 and not results[test['place']]['success']:
                    time.sleep(2)  # Короткая пауза между попытками одного теста

    # Выводим итоговые результаты
    all_success = True
    for test in tests:
        place = test['place']
        result = results[place]

        if result['success']:
            print(f'     ОК: при нажатии на кнопку квиза {test["place"]} отправляется цель "{test["goal"]}"')
        else:
            print(f' ERROR: при нажатии на кнопку квиза {test["place"]} текст "{test["goal"]}" не найден')
            all_success = False

    return all_success

# Параметры для check_quiz_btn_goal
quiz_tests = [
    {
        'quiz_btn': '(//*[@id="w-gektar-idea"]//a[contains(@class, "uk-button-danger")])[1]',
        'goal': 'quiz_btn_v2',
        'place': 'в "Гектар для реализации..."'
    }
]

# Запуск
try:
    check_quiz_btn_goal(quiz_tests)
except Exception as e:
    error_msg = str(e).split('\n')[0]
    print(' ERROR: при проверке кнопок квиза — ', error_msg)


# Вычисляем и выводим время выполнения теста
end_time = time.time()
elapsed_time = end_time - start_time
minutes = int(elapsed_time // 60)
seconds = int(elapsed_time % 60)

if minutes > 0:
    print(f'\n     Время выполнения теста: {minutes} мин {seconds} сек ({elapsed_time:.2f} сек)')
else:
    print(f'\n     Время выполнения теста: {seconds} сек ({elapsed_time:.2f} сек)')