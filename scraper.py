import csv
import requests

from bs4 import BeautifulSoup

BASE_URL = "https://books.toscrape.com/catalogue/page-{}.html"

def scrape_page(page):
    response = requests.get(BASE_URL.format(page), timeout=10)
    if response.status_code != 200:
        return []
    soup = BeautifulSoup(response.text, "html.parser")
    books = []
    for item in soup.select("article.product_pod"):
        title = item.h3.a["title"]
        price = item.select_one("p.price_color").text
        rating = item.p["class"][1]
        books.append({ "title": title, "price": price, "rating": rating })
    return books

def app(pages=6):
    all_books = []
    for page in range(1, pages + 1):
        books = scrape_page(page)
        all_books.extend(books)
        print(f"Page {page}: {len(books)} books")

    with open("books.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["title", "price", "rating"])
        writer.writeheader()
        writer.writerows(all_books)

if __name__ == "__main__":
    app()
