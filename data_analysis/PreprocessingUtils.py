import pandas as pd


class Preprocessor:
    def __init__(self):
        pass

    def preprocess(self, df):
        """Preprocess the input DataFrame."""
        # Drop duplicate rows
        df = df.drop_duplicates()

        # Reduce features
        df = df[
            [
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
        ]

        # Set data types explicitly
        df = df.astype(
            {
                "id": "category",  # IDs as categorical since they are unique identifiers and no arithmetic is needed
                "timestamp": "datetime64[ns]",  # Specify nanoseconds for datetime
                "main_category": "category",
                "sub_category": "category",
                "product_name": "string",
                "brand": "string",
                "price": "string",  # Price remains string for now, will be converted below
                "store_skuId": "category",  # Similarly treat SKU IDs as categories
                "store_storeId": "string",
                "store_storeName": "string",
                "store_quantity": "int64",
                "store_availabilityInfo": "string",
                "store_clickNcollect1h": "bool",
            }
        )

        # Ensure the store_storeId column is of string type and strip any whitespace
        df["store_storeId"] = df["store_storeId"].str.strip()

        # Convert the timestamp column to datetime type
        df["timestamp"] = pd.to_datetime(
            df["timestamp"], errors="coerce"
        )  # To handle any parsing errors

        # Pad the store_storeId values with leading zeros to ensure 13 characters
        df["store_storeId"] = df["store_storeId"].str.zfill(13)

        # Correct the price format by removing currency symbol, replacing commas with periods and converting to float
        df["price"] = (
            df["price"]
            .str.replace(r"\s+", "", regex=True)
            .str.replace("€", "")
            .str.replace(".", "")
            .str.replace(",", ".")
            .astype(float)
        )

        return df

    # save the preprocessed data to a CSV file
    def save_preprocessed_data(self, df, output_path):
        df.to_csv(output_path, index=False)
        print(f"Preprocessed data saved to {output_path}")
