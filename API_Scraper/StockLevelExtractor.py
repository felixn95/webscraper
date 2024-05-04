import time
from RequestUtils import RequestUtils
from ProductDTO import ProductDTO, ProductStockDTO, product_stock_to_dict
from DataProcessingUtils import *


class StockLevelExtractor:
    def __init__(self, filepath):
        self.product_list = pd.read_csv(filepath)
        self.all_product_stocks = []

    def create_product_dtos(self):
        product_dtos = []
        for _, row in self.product_list.iterrows():
            product_dto = ProductDTO(
                id=row['product_id'],
                main_category=row['main_category'],
                sub_category=row['sub_category'],
                product_name=row['name'],
                brand=row['brand'],
                price=row['price'],
                url=row['url'],
                sku_ids=row['sku_ids'].split(';')
            )
            product_dtos.append(product_dto)
        return product_dtos

    def fetch_stock_info(self, product_dtos, store_id):
        timestamp = datetime.now()
        requests_manager = RequestUtils()
        # iterate over all products and fetch stock info for each SKU (product variant, fx. size)
        for product in product_dtos:
            sku_ids = product.sku_ids  #[:3]Limit to first X products
            for sku in sku_ids:
                try:
                    stock_info = requests_manager.fetch_stock_info(sku, product.id, store_id)
                    if stock_info:
                        product_stock = ProductStockDTO(
                            product=product,
                            store_stock=stock_info,
                            timestamp=timestamp
                        )
                        self.all_product_stocks.append(product_stock)
                    print(f"Fetched stock for product {product.id} and sku {sku}")
                    # sleep some milliseconds to avoid getting blocked
                    time.sleep(0.2)
                except Exception as e:
                    print(f"Failed to fetch stock for product {product.product_name} with error {e}")

    def save_to_csv(self):
        product_dicts = [product_stock_to_dict(stock) for stock in self.all_product_stocks]
        product_df = pd.DataFrame(product_dicts)
        main_category = self.all_product_stocks[0].product.main_category
        sub_category = self.all_product_stocks[0].product.sub_category
        if product_df.empty:
            return
        destination_path = f'data/clothing/{main_category}/stocks/stock_{main_category}_{sub_category}'
        timestamp = save_timestamp_as_string(self.all_product_stocks[0].timestamp)
        destination = f"{destination_path}_{timestamp}"
        product_df.to_csv(f'{destination}.csv', index=False)
        print(f"Stock data saved successfully to {destination}.csv")
