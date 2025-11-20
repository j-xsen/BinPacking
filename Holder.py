from direct.directnotify.DirectNotifyGlobal import directNotify
from panda3d.core import NodePath


positions = [
    [[0, 0, 0]],  # 1 item
    [[-6.0, 0, 0], [6.0, 0, 0]],  # 2 items
    [[-12.0, 0, 0], [0.0, 0, 0], [12.0, 0, 0]],  # 3 items
    [[-12.0, 0, 0], [-4.0, 0, 0], [4.0, 0, 0], [12.0, 0, 0]]  # 4 items
]




class Holder(NodePath):
    def __init__(self, notify_tag="Holder"):
        super().__init__(notify_tag.lower())
        self.notify = directNotify.newCategory(notify_tag)
        self.collection = []

    def get(self, obj):
        for item in self.collection:
            if item == obj:
                return item
        self.notify.warning(f"{obj} not found in {self.collection}")
        return None

    def addition(self, add):
        add.reparent_to(self)
        self.collection.append(add)
        if len(self.collection) > len(positions):
            add.hide()
        self.notify.debug(f"Addition {add.get_name()} added to Holder")

    def subtraction(self, sub):
        if sub in self.collection:
            self.collection.remove(sub)
