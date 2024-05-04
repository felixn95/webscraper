import requests
from bs4 import BeautifulSoup
import RandomHeaders as RandomHeaders
import json
from API_Scraper.StoreStockDTO import StoreStockInfo
from requests.exceptions import RequestException
import zlib
import time

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

    def fetch_page(self, url, max_retries=3):
        """
        Fetches the page content for the given URL using custom headers and proxy.
        """
        if not url:
            raise ValueError("URL must be provided")

        headers_manager = RandomHeaders.RandomHeaders()
        retries = 0
        while retries < max_retries:
            headers = headers_manager.get_random_header()
            try:
                response = requests.get(url, headers=headers, proxies=self.proxy)
                response.raise_for_status()
                return BeautifulSoup(response.text, 'html.parser')
            except requests.RequestException as e:
                print(f"Failed to fetch page (retry {retries+1}/{max_retries}): {e}")
                retries += 1
                time.sleep(1)  # Adding a small delay before retrying
        raise RequestException("Failed to fetch page after multiple retries")

    def fetch_stock_info(self, sku_id, model_id, store_id, max_retries=3):
        """
        Fetches stock information from Decathlon's endpoint using random headers and proxy.
        """
        url = f"https://www.decathlon.de/de/ajax/nfs/stocks/store/{sku_id}?modelId={model_id}&storeId={store_id}"
        headers_manager = RandomHeaders.RandomHeaders()

        retries = 0
        while retries < max_retries:
            headers = headers_manager.get_ajax_header()
            try:
                response = requests.get(url, headers=headers, proxies=self.proxy)
                if response.status_code == 200:
                    data = json.loads(response.text)
                    return StoreStockInfo(**data[0])
                else:
                    print(f"Request failed with status code: {response.status_code} (retry {retries+1}/{max_retries})")
            except RequestException as e:
                print(f"Failed to fetch stock info (retry {retries+1}/{max_retries}): {e}")
                print(headers)
            retries += 1
            time.sleep(0.3)  # Adding a small delay before retrying
        raise RequestException("Failed to fetch stock info after multiple retries")

