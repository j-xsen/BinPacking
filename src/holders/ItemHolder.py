from direct.gui.DirectButton import DirectButton
from direct.showbase.DirectObject import DirectObject

from src.dimensions.oned.ValuedItem import ValuedItem
from src.holders.CarouselHolder import CarouselHolder
from src.holders.Holder import Holder
from src.dimensions.oned.Item import Item


class ItemHolder(CarouselHolder, DirectObject):
    def __init__(self):
        super().__init__(Item, (0, 0, -0.7), 1, 'ItemHolder')

        self.create_new_item_button = DirectButton(
            text="Create New Item",
            parent=self.frame,
            scale=0.07,
            pos=(0, 0, -.2),
            command=self.create_new_item
        )

        self.accept("item-clicked", self.on_item_clicked)

    def contains(self, other):
        other_result = False
        if type(other) == str:
            other_result = self.item_from_weight(int(other))
        return other_result

    def get(self, obj):
        if type(obj) == str:
            return self.item_from_weight(int(obj))
        return super().get(obj)

    def on_item_clicked(self, item):
        if type(item) == str:
            item = self.item_from_weight(int(item))
        super().on_item_clicked(item)

    def item_from_weight(self, weight):
        for item in self.collection:
            if int(item.weight) == (weight):
                return item
        return None

    def create_new_item(self, weight=1):
        new_item = Item(weight=weight)
        self.addition(new_item)
        return new_item

    def create_new_valued_item(self, weight=1, value=1):
        new_item = ValuedItem(weight=weight, value=value)
        self.addition(new_item)
