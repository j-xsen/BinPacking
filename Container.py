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

        self.set_name(f"C-{self.uid}")
        self.side_length = side_length

        # add text of weight
        self.max_cap = side_length ** 3
        self._capacity = self.max_cap
        self.capacity_text = OnscreenText(text=f"Volume: {self._capacity}", pos=(0,7), scale=1.25, fg=(1, 1, 1, 1))
        self.capacity_text.set_billboard_axis()
        self.capacity_text.set_render_mode_filled()
        self.capacity_text.reparent_to(self)
        self.capacity_text.hide()
        # self.capacity_text.set_z(self.side_length + 2)  # Position above the cube

        # self.capacity_cube = Cube(0)
        # self.capacity_cube.reparent_to(self)

        self.set_tag("container", '1')

    @property
    def capacity(self):
        return self._capacity
    @capacity.setter
    def capacity(self, value):
        self._capacity = value
        self.capacity_text["text"] = f"Volume: {self._capacity}"
        # self.refresh_capacity_cube()

    def refresh_capacity_cube(self):
        self.capacity_cube.remove_node()
        side_length = (self.max_cap - self._capacity) ** (1/3)
        self.capacity_cube = Cube(side_length)
        self.capacity_cube.set_render_mode_wireframe()
        self.capacity_cube.reparent_to(self)

    def add_item(self, item):
        if type(item) != Item:
            raise TypeError("Only Item instances can be added to Container")
        item.reparent_to(self)
        item.weight_text.hide()
        taskMgr.remove(f"move-{item.uid}")  # Stop item rotation
        item.set_render_mode_filled()
        item.set_hpr(0,0,0)
        self.set_hpr(0,0,0)
        item.set_pos(self.side_length-item.side_length,
                     self.side_length-item.side_length,
                     -self.side_length+item.side_length)  # Position item at the center of the container
        self.capacity-=item.weight