import unittest

from StoresEnum import SelectedStores, StoresNRW
from CategoriesEnum import Categories
from StockLevelExtractor import StockLevelExtractor
from ProductDataAccessor import ProductDataAccessor
from RequestUtils import RequestUtils
from SoupExtractor import SoupExtractor
from ScraperMain import ScraperMain
from decathlon_scraper.BaseMapper import BaseMapper


# Test class structures used for processing the scraper
class TestWorkflow(unittest.TestCase):

    def test_workflow_from_base(self):
        scraper = ScraperMain()

        # Define the categories and stores for scraping
        categories = list(Categories)  # all categories
        stores = list(StoresNRW)  # all target stores

        # Define the base files to be used for scraping
        base = "BASIS_05_14"

        scraper.scrape_from_base(categories, stores, base)



    def test_workflow_per_category_all_stores(self):
        scraper = ScraperMain()

        # Define the categories and stores for scraping
        categories = list(Categories)  # all categories
        stores = list(StoresNRW)  # all target stores

        scraper.scrape_categories_for_stores(categories, stores)

    def test_workflow_sales_ruhrgebiet(self):
        scraper = ScraperMain()

        categories = [Categories.BIKES]
        stores = [SelectedStores.NRW_NEUSS, SelectedStores.NRW_KOELN_QUINCY, SelectedStores.NRW_KOELN_MARSDORF]
        scraper.scrape_categories_for_stores(categories, stores)

class TestBaseMapper(unittest.TestCase):

        def test_base_mapper(self):
            # Create an instance of the BaseMapper
            base_mapper = BaseMapper("data/sportgear/products/")

            # Find the base file for a specific store, main category, sub category, and base
            store_name = SelectedStores.NRW_NEUSS.name
            main_category = Categories.CAMPING_ESSEN.main_category
            sub_category = Categories.CAMPING_ESSEN.sub_category
            base = "BASIS_05_14"

            base_file_path = base_mapper.find_base_file(store_name, main_category, sub_category, base)

            # Assert that the base file path is not None
            self.assertIsNotNone(base_file_path)

            # Print the base file path
            print(base_file_path)


class TestProductDataAccessor(unittest.TestCase):

    def test_jackets_clothing_data_accessing(self):
        data_accessor = ProductDataAccessor()

        # Specify main and sub category
        gender = 'herren'
        category = 'outdoor-jacken'
        size = 5
        store_id = SelectedStores.WUERZBURG.value
        data_accessor.scrape_and_save_clothing(gender, category, store_id, size)
        # assert no exception is raised
        self.assertTrue(True)

    def test_sport_data_accessing(self):
        # Create an instance of the ProductDataAccessor
        data_accessor = ProductDataAccessor()

        # Specify the sport and category
        main_category = Categories.WASSERSPORT_WELT.value.main_category
        sub_category = Categories.WASSERSPORT_WELT.value.sub_category
        size = 20
        store_id = SelectedStores.WUERZBURG.value
        store_name = SelectedStores.WUERZBURG.name

        # Call the method to scrape and save the data
        data_accessor.scrape_and_save_sportgear(main_category, sub_category, store_id, store_name, size)


class TestStockLevelExtractor(unittest.TestCase):
    def test_stock_level_extraction(self):
        # Define the file path for the CSV containing product IDs
        file_path = "data/sportgear/products/BER_WILMERSDORFER_ARCADEN_fitness_fitnessgerate-fur-zuhause_2024-05-06_18-27.csv"
        main_category = "fitness"
        sub_category = "fitnessgerate-fur-zuhause"
        store_id = SelectedStores.BER_WILMERSDORFER_ARCADEN.value
        store_name = SelectedStores.BER_WILMERSDORFER_ARCADEN.name

        # Fetch stock information
        extractor = StockLevelExtractor(file_path, main_category, sub_category, store_id, store_name)
        product_dtos = extractor.create_product_dtos()
        extractor.fetch_stock_info(product_dtos)

        # Save the updated stock information to a new CSV
        extractor.save_to_csv()


class TestSoupExtractor(unittest.TestCase):
    def test_soup_extractor(self):
        # Load the HTML content from a file
        request_manager = RequestUtils()
        url = "https://www.decathlon.de/p/laufshorts-leicht-kiprun-light-herren/_/R-p-325737?mc=8774064&c=blau"
        product_soup = request_manager.fetch_page(url)

        soup_extractor = SoupExtractor(product_soup)

        model_data = soup_extractor.extract_product_info()

        print(model_data)


# This allows the test to be run from the command line
if __name__ == '__main__':
    unittest.main()
