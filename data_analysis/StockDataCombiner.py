import pandas as pd
import glob
import os

class StockDataCombiner:
    def __init__(self, data_directory):
        self.data_directory = data_directory

    def combine_csv_files(self):
        """Combine all CSV files in the directory into a single DataFrame."""
        path_pattern = os.path.join(self.data_directory, '*.csv')
        # List all file paths matching the pattern
        file_list = glob.glob(path_pattern)

        # Check if file list is empty
        if not file_list:
            raise ValueError("No CSV files found in the directory.")

        # Load and concatenate all files into a single DataFrame
        df_list = [pd.read_csv(file) for file in file_list]
        combined_df = pd.concat(df_list, ignore_index=True)
        print("Data combined successfully")
        return combined_df

    def save_combined_data(self, output_path):
        """Save the combined DataFrame to a CSV file."""
        df = self.combine_csv_files()
        df.to_csv(output_path, index=False)
        print(f"Combined data saved to {output_path}")
