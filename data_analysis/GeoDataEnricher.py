import pandas as pd
from haversine import haversine, Unit
import json


class GeoDataEnricher:
    def __init__(self):
        self.json_path = "../decathlon_scraper/data/stores/germany.json"
        self.store_coordinates = self.load_store_coordinates()
        self.store_names = self.load_store_names()
        self.distance_matrix = self.create_distance_matrix()

    def load_store_coordinates(self):
        """
        Load store coordinates from JSON into a dictionary for quick lookup.
        """
        with open(self.json_path, "r") as file:
            data = json.load(file)
        coordinates = {}
        for feature in data["features"]:
            store_id = feature["properties"]["store_id"]
            lon, lat = feature["geometry"]["coordinates"]
            coordinates[store_id] = (lon, lat)
        return coordinates

    def load_store_names(self):
        """
        Load store names from JSON into a dictionary indexed by store_id.
        """
        with open(self.json_path, "r") as file:
            data = json.load(file)
        names = {}
        for feature in data["features"]:
            store_id = feature["properties"]["store_id"]
            store_name = feature["properties"]["name"]
            names[store_id] = store_name
        return names

    def enrich_with_coordinates(self, df):
        """
        Add longitude and latitude columns to the DataFrame based on store_storeId.
        """
        # Create temporary lookup columns for longitude and latitude
        df['longitude'] = df['store_storeId'].map(lambda x: self.store_coordinates.get(x, (None, None))[0])
        df['latitude'] = df['store_storeId'].map(lambda x: self.store_coordinates.get(x, (None, None))[1])
        return df

    def create_distance_matrix(self):
        """
        Create a distance matrix for all stores using store names.
        """
        store_ids = list(self.store_coordinates.keys())
        distances = pd.DataFrame(index=store_ids, columns=store_ids)
        for id1 in store_ids:
            for id2 in store_ids:
                if id1 != id2:
                    dist = haversine(
                        self.store_coordinates[id1],
                        self.store_coordinates[id2],
                        unit=Unit.KILOMETERS,
                    )
                    distances.at[id1, id2] = dist
        distances.rename(index=self.store_names, columns=self.store_names, inplace=True)
        return distances

    def enrich_with_all_distances(self, data_frame):
        """
        Enrich DataFrame with distances to all unique stores found in the DataFrame.
        """
        data_frame["store_name"] = data_frame["store_storeId"].map(
            self.store_names
        )  # Map store IDs to names
        unique_store_names = data_frame["store_name"].unique()

        for other_name in unique_store_names:
            data_frame[f"distance_to_{other_name}"] = data_frame["store_name"].apply(
                lambda x: (
                    self.distance_matrix.loc[x, other_name]
                    if x != other_name and other_name in self.distance_matrix.columns
                    else None
                )
            )
        return data_frame

