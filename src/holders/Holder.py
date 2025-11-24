from direct.directnotify.DirectNotifyGlobal import directNotify
from direct.gui.DirectButton import DirectButton
from direct.gui.DirectGuiGlobals import RIDGE
from pandas import Series

from src.IDNodePath import IDNodePath

positions = [
    [[0.0, 0.0, 0.0]],  # 1 item
    [[-1.0, 0.0, 0.0], [1.0, 0.0, 0.0]],  # 2 items
    [[-1.0, 0.0, 0.0], [0.0, 0.0, 0.0], [1.0, 0.0, 0.0]],  # 3 items
    [[-1.0, 0.0, 0.0], [-0.3333, 0.0, 0.0], [0.3333, 0.0, 0.0], [1.0, 0.0, 0.0]],  # 4 items
    [[-1.0, 0.0, 0.0], [-0.5, 0.0, 0.0], [0.0, 0.0, 0.0], [0.5, 0.0, 0.0], [1.0, 0.0, 0.0]],  # 5 items
    [[-1.0, 0.0, 0.0], [-0.6, 0.0, 0.0], [-0.2, 0.0, 0.0], [0.2, 0.0, 0.0], [0.6, 0.0, 0.0], [1.0, 0.0, 0.0]]  # 6 items
]


class Holder(IDNodePath):
    def __init__(self, item_type, pos, width, notify_tag="Holder", color=(1, 1, 1, 0.2)):
        super().__init__(notify_tag.lower())
        self.notify = directNotify.newCategory(notify_tag)
        self.frame = DirectButton(
            parent=self.parent,
            frameColor=color,
            relief=RIDGE,
            borderWidth=(0.025, 0.025),
            frameSize=(-width, width, -0.1, 0.1),
            pos=pos,
        )
        self.selected = None
        self.z = pos[2]
        self.item_type = item_type
        self.collection = []

    def __str__(self):
        names = [str(item) for item in self.collection]
        return f"Holder-{self.uid} ({', '.join(names)})"

    def __iter__(self):
        return iter(self.collection)

    def __len__(self):
        return len(self.collection)

    def reset(self):
        self.deselect()
        for item in self.collection:
            item.destroy()
        self.collection = []

    def deselect(self):
        if self.selected:
            self.selected.deselect()
            self.selected = None

    def on_item_clicked(self, item):
        if isinstance(item, Series):
            if len(self.collection) <= int(item.name):
                new_container = self.create_new_container()
            item = self.collection[int(item.name)]
            if not item:
                self.notify.warning(f"Clicked Series index {item.name} not found in Holder")
                return
        if not item:
            self.deselect()
            return
        if not isinstance(item, self.item_type):
            self.notify.warning(f"Clicked\n\n{item}\n{type(item)} is not of type {self.item_type.__name__}")
            return
        if not self.selected:
            item.select()
            self.selected = item
        elif self.selected == item:
            self.deselect()
        else:
            self.selected.deselect()
            item.select()
            self.selected = item
        messenger.send("holder-updated")

    def contains(self, other):
        if not isinstance(other,self.item_type):
            # try to convert
            self.notify.error(f"Cannot convert {other} to {self.item_type.__name__}")
        return other in self.collection

    def get(self, obj):
        for item in self.collection:
            if item == obj:
                return item
        self.notify.error(f"[get] {obj} not found in {self}")
        return None

    def set_pos(self, x, y, z):
        self.frame.set_pos(x, y, self.z)

    def rearrange(self):
        active_collection = []
        skip = 0
        if hasattr(self, "current_offset"):
            skip = self.current_offset
        for item in self.collection:
            if item.active:
                if skip > 0:
                    item.hide()
                    skip -= 1
                    continue
                if len(active_collection) < len(positions):
                    item.show()
                    active_collection.append(item)
                else:
                    item.hide()
        if len(active_collection) == 0:
            return

        pos_list = positions[len(active_collection)-1]
        for i, item in enumerate(active_collection):
            item.set_pos(pos_list[i][0],
                            pos_list[i][1],
                            pos_list[i][2])

    def addition(self, add):
        if not add:
            self.notify.error("Cannot add None to Holder")
            return
        if not isinstance(add, self.item_type):
            self.notify.warning(f"Only {self.item_type.__name__} instances can be added to Holder")
            return
        add.reparent_to(self.frame)
        self.collection.append(add)
        self.rearrange()

    def subtraction(self, sub):
        if not sub:
            self.notify.error("Cannot subtract None from Holder")
            return
        if self.selected and self.selected == sub:
            self.selected.deselect()
            self.selected = None
        if sub in self.collection:
            self.collection.remove(sub)
        else:
            self.notify.error(f"[sub] {sub} not found in {self}")
        self.rearrange()

    def return_random(self):
        import random
        if len(self.collection) == 0:
            return None
        return random.choice(self.collection)
