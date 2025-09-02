import json
import os
class InventoryManager:
    def __init__(self, json_file=".\Project\InventoryManagement\category.json"):
        self.json_file = json_file
        self.user = ""
        self.data = self.load_data()

    def load_data(self):
        if os.path.exists(self.json_file):
            try:
                with open(self.json_file, 'r') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                print("JSON Could not be read")
                exit()
        else:
            print("404 File not found")
            exit()
    
    def save_data(self):
        try:
            with open(self.json_file, 'w') as f:
                json.dump(self.data, f, indent=4)
            return True
        except Exception as e:
            print(f"Data is not saved due to {e}")
            return False
        
    def get_user(self):
        while True:
            name = input("Enter your name: ").strip()
            if name:
                self.user = name
                print(f"Welcome, {name}!")
                break
            else:
                print("Please enter a valid name")

    def display_categories(self):
        print("\nInventory Management System")
        print('='*50)
        categories = list(self.data["categories"].keys())

        for i, category in enumerate(categories, 1):
            print(f"{i}. {category}")
        
        return categories
    
    def display_items(self, category):
        print(f"\nItems in {category.upper()}")
        print('='*50)
        items = list(self.data["categories"][category].keys())

        for i, item in enumerate(items, 1):
            item_data = self.data["categories"][category][item]
            print(f"{i}. {item} - Qty: {item_data['quantity']} - Price: Rs{item_data['price']:.2f}")
        return items

    def remove_item(self, category, item, quantity):
        current_qty = self.data["categories"][category][item]["quantity"]
        if quantity > current_qty:
            print(f"Error: Cannot remove {quantity} items. Only {current_qty} available.")
            return False

        self.data["categories"][category][item]["quantity"] -= quantity
        transaction = {
            "user": self.user,
            "action": "removed",
            "category": category,
            "item": item,
            "quantity": quantity,
            "remaining_quantity": self.data["categories"][category][item]["quantity"],
            "Price": self.data["categories"][category][item]["price"],
            "total_value": quantity * self.data["categories"][category][item]["price"]
        }        
        self.data["transactions"].append(transaction)

        if self.save_data():
            print(f"Successfully removed {quantity} {item}(s). Remaining: {self.data['categories'][category][item]['quantity']}")
            return True
        else:
            print("Error saving changes.")
            return False
        
    def gen_report(self):
        while True:
            print("\n" + "="*50)
            print("REPORTS MENU")
            print("="*50)
            print("1. Current Stock Levels")
            print("2. Recent Transactions")
            print("3. Low Stock Items")
            print("4. Total Inventory Value")
            print("5. Back to Main Menu")
            
            choice = input("\nSelect report type (1-5): ").strip()
            
            if choice == "1":
                self.show_current_stock()
            elif choice == "2":
                self.show_recent_txn()
            elif choice == "3":
                self.show_low_stock_items()
            elif choice == "4":
                self.show_total_inventory_value()
            elif choice == "5":
                break
            else:
                print("Invalid choice. Please select 1-5.")
    
    def show_current_stock(self):
        print("\n"+"="*60)
        print("Current Stock Levels")
        print("="*60)

        for category, items in self.data["categories"].items():
            print(f"\n{category}:")
            print("-" * len(category))
            for item, data in items.items():
                print(f"  {item:<20} Qty: {data['quantity']:<5} Price: ${data['price']:.2f}")

    def show_recent_txn(self):
        print("Recent Transactions")
        print("="*50)
        if not self.data["transactions"]:
            print("No transactions recorded")
            return
    
        recent = self.data["transactions"][-10:]
        for transaction in reversed(recent):
            print(f"User: {transaction['user']}")
            print(f"Action: {transaction['action'].title()} {transaction['quantity']} {transaction['item']}(s)")
            print(f"Category: {transaction['category']}")
            print(f"Value: ${transaction['total_value']:.2f}")
            print(f"Remaining Stock: {transaction['remaining_quantity']}")
            print("-" * 40)
    
    def show_low_stock_items(self):
        print("\n" + "="*60)
        print("LOW STOCK ITEMS")
        print("="*60)
        
        threshold = self.data["low_stock_threshold"]
        low_stock_found = False
        
        for category, items in self.data["categories"].items():
            category_has_low_stock = False
            for item, data in items.items():
                if data["quantity"] <= threshold:
                    if not category_has_low_stock:
                        print(f"\n{category}:")
                        print("-" * len(category))
                        category_has_low_stock = True
                    print(f"  {item:<20} Qty: {data['quantity']:<5} (Threshold: {threshold})")
                    low_stock_found = True
        
        if not low_stock_found:
            print("No items below low stock threshold!")
    
    def show_total_inventory_value(self):
        print("\n" + "="*60)
        print("TOTAL INVENTORY VALUE")
        print("="*60)
        
        category_totals = {}
        grand_total = 0
        
        for category, items in self.data["categories"].items():
            category_total = 0
            print(f"\n{category}:")
            print("-" * len(category))
            
            for item, data in items.items():
                item_total = data["quantity"] * data["price"]
                category_total += item_total
                print(f"  {item:<20} {data['quantity']} × ${data['price']:.2f} = ${item_total:.2f}")
            
            category_totals[category] = category_total
            grand_total += category_total
            print(f"  {category} Total: ${category_total:.2f}")
        
        print("\n" + "="*40)
        print(f"GRAND TOTAL: ${grand_total:.2f}")
        print("="*40)
    
    def run(self):
        """Main program loop"""
        print("="*50)
        print("INVENTORY MANAGEMENT SYSTEM")
        print("="*50)
        
        self.get_user()
        
        while True:
            print("\n" + "="*50)
            print("MAIN MENU")
            print("="*50)
            print("1. Buy Items")
            print("2. Generate Reports")
            print("3. Exit")
            
            main_choice = input("\nSelect option (1-3): ").strip()
            
            if main_choice == "1":
                categories = self.display_categories()
                
                try:
                    cat_choice = int(input(f"\nSelect category (1-{len(categories)}): ")) - 1
                    if 0 <= cat_choice < len(categories):
                        selected_category = categories[cat_choice]
                        
                        items = self.display_items(selected_category)
                        
                        try:
                            item_choice = int(input(f"\nSelect item (1-{len(items)}): ")) - 1
                            if 0 <= item_choice < len(items):
                                selected_item = items[item_choice]
                                
                                current_qty = self.data["categories"][selected_category][selected_item]["quantity"]
                                print(f"\nCurrent quantity of {selected_item}: {current_qty}")
                                
                                try:
                                    qty_to_remove = int(input("Enter quantity to remove: "))
                                    if qty_to_remove > 0:
                                        self.remove_item(selected_category, selected_item, qty_to_remove)
                                    else:
                                        print("Quantity must be greater than 0.")
                                except ValueError:
                                    print("Invalid quantity. Please enter a number.")
                            else:
                                print("Invalid item selection.")
                        except ValueError:
                            print("Invalid input. Please enter a number.")
                    else:
                        print("Invalid category selection.")
                except ValueError:
                    print("Invalid input. Please enter a number.")
            
            elif main_choice == "2":
                self.gen_report()
            
            elif main_choice == "3":
                print(f"\nThank you for using the Inventory Management System, {self.user}!")
                break
            
            else:
                print("Invalid choice. Please select 1-3.")

def main():
    try:
        inventory = InventoryManager()
        inventory.run()
    except KeyboardInterrupt:
        print("\n\nProgram interrupted by user.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()        