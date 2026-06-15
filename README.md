# 📈 MarketFlow v1.0

A modular price tracking and market analysis system built with Python and SQLite3. Designed to capture historical prices from web sources via hybrid scraping, intelligently match products using fuzzy matching, and visualize interactive market trends.

## 🚀 Key Features

* **Optimized Web Scraping:** Uses `requests` and `BeautifulSoup4` to quickly extract the item title from URLs, bypassing anti-bot blocks without needing to download the entire website.
* **Smart Product Matching (Fuzzy Matching):** Implements the `thefuzz` library to map noisy and messy web titles directly to clean catalog names in the database, ignoring extra words or their order.
* **Visual Trend Analysis:** Transforms raw SQLite data into interactive line charts using `pandas` and `matplotlib`. Allows visualizing and comparing historical price evolution, filtering by suppliers, competitors, and product variants.

## 🛠️ Tech Stack

* **Language:** Python 3.x
* **Database Engine:** SQLite 3 (Relational structure)
* **Web Scraping:** `requests`, `beautifulsoup4`
* **Natural Language Processing / Matching:** `thefuzz` (Levenshtein Distance)
* **Data Science & Visualization:** `pandas`, `matplotlib`

## 📐 Database Design & Relational Schema

The database architecture is optimized to record history as a ledger, maintaining integrity through `FOREIGN KEY` constraints:

1. **`price_sources`:** Master table that classifies where prices come from using the `type` field (e.g., `Supplier`, `Competition`, `Internal`). Prevents data redundancy.
2. **`price_history`:** The core of the system. Records every price fluctuation associated with a `product_name`, its specific `variant`, the exact date (`record_date`), and its source (`id_source`).

## 📂 Project Structure

* `main.py` - Program launcher and main loop.
* `menu.py` - Command Line Interface (CLI) controller and input validation.
* `database.py` - SQLite connection manager, raw queries, and initialization system (Fail-Safe).
* `scraper.py` - URL cleaning engine, HTML extraction, and Fuzzy Match algorithm.
* `analytics.py` - DataFrames processor (Pandas) and chart generator (Matplotlib).
* `populate_db.py` - Script for mass data loading (Bulk Insert) from `.csv` files to simulate histories.
* `marketflow.sql` - Schema file containing table declarations and relational integrity.

## ⚙️ Installation & Usage

### 1. Requirements & Dependencies
Ensure you have Python 3.x installed. Then, install the required libraries by running the following command in your terminal:
```bash
pip install requests beautifulsoup4 thefuzz[speedup] pandas matplotlib
```

### 2. Automatic Initialization
There is no need to manually configure the database. Simply run the main program and the system will create `marketflow.db` with its respective tables if it detects a fresh environment.

### 3. Launch the Application
```bash
python main.py
```

## 📊 Functionality Preview
The system operates through an interactive Menu:
```bash
======================================
        MarketFlow SYSTEM v1.0        
======================================
1. 🌐 Capture Price from URL
2. 📈 Analyze Trends (Chart)
3. 📋 View Product Catalog
4. ❌ Exit
======================================
Choose an option (1-4): 4
```
