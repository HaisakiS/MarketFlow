from playwright.sync_api import sync_playwright
from database import connect_db
from thefuzz import process, fuzz
import re

def get_page_data(url):
    with sync_playwright() as p:
        browser = p.chromium.launch_persistent_context( #chromium browser with its own cookies to avoid blocks
            user_data_dir="playwright_profile",
            headless=True
        )
        page = browser.new_page()
        page.goto(url, wait_until="domcontentloaded")
        
        # Timeout to load the page
        page.wait_for_timeout(3000)
        
        # Extracting the title
        title = page.title()
        #Extracting price
        price = get_price_from_page(page,get_source_name(url)) 
        
        browser.close()
        return title, price


def get_source_name(url):
    conn = connect_db()
    if conn is None:
        return "Unknown"
        
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT source_name FROM price_sources;")
        db_sources = [row[0] for row in cursor.fetchall()]
    except Exception as e:
        print(f"Error reading sources: {e}")
        return "Unknown"
    finally:
        conn.close()

    url_lower = url.lower() #lower to compare
    
    for source in db_sources:
        clean_name = source.lower().replace(' ', '') #remove possible spaces in database source list
        if clean_name in url_lower:
            return source
            
    return "Unknown"


def get_scraped_data(url):
    source_name = get_source_name(url)
    
    if source_name == "Unknown":
         return "Unsupported URL", "Unknown", 0
    
    print(f"\nProcessing {source_name} URL...")
    
    try:
        # Playwright scrapping
        extracted_title, extracted_price = get_page_data(url)
        #Shortening and cleaning the title
        extracted_title = extracted_title.replace('Amazon.com: ','') #In case of Amazon link
        
        if extracted_title:
            if ',' in extracted_title:
                clean_title = extracted_title.split(',', 1)[0]
            elif ' - ' in extracted_title:
                clean_title = extracted_title.split(' - ', 1)[0]
            elif ' | ' in extracted_title:
                clean_title = extracted_title.split(' | ', 1)[0]
            else:
                clean_title = extracted_title
            return clean_title, source_name, extracted_price
            
        else:
            return "Tags not found", source_name, extracted_price
            
    except Exception as e:
        return f"Error processing URL: {e}", source_name, extracted_price


def find_product_match(scraped_title, database_products, scraped_price):
    if not scraped_title:
        print("No title")
        return []
    
    if not database_products:
        print("No products registered in history to compare.")
        return []
    
    matches = process.extract(
        scraped_title, 
        database_products, 
        scorer=fuzz.token_set_ratio, 
        limit=3 
    ) 
    
    print(f"\nAnalyzing web title: '{scraped_title}'...\n")
    print(f"\nPrice: $ {scraped_price}\n")
    print("🎯 Options found in your MarketFlow database:")
    print("-" * 65)
    for index, match in enumerate(matches): #matches are saved as [(prod1, score1), (prod2, score2), (prod3, score3)]
        product_name = match[0]
        score = match[1]
        
        #score is % of match
        if score >= 80:
            status = "✅ HIGH MATCH"
        elif score >= 50:
            status = "⚠️ PARTIAL MATCH"
        else:
            status = "❌ LOW MATCH"
            
        print(f"{index + 1}. {product_name:<30} | Match: {score}% | {status}")
    print("0. ➕ Add as a new product\n")
    print("-" * 65)
    
    return matches


def clean_price_text(text):
    if not text:
        return 0.0
    
    # Regex to clean currency paterns
    match = re.search(r'(\d+[\.,]?\d*)', text)
    
    if match:
        clean_str = match.group(1).replace(',', '.')
        try:
            return float(clean_str)
        except ValueError:
            return 0.0
    return 0.0


def get_price_from_page(page, source_name):
    price_text = ""
    try: #locate tags, price is stored on different tags depending the website
        if source_name == "Amazon":
            price_text = page.locator(".a-price-whole").first.text_content()
        elif source_name == "Ebay":
            price_text = page.locator(".x-price-primary").first.text_content()
        elif source_name == "Aliexpress":
            price_text = page.locator("span[class*='price-default--current']").first.text_content()
        elif source_name == "Facebook":
            #Facebook is a special case, it uses dinamic tags so look for the currency symbol instead
            currency = 'S/' #variates with country
            price_text = page.locator("span[dir='auto']").filter(has_text=currency).first.text_content()
        
        return clean_price_text(price_text)
        
    except Exception:
        return 0.0