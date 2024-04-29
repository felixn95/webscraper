import unittest
from StockLevelExtractor import StockLevelExtractor
from ProductDataAccessor import ProductDataAccessor


class TestProductDataAccessor(unittest.TestCase):

    def test_jackets_clothing_data_accessing(self):
        # Create an instance of the ProductDataAccessor
        data_accessor = ProductDataAccessor()

        # Specify the sport and category
        gender = 'damen'
        category = 'jacken'

        # Call the method to scrape and save the data
        data_accessor.scrape_and_save_clothing(gender, category)

    def test_sport_data_accessing(self):
        # Create an instance of the ProductDataAccessor
        data_accessor = ProductDataAccessor()

        # Specify the sport and category
        sport = 'padel-tennis'
        category = 'padelausrustung'

        # Call the method to scrape and save the data
        data_accessor.scrape_and_save_sportgear(sport, category)


class TestStockLevelExtractor(unittest.TestCase):
    def test_stock_level_extraction(self):
        # Define the file path for the CSV containing product IDs
        file_path = "data/clothing/damen/products/damen_jacken_2024-04-29_20-13_ids.csv"

        extractor = StockLevelExtractor(file_path)
        product_dtos = extractor.create_product_dtos()

        # Fetch stock information for the products
        extractor.fetch_stock_info(product_dtos)

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


# This allows the test to be run from the command line
if __name__ == '__main__':
    unittest.main()
