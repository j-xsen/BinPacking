from direct.gui.DirectButton import DirectButton
from direct.gui.DirectFrame import DirectFrame
from direct.gui.DirectLabel import DirectLabel
from direct.gui.OnscreenText import OnscreenText
from panda3d.core import NodePath, TextNode
from direct.gui import DirectGuiGlobals as DGG

from IDNodePath import IDNodePath
from colors import unselect_colors, selected_colors


class Item(IDNodePath):
    def __init__(self, value=0):
        super().__init__('Item')

        self.set_name(f"I-{self.uid}")

        self.active = True

        self.frame = DirectButton(
            parent=self,
            command=lambda: messenger.send("item-clicked", [self]),
            frameColor=unselect_colors,
            relief=DGG.RIDGE,
            borderWidth=(0.02, 0.02),
            frameSize=(-0.1, 0.1, -0.1, 0.1),
            pos=(0, 0, 0),
            text=f"{value}",
            text_scale=0.07,
        )

        self.uid_text = DirectLabel(
            parent=self.frame,
            text=f"{self.uid}",
            scale=0.05,
            pos=(0.04, 0, -0.085),
            frameColor=(0, 0, 0, 0),
            text_fg=(0, 0, 0, 0.5),
        )

        self.value = value

    def select(self):
        self.frame["frameColor"] = selected_colors

    def deselect(self):
        self.frame["frameColor"] = unselect_colors

    @property
    def value(self):
        return self._value
    @value.setter
    def value(self, value):
        self.frame.setText(f"{value}")
        self._value = value
