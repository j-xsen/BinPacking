from panda3d.core import NodePath

from src.holders.Container import Container
from src.holders.ContainerHolder import ContainerHolder
from src.holders.ItemHolder import ItemHolder


class TwoD(NodePath):
    def __init__(self):
        super().__init__('2DView')
        self._item_selected = None

        container_one = Container(side_length=4)

        self.container_holder = ContainerHolder()
        self.container_holder.addition(container_one)
        self.container_holder.set_pos(0, 80, 0)
        self.container_holder.reparent_to(render)

        item_one = Item(side_length=1)

        self.item_holder = ItemHolder()
        self.item_holder.addition(item_one)
        self.item_holder.set_pos(0, 80, -10)
        self.item_holder.reparent_to(render)

    @property
    def item_selected(self):
        if self._item_selected is None:
            return None
        return self._item_selected
    @item_selected.setter
    def item_selected(self, value):
        value = self.item_holder.get(value)

        if not value:
            self.notify.warning("No item selected")
            return

        # no item selected, fill
        if not self._item_selected:
            if value is None:
                self.notify.warning(f"Selected item {value} not found in ItemHolder")
                return
            value.select()
            self._item_selected = value
        # item selected, toggle
        else:
            # deselect if same item
            if value == self._item_selected:
                value.deselect()
                self._item_selected = None
            # select if new item
            else:
                self._item_selected.deselect()
                value.select()
                self._item_selected = value