import unittest

from StoreIds import StoreIds
from Sku_Ids import SkuIds_MenJacket
from StockLevelExtractor import StockLevelExtractor
from ProductDataAccessor import ProductDataAccessor
from RequestUtils import RequestUtils
from SoupExtractor import SoupExtractor


class TestProductDataAccessor(unittest.TestCase):

    def test_jackets_clothing_data_accessing(self):

        data_accessor = ProductDataAccessor()

        # Specify main and sub category
        gender = 'herren'
        category = 'outdoor-jacken'
        size = 5

        data_accessor.scrape_and_save_clothing(gender, category, size)
        # assert no exception is raised
        self.assertTrue(True)

    def test_sport_data_accessing(self):
        # Create an instance of the ProductDataAccessor
        data_accessor = ProductDataAccessor()

        # Specify the sport and category
        sport = 'wassersport-welt'
        category = 'strandspiele'
        size = 5
        store_id = StoreIds.WUERZBURG.value

        # Call the method to scrape and save the data
        data_accessor.scrape_and_save_sportgear(sport, category, store_id, size)


class TestStockLevelExtractor(unittest.TestCase):
    def test_stock_level_extraction(self):
        # Define the file path for the CSV containing product IDs
        file_path = "data/sportgear/products/wassersport-welt_strandspiele_2024-05-05_10-28.csv"

        extractor = StockLevelExtractor(file_path)
        product_dtos = extractor.create_product_dtos()

        # Fetch stock information
        store_id = StoreIds.WUERZBURG.value

        extractor.fetch_stock_info(product_dtos, store_id)

        # Save the updated stock information to a new CSV
        extractor.save_to_csv()


class TestWorkflow(unittest.TestCase):
    def test_workflow(self):
        data_accessor = ProductDataAccessor()
        # Specify the sport and category
        gender = 'damen'
        category = 'jacken'

        # Call the method to scrape and save the data
        path = data_accessor.build_destination_path(data_accessor.CLOTHING, gender, category)

        data_accessor.scrape_and_save_clothing(gender, category)

        extractor = StockLevelExtractor(path)
        product_dtos = extractor.create_product_dtos()

        # Fetch stock information for the products
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
