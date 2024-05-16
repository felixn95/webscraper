import ProductDataAccessor
import StockLevelExtractor
import BaseMapper


class ScraperMain:
    def __init__(self):
        self.data_accessor = ProductDataAccessor.ProductDataAccessor()
        self.stock_extractor = None  # will be initialized later
        self.base_mapper = BaseMapper.BaseMapper("data/sportgear/products/")

    def scrape_categories_for_stores(self, categories, stores):
        for category in categories:
            for store in stores:
                self._scrape_category_for_store(category, store)

    def _scrape_category_for_store(self, category, store, size=40):
        main_category = category.main_category
        sub_category = category.sub_category
        store_id = store.value
        store_name = store.name

        # Build the destination path
        destination_path = self.data_accessor.build_destination_path(
            self.data_accessor.SPORTGEAR, main_category, sub_category, store_name)

        # Scrape and save data
        self.data_accessor.scrape_and_save_sportgear(
            main_category, sub_category, store_id, store_name, size)

        # Initialize and use the stock extractor
        self.stock_extractor = StockLevelExtractor.StockLevelExtractor(
            destination_path, main_category, sub_category, store_id, store_name)
        product_dtos = self.stock_extractor.create_product_dtos()
        self.stock_extractor.fetch_stock_info(product_dtos)
        self.stock_extractor.save_to_csv()

    # Instead of fetching new products, extract the stock levels from the base file (to also find out-of-stock items)
    def scrape_from_base(self, categories, stores, base):
        for category in categories:
            for store in stores:
                main_category = category.main_category
                sub_category = category.sub_category
                store_id = store.value
                store_name = store.name

                # Find the correct base file
                base_file_path = self.base_mapper.find_base_file(store_name, main_category, sub_category, base)
                if base_file_path is None:
                    print(f"No base file found for {store_name}, {main_category}, {sub_category}, {base}")
                    continue

                # Initialize and use the stock extractor with the base file path
                self.stock_extractor = StockLevelExtractor.StockLevelExtractor(
                    base_file_path, main_category, sub_category, store_id, store_name)
                product_dtos = self.stock_extractor.create_product_dtos()
                self.stock_extractor.fetch_stock_info(product_dtos)
                self.stock_extractor.save_to_csv()


