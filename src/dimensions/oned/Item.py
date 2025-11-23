from direct.gui.DirectButton import DirectButton
from direct.gui.DirectLabel import DirectLabel
from direct.gui import DirectGuiGlobals as DGG

from src.IDNodePath import IDNodePath
from src.Colors import unselect_colors, selected_colors


class Item(IDNodePath):
    def __init__(self, weight=0):
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
            text=f"{weight}",
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

        self.weight = weight

    def select(self):
        self.frame["frameColor"] = selected_colors
        self.show()

    def deselect(self):
        self.frame["frameColor"] = unselect_colors

    def destroy(self):
        self.frame.destroy()
        self.uid_text.destroy()
        super().destroy()

    @property
    def weight(self):
        return self._weight
    @weight.setter
    def weight(self, value):
        self.frame.setText(f"{value}")
        self._weight = value

    def __str__(self):
        return f"Item-{self.uid} ({self.weight})"
