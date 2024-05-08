from bs4 import BeautifulSoup
import json
import re

class SoupExtractor:
    def __init__(self, soup):
        if not isinstance(soup, BeautifulSoup):
            raise ValueError("Expected a BeautifulSoup object")
        self.soup = soup

    def extract_product_info(self):
        try:
            # Find the first <script type="application/ld+json"> tag in the HTML
            script = self.soup.find('script', attrs={'type': 'application/ld+json'})
            if not script:
                raise ValueError("No <script type='application/ld+json'> tag found in the HTML.")

            # Parse the JSON content within the script tag
            data = json.loads(script.string)

            # Validate if the data is of the expected product type
            if data["@type"] != "Product":
                raise ValueError("Data extracted is not of type 'Product'.")

            # Extract the product ID, name, and offers including all variants and sku ids
            product_info = {
                "productID": data.get("productID", ""),
                "name": data.get("name", ""),
                "offers": data.get("offers", [])
            }
            # parse to json and return
            return json.dumps(product_info)

        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
        except ValueError as e:
            print(f"Error: {e}")

    def get_brand_name(self):
        """
        Extracts the brand name from the soup if available in a specified anchor tag.

        Returns:
            str: The brand name if found, otherwise returns 'Brand Not Found'.
        """
        brand_tag = self.soup.find('a', class_='vtmn-typo_text-2')
        if brand_tag and brand_tag.text:
            return brand_tag.text.strip()
        return 'Brand Not Found'
