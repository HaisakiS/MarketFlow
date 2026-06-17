from database import get_marketflow_products
from analytics import plot_product_trend
from scraper import get_scraped_title, find_product_match

def print_menu():
    print("\n======================================")
    print("        MarketFlow SYSTEM v1.0        ")
    print("======================================")
    print("1. 🌐 Capture Price from URL")
    print("2. 📈 Analyze Trends (Chart)")
    print("3. 📋 View Product Catalog")
    print("4. ❌ Exit")
    print("======================================")

def handle_capture_price():
    #Allows scraping and register new price
    print("\n" + "=" * 38)
    print("           CAPTURE NEW PRICE           ")
    print("=" * 38)
    
    url = input("Enter the product URL (Facebook, Aliexpress, Amazon, Ebay.): \n").strip()
    if not url:
        print("⚠️ URL cannot be empty.")
        return
        
    extracted_title, source = get_scraped_title(url)
    db_products = get_marketflow_products()
    
    #Searching for matches in the database
    matches = find_product_match(extracted_title, db_products)
    
    """TO DO: Code to record the price, give choices..."""

def handle_view_analytics():
    #Show the graph of a product's price history
    print("\n" + "=" * 38)
    print("             TREND ANALYSIS             ")
    print("=" * 38)
    
    #Shows list to choose product
    products = get_marketflow_products()
    
    if not products:
        print("There are no productos to analyze.")
        return
        
    print("Catalog available for analysis:\n")
    for index, product in enumerate(products):
        print(f"  {index+1}. {product}")
        
    print("-" * 38)
    selection = input(f"Choose the product number to chart (1-{len(products)}): ").strip()
    
    try:
        selected_index = int(selection) - 1
        if 0 <= selected_index < len(products):
            chosen_product = products[selected_index]
            print(f"\n📊 Generating chart for '{chosen_product}'...")
            plot_product_trend(chosen_product)
        else:
            print("Error: Number out of range.")
    except ValueError:
        print("Error: Please enter a valid number.")

def handle_view_catalog():
    #List the registered products
    print("\n" + "=" * 38)
    print("            PRODUCT CATALOG            ")
    print("=" * 38)
    
    products = get_marketflow_products()
    
    if products:
        for index, product in enumerate(products, 1):
            print(f"  {index}. {product}")
    else:
        print("No products registered in history.")