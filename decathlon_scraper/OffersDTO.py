from dataclasses import dataclass
from typing import List

@dataclass
class Seller:
    type: str = None
    name: str = None

@dataclass
class Offer:
    type: str = None
    sku: str = None
    price: float = None
    priceCurrency: str = None
    availability: str = None
    itemCondition: str = None
    image: str = None
    seller: Seller = None
    url: str = None

@dataclass
class OfferCollection:
    offers: List[Offer]

def from_json(data: dict) -> OfferCollection:
    offers = [
        Offer(
            type=offer["@type"],
            sku=offer["sku"],
            price=offer["price"],
            priceCurrency=offer["priceCurrency"],
            availability=offer["availability"],
            itemCondition=offer["itemCondition"],
            image=offer["image"],
            seller=Seller(type=offer["seller"]["@type"], name=offer["seller"]["name"]),
            url=offer["url"]
        )
        for offer in data["offers"][0]
    ]
    return OfferCollection(offers=offers)
