import sqlite3
import os
from datetime import datetime

DB_NAME = "marketflow.db"
SCHEMA_FILE = "marketflow.sql"

def connect_db():
    conn = None
    try:
        conn = sqlite3.connect(DB_NAME)
        conn.execute("PRAGMA foreign_keys = ON;")
        return conn
    except sqlite3.Error as e:
        print(f"Error connecting to database: {e}")
        return conn


def initialize_sys():
    conn = connect_db()
    if conn is None:
        return
        
    try:
        #Verify database file exists
        if not os.path.exists(SCHEMA_FILE):
            print(f"Warning: Schema file '{SCHEMA_FILE}' not found. Cannot initialize tables.")
            return
            
        with open(SCHEMA_FILE, 'r', encoding='utf-8') as file:
            sql_script = file.read()
            
        conn.executescript(sql_script)
        conn.commit()
        
    except sqlite3.Error as e:
        print(f"Database error during initialization: {e}")
    finally:
        if conn:
            conn.close()


def get_marketflow_products():
    conn = connect_db()
    if conn is None:
        print("Could not connect to the database.")
        return []
        
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT DISTINCT product_name FROM price_history;") #Avoid repeated names
        
        products = [row[0] for row in cursor.fetchall()]
        return products
        
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return []
    finally:
        if conn:
            conn.close()
            
            
def save_price_record(product_name, price, source):
    #Saves the captured price in the price_history table
    conn = connect_db()
    if conn is None:
        print("❌ Error: Could not connect to the database.")
        return
    
    try:
        cursor = conn.cursor()
        #Getting id_source
        cursor.execute('SELECT id_source FROM price_sources WHERE source_name = ?', (source,))
        id_source = cursor.fetchone()[0]
        #Getting variants
        cursor.execute("SELECT DISTINCT variant FROM price_history WHERE product_name = ?", (product_name,))
        available_variants = cursor.fetchall()
        
        if available_variants:
            print(f"\nFound variants for '{product_name}':")
            print("-" * 65)
            for index, var in enumerate(available_variants):
                variant_name = var[0]
                print(f"{index + 1}. {variant_name:<20}")
            print("0. ➕ Add as a new product\n")
            print("-" * 65)
            choice = input(f"\nChoose variant option to save as (1-{len(available_variants)}) or (0) to add new: ")
            
            if choice.isdigit() and 1 <= int(choice) <= len(available_variants):
                choosen_variant = available_variants[int(choice) - 1][0]
            elif choice == '0':
                choosen_variant = input("Write variant for the product: ")
            else:
                print("Invalid option")
                return
        else:
            print(f"Registering new product '{product_name}'.")
            choosen_variant = input("Write variant or left blank for 'Unique': ")
            if choosen_variant == '': choosen_variant = 'Unique'
            
            
        #Inserting into the TABLE
        query = '''
            INSERT INTO price_history (product_name, variant, recorded_price, id_source, record_date)
            VALUES (?, ?, ?, ?, ?)
        '''
        cursor.execute(query, (product_name, choosen_variant, price, id_source, datetime.now().strftime("%d/%m/%Y")))
        conn.commit()
        print(f"\n✅ Price S/{price} saved for '{product_name} | {choosen_variant}' (Source: {source})")
    except sqlite3.Error as e:
        print(f"❌ Error saving to database: {e}")
    finally:
        conn.close()
        
