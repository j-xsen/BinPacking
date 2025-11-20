import random

from direct.directnotify.DirectNotifyGlobal import directNotify
from direct.gui.OnscreenText import OnscreenText

from Geom.Cube import Cube
from Geom.Square import Square


class Item(Cube):
    def __init__(self, side_length, weight=None):
        super().__init__(side_length)

        min_bound, max_bound = self.get_tight_bounds()

        self.notify = directNotify.newCategory("Item")
        self.set_name(f"I-{self.uid}")

        # color green
        for face in self.faces:
            face.set_color((0, 1, 0, 1))  # Green

        # select pane
        square = Square(side_length * 2)
        square.set_color((1, 0, 0, 1))  # Red
        square.set_pos(0, 0, 0)
        square.reparent_to(self)
        square.set_billboard_axis()
        square.hide()
        self.select_square = square
        self._selected = False

        if weight:
            self.weight = weight
        else:
            self.weight = side_length**3
        self.weight_text = OnscreenText(text=f"Volume: {side_length ** 3}", pos=(0, side_length+2), scale=1.25, fg=(1, 1, 1, 1))
        self.weight_text.set_billboard_axis()
        self.weight_text.reparent_to(self)

        self.set_tag("item", '1')

    @property
    def selected(self):
        return self._selected
    @selected.setter
    def selected(self, value):
        self._selected = value
        if self._selected:
            self.select_square.show()
        else:
            self.select_square.hide()

    def select(self):
        self.notify.debug(f"Item {self.get_name()} selected")
        self.selected = True

    def deselect(self):
        self.notify.debug(f"Item {self.get_name()} deselected")
        self.selected = False
