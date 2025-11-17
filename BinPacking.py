from direct.showbase.ShowBase import ShowBase

from Container import Container
from Item import Item


# from panda3d.core import loadPrcFileData
# loadPrcFileData("", "want-directtools #t")
# loadPrcFileData("", "want-tk #t")

class BinPacking(ShowBase):
    def __init__(self):
        super().__init__()

        # window set up
        self.title = "Bin Packing Visualization"
        self.set_background_color(0, 0, 0.2, 1)

        container_one = Container(side_length=4)
        container_one.reparent_to(render)
        container_one.set_pos(0,80,0)

        item_one = Item(side_length=1, weight=1)
        item_one.set_pos(-15,80,-10)
        item_one.reparent_to(render)

        item_two = Item(side_length=2, weight=2)
        item_two.set_pos(-5, 80, -10)
        item_two.reparent_to(render)

        item_three = Item(side_length=3, weight=3)
        item_three.set_pos(5, 80, -10)
        item_three.reparent_to(render)

        item_four = Item(side_length=4, weight=4)
        item_four.set_pos(17, 80, -10)
        item_four.reparent_to(render)

        # exit
        self.accept("escape", self.userExit)
        self.setup_scene()

    def setup_scene(self):
        # Placeholder for setting up the 3D scene
        pass

bin_packing_app = BinPacking()
bin_packing_app.run()
