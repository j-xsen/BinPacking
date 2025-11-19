import random

from direct.gui.OnscreenText import OnscreenText

from Geom.Cube import Cube
from Item import Item


class Container(Cube):
    def __init__(self, side_length):
        super().__init__(side_length)
        # color blue
        for face in self.faces:
            face.set_color((0, 0, 1, 1))  # Blue

        # wireframe
        self.set_render_mode_wireframe()

        self.set_name(f"C-{random.randint(1000, 9999)}")

        # add text of weight
        self._capacity = side_length ** 3
        self.capacity_text = OnscreenText(text=f"Volume: {self._capacity}", pos=(0,7), scale=1.25, fg=(1, 1, 1, 1))
        self.capacity_text.set_billboard_axis()
        self.capacity_text.set_render_mode_filled()
        self.capacity_text.reparent_to(self)
        # self.capacity_text.set_z(self.side_length + 2)  # Position above the cube

        self.set_tag("container", '1')

    @property
    def capacity(self):
        return self._capacity
    @capacity.setter
    def capacity(self, value):
        self._capacity = value
        self.capacity_text["text"] = f"Volume: {self._capacity}"

    def add_item(self, item):
        if type(item) != Item:
            raise TypeError("Only Item instances can be added to Container")
        item.reparent_to(self)
        item.weight_text.hide()
        item.set_render_mode_filled()
        item.set_pos(0, 0, 0)  # Position item at the center of the container
        self.capacity-=item.weight