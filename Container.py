from Geom.Square import Square
from Holder import Holder
from Item import Item
from colors import unselect_colors, selected_colors


class Container(Holder):
    def __init__(self):
        super().__init__(Item, (0,0,0.7), 0.2, notify_tag="Container",
                         color=unselect_colors)
        self.frame["frameSize"] = (-0.1, 0.1, -0.1, 0.1)
        self.frame["command"] = lambda: messenger.send("container-clicked", [self])

        self.set_name(f"C-{self.uid}")

        self.set_tag("container", '1')

    def select(self):
        self.frame["frameColor"] = selected_colors

    def deselect(self):
        self.frame["frameColor"] = unselect_colors
