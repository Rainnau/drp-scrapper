from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import StaleElementReferenceException
import json
import time

def scrape_quotes(author_name=None, tag_name=None):
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get("http://quotes.toscrape.com/")
    time.sleep(1)

    all_quotes = []

    while True:
        quotes = driver.find_elements(By.CLASS_NAME, "quote")

        for q in quotes:
            try:
                text = q.find_element(By.CLASS_NAME, "text").text
                author = q.find_element(By.CLASS_NAME, "author").text
                tags = [t.text for t in q.find_elements(By.CLASS_NAME, "tag")]

                if (author_name is None or author.lower() == author_name.lower()) and \
                   (tag_name is None or tag_name.lower() in [t.lower() for t in tags]):
                    all_quotes.append({
                        "text": text,
                        "author": author,
                        "tags": tags
                    })
            except StaleElementReferenceException:
                continue  

        try:
            next_btn = driver.find_element(By.CSS_SELECTOR, ".next a")
            next_btn.click()
            time.sleep(1.5) 
        except:
            break

    driver.quit()

    with open("quotes_data.json", "w", encoding="utf-8") as f:
        json.dump(all_quotes, f, ensure_ascii=False, indent=4)

    print(f"\n Total quotes ditemukan: {len(all_quotes)}")
    print(" Data disimpan ke file 'quotes_data.json'")
    return all_quotes


if __name__ == "__main__":
    print("=== Quotes Scraper ===")
    author = input("Masukkan nama author (kosongkan jika ingin semua): ")
    tag = input("Masukkan tag (kosongkan jika ingin semua): ")

    result = scrape_quotes(
        author_name=author if author else None,
        tag_name=tag if tag else None
    )

    for r in result:
        print(f"\n{r['text']}\n— {r['author']} | Tags: {', '.join(r['tags'])}")