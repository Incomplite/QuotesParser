import json

import requests

from bs4 import BeautifulSoup

url = "https://quotes.toscrape.com/"

data = []


def parse_page(page_url):
    response = requests.get(page_url)
    soup = BeautifulSoup(response.text, "html.parser")

    quotes = soup.find_all("div", class_="quote")
    for quote in quotes:
        text = quote.find("span", class_="text").get_text()
        author = quote.find("small", class_="author").get_text()
        tags = [tag.get_text() for tag in quote.find_all("a", class_="tag")]
        data.append({"quote": text, "author": author, "tags": tags})

    # Проверяем на наличие следующей страницы
    next_button = soup.find("li", class_="next")
    if next_button:
        next_url = url + next_button.find("a")["href"]
        parse_page(next_url)

# Запускаем парсинг
parse_page(url)

# Сохранение данных в JSON
with open("data.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=4)
