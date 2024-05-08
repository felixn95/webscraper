from enum import Enum

class Categories(Enum):
    CAMPING = ('camping', 'zelte')
    WASSERSPORT_WELT = ('wassersport-welt', 'pools-und-wasserspielzeug')
    BASKETBALL = ('basketball', 'basketballe-netballe')
    PADEL_TENNIS = ('padel-tennis', 'padelausrustung')
    FITNESS = ('fitness', 'fitnessgerate-fur-zuhause')
    BIKES = ('fahrrad-welt', 'fahrrader')
    # WINTERSPORT = ('wintersport', 'skiausrustung')

    def __init__(self, main_category, sub_category):
        self.main_category = main_category
        self.sub_category = sub_category
