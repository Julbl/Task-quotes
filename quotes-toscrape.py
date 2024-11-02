import json
from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin


def parse_quotes_toscrape(page_url, quotes_toscrape_data=None):
    if quotes_toscrape_data is None:
        quotes_toscrape_data = []

    try:
        response = requests.get(page_url)
        response.raise_for_status()

    except requests.exceptions.HTTPError as e:
        print(f"Не удалось получить доступ к странице: {page_url} - {str(e)}")
        return quotes_toscrape_data

    bs = BeautifulSoup(response.text, "html.parser")
    quotes = bs.find_all('div', class_="quote")

    for quote in quotes:
        text = quote.find('span', 'text').get_text()
        author = quote.find('small', 'author').get_text()
        tags = [tag.get_text() for tag in quote.find_all('a', 'tag')]

        quotes_toscrape_data.append({
            "text": text,
            "author": author,
            "tags": tags
        })


    next_btn = bs.find('li', class_='next')
    if next_btn:
        next_url = urljoin(page_url, next_btn.find("a")["href"])
        return parse_quotes_toscrape(next_url, quotes_toscrape_data)

    if quotes_toscrape_data:
        with open("quotes.json", "w", encoding="utf-8") as f:
            json.dump(quotes_toscrape_data, f, ensure_ascii=False, indent=4)


def main():
    url = 'https://quotes.toscrape.com/'
    parse_quotes_toscrape(url)


if __name__ == "__main__":
    main()
