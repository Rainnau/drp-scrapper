from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import json
import time

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get("http://books.toscrape.com/")
time.sleep(2)

print("=== Books Scraper ===")
category_input = input("Masukkan kategori buku (misal: travel, music, poetry, art, dll): ").strip().lower()
min_price = float(input("Masukkan harga minimum (contoh: 0): "))
max_price = float(input("Masukkan harga maksimum (contoh: 100): "))

books_data = []

try:
    category_elems = driver.find_elements(By.CSS_SELECTOR, "ul.nav-list ul li a")
    category_links = [{"name": cat.text.strip(), "url": cat.get_attribute("href")} for cat in category_elems]

    for cat in category_links:
        if category_input and category_input not in cat["name"].lower():
            continue

        driver.get(cat["url"])
        time.sleep(1)

        while True:
            books = driver.find_elements(By.CSS_SELECTOR, "article.product_pod")
            for book in books:
                title = book.find_element(By.CSS_SELECTOR, "h3 a").get_attribute("title")
                price_text = book.find_element(By.CSS_SELECTOR, ".price_color").text.replace("£", "")
                price = float(price_text)
                if min_price <= price <= max_price:
                    books_data.append({"title": title, "price": price, "category": cat["name"]})

            next_btn = driver.find_elements(By.CSS_SELECTOR, "li.next a")
            if next_btn:
                next_btn[0].click()
                time.sleep(1)
            else:
                break

finally:
    driver.quit()

if books_data:
    total_books = len(books_data)
    avg_price = sum(book["price"] for book in books_data) / total_books
    print(f"\nTotal buku ditemukan: {total_books}")
    print(f"Rata-rata harga: £{avg_price:.2f}")
    print("Data disimpan ke 'books_filtered.json'")
    with open("books_filtered.json", "w", encoding="utf-8") as f:
        json.dump(books_data, f, indent=4)
else:
    print("\nTidak ada buku sesuai filter yang kamu masukkan.")