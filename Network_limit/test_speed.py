from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


def run_speedtest():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")

    service = Service('/usr/bin/chromedriver')
    driver = webdriver.Chrome(service=service, options=options)

    try:
        driver.get("https://www.speedtest.net")

        # Ожидание загрузки кнопки "Go" и нажатие на нее
        go_button = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "a.js-start-test.test-mode-multi")))
        go_button.click()

        time.sleep(40)

        # Ожидание появления результатов
        download_speed = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "span.download-speed")))

        upload_speed = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "span.upload-speed")))

        download_result = download_speed.text
        upload_result = upload_speed.text
        print(f"Download Speed: {download_result} Mbps")
        print(f"Upload Speed: {upload_result} Mbps")
    finally:
        driver.quit()


if __name__ == "__main__":
    t1 = time.time()
    run_speedtest()
    print(f"{int(time.time() - t1)} сек")
