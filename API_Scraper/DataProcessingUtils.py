from datetime import datetime
import pandas as pd
import re


def add_product_id_to_csv(input_csv_path):
    # Load the CSV file
    df = pd.read_csv(input_csv_path)

    # Define a function to extract the products ID
    def extract_product_id(url):
        match = re.search(r'mc=(\d+)', url)
        return match.group(1) if match else None

    # Apply the function to extract the ID and create a new column
    df['product_id'] = df['url'].apply(extract_product_id)

    # Construct the path for the new CSV file
    output_csv_path = input_csv_path

    # Save the DataFrame to the new CSV file
    df.to_csv(output_csv_path, index=False)

    # Optionally, print the path of the new file
    print(f"New file saved: {output_csv_path}")

# method to save timestamp as string
def save_timestamp_as_string(timestamp: datetime):
    formatted_string = timestamp.strftime("%Y-%m-%d_%H-%M")
    return formatted_string
