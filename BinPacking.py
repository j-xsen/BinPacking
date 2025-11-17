from direct.showbase.ShowBase import ShowBase

from Cube import Cube
from Square import Square

from panda3d.core import loadPrcFileData
loadPrcFileData("", "want-directtools #t")
loadPrcFileData("", "want-tk #t")
class BinPacking(ShowBase):
    def __init__(self):
        super().__init__()

        # window set up
        self.title = "Bin Packing Visualization"
        self.set_background_color(0, 0, 0.2, 1)

        square = Cube(side_length=4)
        square.reparent_to(render)
        square.set_pos(0,80,0)
        square.set_h(45)
        square.set_p(45)

        # exit
        self.accept("escape", self.userExit)
        self.setup_scene()

    def setup_scene(self):
        # Placeholder for setting up the 3D scene
        pass

bin_packing_app = BinPacking()
bin_packing_app.run()
