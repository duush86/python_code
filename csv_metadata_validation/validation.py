import pandas as pd
import re

# Define a dictionary to store validation rules
validation_rules = {
    "text": r".*",
    "number": r"^\d+$",
    "Date": r"^\d{2}/\d{2}/\d{4}$",
    "Regex": None,  # Custom regex patterns will be applied separately
    "list": ["movie", "episode"],
    "URL": r"^(https?|http):\/\/[^\s/$.?#].[^\s]*$"
}

# Read the CSV validation feed into a DataFrame
validation_feed = pd.read_csv('validation_file.csv')

# Create a function to validate a value based on its type and rules
def validate_value(value, column_type, regex_pattern):
    if column_type == "list":
        return value.lower() in validation_rules[column_type]
    elif column_type == "Regex":
        if regex_pattern:
            return bool(re.match(regex_pattern, value))
        else:
            return True
    else:
        return bool(re.match(validation_rules[column_type], value))

# Read the CSV input file for validation
input_file = pd.read_csv('antonio_tna2.csv')

# Initialize a list to store validation results
validation_results = []

# Iterate through each row in the input file
for index, row in input_file.iterrows():
    validation_result = {"Row": index + 1, "Valid": True, "Errors": []}

    # Iterate through each column in the validation feed
    for _, validation_row in validation_feed.iterrows():
        column_name = validation_row["Column Name"]
        column_type = validation_row["Column Type"]
        is_required = validation_row["Is Required"]
        regex_pattern = validation_row["Limits"]

        value = row[column_name]

        if pd.isna(value) and is_required:
            validation_result["Valid"] = False
            validation_result["Errors"].append(f"{column_name} is required")

        if not pd.isna(value) and not validate_value(str(value), column_type, regex_pattern):
            validation_result["Valid"] = False
            validation_result["Errors"].append(f"{column_name} is invalid")

    validation_results.append(validation_result)

# Print validation results
for result in validation_results:
    if result["Valid"]:
        print(f"Row {result['Row']} is valid.")
    else:
        print(f"Row {result['Row']} is invalid. Errors: {', '.join(result['Errors'])}")
