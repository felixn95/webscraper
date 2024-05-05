import json

import pandas as pd
import logging
from bs4 import BeautifulSoup

from API_Scraper.SoupExtractor import SoupExtractor
from RequestUtils import RequestUtils
from DataProcessingUtils import *
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class ProductDataAccessor:
    BASE_URL = 'https://www.decathlon.de'
    CLOTHING = 'clothing'
    SPORTGEAR = 'sportgear'
    SPORT_BASE = 'alle-sportarten-a-z'

    def __init__(self, data_dir='data'):
        self.data_dir = data_dir

    def scrape_and_save_clothing(self, gender: str, category: str, store_id: str, size: int = 30):
        """Scrapes product data for a given category and gender and saves it to a CSV file."""
        url = self.build_url(self.CLOTHING, gender, category, store_id, size)
        destination_path = self.build_destination_path(self.CLOTHING, gender, category)
        self.scrape_and_save(url, destination_path, gender, category)

    def scrape_and_save_sportgear(self, sport: str, category: str, store_id: str, size: int = 30):
        """Scrapes product data for a given sport and category and saves it to a CSV file."""
        url = self.build_url(self.SPORTGEAR, sport, category, store_id, size)
        destination_path = self.build_destination_path(self.SPORTGEAR, sport, category)
        self.scrape_and_save(url, destination_path, sport, category)

    def build_url(self, c_type: str, main_category: str, sub_category: str, store_id: str, size: int = 30) -> str:
        """Builds the URL based on the type of product."""
        if c_type == self.CLOTHING:
            return f'{self.BASE_URL}/{main_category}/{sub_category}?storeid={store_id}from=1&size={size}'
        elif c_type == self.SPORTGEAR:
            # https://www.decathlon.de/alle-sportarten-a-z/wassersport-welt/strandspiele?storeid=0070048700487
            return f'{self.BASE_URL}/{self.SPORT_BASE}/{main_category}/{sub_category}?storeid={store_id}from=1&size={size}'

    def build_destination_path(self, c_type: str, main_category: str, sub_category: str) -> str:
        """Builds the file path for storing scraped data."""
        timestamp = save_timestamp_as_string(datetime.now())
        if c_type == self.CLOTHING:
            return f'{self.data_dir}/{c_type}/{main_category}/products/{main_category}_{sub_category}_{timestamp}.csv'
        else:
            return f'{self.data_dir}/{c_type}/products/{main_category}_{sub_category}_{timestamp}.csv'

    def scrape_and_save(self, url: str, destination_path: str, main_category: str, sub_category: str):
        """General method to scrape and save product data."""
        try:
            request_manager = RequestUtils()
            items_soup = request_manager.fetch_page(url)
            products_dict = self.extract_items(items_soup, main_category, sub_category)

            # Initialize an empty list to store SKU ids
            sku_ids_list = []

            # Enrich the product data SKU ids by searching the product URL
            for index, product in products_dict.iterrows():
                product_url = product['url']
                product_soup = request_manager.fetch_page(product_url)
                soup_extractor = SoupExtractor(product_soup)
                product_details = soup_extractor.extract_product_info()
                product_json = json.loads(product_details)

                if product_json and 'offers' in product_json:
                    # Handle nested list in offers
                    sku_ids = [offer['sku'] for sublist in product_json['offers'] for offer in sublist]
                    # separate sku ids by semicolon
                    sku_ids_list.append(';'.join(sku_ids))

            # Ensure that sku_ids_list has an entry for each row in the DataFrame
            products_dict['sku_ids'] = sku_ids_list

            # Save the DataFrame to CSV
            products_dict.to_csv(destination_path, index=False)
            add_product_id_to_csv(destination_path)

            logging.info(f"Data saved successfully to {destination_path}")
        except Exception as e:
            logging.error(f"Failed to scrape and save data: {e}")

    def extract_items(self, soup: BeautifulSoup, main_category: str, sub_category: str) -> pd.DataFrame:
        """Extracts product data from a BeautifulSoup object and returns it as a DataFrame."""
        products = soup.find_all('div', role='listitem')
        product_list = []

        for product in products:
            product_data = self.extract_product_data(product, main_category, sub_category)
            product_list.append(product_data)

        return pd.DataFrame(product_list)

    def extract_product_data(self, product, main_category: str, sub_category: str) -> dict:
        """Extracts data from a single product div."""
        product_name = product.find('span', class_='vh').text.strip() if product.find('span', class_='vh') else ''
        product_url = product.find('a', class_='dpb-product-model-link')['href'] if product.find('a',
                                                                                                 'dpb-product-model-link') else ''
        brand = product.find('strong', class_='vtmn-block').text.strip() if product.find('strong', 'vtmn-block') else ''
        price_element = product.find('span', class_='vtmn-price')
        price = price_element.text.strip() if price_element else ''

        # build product dto
        return {
            'name': product_name,
            'main_category': main_category,
            'sub_category': sub_category,
            'url': f'{self.BASE_URL}{product_url}' if product_url else '',
            'brand': brand,
            'price': price
        }
