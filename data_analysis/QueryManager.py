import pandas as pd
import matplotlib.pyplot as plt

class QueryManager:
    def __init__(self, df):
        self.df = df

    def order_by_timestamp(self):
        self.df = self.df.sort_values(by="timestamp")
        return self.df

    def product_variants_in_all_stores(self):
        grouped = self.df.groupby(["id", "store_skuId"])
        all_stores_df = grouped.filter(
            lambda x: x["store_storeId"].nunique() == self.df["store_storeId"].nunique()
        )
        return all_stores_df[
            [
                "id",
                "main_category",
                "sub_category",
                "product_name",
                "brand",
                "price",
                "store_skuId",
            ]
        ].drop_duplicates()

    def product_variants_in_at_least_x_stores(self, x):
        grouped = self.df.groupby(["id", "store_skuId"])
        at_least_x_stores_df = grouped.filter(
            lambda y: y["store_storeId"].nunique() >= x
        )
        return at_least_x_stores_df[
            [
                "id",
                "main_category",
                "sub_category",
                "product_name",
                "brand",
                "price",
                "store_skuId",
            ]
        ].drop_duplicates()

    def positive_stock_in_all_stores(self):
        all_stores_df = self.product_variants_in_all_stores()
        positive_stock_df = self.df[self.df["store_availabilityInfo"] == True]
        positive_stock_df = positive_stock_df[
            positive_stock_df.duplicated(subset=["id", "store_skuId"], keep="first")
        ]
        return all_stores_df.merge(
            positive_stock_df,
            on=[
                "id",
                "main_category",
                "sub_category",
                "product_name",
                "brand",
                "price",
                "store_skuId",
            ],
            how="inner",
        ).drop_duplicates()

    def positive_stock_in_at_least_x_stores(self, x):
        at_least_x_stores_df = self.product_variants_in_at_least_x_stores(x)
        positive_stock_df = self.df[self.df["store_availabilityInfo"] == True]
        positive_stock_df = positive_stock_df[
            positive_stock_df.duplicated(subset=["id", "store_skuId"], keep="first")
        ]
        return at_least_x_stores_df.merge(
            positive_stock_df,
            on=[
                "id",
                "main_category",
                "sub_category",
                "product_name",
                "brand",
                "price",
                "store_skuId",
            ],
            how="inner",
        ).drop_duplicates()

    def sold_out_products(self, filtered_df):
        # Filter the products from the original dataframe that were ever sold out
        sold_out_df = self.df[self.df['store_availabilityInfo'] == False]
        result_df = filtered_df.merge(sold_out_df,
                                      on=['id', 'main_category', 'sub_category', 'product_name', 'brand', 'price',
                                          'store_skuId'], how='inner').drop_duplicates(subset=['id', 'store_skuId'])
        return result_df



