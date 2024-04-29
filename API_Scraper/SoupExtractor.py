from bs4 import BeautifulSoup


class SoupExtractor:
    def __init__(self, soup):
        if not isinstance(soup, BeautifulSoup):
            raise ValueError("Expected a BeautifulSoup object")
        self.soup = soup

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
