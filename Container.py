from direct.gui.OnscreenText import OnscreenText

from Geom.Cube import Cube


class Container(Cube):
    def __init__(self, side_length):
        super().__init__(side_length)
        # color blue
        for face in self.faces:
            face.set_color((0, 0, 1, 1))  # Blue

        # wireframe
        self.set_render_mode_wireframe()

        # add text of weight
        self.capacity_text = OnscreenText(text=f"Capacity: {side_length ** 3}", pos=(0,7), scale=1.25, fg=(1, 1, 1, 1))
        self.capacity_text.set_billboard_axis()
        self.capacity_text.set_render_mode_filled()
        self.capacity_text.reparent_to(self)
        # self.capacity_text.set_z(self.side_length + 2)  # Position above the cube