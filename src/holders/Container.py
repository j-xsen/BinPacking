from direct.gui.DirectLabel import DirectLabel

from src.holders.Holder import Holder
from src.dimensions.oned.Item import Item
from src.Colors import unselect_colors, selected_colors
from direct.gui import DirectGuiGlobals as DGG


class Container(Holder):
    def __init__(self, capacity=5):
        super().__init__(Item, (0,0,0.7), 0.2, notify_tag="Container",
                         color=unselect_colors)
        self.frame["frameSize"] = (-0.1, 0.1, -0.1, 0.1)
        self.frame["command"] = lambda: messenger.send("container-clicked", [self])

        self.set_name(f"C-{self.uid}")

        self.active = True

        self.uid_text = DirectLabel(
            parent=self.frame,
            text=f"{self.uid}",
            scale=0.05,
            pos=(0.04, 0, -0.085),
            frameColor=(0, 0, 0, 0),
            text_fg=(0, 0, 0, 0.5),
        )

        self.capacity_text = DirectLabel(
            parent=self.frame,
            text=f"{capacity}",
            scale=0.07,
            pos=(0, 0, -.15),
            frameColor=(0, 0, 0, 0),
            text_fg=(1, 1, 1, 1),
        )

        self._capacity = capacity
        self._carrying = 0

        self.set_tag("container", '1')

    @property
    def capacity(self):
        return self._capacity
    @capacity.setter
    def capacity(self, capacity):
        self._capacity = capacity
        self.capacity_text['text'] = f"{capacity}"
    @property
    def carrying(self):
        return self._carrying
    @carrying.setter
    def carrying(self, carrying):
        self._carrying = carrying
        self.capacity_text['text'] = f"{carrying}/{self.capacity}"

    def can_add(self, item):
        return (self.carrying + item.value) <= self.capacity

    def select(self):
        self.frame["frameColor"] = selected_colors

    def deselect(self):
        self.frame["frameColor"] = unselect_colors

    def addition(self, add):
        add.frame["frameSize"] = (-0.05, 0.05, -0.05, 0.05)
        add.frame["text_pos"] = (0, -0.02)
        add.frame["borderWidth"] = (0.01, 0.01)
        add.frame["state"] = DGG.DISABLED
        add.frame.setPos(0, 0, len(self.collection)*-0.12)
        add.set_pos(0, 0, 0)
        add.active = False
        super().addition(add)
        add.uid_text.hide()

        self.frame["frameSize"] = (-0.1, 0.1, -0.115*(len(self.collection)), 0.1)
        self.capacity_text.setPos(0, 0, -0.08 - (0.115*(len(self.collection))))
        self.uid_text.setPos(0.04, 0, -(0.115*(len(self.collection))))

        self.carrying += add.value

        messenger.send("container-clicked",[None])
        messenger.send("item-clicked",[None])
