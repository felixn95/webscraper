from enum import Enum

class SkuIds_MenJacket(Enum):
    S = 4194321
    M = 4194320
    L = 4194319
    XL = 4194322
    XXL = 4194316
    XXXL = 4194317

    @classmethod
    def values(cls):
        return [item.value for item in cls]
