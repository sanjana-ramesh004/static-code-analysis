"""
Inventory Management System

This module provides basic CRUD operations for managing inventory
stock data. Functions include adding/removing items, checking
quantities, and data persistence.
"""
import json
from datetime import datetime


stock_data = {}


def add_item(item="default", qty=0, logs=None):
    """
    Add an item to inventory with specified quantity.

    Args:
        item (str): Name of the item to add
        qty (int): Quantity to add (must be non-negative)
        logs (list, optional): List to append log entries to

    Returns:
        bool: True if successful, False otherwise
    """
    if logs is None:
        logs = []

    # Input validation
    if not item or not isinstance(item, str):
        print(
            f"Error: Invalid item name '{item}'. "
            "Must be a non-empty string."
        )
        return False

    if not isinstance(qty, int) or qty < 0:
        print(
            f"Error: Quantity must be a non-negative integer, "
            f"got '{qty}'"
        )
        return False

    stock_data[item] = stock_data.get(item, 0) + qty
    log_entry = f"{datetime.now()}: Added {qty} of {item}"
    logs.append(log_entry)
    return True


def remove_item(item, qty):
    """
    Remove specified quantity of an item from inventory.

    Args:
        item (str): Name of the item to remove
        qty (int): Quantity to remove

    Returns:
        bool: True if successful, False if item not found
    """
    try:
        if item not in stock_data:
            print(f"Error: Item '{item}' not found in inventory")
            return False

        stock_data[item] -= qty
        if stock_data[item] <= 0:
            del stock_data[item]
        return True
    except KeyError:
        print(f"Error: Item '{item}' does not exist in inventory")
        return False


def get_qty(item):
    """
    Get the current quantity of an item in inventory.

    Args:
        item (str): Name of the item to query

    Returns:
        int: Current quantity (returns 0 if item not found)
    """
    return stock_data.get(item, 0)


def load_data(file="inventory.json"):
    """
    Load inventory data from a JSON file.

    Args:
        file (str): Path to the JSON file to load from

    Returns:
        dict: The loaded stock data
    """
    try:
        with open(file, "r", encoding="utf-8") as f:
            loaded_data = json.load(f)
            stock_data.update(loaded_data)
            return stock_data
    except FileNotFoundError:
        print(
            f"Warning: File '{file}' not found. "
            "Starting with empty inventory."
        )
        return stock_data
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON format in '{file}'")
        return stock_data


def save_data(file="inventory.json"):
    """
    Save current inventory data to a JSON file.

    Args:
        file (str): Path to the JSON file to save to

    Returns:
        bool: True if save successful, False otherwise
    """
    try:
        with open(file, "w", encoding="utf-8") as f:
            json.dump(stock_data, f, indent=2)
        return True
    except IOError as e:
        print(f"Error: Unable to save data - {e}")
        return False


def print_data():
    """Print a formatted report of all items in inventory."""
    print("Items Report")
    print("-" * 40)
    if not stock_data:
        print("Inventory is empty")
    else:
        for item_name, quantity in stock_data.items():
            print(f"{item_name} -> {quantity}")


def check_low_items(threshold=5):
    """
    Find items with quantity below a specified threshold.

    Args:
        threshold (int): Minimum quantity threshold (default: 5)

    Returns:
        list: Names of items below the threshold
    """
    result = []
    for item_name, quantity in stock_data.items():
        if quantity < threshold:
            result.append(item_name)
    return result


def main():
    """Main execution function demonstrating inventory operations."""
    # Valid operations
    add_item("apple", 10)
    add_item("orange", 7)

    # These will be caught by validation and handled gracefully
    add_item("banana", -2)  # Invalid: negative quantity
    add_item(123, "ten")     # Invalid: wrong types

    # Remove operations
    remove_item("apple", 3)
    remove_item("grape", 1)  # Item doesn't exist

    # Query operations
    apple_qty = get_qty("apple")
    print(f"Apple stock: {apple_qty}")

    low_items = check_low_items()
    if low_items:
        print(f"Low stock items: {low_items}")

    # File operations
    save_data()
    load_data()
    print_data()


if __name__ == "__main__":
    main()
