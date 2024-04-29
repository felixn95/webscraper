from dataclasses import dataclass, field
from datetime import datetime
from API_Scraper.StoreStockDTO import StoreStockInfo
import pandas as pd
from dataclasses import dataclass, field
from datetime import datetime

@dataclass
class ProductDTO:
    id: str
    main_category: str
    sub_category: str
    product_name: str
    brand: str = None
    price: str = None

@dataclass
class ProductStockDTO:
    product: ProductDTO
    store_stock: StoreStockInfo
    timestamp: datetime = field(default_factory=datetime.now)

    @property
    def id(self):
        return self.product.id

    @property
    def main_category(self):
        return self.product.main_category

    @property
    def sub_category(self):
        return self.product.sub_category

    @property
    def product_name(self):
        return self.product.product_name

    @property
    def brand(self):
        return self.product.brand

    @property
    def price(self):
        return self.product.price

def product_stock_to_dict(product_stock):
    """Convert ProductStockDTO to dictionary, flattening the StoreStockInfo."""
    product_dict = {
        "id": product_stock.product.id,
        "main_category": product_stock.product.main_category,
        "sub_category": product_stock.product.sub_category,
        "product_name": product_stock.product.product_name,
        "brand": product_stock.product.brand,
        "price": product_stock.product.price,
        "timestamp": product_stock.timestamp,
        # Add StoreStockInfo fields, prefixing with 'store_'
        "store_aboveThreshold": product_stock.store_stock.aboveThreshold,
        "store_address": product_stock.store_stock.address,
        "store_availabilityInfo": product_stock.store_stock.availabilityInfo,
        "store_clickNcollect1h": product_stock.store_stock.clickNcollect1h,
        "store_favoriteStore": product_stock.store_stock.favoriteStore,
        "store_latitude": product_stock.store_stock.latitude,
        "store_longitude": product_stock.store_stock.longitude,
        "store_optionId": product_stock.store_stock.optionId,
        "store_originId": product_stock.store_stock.originId,
        "store_phoneNumber": product_stock.store_stock.phoneNumber,
        "store_priceId": product_stock.store_stock.priceId,
        "store_quantity": product_stock.store_stock.quantity,
        "store_quantityShowroom": product_stock.store_stock.quantityShowroom,
        "store_replenishmentEndDate": product_stock.store_stock.replenishmentEndDate,
        "store_replenishmentStartDate": product_stock.store_stock.replenishmentStartDate,
        "store_securedStockLevel": product_stock.store_stock.securedStockLevel,
        "store_skuId": product_stock.store_stock.skuId,
        "store_storeId": product_stock.store_stock.storeId,
        "store_storeName": product_stock.store_stock.storeName,
        "store_storeSchedule": product_stock.store_stock.storeSchedule,
        "store_storeUrl": product_stock.store_stock.storeUrl,
    }
    return product_dict

# return pd data frame from a list of ProductStockDTO
def product_stock_to_df(product_stocks):
    return pd.DataFrame([product_stock_to_dict(product_stock) for product_stock in product_stocks])


