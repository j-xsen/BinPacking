import random

from direct.gui.DirectLabel import DirectLabel

from src.dimensions.oned.Item import Item


class ValuedItem(Item):
    def __init__(self, weight, value=random.randint(0,10)):
        super().__init__(weight=weight)

        self.set_name(f"V-{self.uid}")
        self.value = value
        self.value_text = DirectLabel(
            parent=self.frame,
            text=f"{self.value}",
            scale=0.05,
            pos=(0, 0, -.05),
            frameColor=(0, 0, 0, 0),
            text_fg=(0, 0, 0, 1),
        )
