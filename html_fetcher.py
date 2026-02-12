from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


def get_grand_train_page():
    try:
        options = Options()
        options.add_argument("--headless")  # Run browser in headless mode (no GUI)
        driver = webdriver.Chrome(options=options)
        driver.set_page_load_timeout(15)
        driver.get("https://grandtrain.ru/search/2078001-2000000/28.02.2026/028%D0%A1/")
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CLASS_NAME, "car-class__fare-item"))
        )
    except TimeoutException as e:
        driver.quit()
        return {"failed": e}
    html = driver.page_source  # The full HTML after JS execution
    driver.quit()
    return {"ok": html}

if __name__ == '__main__':
    print(get_grand_train_page())
