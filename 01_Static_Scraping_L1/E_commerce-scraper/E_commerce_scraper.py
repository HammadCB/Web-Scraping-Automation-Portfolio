# ecommerce_scraper.py
# Level 1 Project: Multi-Page E-commerce Inventory Scraper
# Demonstrates professional skills in multi-page traversal (Pagination) and proxy readiness.

import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
from typing import List, Dict, Any

# --------------------------------------------------------------------------
# 1. CONFIGURATION (Pagination and Professional Headers)
# --------------------------------------------------------------------------

# Target Site: The mock site for pagination practice
BASE_URL = 'https://scrapeme.live/shop/page/' 
START_PAGE = 1
END_PAGE = 3 # Scrapes pages 1 through 3 for robust practice

# MOCK PROXY SETUP: Demonstrates readiness for client's paid proxy service
PROXY_ENABLED = False 
MOCK_PROXY = {
    "http": "http://user:password@proxy_host:port",
    "https": "https://user:password@proxy_host:port"
}

# --------------------------------------------------------------------------
# 2. DATA EXTRACTION FUNCTION (Inventory Data)
# --------------------------------------------------------------------------

def extract_product_data(soup: BeautifulSoup) -> List[Dict[str, Any]]:
    """
    Extracts structured inventory data (Title, Price, Rating) from a single parsed HTML page.
    """
    product_data = []
    # Find all product containers (li with class 'product')
    product_containers = soup.find_all('li', class_='product')
    
    for container in product_containers:
        try:
            # 1. Title 
            title_element = container.find('h2', class_='woocommerce-loop-product__title')
            title = title_element.get_text(strip=True) if title_element else 'N/A'
            
            # 2. Price (Cleansing Euro symbol for clean analysis)
            price_element = container.find('span', class_='price')
            price = price_element.get_text(strip=True).replace('€', '').strip() if price_element else 'N/A'
            
            # 3. Rating Status (Checks for element existence)
            rating_element = container.find('div', class_='star-rating')
            rating_status = 'Rated' if rating_element else 'Unrated'
            
            product_data.append({
                'Product_Title': title,
                'Price_EUR': price,
                'Rating_Status': rating_status
            })
        except Exception:
            continue
            
    return product_data

# --------------------------------------------------------------------------
# 3. MAIN EXECUTION WITH PAGINATION LOOP
# --------------------------------------------------------------------------

def run_multi_page_scraper():
    """Main function to orchestrate fetching, extraction, and saving across pages."""
    all_scraped_data = []
    print("--- Starting Multi-Page Inventory Scraper ---")
    
    # Setup a persistent session with headers
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit=537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    })
    
    if PROXY_ENABLED:
        session.proxies.update(MOCK_PROXY)
        print("INFO: Proxy feature enabled.")
        
    for page_num in range(START_PAGE, END_PAGE + 1):
        page_url = f"{BASE_URL}{page_num}/" 
        print(f"\n-> Fetching Page {page_num} from: {page_url}")
        
        try:
            response = session.get(page_url, timeout=15)
            response.raise_for_status() 
            
            soup = BeautifulSoup(response.content, 'html.parser')
            current_page_data = extract_product_data(soup)
            all_scraped_data.extend(current_page_data) 
            
            print(f"-> Extracted {len(current_page_data)} items.")
            time.sleep(2) # Polite delay

        except requests.exceptions.RequestException as e:
            print(f"FATAL ERROR: Failed to fetch {page_url}. Stopping scraper. Error: {e}")
            break
            
    if not all_scraped_data:
        print("\nScraping failed: No data was collected.")
        return

    df = pd.DataFrame(all_scraped_data)
    output_filename = 'scraped_ecommerce_inventory.csv'
    df.to_csv(output_filename, index=False, encoding='utf-8')
    
    print("\nSuccess: Multi-page scrape complete.")
    print(f"Total records: {len(df)}. Data saved to {output_filename}")
    
if __name__ == "__main__":
    run_multi_page_scraper()