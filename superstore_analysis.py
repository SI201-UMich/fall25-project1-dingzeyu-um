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


def calculate_discount_impact(data):
    """
    Calculate percentage of items (by quantity) with discount > 0.2 by sub-category and segment.
    Uses columns: Discount, Quantity, Segment, Sub-Category

    Parameters:
        data (list): List of dictionaries containing sales data

    Returns:
        dict: Nested dictionary with structure {Sub-Category: {Segment: discount_percentage}}
    """
    subcategory_stats = {}

    for row in data:
        subcategory = row["Sub-Category"]
        discount = row["Discount"]
        quantity = row["Quantity"]
        segment = row["Segment"]

        if subcategory not in subcategory_stats:
            subcategory_stats[subcategory] = {}

        if segment not in subcategory_stats[subcategory]:
            subcategory_stats[subcategory][segment] = {
                "total_quantity": 0,
                "high_discount_quantity": 0,
            }

        # Accumulate total quantity
        subcategory_stats[subcategory][segment]["total_quantity"] += quantity

        # Accumulate quantity with discount > 0.2
        if discount > 0.2:
            subcategory_stats[subcategory][segment][
                "high_discount_quantity"
            ] += quantity

    discount_impact = {}
    for subcategory in subcategory_stats:
        discount_impact[subcategory] = {}
        for segment in subcategory_stats[subcategory]:
            total_qty = subcategory_stats[subcategory][segment]["total_quantity"]
            high_discount_qty = subcategory_stats[subcategory][segment][
                "high_discount_quantity"
            ]

            if total_qty > 0:
                percentage = (high_discount_qty / total_qty) * 100
            else:
                percentage = 0

            discount_impact[subcategory][segment] = round(percentage, 2)

    return discount_impact


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
        file.write("2. PERCENTAGE OF ITEMS (BY QUANTITY) WITH HIGH DISCOUNT (>20%)\n")
        file.write("   BY SUB-CATEGORY AND SEGMENT\n")
        file.write("-" * 80 + "\n\n")

        for subcategory in sorted(discount_impact.keys()):
            file.write(f"Sub-Category: {subcategory}\n")
            segment_data = discount_impact[subcategory]

            for segment in sorted(segment_data.keys()):
                percentage = segment_data[segment]
                file.write(f"  {segment}: {percentage}%\n")
            file.write("\n")

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
            {
                "Sub-Category": "Phones",
                "Discount": 0.3,
                "Quantity": 2,
                "Segment": "Consumer",
            },
            {
                "Sub-Category": "Phones",
                "Discount": 0.1,
                "Quantity": 1,
                "Segment": "Consumer",
            },
            {
                "Sub-Category": "Phones",
                "Discount": 0.25,
                "Quantity": 3,
                "Segment": "Consumer",
            },
            {
                "Sub-Category": "Phones",
                "Discount": 0.0,
                "Quantity": 4,
                "Segment": "Consumer",
            },
        ]
        result_1 = calculate_discount_impact(test_data_1)
        expected_1 = {"Phones": {"Consumer": 50.0}}  # (2+3)/(2+1+3+4) = 5/10 = 50%
        self.assertEqual(result_1, expected_1)
        print("✓ Test 1 Passed: General case with mixed discounts")

        # Test Case 2: General case with multiple sub-categories and segments
        test_data_2 = [
            {
                "Sub-Category": "Chairs",
                "Discount": 0.4,
                "Quantity": 5,
                "Segment": "Corporate",
            },
            {
                "Sub-Category": "Chairs",
                "Discount": 0.1,
                "Quantity": 5,
                "Segment": "Corporate",
            },
            {
                "Sub-Category": "Tables",
                "Discount": 0.3,
                "Quantity": 10,
                "Segment": "Home Office",
            },
        ]
        result_2 = calculate_discount_impact(test_data_2)
        expected_2 = {"Chairs": {"Corporate": 50.0}, "Tables": {"Home Office": 100.0}}
        self.assertEqual(result_2, expected_2)
        print("✓ Test 2 Passed: Multiple sub-categories and segments")

        # Test Case 3: Edge case with no high discounts
        test_data_3 = [
            {
                "Sub-Category": "Paper",
                "Discount": 0.1,
                "Quantity": 5,
                "Segment": "Consumer",
            },
            {
                "Sub-Category": "Paper",
                "Discount": 0.0,
                "Quantity": 3,
                "Segment": "Consumer",
            },
            {
                "Sub-Category": "Paper",
                "Discount": 0.15,
                "Quantity": 2,
                "Segment": "Consumer",
            },
        ]
        result_3 = calculate_discount_impact(test_data_3)
        expected_3 = {"Paper": {"Consumer": 0.0}}
        self.assertEqual(result_3, expected_3)
        print("✓ Test 3 Passed: Edge case with no high discounts")

        # Test Case 4: Edge case with all high discounts
        test_data_4 = [
            {
                "Sub-Category": "Binders",
                "Discount": 0.5,
                "Quantity": 8,
                "Segment": "Corporate",
            },
            {
                "Sub-Category": "Binders",
                "Discount": 0.3,
                "Quantity": 2,
                "Segment": "Corporate",
            },
        ]
        result_4 = calculate_discount_impact(test_data_4)
        expected_4 = {"Binders": {"Corporate": 100.0}}
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
