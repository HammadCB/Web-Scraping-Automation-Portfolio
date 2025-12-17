import pandas as pd
import time
import re
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

def setup_driver():
    """Configures professional-grade Chrome options for e-commerce scraping."""
    chrome_options = Options()
    
    chrome_options.add_argument("--disable-blink-features=AutomationControlled") 
    chrome_options.add_argument("--start-maximized")
    
    service = Service(ChromeDriverManager().install())
    return webdriver.Chrome(service=service, options=chrome_options)

def scrape_tech_accessories():
    driver = setup_driver()
    tech_inventory = []
    
    # Targeting an Electronics/Tech Accessories sandbox environment
    url = "https://webscraper.io/test-sites/e-commerce/static/computers/laptops"
    
    try:
        driver.get(url)
        print(f"Initializing Tech Marketplace Intelligence Tool...")

        # Explicit Wait
        wait = WebDriverWait(driver, 10)
        
        while True:
            # Locate all product 
            product_cards = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "thumbnail")))

            for product in product_cards:

                # Attribute Extraction
                name = product.find_element(By.CLASS_NAME, "title").get_attribute("title")
                description = product.find_element(By.CLASS_NAME, "description").text
                price_raw = product.find_element(By.CLASS_NAME, "price").text
                
                #  Data Normalization: Converting '$1200.00' to a float 1200.0
                clean_price = float(re.sub(r'[^\d.]', '', price_raw))
                
                # Sentiment & Feedback Extraction
                reviews_count = product.find_element(By.CLASS_NAME, "ratings").find_element(By.TAG_NAME, "p").text
                
                tech_inventory.append({
                    "Product Model": name,
                    "Specifications": description,
                    "Price (USD)": clean_price,
                    "Review Count": reviews_count,
                    "Category": "Laptops & Accessories"
                })

            # Professional Pagination Handling

            print(f"✅ Extracted {len(product_cards)} tech items from current view.")
            break 


        df = pd.DataFrame(tech_inventory)
        
        #  Flag 'Premium' items (Price > 1000)
        df['Market Segment'] = df['Price (USD)'].apply(lambda x: 'Premium' if x > 1000 else 'Standard')
        
        df.to_csv("tech_market_analysis.csv", index=False)
        print(f"\n✨ SUCCESS: Market analysis saved to 'tech_market_analysis.csv'.")

    finally:
        driver.quit()

if __name__ == "__main__":
    scrape_tech_accessories()