from direct.gui.OnscreenText import OnscreenText

from Geom.Cube import Cube


class Item(Cube):
    def __init__(self, side_length, weight):
        super().__init__(side_length)

        min_bound, max_bound = self.get_tight_bounds()
        print("Item bounds:", min_bound, max_bound)

        # color green
        for face in self.faces:
            face.set_color((0, 1, 0, 1))  # Green

        self.weight = weight

        self.weight_text = OnscreenText(text=f"Weight: {side_length ** 3}", pos=(0, 0), scale=1.25, fg=(1, 1, 1, 1))
        self.weight_text.set_billboard_axis()
        self.weight_text.reparent_to(self)
        self.weight_text.set_z(self.side_length + 2)  # Position above the cube