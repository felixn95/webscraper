import requests
from bs4 import BeautifulSoup
import RandomHeaders as RandomHeaders
import json
from API_Scraper.StoreStockDTO import StoreStockInfo
from requests.exceptions import RequestException
import zlib

class RequestUtils:
    # Initialize with proxy settings
    def __init__(self):
        self.proxy_url = 'https://ip.smartproxy.com/json'
        self.username = 'spk8vldbxp'
        self.password = 'fN9Mcd4_32tvarpLhB'
        self.proxy = {
            'http': f"http://{self.username}:{self.password}@de.smartproxy.com:20000",
            'https': f"http://{self.username}:{self.password}@de.smartproxy.com:20000"
        }

    def fetch_page(self, url):
        """
        Fetches the page content for the given URL using custom headers and proxy.
        """
        if not url:
            raise ValueError("URL must be provided")

        headers_manager = RandomHeaders.RandomHeaders()
        try:
            response = requests.get(url, headers=headers_manager.get_random_header(), proxies=self.proxy)
            response.raise_for_status()
        except requests.RequestException as e:
            print(f"Failed to fetch page: {e}")
            raise

        return BeautifulSoup(response.text, 'html.parser')

    def fetch_stock_info(self, sku_id, model_id, store_id):
        """
        Fetches stock information from Decathlon's endpoint using random headers and proxy.
        """
        url = f"https://www.decathlon.de/de/ajax/nfs/stocks/store/{sku_id}?modelId={model_id}&storeId={store_id}"
        headers_manager = RandomHeaders.RandomHeaders()

        try:
            response = requests.get(url, headers=headers_manager.get_random_header(), proxies=self.proxy)
            # Check status code is 200
            if response.status_code == 200:
                print(response.text)
                data = json.loads(response.text)
                return StoreStockInfo(**data[0])
            else:
                print(f"Request failed with status code: {response.status_code}")
                return None
        except RequestException as e:
            print(f"Failed to fetch stock info: {e}")
            raise
