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
        #Inserting into the TABLE
        query = '''
            INSERT INTO price_history (product_name, recorded_price, id_source, record_date)
            VALUES (?, ?, ?, ?)
        '''
        cursor.execute(query, (product_name, price, id_source, datetime.now().strftime("%d/%m/%Y")))
        conn.commit()
        print(f"✅ Price S/{price} saved for '{product_name}' (Source: {source})")
    except sqlite3.Error as e:
        print(f"❌ Error saving to database: {e}")
    finally:
        conn.close()
        
