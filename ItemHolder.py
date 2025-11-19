from Holder import Holder
from Item import Item


class ItemHolder(Holder):
    def __init__(self):
        super().__init__('ItemHolder')

    def addition(self, add):
        if type(add) != Item:
            self.notify.warning("Only Item instances can be added to ItemHolder")
            return
        self.notify.debug(f"Adding Item {add.get_name()} to ItemHolder")

        add.reparent_to(self)
        self.collection.append(add)
        self.notify.debug(f"Item {add.get_name()} added to ItemHolder")
