# Decathlon Webscraper

Flexible webscraper to scrape any category of products from the Decathlon Webshop.

*decathlon_scraper* package contains all scraping related classes and functions and scraped data. <br>
*data_analysis* package contains analysis of the scraped data. (Currently only the combined data and a first small EDA)

The data set gets updated every 24 hours. Started 7th of May, 2024.

Python 3.10 | Packages listed in requirements.txt

### Central Scraping Classes

`CategoriesEnum` <br>
Defined Enum to store the main and sub categories of the decathlon website used in this project. <br>

`StoresEnum` <br>
Defined Enum to store the store ids and names used in this project. <br>

`ProductDataAccessor` <br>
1. Builds request URLs for a given category and store
2. Finds all products listed at a defined link (subcategory)
3. Extracts product details from each product page
4. Validates & stores each tuple within a defined schema (`ProductDTO`)
5. Catches all sku ids of a product (stock-keeping unit)
   - sku ids define the different variants (like sizes or colors)
6. Saves the product details in a csv file per store, category and timestamp
7. Error handling is implemented to manage and log exceptions during data fetching and processing.

*Example usage:*
Goal is to the scrape the first shown 20 product details of <br>
https://www.decathlon.de/alle-sportarten-a-z/wassersport-welt/pools-und-wasserspielzeug?storeid=0070048700487from=1&size=20
```
data_accessor = ProductDataAccessor()
# Specify the sport and category
main_category = Categories.WASSERSPORT_WELT.value.main_category #wassersport-welt
sub_category = Categories.WASSERSPORT_WELT.value.sub_category #pools-und-wasserspielzeug
size = 20
store_id = SelectedStores.WUERZBURG.value
store_name = SelectedStores.WUERZBURG.name
data_accessor.scrape_and_save_sportgear(main_category, sub_category, store_id, store_name, size)
```

Within these product pages, there are no insights on the different store stock levels of the products. <br>
This has to be done by defined API-Calls to the stock data API of decathlon:

`StockLevelExtractor` <br>
Class designed to manage the extraction and processing of product stock levels from CSV files for specific store categories.

1. Created with a defined product csv path and category identifiers.
2. Converts csv data into `ProductDTO` objects.
3. Retrieves stock information for each product sku per store.
4. Validates & stores each tuple within a defined schema (`ProductStockDTO`).
5. The collected stock data is saved into a CSV format specific to the store and category.
6. Error handling is implemented to manage and log exceptions during data fetching and processing.

*Example usage:*
```
extractor = StockLevelExtractor(file_path, main_category, sub_category, store_id, store_name)
product_dtos = extractor.create_product_dtos()
extractor.fetch_stock_info(product_dtos)
extractor.save_to_csv() 
```

`RequestUtils` <br>
Utility class responsible for performing requests to fetch web pages and stock information. 
Implements proxy rotating and random headers to manage request reliability and bot detection.

`ScraperMain` <br>
Main class to run the entire scraping workflow. Inputs are lists of Categories and Stores. 
The class iterates over all combinations of categories and stores and runs the scraping and stock extraction process. <br>

*Example usage:*
```
scraper = ScraperMain()
# Define the categories and stores for scraping
categories = [Categories.BIKES, Categories.CAMPING, Categories.FITNESS, Categories.PADEL_TENNIS]
stores = list(SelectedStores) # all stores
scraper.scrape_categories_for_stores(categories, stores)
```
