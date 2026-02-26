import csv
import time
from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Safari()
rows = []

try:
    page_num = 1
    url = "https://ru.wikipedia.org/wiki/Категория:Еда_и_напитки"

    while url and page_num <= 5:
        driver.get(url)
        time.sleep(2)

        for element in driver.find_elements(By.CSS_SELECTOR, ".mw-category-group a"):
            if element.text.strip() and element.get_attribute("href"):
                rows.append({
                    "title": element.text.strip(),
                    "url": element.get_attribute("href"),
                    "page": page_num,
                    "collected_at": time.strftime("%Y-%m-%d %H:%M:%S"),
                })

        next_url = None
        for element in driver.find_elements(By.CSS_SELECTOR, "#mw-pages a"):
            if (element.text or "").strip().lower() == "следующая страница":
                next_url = element.get_attribute("href")
                break

        url = next_url
        page_num += 1

finally:
    driver.quit()

with open("result.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(file, fieldnames=["title", "url", "page", "collected_at"])
    writer.writeheader()
    writer.writerows(rows)

print("Saved: result.csv")