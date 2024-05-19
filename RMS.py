from collections import deque, Counter

tables = {
    table_number: {
        "status": "free",
        "orders": [],
        "bill": 0,
        "tip": 0,
        "payment_method": "" 
    }
    for table_number in range(1, 6)  
}

order_queue = deque()
priority_order_queue = deque()
menu = { 
    "House Cured Bourbon Gravadlax": 9.99,
    "Bloc de Pate": 14.99,
    "Roasted Peppers": 7.99,
    "Cornish Crab": 14.99,
    "Goats Cheese": 9.99,
    "Fillet Mignon": 45.99,
    "Truffle Gnocchi": 49.99,
    "Salmon": 49.99,
    "Lamb Shank": 24.99,
    "Cassoulet": 24.99,
    "Spaghetti": 29.99,
    "Lobster Thermidor": 59.99,
    "Steak Diane": 54.99,
    "Chocolate Nemesis": 8.99,
    "Apple Tart Tatin": 7.99,
    "Bread & Butter Pudding": 7.99,
    "Eton Mess": 8.99,
    "Affogato": 8.99,
    "Cheese Board": 5.99
}

order_summary = Counter() 

def display_table_availability():
    for table_number, data in tables.items():
        print(f"Table {table_number}: {data['status']}")

def is_table_free(table_number):
    return tables[table_number]["status"] == "free"

def book_table(table_number):
    if is_table_free(table_number):
        tables[table_number]["status"] = "occupied"
        print(f"Table {table_number} booked successfully!")
    else:
        print(f"Sorry, table {table_number} is already occupied.")

def free_table(table_number):
    if not is_table_free(table_number):
        tables[table_number]["status"] = "free"
        tables[table_number]["orders"] = []
        tables[table_number]["bill"] = 0
        tables[table_number]["tip"] = 0
        print(f"Table {table_number} is now free.")
    else:
        print(f"Table {table_number} is already free.")

def take_order(table_number, items):
    if not is_table_free(table_number):
        for item in items:
            if item in menu:
                tables[table_number]["orders"].append(item)
                if item in ["Lobster Thermidor", "Steak Diane"]:
                    priority_order_queue.appendleft((table_number, item)) 
                else:
                    order_queue.append((table_number, item)) 
                print(f"{item} added to the order for table {table_number}.")
            else:
                print(f"Sorry, '{item}' is not on our menu.")
    else:
        print(f"Table {table_number} is not occupied.")

def process_order():
    if priority_order_queue:
        table_number, item = priority_order_queue.popleft()
    elif order_queue:
        table_number, item = order_queue.popleft()
    else:
        print("No orders in queue.")
        return

    print(f"\nProcessing order for table {table_number}: {item}")
    print(f"{item} is ready for table {table_number}!")

def calculate_bill(table_number):
    if not is_table_free(table_number):
        subtotal = sum(menu[item] for item in tables[table_number]["orders"])
        if tables[table_number]["payment_method"] == "card":
            subtotal *= 1.10  
        tables[table_number]["bill"] = subtotal
        return subtotal
    else:
        print(f"Table {table_number} is not occupied.")
        return 0


def close_table(table_number):
    if not is_table_free(table_number):
        bill = calculate_bill(table_number)
        print(f"\nBill for Table {table_number}: £{bill:.2f}")

        while True:
            try:
                tip = float(input("Enter tip amount (0 for no tip): "))
                if tip >= 0:  
                    break
                else:
                    print("Tip cannot be negative. Please enter a valid amount.")
            except ValueError:
                print("Invalid input. Please enter a number.")

        bill += tip
        tables[table_number]["tip"] = tip
        print(f"Final bill: £{bill:.2f}")
        print("Thank you for dining with us!")
        free_table(table_number)  
    else:
        print(f"Table {table_number} is not occupied.")

def generate_evening_report():
    total_income = sum(tables[table]["bill"] for table in tables)
    highest_spending_table = max(tables, key=lambda k: tables[k]["bill"])
    most_popular_items = order_summary.most_common(3)  
    total_tips = sum(tables[table]["tip"] for table in tables)

    print("\n--- Evening Report ---")
    print(f"Total Income: £{total_income:.2f}")
    print(f"Highest Spending Table: {highest_spending_table} (£{tables[highest_spending_table]['bill']:.2f})")
    print("Most Popular Items:")
    for item, count in most_popular_items:
        print(f"  - {item}: {count} orders")
    print(f"Total Tips: £{total_tips:.2f}")

# --- Main Program Loop ---
while True:
    print("\n--- Welcome to Luccio Carlo's Restaurant ---")
    print("1. Check Table Availability")
    print("2. Book Table")
    print("3. Free Table")
    print("4. Take Order")
    print("5. Process Order")
    print("6. Close Table")
    print("7. Generate Evening Report")
    print("8. Exit")

    choice = input("Enter your choice: ")

    if choice == '1':
        display_table_availability() 
    elif choice == '2':
        table_number = int(input("Enter table number to book: "))
        book_table(table_number)
    elif choice == '3':
        table_number = int(input("Enter table number to free: "))
        free_table(table_number)
    elif choice == '4':
        table_number = int(input("Enter table number: "))
        if not is_table_free(table_number):
            print("\n--- Menu ---")
            for item, price in menu.items():
                print(f"{item}: £{price:.2f}")
            order = input("\nEnter order (comma-separated items): ")
            items = [item.strip() for item in order.split(",")]
            take_order(table_number, items)
        else:
            print(f"Table {table_number} is not occupied.")
    elif choice == '5':
        process_order()
    elif choice == '6':
        table_number = int(input("Enter table number to close: "))
        while True:
            payment_method = input("Payment method (cash or card): ").lower()
            if payment_method in ["cash", "card"]:
                tables[table_number]["payment_method"] = payment_method
                break
            else:
                print("Invalid payment method. Please enter 'cash' or 'card'.")        
        close_table(table_number)  
    elif choice == '7':
        generate_evening_report()
    elif choice == '8':
        print("Exiting...")
        break
    else:
        print("Invalid choice. Please try again.")
