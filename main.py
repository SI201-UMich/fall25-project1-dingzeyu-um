"""
Project 1: Data Analysis
Name: Dingze Yu
Student ID: 94942535
Email: dingzeyu@umich.edu
Collaborators: Used Claude (GenAI) for code structure and implementation assistance
"""

import csv
import unittest


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


class Tests(unittest.TestCase):

    def test_calculate_profit_margins(self):
        """Test cases for calculate_profit_margins function."""

        print("Testing calculate_profit_margins()...")

        # Test Case 1: General case with positive profits
        test_data_1 = [
            {"Category": "Technology", "Region": "West", "Sales": 1000, "Profit": 200},
            {"Category": "Technology", "Region": "West", "Sales": 500, "Profit": 100},
        ]
        result_1 = calculate_profit_margins(test_data_1)
        expected_1 = {"Technology": {"West": 20.0}}
        self.assertEqual(result_1, expected_1)
        print("✓ Test 1 Passed: General case with positive profits")

        # Test Case 2: General case with multiple categories and regions
        test_data_2 = [
            {"Category": "Furniture", "Region": "East", "Sales": 2000, "Profit": 400},
            {"Category": "Technology", "Region": "West", "Sales": 1000, "Profit": 150},
        ]
        result_2 = calculate_profit_margins(test_data_2)
        expected_2 = {"Furniture": {"East": 20.0}, "Technology": {"West": 15.0}}
        self.assertEqual(result_2, expected_2)
        print("✓ Test 2 Passed: Multiple categories and regions")

        # Test Case 3: Edge case with zero sales
        test_data_3 = [
            {"Category": "Office", "Region": "South", "Sales": 0, "Profit": 0}
        ]
        result_3 = calculate_profit_margins(test_data_3)
        expected_3 = {"Office": {"South": 0}}
        self.assertEqual(result_3, expected_3)
        print("✓ Test 3 Passed: Edge case with zero sales")

        # Test Case 4: Edge case with negative profit (loss)
        test_data_4 = [
            {
                "Category": "Furniture",
                "Region": "Central",
                "Sales": 1000,
                "Profit": -100,
            }
        ]
        result_4 = calculate_profit_margins(test_data_4)
        expected_4 = {"Furniture": {"Central": -10.0}}
        self.assertEqual(result_4, expected_4)
        print("✓ Test 4 Passed: Edge case with negative profit")

        print("All profit margin tests passed!\n")

    def test_calculate_discount_impact(self):
        """Test cases for calculate_discount_impact function."""

        print("Testing calculate_discount_impact()...")

        # Test Case 1: General case with some high discounts
        test_data_1 = [
            {"Sub-Category": "Phones", "Discount": 0.3, "Sales": 100, "Quantity": 1},
            {"Sub-Category": "Phones", "Discount": 0.1, "Sales": 150, "Quantity": 1},
            {"Sub-Category": "Phones", "Discount": 0.25, "Sales": 200, "Quantity": 1},
            {"Sub-Category": "Phones", "Discount": 0.0, "Sales": 120, "Quantity": 1},
        ]
        result_1 = calculate_discount_impact(test_data_1)
        expected_1 = {"Phones": 50.0}  # 2 out of 4 have discount > 0.2
        self.assertEqual(result_1, expected_1)
        print("✓ Test 1 Passed: General case with mixed discounts")

        # Test Case 2: General case with multiple sub-categories
        test_data_2 = [
            {"Sub-Category": "Chairs", "Discount": 0.4, "Sales": 300, "Quantity": 2},
            {"Sub-Category": "Chairs", "Discount": 0.1, "Sales": 200, "Quantity": 1},
            {"Sub-Category": "Tables", "Discount": 0.3, "Sales": 500, "Quantity": 1},
        ]
        result_2 = calculate_discount_impact(test_data_2)
        expected_2 = {"Chairs": 50.0, "Tables": 100.0}
        self.assertEqual(result_2, expected_2)
        print("✓ Test 2 Passed: Multiple sub-categories")

        # Test Case 3: Edge case with no high discounts
        test_data_3 = [
            {"Sub-Category": "Paper", "Discount": 0.1, "Sales": 50, "Quantity": 5},
            {"Sub-Category": "Paper", "Discount": 0.0, "Sales": 40, "Quantity": 4},
            {"Sub-Category": "Paper", "Discount": 0.15, "Sales": 60, "Quantity": 6},
        ]
        result_3 = calculate_discount_impact(test_data_3)
        expected_3 = {"Paper": 0.0}
        self.assertEqual(result_3, expected_3)
        print("✓ Test 3 Passed: Edge case with no high discounts")

        # Test Case 4: Edge case with all high discounts
        test_data_4 = [
            {"Sub-Category": "Binders", "Discount": 0.5, "Sales": 100, "Quantity": 2},
            {"Sub-Category": "Binders", "Discount": 0.3, "Sales": 150, "Quantity": 3},
        ]
        result_4 = calculate_discount_impact(test_data_4)
        expected_4 = {"Binders": 100.0}
        self.assertEqual(result_4, expected_4)
        print("✓ Test 4 Passed: Edge case with all high discounts")

        print("All discount impact tests passed!\n")


def main():
    """Main function to perform the data analysis."""

    csv_filename = "SampleSuperstore.csv"
    data = read_csv_to_dict(csv_filename)

    profit_margins = calculate_profit_margins(data)

    discount_impact = calculate_discount_impact(data)

    print("Writing results to file...")
    output_filename = "analysis_results.txt"
    write_results_to_file(profit_margins, discount_impact, output_filename)

    print(f"Results written to '{output_filename}'")
    print(f"  - Analyzed {len(profit_margins)} categories across regions")
    print(f"  - Analyzed discount patterns for {len(discount_impact)} sub-categories")


if __name__ == "__main__":
    # unittest.main()
    main()
