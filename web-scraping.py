import csv
import time
from urllib.parse import urljoin
from urllib.robotparser import RobotFileParser

import requests
from bs4 import BeautifulSoup

START_URL = "https://quotes.toscrape.com/"
USER_AGENT = "BeginnerQuoteScraper/1.0"


def robots_allows(url):
    robots_url = urljoin(url, "/robots.txt")
    parser = RobotFileParser()
    parser.set_url(robots_url)

    try:
        response = requests.get(
            robots_url,
            headers={"User-Agent": USER_AGENT},
            timeout=15,
        )

        if response.status_code == 404:
            parser.parse([])
            return True

        if response.status_code != 200:
            return False

        parser.parse(response.text.splitlines())
        return parser.can_fetch(USER_AGENT, url)

    except requests.RequestException:
        return False


def scrape_page(session, url):
    response = session.get(url, timeout=20)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    quotes = []

    for card in soup.select("div.quote"):
        quote = card.select_one("span.text")
        author = card.select_one("small.author")
        tags = [tag.get_text(strip=True) for tag in card.select("a.tag")]

        quotes.append({
            "quote": quote.get_text(strip=True) if quote else "",
            "author": author.get_text(strip=True) if author else "",
            "tags": ", ".join(tags),
        })

    next_link = soup.select_one("li.next a")
    next_url = urljoin(url, next_link["href"]) if next_link else None

    return quotes, next_url


def main():
    if not robots_allows(START_URL):
        print("مش مسموح بالسحب حسب robots.txt،")
        return

    session = requests.Session()
    session.headers.update({"User-Agent": USER_AGENT})

    all_quotes = []
    current_url = START_URL

  
    for page in range(2):
        if not current_url:
            break

        print(f"بنجمع الصفحة {page + 1}...")
        quotes, current_url = scrape_page(session, current_url)
        all_quotes.extend(quotes)

        if current_url and page < 1:
            time.sleep(1)

    with open("quotes.csv", "w", newline="", encoding="utf-8-sig") as file:
        columns = ["quote", "author", "tags"]
        writer = csv.DictWriter(file, fieldnames=columns)
        writer.writeheader()
        writer.writerows(all_quotes)

    print(f"خلصنا! جمعنا {len(all_quotes)} اقتباس في quotes.csv")


if __name__ == "__main__":
    main()