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


print(read_csv_to_dict("samplesuperstore.csv"))
