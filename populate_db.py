import sqlite3
from database import connect_db, initialize_sys

def populate_real_data():
    initialize_sys() #Create Tables if don't exist already
    
    conn = connect_db()
    if conn is None:
        print("Could not connect to the database.")
        return
        
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
            ('Temu', 'Supplier'),       # ID 1
            ('Ebay', 'Supplier'),       # ID 2
            ('Facebook', 'Competition') # ID 3
        ]
        cursor.executemany("""INSERT INTO price_sources (source_name, type) 
                              VALUES (?, ?);""", source_list)
        
        print("Populating historical data for charts...")
        price_list = [
            ('Gamesir Nova Lite 2', 'Blanco', 40.0, '15/01/2026', 1),
            ('Gamesir Nova Lite 2', 'Blanco', 42.5, '10/02/2026', 1),
            ('Gamesir Nova Lite 2', 'Blanco', 38.0, '05/03/2026', 1), 
            ('Gamesir Nova Lite 2', 'Blanco', 45.0, '12/04/2026', 1),
            ('Gamesir Nova Lite 2', 'Blanco', 48.0, '13/05/2026', 1),
            
            ('Gamesir Nova Lite 2', 'Blanco', 55.0, '20/01/2026', 3),
            ('Gamesir Nova Lite 2', 'Blanco', 52.0, '15/02/2026', 3),
            ('Gamesir Nova Lite 2', 'Blanco', 49.0, '10/03/2026', 3), 
            ('Gamesir Nova Lite 2', 'Blanco', 58.0, '18/04/2026', 3),
            ('Gamesir Nova Lite 2', 'Blanco', 60.0, '15/05/2026', 3),

            ('Flydigi Dunefox', 'Rosa', 60.0, '01/02/2026', 2),
            ('Flydigi Dunefox', 'Rosa', 65.0, '15/03/2026', 2),
            ('Flydigi Dunefox', 'Rosa', 63.0, '18/05/2026', 2),
            
            ('Flydigi Dunefox', 'Rosa', 80.0, '10/02/2026', 3),
            ('Flydigi Dunefox', 'Rosa', 78.0, '20/03/2026', 3),
            ('Flydigi Dunefox', 'Rosa', 75.0, '20/05/2026', 3),
            
            ('Gamesir X5 Lite', 'Negro', 40.0, '15/01/2026', 1),
            ('Gamesir X5 Lite', 'Negro', 42.5, '10/02/2026', 1),
            ('Gamesir X5 Lite', 'Negro', 38.0, '05/03/2026', 1), 
            ('Gamesir X5 Lite', 'Negro', 45.0, '12/04/2026', 1),
            ('Gamesir X5 Lite', 'Negro', 48.0, '13/05/2026', 1),
            
            ('Gamesir X5 Lite', 'Verde', 55.0, '20/01/2026', 1),
            ('Gamesir X5 Lite', 'Verde', 52.0, '15/02/2026', 1),
            ('Gamesir X5 Lite', 'Verde', 49.0, '10/03/2026', 1), 
            ('Gamesir X5 Lite', 'Verde', 58.0, '18/04/2026', 1),
            ('Gamesir X5 Lite', 'Verde', 60.0, '15/05/2026', 1),
        ]
        
        """[TO DO: Read data in .csv for larger lists]"""
        
        cursor.executemany("""INSERT INTO price_history 
                              (product_name, variant, recorded_price, record_date, id_source) 
                              VALUES (?, ?, ?, ?, ?);""", price_list)

        conn.commit()
        print("\nDatabase successfully wiped and re-populated.")
        
    except sqlite3.Error as e:
        print(f"Database error: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    populate_real_data()