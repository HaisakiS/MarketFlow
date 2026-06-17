import sqlite3
from database import connect_db, initialize_sys
import csv
import os
import sys

def populate_real_data():
    initialize_sys() #Create Tables if don't exist already
    
    conn = connect_db()
    if conn is None:
        print("Could not connect to the database.")
        return
    
    csv_filename = "product_list.csv"
    if not os.path.exists(csv_filename):
        print(f"Error: The file '{csv_filename}' was not found in the current folder.")
        sys.exit(1)  
    
    try:
        cursor = conn.cursor()
        
        #Deleting old data to avoid duplicates
        print("Wiping old data...")
        cursor.execute("DELETE FROM price_history;")
        cursor.execute("DELETE FROM price_sources;")
        
        #Reseting the sqlite sequence to 0
        cursor.execute("DELETE FROM sqlite_sequence WHERE name='price_history';")
        cursor.execute("DELETE FROM sqlite_sequence WHERE name='price_sources';")
        
        #Inserting Data
        print("Inserting price sources...")
        source_list = [
            ('Aliexpress', 'Supplier'),       # ID 1
            ('Ebay', 'Supplier'),       # ID 2
            ('Facebook', 'Competition'), # ID 3
            ('Amazon', 'Supplier') # ID 4
        ]
        cursor.executemany("""INSERT INTO price_sources (source_name, type) 
                              VALUES (?, ?);""", source_list)
        
        #Obtaining IDs
        cursor.execute("SELECT source_name, id_source FROM price_sources;")
        source_mapping = dict(cursor.fetchall())
        
        #Populate with data from the .csv file
        print(f"Reading '{csv_filename}' and populating history...")
        
        price_list = []
        with open(csv_filename, mode='r', encoding='utf-8') as file:
            csv_reader = csv.DictReader(file) #Read colums title
            
            for row in csv_reader:
                current_source = row['source_name']
                
                if current_source in source_mapping:
                    id_source = source_mapping[current_source]
                else:
                    print(f"Error: Source '{current_source}' doesn't exist in database.")
                    sys.exit(1)
                
                # Saving data from each colum of the current row
                record = (
                    row['product_name'], 
                    row['variant'], 
                    float(row['recorded_price']),
                    row['record_date'], 
                    id_source
                )
                price_list.append(record) #adding to the list
        
        cursor.executemany("""INSERT INTO price_history 
                              (product_name, variant, recorded_price, record_date, id_source) 
                              VALUES (?, ?, ?, ?, ?);""", price_list)

        conn.commit()
        print(f"\nSuccess! {len(price_list)} historical records have been added to the database.")
        
    except sqlite3.Error as e:
            print(f"Database error: {e}")
    except Exception as e:
        print(f"An error occurred while processing the CSV: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    populate_real_data()