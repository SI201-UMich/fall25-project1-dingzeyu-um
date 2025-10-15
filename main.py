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


profit_margins = calculate_profit_margins(data)


def calculate_discount_impact(data):
    """
    Calculate percentage of sales with discount > 0.2 by sub-category.
    Uses columns: Discount, Sales, Quantity, Sub-Category

    Parameters:
        data (list): List of dictionaries containing sales data

    Returns:
        dict: Dictionary with structure {Sub-Category: discount_percentage}
    """
    subcategory_stats = {}

    for row in data:
        subcategory = row["Sub-Category"]
        discount = row["Discount"]

        if subcategory not in subcategory_stats:
            subcategory_stats[subcategory] = {
                "total_count": 0,
                "high_discount_count": 0,
            }

        subcategory_stats[subcategory]["total_count"] += 1

        # Count transactions with discount > 0.2
        if discount > 0.2:
            subcategory_stats[subcategory]["high_discount_count"] += 1

    discount_impact = {}
    for subcategory in subcategory_stats:
        total = subcategory_stats[subcategory]["total_count"]
        high_discount = subcategory_stats[subcategory]["high_discount_count"]

        if total > 0:
            percentage = (high_discount / total) * 100
        else:
            percentage = 0

        discount_impact[subcategory] = round(percentage, 2)

    return discount_impact


discount_impact = calculate_discount_impact(data)


def write_results_to_file(profit_margins, discount_impact, output_filename):
    """
    Write analysis results to a text file.

    Parameters:
        profit_margins (dict): Profit margin results
        discount_impact (dict): Discount impact results
        output_filename (str): Name of output file

    Returns:
        None
    """
    with open(output_filename, "w") as file:
        file.write("=" * 80 + "\n")
        file.write("SUPERSTORE DATA ANALYSIS RESULTS\n")
        file.write("=" * 80 + "\n\n")

        # Write Profit Margins
        file.write("1. AVERAGE PROFIT MARGIN BY CATEGORY AND REGION\n")
        file.write("-" * 80 + "\n\n")

        for category in sorted(profit_margins.keys()):
            file.write(f"Category: {category}\n")
            for region in sorted(profit_margins[category].keys()):
                margin = profit_margins[category][region]
                file.write(f"  {region}: {margin}%\n")
            file.write("\n")

        # Write Discount Impact
        file.write("\n" + "=" * 80 + "\n")
        file.write("2. PERCENTAGE OF SALES WITH HIGH DISCOUNT (>20%) BY SUB-CATEGORY\n")
        file.write("-" * 80 + "\n\n")

        for subcategory in sorted(discount_impact.keys()):
            percentage = discount_impact[subcategory]
            file.write(f"{subcategory}: {percentage}%\n")

        file.write("\n" + "=" * 80 + "\n")


write_results_to_file(profit_margins, discount_impact, "123")
