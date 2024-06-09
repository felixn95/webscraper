from decathlon_scraper.StoresEnum import StoresNRW


class FilteringUtils:
    def __init__(self):
        pass

    def filter_nrw_stores(self, df):

        # Access the specific enum for NRW stores
        nrw_area = StoresNRW

        # Create a list with the enum values, ensuring no leading/trailing whitespace
        nrw_stores = [str(store.value).strip() for store in nrw_area]

        # Filter the DataFrame for the stores in the NRW area
        nrw_df = df[df["store_storeId"].isin(nrw_stores)]
        return nrw_df

    def sort_by_timestamp(self, df):
        return df.sort_values(by="timestamp")

