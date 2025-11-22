from direct.gui.DirectButton import DirectButton
from panda3d.core import NodePath
from direct.gui import DirectGuiGlobals as DGG


class Crowd(NodePath):
    def __init__(self, data):
        super().__init__("Crowd")
        self.time = data["time"][0]
        data.drop("time",axis=1,inplace=True)
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
        print(f"in {self.time:.5f}s")
