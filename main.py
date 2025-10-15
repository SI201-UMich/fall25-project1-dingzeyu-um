"""
Project 1: Data Analysis
Name: Dingze Yu
Student ID: 94942535
Email: dingzeyu@umich.edu
Collaborators: Used Claude (GenAI) for code structure and implementation assistance
"""

import csv


def read_csv_to_dict(filename):
    """
    Reads CSV file and converts to list of dictionaries.

    Parameters:
        filename (str): Path to the CSV file

    Returns:
        list: List of dictionaries where each dict represents a row
    """
    data = []

    with open(filename, "r") as file:
        csv_reader = csv.DictReader(file)

        for row in csv_reader:
            processed_row = {
                "Ship Mode": row["Ship Mode"],
                "Segment": row["Segment"],
                "Country": row["Country"],
                "City": row["City"],
                "State": row["State"],
                "Postal Code": int(row["Postal Code"]),
                "Region": row["Region"],
                "Category": row["Category"],
                "Sub-Category": row["Sub-Category"],
                "Sales": float(row["Sales"]),
                "Quantity": int(row["Quantity"]),
                "Discount": float(row["Discount"]),
                "Profit": float(row["Profit"]),
            }
            data.append(processed_row)

    return data

data = read_csv_to_dict("samplesuperstore.csv")

def calculate_profit_margins(data):
    """
    Calculate average profit margin by category and region.
    Uses columns: Category, Region, Sales, Profit

    Parameters:
        data (list): List of dictionaries containing sales data

    Returns:
        dict: Nested dictionary with structure {Category: {Region: profit_margin}}
    """
    aggregates = {}

    for row in data:
        category = row["Category"]
        region = row["Region"]
        sales = row["Sales"]
        profit = row["Profit"]

        if category not in aggregates:
            aggregates[category] = {}

        if region not in aggregates[category]:
            aggregates[category][region] = {"total_sales": 0, "total_profit": 0}

        aggregates[category][region]["total_sales"] += sales
        aggregates[category][region]["total_profit"] += profit

    profit_margins = {}
    for category in aggregates:
        profit_margins[category] = {}
        for region in aggregates[category]:
            total_sales = aggregates[category][region]["total_sales"]
            total_profit = aggregates[category][region]["total_profit"]

            if total_sales > 0:
                margin = (total_profit / total_sales) * 100
            else:
                margin = 0

            profit_margins[category][region] = round(margin, 4)

    return profit_margins

print(calculate_profit_margins(data))