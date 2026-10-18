# Beginner Web Scraper

A beginner-friendly Python project that collects quotes, authors, and tags from [Quotes to Scrape](https://quotes.toscrape.com/) and saves them to a CSV file.

## Features

- Scrapes quotes, authors, and tags from the first two pages.
- Checks the website's `robots.txt` before scraping.
- Saves the results in `quotes.csv`.

## Requirements

- Python 3
- `requests`
- `beautifulsoup4`

## Installation

Install the required packages:

```bash
python -m pip install requests beautifulsoup4
```

## Run the scraper

```bash
python web-scraping.py
```

The results will be saved in `quotes.csv` in the project folder.

## Output

The CSV file contains three columns:

- `quote`
- `author`
- `tags`

This project is for learning web scraping with Python, Requests, and Beautiful Soup.
