import sys
from populate_db import populate_real_data
from menu import (
    print_menu, 
    handle_capture_price, 
    handle_view_analytics, 
    handle_view_catalog
)

def main():

    #Create Tables and popualte them (wipe before populate in case already had data)
    populate_real_data()
    
    while True:
        print_menu()
        choice = input("Choose an option (1-4): ").strip()

        if choice == '1':
            handle_capture_price()
        elif choice == '2':
            handle_view_analytics()
        elif choice == '3':
            handle_view_catalog()
        elif choice == '4':
            print("\nClosing MarketFlow... See you soon!")
            sys.exit(0)
        else:
            print("\nInvalid option. Please choose a number from 1 to 4.")

if __name__ == "__main__":
    main()