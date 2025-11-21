from direct.gui.DirectButton import DirectButton
from direct.showbase.DirectObject import DirectObject

from src.holders.Holder import Holder
from src.dimensions.oned.Item import Item


class ItemHolder(Holder, DirectObject):
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

    def create_new_item(self, value=1):
        new_item = Item(value=value)
        self.addition(new_item)
        self.notify.debug(f"New Item created: {new_item}")
        self.notify.debug(f"Current Items: {self.collection}")
        return new_item

    def subtraction(self, sub):
        super().subtraction(sub)
        self.rearrange()
