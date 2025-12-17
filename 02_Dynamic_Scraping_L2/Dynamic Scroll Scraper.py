# Level 2 Project: Dynamic Scroll and Wait Automator
# Demonstrates controlling a browser (Selenium) to load JavaScript content.

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time
from typing import List, Dict, Any

# --- CONFIGURATION ---

TARGET_URL = 'http://quotes.toscrape.com/scroll' 

# --- 1. CORE AUTOMATION FUNCTION ---

def run_dynamic_scraper(url: str):
    
    print(f"--- Starting Dynamic Scraper (Selenium) for: {url} ---")
    
    # Initialize the WebDriver 
    try:
        
        driver = webdriver.Chrome(service=Service())
        driver.get(url)
        print("Browser initialized and navigated to target URL.")
        
        
        QUOTE_CLASS = "quote"
        
      # AUTOMATICALLY SCROLL TO LOAD MORE CONTENT ---
        
        scroll_count = 3 
        print(f"Starting auto-scroll sequence ({scroll_count} times)...")
        
        for i in range(scroll_count):
            
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            
            # Explicit Wait
            
            try:
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, QUOTE_CLASS))
                )
                print(f"  -> Scroll {i+1} successful. New content loaded.")
                time.sleep(1) 
            except Exception:
                print(f"  -> Scroll {i+1} failed to load new content. Page end reached.")
                break
        
        print("\n--- PHASE 2: EXTRACTING ALL LOADED DATA ---")
        
       
        all_quotes = driver.find_elements(By.CLASS_NAME, QUOTE_CLASS)
        print(f"Total quotes found on page (after scrolling): {len(all_quotes)}")
        
        scraped_data: List[Dict[str, str]] = []
        for quote_el in all_quotes:

            
            text = quote_el.find_element(By.CLASS_NAME, 'text').text
            author = quote_el.find_element(By.CLASS_NAME, 'author').text
            
            scraped_data.append({
                'Quote': text,
                'Author': author,
                'Method': 'Selenium Scroll'
            })
            
        # ---  CLEAN UP AND SAVE ---
        driver.quit() 
        
        if scraped_data:
            df = pd.DataFrame(scraped_data)
            output_filename = 'scraped_dynamic_scroll_data.csv'
            df.to_csv(output_filename, index=False, encoding='utf-8')
            print(f"\nSuccess: Scraped {len(df)} records. Data saved to {output_filename}")
        else:
            print("\nWARNING: No data was extracted.")
            
    except Exception as e:
        print(f"A major error occurred during scraping: {e}")
        
        if 'driver' in locals():
            driver.quit()

if __name__ == "__main__":
    run_dynamic_scraper(TARGET_URL)