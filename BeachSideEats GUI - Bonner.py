# Author : Sa'Cairo Bonner
# Class : ITN160
# Class Section : 601
# Date : 11/13/2024
# Assignment : Final Project: Beach Side Restaurant

import json
import os
from guizero import App, Text, TextBox, PushButton, Box, ListBox, Window, error


# Path to save JSON file
current_menu_file = "current_menu.json"

# Function to load existing data or create a new file
def load_data():
    # Debugging Purposes: Checking if file exists
    print("Checking for file:", current_menu_file)
    print("File exists:", os.path.exists(current_menu_file))

    if os.path.exists(current_menu_file):
        with open(current_menu_file, "r") as file:
            try:
                raw_data = json.load(file)
                # Transform JSON structure to match expected format
                return {
                    int(k): (v["item_name"], v["price"]) for k, v in raw_data.items()
                }
            except json.JSONDecodeError:
                error("JSON Error", "menu file was empty or incorrectly formatted. Using default menu.")
    else:
        error("JSON Error", "Menu file not found. Loading default menu...")
    # Fallback to default menu if file is missing or invalid for whatever reason
    return {
        1: ("Drink: Lemonade", 2.75),
        2: ("Drink: Iced Tea", 2.75),
        3: ("Drink: Water", 1.50),
        4: ("Drink: Pepsi", 2.85),
        5: ("Entrée: Fish Tacos", 7.50),
        6: ("Entrée: Grilled Chicken Sandwich", 10.00),
        7: ("Side: French Fries", 3.50),
        8: ("Side: Baby Shrimp", 4.25)
    }

def update_menu_listbox():
    menu_items = load_data()  # Load data from the JSON file
    print("Loaded menu items:", menu_items)
    if isinstance(menu_items, dict):  # Ensure the menu is a dictionary
        formatted_items = [
            f"{num}. {desc[0]} - ${desc[1]:.2f}" for num, desc in menu_items.items()
        ]
        current_menu_list.clear()  # Clear existing items in the ListBox
        for item in formatted_items:  # Add each formatted item one by one
            current_menu_list.append(item)
    else:
        print("Menu data is invalid or empty.")


''' ( 11/25/24 -- Dont need this!)
# Save menu to JSON file to persist changes
def save_menu(menu):
    with open(current_menu_file, "w") as file:
        json.dump(menu, file, indent=4)
    print("Menu saved successfully!")
'''


# Initialize menu
menu = load_data()
order = {}

def get_valid_input(prompt, valid_values=None, input_type=int):
    while True:
        try:
            user_input = input_type(input(prompt))
            if valid_values is not None and user_input not in valid_values:
                print("Invalid input. Please try again.")
            else:
                return user_input
        except ValueError:
            print(f"Invalid input. Please enter a valid {input_type.__name__}.")

# Function to add item to order
def add_to_order():
    print("Add to Order function called!")  # Debugging purposes
    try:
        item_num = int(item_box.value)
        quantity = int(quantity_box.value)
        if item_num in menu:
            order[item_num] = order.get(item_num, 0) + quantity
            display_order()
            item_box.clear()
            quantity_box.clear()
        else:
            item_box.clear()
            quantity_box.clear()
            error("Invalid Input", "Invalid item number. Please try again.")
    except ValueError:
        item_box.clear()
        quantity_box.clear()
        error("Invalid Input", "Enter valid numbers for item and quantity.")

# Function to display order in GUI
def display_order():
    print(f"Order: {order}")  # Debugging purposes: Prints the current 'order' dictionary to validate its contents
    order_list.clear()
    for item_num, quantity in order.items(): # Iterates through the 'order' dictionary (item number and quantity)
        item_name, price = menu[item_num] # Retrieves the item name and price from the 'menu' using the item number

        # Formats and appends the item name, quantity, and total cost to the GUI list
        order_list.append(f"{item_name} x{quantity} - ${price * quantity:.2f}")

