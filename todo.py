from seleniumwire import webdriver
from selenium.webdriver.common.by import By

# переделать проверку lgForm по этому образцу
def check_request_on_page(page_url, button_selector, expected_text):
    driver = webdriver.Chrome()
    driver.get(page_url)

    # Клик по указанной кнопке
    driver.find_element(By.CSS_SELECTOR, button_selector).click()

    # Проверка запросов
    result = any(expected_text in req.url for req in driver.requests)

    if result:
        print(f"✅ На странице {page_url} найден текст '{expected_text}'")
    else:
        print(f"❌ На странице {page_url} текст '{expected_text}' не найден")

    driver.quit()
    return result


# Пример использования
check_request_on_page(
    page_url="https://example.com/page1",
    button_selector="#submit-btn-1",
    expected_text="api/v1/submit"
)

check_request_on_page(
    page_url="https://example.com/page2",
    button_selector=".ajax-button",
    expected_text="graphql/query"
)