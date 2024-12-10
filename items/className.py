from items.goods import *
from items.armors import *
from items.weapons import *


GOODS = {}
GOODS[TestItem.NAME] = TestItem.create
GOODS[TestItemOther.NAME] = TestItemOther.create
GOODS[WoodenSword.NAME] = WoodenSword.create
GOODS[StoneSword.NAME] = StoneSword.create
GOODS[IronSword.NAME] = IronSword.create
GOODS[GoldenSword.NAME] = GoldenSword.create
GOODS[DiamondSword.NAME] = DiamondSword.create