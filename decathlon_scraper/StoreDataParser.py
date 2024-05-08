import json
from enum import Enum

class StoreDataParser:
    def __init__(self, file_path=None):
        if file_path:
            self.data = self.read_json_from_file(file_path)
        else:
            self.data = []

    def read_json_from_file(self, file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
                # Ensure the 'features' key exists and contains a list
                if "features" in data and isinstance(data["features"], list):
                    return data["features"]
                else:
                    raise ValueError("JSON data does not contain 'features' key or is not formatted as expected.")
        except json.JSONDecodeError as e:
            print("Error decoding JSON:", e)
            return []
        except Exception as e:
            print("Error reading JSON file:", e)
            return []

    def get_store_info(self):
        # Extract store information (id and name)
        stores = []
        for feature in self.data:
            try:
                store_id = feature['properties']['store_id']
                name = feature['properties']['name'].upper().replace(" ", "_").replace("\u00fc", "UE")
                stores.append((name, store_id))
            except KeyError as e:
                print(f"Missing key in JSON data: {e}")
            except TypeError as e:
                print(f"Type error in JSON handling: {e}")
        return stores

    def generate_enum_class_definition(self, stores):
        class_def = "from enum import Enum\n\n\nclass StoreIds(Enum):\n"
        for name, store_id in stores:
            class_def += f"    {name} = \"{store_id}\"\n"
        return class_def

file_path = 'G:\My Drive\Master IS\Repos\webscraper\API_Scraper\data\stores\south_germany.json'
parser = StoreDataParser(file_path)
stores = parser.get_store_info()
if stores:
    class_definition = parser.generate_enum_class_definition(stores)
    print(class_definition)
else:
    print("No stores found or JSON data is incorrect.")
