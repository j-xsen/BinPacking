from direct.directnotify.DirectNotifyGlobal import directNotify
from direct.gui.DirectButton import DirectButton
from direct.gui.DirectFrame import DirectFrame
from direct.gui.DirectGuiGlobals import RIDGE
from panda3d.core import NodePath

from IDNodePath import IDNodePath

positions = [
    [[0.0, 0.0, 0.0]],  # 1 item

    [[-1.0, 0.0, 0.0], [1.0, 0.0, 0.0]],  # 2 items

    [[-1.0, 0.0, 0.0], [0.0, 0.0, 0.0], [1.0, 0.0, 0.0]],  # 3 items

    [[-1.0, 0.0, 0.0], [-0.3333, 0.0, 0.0], [0.3333, 0.0, 0.0], [1.0, 0.0, 0.0]]  # 4 items
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
        self.selected_item = None
        self.z = pos[2]
        self.item_type = item_type
        self.collection = []

    def on_item_clicked(self, item):
        if not self.selected_item:
            item.select()
            self.selected_item = item
        elif self.selected_item == item:
            item.deselect()
            self.selected_item = None
        else:
            self.selected_item.deselect()
            item.select()
            self.selected_item = item

    def get(self, obj):
        for item in self.collection:
            if item == obj:
                return item
        self.notify.warning(f"{obj} not found in {self.collection}")
        return None

    def set_pos(self, x, y, z):
        self.frame.set_pos(x, y, self.z)

    def rearrange(self):
        count = len(self.collection)
        if count == 0:
            return

        pos_list = positions[min(count, len(positions)) - 1]

        for i, item in enumerate(self.collection):
            if i < len(pos_list):
                if hasattr(item, "frame"):
                    item.frame.show()
                item.show()
            else:
                if hasattr(item, "frame"):
                    item.frame.hide()
                item.hide()
                continue
            item.set_pos(pos_list[i][0], pos_list[i][1], pos_list[i][2])

    def addition(self, add):
        if not type(add) == self.item_type:
            self.notify.warning(f"Only {self.item_type.__name__} instances can be added to Holder")
            return
        add.reparent_to(self.frame)
        self.collection.append(add)
        self.notify.debug(f"Addition {add.get_name()} added to Holder")
        self.rearrange()

    def subtraction(self, sub):
        if sub in self.collection:
            self.collection.remove(sub)
