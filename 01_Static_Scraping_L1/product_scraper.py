# product_scraper.py
# Level 1 Project: Static Quotes Scraper

import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
from typing import List, Dict, Any


TARGET_URL = 'http://quotes.toscrape.com/tag/life/' 

def fetch_and_parse(url: str) -> BeautifulSoup:
    print(f"-> Attempting to fetch URL: {url}")
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status() 
        time.sleep(1) 
        return BeautifulSoup(response.content, 'html.parser')
    except requests.exceptions.RequestException as e:
        print(f"ERROR: Request failed: {e}")
    return None

def extract_product_data(soup: BeautifulSoup) -> List[Dict[str, Any]]:
    if not soup: return []
    all_quotes = []

    quote_elements = soup.find_all('div', class_='quote')
    for quote_el in quote_elements:
        try:

            quote_text = quote_el.find('span', class_='text').get_text(strip=True)
            author_name = quote_el.find('small', class_='author').get_text(strip=True)
            tags = [tag.get_text(strip=True) for tag in quote_el.find('div', class_='tags').find_all('a')]
            all_quotes.append({
                'quote': quote_text, 
                'author': author_name, 
                'tags': ', '.join(tags) 
            })
        except Exception:
            continue
    return all_quotes

def run_scraper():
    print("--- Starting L1 Scraper ---")
    parsed_html = fetch_and_parse(TARGET_URL)
    if parsed_html is None: return
    scraped_data = extract_product_data(parsed_html)
    if not scraped_data: return
    df = pd.DataFrame(scraped_data)
    output_filename = 'scraped_quotes_data.csv'
    df.to_csv(output_filename, index=False, encoding='utf-8')
    print(f"\nSuccess: Data saved to {output_filename}")

if __name__ == "__main__":
    run_scraper()