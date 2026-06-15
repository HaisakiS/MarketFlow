import requests #Library for HTTP requests
from bs4 import BeautifulSoup #Library to parse HTML code
from thefuzz import process, fuzz #Library to match product name

def clean_url(dirty_url):
    #Cleans the Facebook URL striping text after the id of the product
    clean_link = dirty_url.split('?')[0]
    return clean_link

'''[TO DO: Add support for Ebay and TEMU]'''

def get_facebook_title(url):
    clean_link = clean_url(url)
    print(f"Processing clean URL: {clean_link}")
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    try:
        response = requests.get(clean_link, headers=headers, timeout=5) #download HTML code
        soup = BeautifulSoup(response.text, 'html.parser') #parse the response
        meta_tag = soup.find('meta', property='og:title') #look for a <meta> tag with "og:title" property
        #F.E: Facebook has the item title in <meta property="og:title" content="Gamesir Nova Lite">
        
        if meta_tag and meta_tag.get('content'): #verify it isn't empty
            return meta_tag['content']
        else:
            return "Tag not found"
    except Exception as e:
        return f"Error processing URL: {e}"

def find_product_match(scraped_title, database_products):
    #Matches scraped product with existing products in the list.
    if not database_products:
        print("No products registered in history to compare.")
        return None
        
    print(f"\nAnalyzing web title: '{scraped_title}'...\n")
    
    matches = process.extract(
        scraped_title, 
        database_products, #Compares scraped title from website with the database
        scorer=fuzz.token_set_ratio, #Compares by repeated words
        limit=3 #Takes the top 3 coincidences.
    ) 
    
    print("🎯 Options found in your MarketFlow database:")
    print("-" * 65)
    for index, match in enumerate(matches): #matches are saves as [(prod1, score1), (prod2, score2), (prod3, score3)]
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
    print("-" * 65)
    
    return matches