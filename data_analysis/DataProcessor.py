import pandas as pd
from data_analysis.FilteringUtils import FilteringUtils
import os


class DataProcessor:
    def __init__(self):
        self.data_directory = "processed_nrw_data/"

    def process_nrw_data(self, month_day):
        output_filename = self.generate_filename(month_day)

        if os.path.exists(output_filename):
            print(
                f"File already exists: {output_filename}. Loading DataFrame from file."
            )
            nrw_data = pd.read_csv(output_filename)
            self.cast_feature_types(nrw_data)
            self.preprocess_common(nrw_data)
            return nrw_data

        print("File does not exist. Processing new data frame...")
        raw_data = pd.read_csv("combined_stock_data.csv")
        processed_data = self.process_raw_stock_data(raw_data)
        nrw_data = FilteringUtils().filter_nrw_stores(processed_data)

        self.save_data(nrw_data, month_day)
        return nrw_data

    def process_raw_stock_data(self, df):

        df = df.drop_duplicates()
        df = self.reduce_features(df)
        df = self.cast_feature_types(df)
        df = self.preprocess_common(df)
        return df

    def preprocess_common(self, df):
        df = self.transform_stock_availability(df)
        df = self.cast_feature_types(df)  # Reassert types
        df = self.format_store_ids(df)
        df = self.cast_feature_types(df)  # Reassert types
        df = self.format_prices(df)
        df = self.cast_feature_types(df)  # Reassert types
        df = self.format_timestamps(df)
        df = self.cast_feature_types(
            df
        )  # Final reassertion to ensure types are correct
        return df

    def preprocess_geo(self, df):
        df = self.cast_feature_types(df)
        df = self.preprocess_common(df)
        return df

    def reduce_features(self, df):
        features = [
            "id",
            "timestamp",
            "main_category",
            "sub_category",
            "product_name",
            "brand",
            "price",
            "store_skuId",
            "store_storeId",
            "store_storeName",
            "store_quantity",
            "store_availabilityInfo",
            "store_clickNcollect1h",
        ]
        df = df[features]
        return df

    def cast_feature_types(self, df):
        # Define a dictionary of desired column type mappings
        dtype_map = {
            "id": "category",
            "timestamp": "datetime64[ns]",
            "main_category": "category",
            "sub_category": "category",
            "product_name": "string",
            "brand": "string",
            "price": "string",
            "store_skuId": "category",
            "store_storeId": "string",
            "store_storeName": "string",
            "store_quantity": "int64",
            "store_availabilityInfo": "bool",
            "store_clickNcollect1h": "bool",
        }

        # Apply casting only to columns that exist in the DataFrame
        for column, dtype in dtype_map.items():
            if column in df.columns:
                try:
                    df[column] = df[column].astype(dtype)
                except Exception as e:
                    print(f"Error casting {column} to {dtype}: {e}")
                    # Optionally handle or log the error

        return df

    def format_store_ids(self, df):
        if "store_storeId" in df.columns:
            df["store_storeId"] = (
                df["store_storeId"].astype(str).str.strip().str.zfill(13)
            )
        return df

    def format_prices(self, df):
        df["price"] = (
            df["price"]
            .str.replace(r"\s+", "", regex=True)
            .str.replace("€", "")
            .str.replace(",", ".")
            .str.replace(r"\.(?=\d{3})", "", regex=True)
            .astype(float)
        )
        return df

    def format_timestamps(self, df):
        df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
        return df

    def transform_stock_availability(self, df):
        # Ensure that store_availabilityInfo is of a compatible type
        if "store_availabilityInfo" in df.columns:
            # Explicitly converting the 'store_availabilityInfo' column to string if not already
            df["store_availabilityInfo"] = (
                df["store_availabilityInfo"].astype(str).str.lower()
            )

            # Map the normalized availability information to boolean
            df["store_availabilityInfo"] = df["store_availabilityInfo"].map(
                {"instock": True, "nostock": False}
            )

            # Fill missing values with False
            df["store_availabilityInfo"] = df["store_availabilityInfo"].fillna(False)

            # Infer objects to ensure the entire column is of boolean type
            df["store_availabilityInfo"] = df["store_availabilityInfo"].infer_objects(
                copy=False
            )

            # Optionally, ensure the entire column is of boolean type
            df["store_availabilityInfo"] = df["store_availabilityInfo"].astype(bool)

        return df

    def save_data(self, df, month_day):
        output_filename = self.generate_filename(month_day)
        df.to_csv(output_filename, index=False)
        print(f"Preprocessed data saved to {output_filename}")

    def generate_filename(self, month_day):
        return f"{self.data_directory}{month_day}_nrw_stock_data.csv"

    def read_and_process_from_path_with_geo_data(self, path):
        df = pd.read_csv(path)
        df = self.preprocess_geo(df)
        return df

    def save_enriched_data_as_filename(self, df, filename):
        path = f"{self.data_directory}{filename}.csv"
        df.to_csv(path, index=False)
        print(f"Processed data saved to {path}")


    # remove all rows with "fahrrad_sale" as sub_category
    def remove_fahrrad_sale(self, df):
        return df[df["sub_category"] != "fahrrad_sale"]
