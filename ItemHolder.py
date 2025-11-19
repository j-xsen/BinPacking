from direct.directnotify.DirectNotifyGlobal import directNotify
from panda3d.core import NodePath, CollisionNode, CollisionRay, GeomNode

from Item import Item


class ItemHolder(NodePath):
    def __init__(self):
        super().__init__('item_holder')
        self.notify = directNotify.newCategory("ItemHolder")
        self.items = []

    def get_item(self, id):
        if type(id) == NodePath:
            id = id.get_name()
        for item in self.items:
            if item.get_name()== id:
                return item
        self.notify.warning("Item not found")
        return None

    def add_item(self, item):
        if type(item) != Item:
            self.notify.warning("Only Item instances can be added to ItemHolder")
            return
        item.reparent_to(self)
        self.items.append(item)
        self.notify.debug(f"Item {item.get_name()} added to ItemHolder")

    def remove_item(self, item):
        if item in self.items:
            self.items.remove(item)
