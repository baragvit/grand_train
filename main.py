from selenium.webdriver.common.by import By

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

options = Options()
# options.add_argument("--headless")  # Run browser in headless mode (no GUI)
driver = webdriver.Chrome(options=options)
driver.get("https://grandtrain.ru/search/2000000-2078001/02.01.2026/028%D0%9C/")
WebDriverWait(driver, 60).until(
    EC.presence_of_element_located((By.CLASS_NAME, "car-class__fare-item"))
)

html = driver.page_source  # The full HTML after JS execution

with open("page.html", "w", encoding="utf-8") as f:
    f.write(html)

driver.quit()

