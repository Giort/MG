from selenium.webdriver.common.by import By


def remove_popups(driver, skip=None):
    """
    Удаляет попапы, мешающие проверкам.

    Args:
        driver: экземпляр Selenium WebDriver
        skip:   список id/классов попапов которые не нужно удалять, например ['wStickyVideo']
    """
    skip = skip or []

    # Удаляет попап посетителей (#visitors-popup).
    # Появляется на главной странице, когда доскроллили до блока спецпредложений
    if 'visitors-popup' not in skip:
        try:
            popup = driver.find_element(By.XPATH, "//div[@id='visitors-popup']")
            driver.execute_script("arguments[0].remove();", popup)
        except Exception:
            pass

    # Удаляет попап запущенного вебинара (.js-webinar-running-event-modal).
    # Может появляться на любой странице при первом открытии сайта.
    if 'js-webinar-running-event-modal' not in skip:
        try:
            popup = driver.find_element(By.XPATH, "//*[contains(@class, 'js-webinar-running-event-modal')]")
            driver.execute_script("arguments[0].remove();", popup)
        except Exception:
            pass

    # Удаляет попап фиксированного видео на главной (#wStickyVideo).
    # Появляется на деск сразу при открытии сайта, а на моб через 10 секунд после открытия
    # Если перезагрузить страницу - появится снова
    if 'wStickyVideo' not in skip:
        try:
            popup = driver.find_element(By.ID, "wStickyVideo")
            driver.execute_script("arguments[0].remove();", popup)
        except Exception:
            pass