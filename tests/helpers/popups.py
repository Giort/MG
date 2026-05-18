from selenium.webdriver.common.by import By


def remove_popups(driver):
    """
    Удаляет попап посетителей (#visitors-popup).
    Используется при проверке нижней части главной страницы,
    где попап может перекрывать элементы.

    Args:
        driver: экземпляр Selenium WebDriver
    """
    try:
        popup = driver.find_element(By.XPATH, "//div[@id='visitors-popup']")
        driver.execute_script("arguments[0].remove();", popup)
    except Exception:
        pass

    """
    Удаляет попап запущенного вебинара (.js-webinar-running-event-modal).
    Может появляться на любой странице при первом открытии сайта.

    Args:
        driver: экземпляр Selenium WebDriver
    """
    try:
        popup = driver.find_element(By.XPATH, "//*[contains(@class, 'js-webinar-running-event-modal')]")
        driver.execute_script("arguments[0].remove();", popup)
    except Exception:
        pass