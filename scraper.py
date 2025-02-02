"""
Einfacher Webscraper für Bücherdaten 
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
from pathlib import Path

def scrape_books():
    base_url = "https://books.toscrape.com/"
    current_page = base_url
    books_data = []

    while True:
        try:
            response = requests.get(current_page)
            response.raise_for_status()  

            soup = BeautifulSoup(response.text, "html.parser")
            books = soup.find_all("article", class_="product_pod")

            for book in books:
                title = book.h3.a["title"]
                price = book.find("p", class_="price_color").get_text().strip()
                rating = book.p["class"][1] + " Stars"
                books_data.append({
                    "Title": title,
                    "Price": price,
                    "Rating": rating
                })

            next_page = soup.find("li", class_="next")
            if next_page:
                next_page_url = next_page.a["href"]
                current_page = base_url + next_page_url
            else:
                break

        except requests.exceptions.RequestException as e:
            print(f"Fehler bei der Anfrage: {e}")
            break

    return books_data

def save_to_excel(data, filename="books_data.xlsx"):
    df = pd.DataFrame(data)
    output_path = Path(__file__).parent / filename
    df.to_excel(output_path, index=False)
    print(f"Daten erfolgreich exportiert nach: {output_path}")

if __name__ == "__main__":
    print("Starte Scraping...")
    books = scrape_books()
    save_to_excel(books)
    print("Fertig!")