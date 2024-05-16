import os
import re
class BaseMapper:
    def __init__(self, base_path):
        self.base_path = base_path

    def find_base_file(self, store_name, main_category, sub_category, base):
        search_path = os.path.join(self.base_path, f'{base}')
        if not os.path.exists(search_path):
            print(f"Path {search_path} does not exist")
            return None

        pattern = re.compile(
            rf'^(.*)_{re.escape(main_category)}_{re.escape(sub_category)}_{re.escape(base)}\.csv$')

        for root, _, files in os.walk(search_path):
            for file in files:
                match = pattern.match(file)
                if match:
                    found_store_name = match.group(1)
                    if found_store_name == store_name:
                        return os.path.join(root, file).replace('\\', '/')
        return None