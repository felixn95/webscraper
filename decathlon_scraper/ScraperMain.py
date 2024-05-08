import ProductDataAccessor
import StockLevelExtractor


class ScraperMain:
    def __init__(self):
        self.data_accessor = ProductDataAccessor.ProductDataAccessor()
        self.stock_extractor = None  # will be initialized later

    def scrape_categories_for_stores(self, categories, stores, size=20):
        for category in categories:
            for store in stores:
                self._scrape_category_for_store(category, store, size)

    def _scrape_category_for_store(self, category, store, size=20):
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
