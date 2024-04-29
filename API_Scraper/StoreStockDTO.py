from dataclasses import dataclass, field

@dataclass
class StoreStockInfo:
    aboveThreshold: bool = False
    address: str = None
    availabilityInfo: str = None
    clickNcollect1h: bool = False
    favoriteStore: bool = False
    latitude: float = 0.0
    longitude: float = 0.0
    optionId: str = None
    originId: str = None
    phoneNumber: str = None
    priceId: str = None
    quantity: int = 0
    quantityShowroom: int = 0
    replenishmentEndDate: str = None
    replenishmentStartDate: str = None
    securedStockLevel: int = 0
    skuId: str = None
    storeId: str = None
    storeName: str = None
    storeSchedule: str = None
    storeUrl: str = None

