import random

from direct.gui.DirectButton import DirectButton

from Holder import Holder, positions
from Item import Item


class ItemHolder(Holder):
    def __init__(self):
        super().__init__('ItemHolder')

        self.create_new_item_button = DirectButton(
            text="Create New Item",
            scale=0.07,
            pos=(0, 0, 0.9),
            command=self.create_new_item
        )

    def rearrange(self):
        count = len(self.collection)
        if count == 0:
            return

        pos_list = positions[min(count, len(positions)) - 1]

        for i, item in enumerate(self.collection):
            if i < len(pos_list):
                item.show()
            else:
                item.hide()
                continue
            item.set_pos(pos_list[i][0] * 2, pos_list[i][1] * 2, pos_list[i][2] * 2)
        self.notify.debug("ItemHolder rearranged items")

    def create_new_item(self):
        new_item = Item(side_length=random.randint(1,5))
        self.addition(new_item)
        self.rearrange()

    def subtraction(self, sub):
        super().subtraction(sub)
        self.rearrange()

    def addition(self, add):
        if type(add) != Item:
            self.notify.warning("Only Item instances can be added to ItemHolder")
            return
        super().addition(add)
