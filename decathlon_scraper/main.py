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

        # categories = [Categories.FITNESS, Categories.BIKES]
        stores = list(StoresNRW)  # all target stores

        # Define the base files to be used for scraping
        base = "BASIS_05_14"

        scraper.scrape_from_base(categories, stores, base)


# This allows the test to be run from the command line
if __name__ == "__main__":
    unittest.main()
