from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import json
import time
import random

chrome_options = Options()
chrome_options.add_argument("--log-level=3")
chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])


def write_to_json(books_data):
    with open("books_filtered.json", "w", encoding="utf-8") as f:
        json.dump(books_data, f, indent=4)

def highest_price(books):
    price = 0
    selected_book = books[0]
    for book in books:
        if book["price"] > price:
            price = book["price"]
            selected_book = book
    return selected_book

def lowest_price(books):
    price = books[0]["price"]
    selected_book = books[0]
    for book in books:
        if book["price"] < price:
            price = book["price"]
            selected_book = book
    return selected_book

def list_found_books(books):
    n = 1
    for book in books:
        print(f"{n})\t\"{book["title"]}\" (£{book["price"]}) | {book["category"]}")
        n += 1

def filter_books(cat_input, min, max):
    driver = webdriver.Chrome(options=chrome_options, service=Service(ChromeDriverManager().install()))
    driver.get("http://books.toscrape.com/")
    time.sleep(2)
    
    books_data = []

    try:
        category_elems = driver.find_elements(By.CSS_SELECTOR, "ul.nav-list ul li a")
        category_links = [{"name": cat.text.strip(), "url": cat.get_attribute("href")} for cat in category_elems]

        for cat in category_links:
            if cat_input and cat_input not in cat["name"].lower():
                continue

            driver.get(cat["url"])
            time.sleep(1)

            while True:
                books = driver.find_elements(By.CSS_SELECTOR, "article.product_pod")
                for book in books:
                    title = book.find_element(By.CSS_SELECTOR, "h3 a").get_attribute("title")
                    price_text = book.find_element(By.CSS_SELECTOR, ".price_color").text.replace("£", "")
                    price = float(price_text)
                    if min <= price <= max:
                        books_data.append({"title": title, "price": price, "category": cat["name"]})

                next_btn = driver.find_elements(By.CSS_SELECTOR, "li.next a")
                if next_btn:
                    next_btn[0].click()
                    time.sleep(1)
                else:
                    break
    finally:
        driver.quit()

    return books_data

def main_loop():
    running = True
    while running:
        usr_input = ""
        category_input = ""
        min_price = 0
        max_price = 0

        print("\n=== Books Scraper ===")

        while True:
            try:
                category_input = input("Masukkan kategori buku (misal: travel, music, poetry, art, dll)\n> ").strip().lower()
                min_price = float(input("Masukkan harga minimum (contoh: 0)\n> "))
                max_price = float(input("Masukkan harga maksimum (contoh: 100)\n> "))

            except ValueError:
                print("\n~!!!~ Salah input ~!!!~\n")
                continue

            else:
                break

        print("\n=== Pencarian Buku ===")
        
        books_data = filter_books(category_input, min_price, max_price)
        
        if books_data:
            total_books = len(books_data)
            avg_price = sum(book["price"] for book in books_data) / total_books
            expensive_book = highest_price(books_data)
            cheap_book = lowest_price(books_data)
            rec_index = random.randrange(0, total_books)
            recommended_book = books_data[rec_index]
            print(f"Total buku ditemukan:\t{total_books} buku")
            print(f"Rata-rata harga:\t£{avg_price:.2f}")

            print("\n=== Detail Pencarian ===")
            print(f"Harga minimum: \t\t\"{cheap_book["title"]}\" (£{cheap_book["price"]}) | {cheap_book["category"]}")
            print(f"Harga tertinggi:\t\"{expensive_book["title"]}\" (£{expensive_book["price"]}) | {expensive_book["category"]}")
            print(f"Buku Rekomendasi:\t\"{recommended_book["title"]}\" (£{recommended_book["price"]}) | {recommended_book["category"]}")
            
            print("\nData disimpan ke 'books_filtered.json'")
            while True:
                usr_input = input("\nList semua buku yang ditemukan? (y/n)\n> ")
                if usr_input == "y":
                    list_found_books(books_data)
                    break
                elif usr_input =="n":
                    break
                else:
                    continue
        else:
            print("Tidak ada buku sesuai filter yang kamu masukkan.")
        
        while True:
            usr_input = input("\nCari ulang buku? (y/n)\n> ")
            if usr_input == "y":
                break
            elif usr_input == "n":
                running = False
                break
            else:
                continue


if __name__ == "__main__":
    main_loop()
