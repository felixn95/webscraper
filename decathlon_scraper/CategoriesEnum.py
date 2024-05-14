from enum import Enum

class Categories(Enum):
    CAMPING = ('camping', 'zelte')
    # WASSERSPORT_WELT = ('wassersport-welt', 'pools-und-wasserspielzeug')
    # STAND_UP_PADDLING = ('wassersport-welt', 'stand-up-paddle-sup')
    # BASKETBALL = ('basketball', 'basketballe-netballe')
    # PADEL_TENNIS = ('padel-tennis', 'padelausrustung')
    FITNESS = ('fitness', 'fitnessgerate-fur-zuhause')
    BIKES = ('fahrrad-welt', 'fahrrader')
    BIKES_SALE = ('fahrrad-welt', 'fahrrad_sale')
    # WINTERSPORT = ('wintersport', 'skiausrustung')
    #https://www.decathlon.de/deals/sale-produkte/f-sport-group_fahrrad-city_fahrrad-mtb_fahrrad-rennrad_fahrrad-trekking-gravel-cross?storeid=0070048700487

    def __init__(self, main_category, sub_category):
        self.main_category = main_category
        self.sub_category = sub_category
