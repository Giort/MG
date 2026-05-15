from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


def auth_mg(driver, auth_url: str, creds: dict, btn_index: int = 1) -> bool:
    """
    Авторизация на сайте МГ через модальное окно.

    Args:
        driver:     экземпляр Selenium WebDriver
        auth_url:   URL страницы, с которой открывается модалка авторизации
        creds:      словарь с ключами "login" и "password"
        btn_index:  индекс кнопки открытия модалки (1 — десктоп, 6 — мобайл)

    Returns:
        True если авторизация прошла успешно, False иначе
    """
    try:
        driver.get(auth_url)

        # Открываем модальное окно авторизации
        auth_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, f'(//*[@href="#modal-auth-lk"])[{btn_index}]')
            )
        )
        auth_btn.click()
        time.sleep(1)

        # Переключаемся на вкладку "По паролю"
        driver.find_element(By.XPATH, '//*[text()="По паролю"]').click()
        time.sleep(0.5)

        # Заполняем форму
        driver.find_element(By.XPATH, '//*[@id="authform-login"]').send_keys(str(creds["login"]))
        driver.find_element(By.XPATH, '//*[@id="authform-password"]').send_keys(str(creds["password"]))
        driver.find_element(By.XPATH, '//*[text()="Войти"]').click()

        time.sleep(5)
        return True

    except Exception as e:
        print(f" ERROR: Не удалось авторизоваться — {str(e)}")
        return False