# Function to calculate and display total
def calculate_total():
    if not order:
        error("Invalid Submission","Your order is empty. Please add items first.")
        return
    total = sum(menu[item_num][1] * quantity for item_num, quantity in order.items())
    total_text.value = f"Grand Total: ${total:.2f}"


# Function that creates a new window to display an itemized order list
# Alongside subtotals for each item and the grand total for the order.
# Triggered when the user chooses to exit the program, ensuring that they
# see a summary of their order before the application closes.
# -----------------------------------
# Note:
# - If the order is empty, the function prints a message and does not open the window.
# - The function ensures proper cleanup by destroying both the itemized window
#   and the main application upon exit.
# -----------------------------------
# Future Improvements (11/24/24):
# - Add styling to the text for better readability.
# - Save the itemized order summary to a file for record-keeping if needed.
def display_itemized_order_gui():
    if not order:
        print("No items in the order.")  # Fallback for debugging
        error("Invalid Submission","No items in the order. Please add items first.")
        return

    # New window to display the itemized order
    itemized_window = Window(app, title="Itemized Order", width=355, height=400, layout="grid")
    itemized_window.bg = "#8c4ec5"

    # Display the itemized order in the new window
    itemized_list = []
    grand_total = 0

    for item_num, quantity in order.items():
        item_name, price = menu[item_num]
        subtotal = price * quantity
        grand_total += subtotal
        itemized_list.append(f"{item_name} x{quantity} - ${subtotal:.2f}")

    itemized_list.append("---------------------")
    itemized_list.append(f"Grand Total: ${grand_total:.2f}")

    # Adds the itemized list to the new window
    Text(itemized_window, text="\n".join(itemized_list), grid=[0, 0])

    # close_and_exit function defined inside this function to ensure it is recognized within the scope of 'pushbutton'
    def close_and_exit():
        print("Exiting program...")
        itemized_window.destroy()  # Closes the itemized order window
        app.destroy()  # Closes the main app

    # Button to close the program after viewing the order
    PushButton(itemized_window, text="Exit Program", command=close_and_exit, grid=[0, 1])


# GUI Setup
app_width = 360
app_height = 650

app = App("BeachSide Eats", layout="grid", width=app_width, height=app_height, bg="#8c4ec5")

# Centering container
center_box = Box(app, layout="grid", grid=[1, 1], align="top")  # Use grid placement and padding to center

# Title
Text(center_box, "Welcome to BeachSide Eats!", grid=[0, 0], size=20)

# Display menu
Text(center_box, "Menu:", grid=[0, 1])
current_menu_list = ListBox(
    center_box,
    width=250,
    height=145,
    grid=[0, 2]
)

# Updates the ListBox with items from the JSON file
update_menu_listbox()

# Input for selecting item and quantity
Text(center_box, "Enter Item Number:", grid=[0, 3])
item_box = TextBox(center_box, grid=[0, 4])
Text(center_box, "Enter Quantity:", grid=[0, 5])
quantity_box = TextBox(center_box, grid=[0, 6])

# Add to order button
PushButton(center_box, text="Add to Order", command=add_to_order, grid=[0, 7])

# Section to display the order
Text(center_box, "Current Order:", grid=[0, 8])
order_list = ListBox(center_box, width=250, height=145, grid=[0, 9])


# Total display
total_text = Text(center_box, "", grid=[0, 10])

# Calculate total button
PushButton(center_box, text="Calculate Total", command=calculate_total, grid=[0, 11])

def show_order():
    # Open itemized order before exiting
    display_itemized_order_gui()

# Button to exit program (Update: Opens the Itemized order window when clicked.)
# (11/25/24) Changed text & command for button to "Show Order" to better reflect its actions within code base.
show_order_button = PushButton(app, text="Show Order", command=show_order, grid=[1, 11])

# padding around the center box for better centering
app.tk.geometry("")  # Adjust as needed for the display ratio to change

# Start the GUI
app.display()
