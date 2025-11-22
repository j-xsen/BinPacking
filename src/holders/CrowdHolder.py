from direct.gui.DirectButton import DirectButton
from direct.gui.DirectFrame import DirectFrame
from panda3d.core import NodePath
from pandas import DataFrame

from src.holders.CarouselHolder import CarouselHolder
from src.holders.Holder import positions
from direct.gui import DirectGuiGlobals as DGG


class Crowd(NodePath):
    def __init__(self, data):
        super().__init__("Crowd")
        self.data = data
        self.active = True
        self.frame=DirectButton(
            relief=DGG.RIDGE,
            borderWidth=(0.02, 0.02),
            frameSize=(-0.1, 0.1, -0.1, 0.1),
            pos=(0, 0, 0),
            parent=self,
            command=self.command,
            text=f"{data["Capacity"].mean():.2f}\n#{data.shape[0]}",
            text_scale=0.06,
        )
    def command(self):
        print(self.data)


class CrowdHolder(CarouselHolder):
    def __init__(self):
        super().__init__(Crowd, (0, 0, 0), 1)
        self.crowds = []

    def addition(self, add):
        if isinstance(add, DataFrame):
            add = Crowd(add)
        if not add:
            self.notify.error("Cannot add None to Holder")
            return
        if not isinstance(add, self.item_type):
            self.notify.warning(f"Only {self.item_type.__name__} instances can be added to Holder")
            return
        add.reparent_to(self.frame)
        self.collection.append(add)
        self.rearrange()
        if len(self.collection) > len(positions):
            self.right_button['state'] = DGG.NORMAL
