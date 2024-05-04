import random
import requests

class RandomHeaders:
    def __init__(self):
        self.headers = []  # Initialize with an empty list of headers

    def get_random_header(self):
        if self.headers:
            return random.choice(self.headers)
        else:
            print("No headers available. Please fetch headers using fetch_new_headers().")
            return None

    def get_ajax_header(self):
        return {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36',
            'Accept': 'application/json',  # Expect JSON data
            'Content-Type': 'application/json',  # Sending JSON data
            'X-Requested-With': 'XMLHttpRequest',  # Marks it as AJAX
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-Mode': 'cors',  # Typically, AJAX might be cross-origin
            'Sec-Fetch-User': '?1',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'en-US,de;q=0.7'
        }

    def fetch_new_headers(self):
        try:
            response = requests.get(
                url='https://headers.scrapeops.io/v1/browser-headers',
                params={
                    'api_key': '476d386a-1945-4c56-a876-ee1f0de30cd8',
                    'num_results': '10'}
            )
            response.raise_for_status()  # Raises a HTTPError for bad requests (4XX or 5XX)
            data = response.json()
            if 'result' in data:
                self.headers = data['result']
            else:
                print("Key 'result' not found in response")
                self.headers = []
        except requests.exceptions.RequestException as e:
            print("Request failed:", e)
            self.headers = []
        except KeyError:
            print("Unexpected JSON structure:", data)
            self.headers = []