from direct.gui.DirectButton import DirectButton
from direct.gui import DirectGuiGlobals as DGG

from src.holders.Holder import Holder, positions


class CarouselHolder(Holder):
    def __init__(self, item_class, pos, item_scale, name='CarouselHolder'):
        super().__init__(item_class,pos,item_scale, name)
        self.current_offset = 0
        self.left_button = DirectButton(
            text="<",
            parent=self.frame,
            scale=0.1,
            pos=(-1.2, 0, -0.03),
            command=self.move_left,
            frameColor=((.9, .9, .9, .9),
                        (0.9, 0.9, 0.9, 1),
                        (0.8, 0.8, 0.8, 1),
                        (0.2, 0.2, 0.2, 1)),
            state=DGG.DISABLED
        )
        self.right_button = DirectButton(
            text=">",
            parent=self.frame,
            scale=0.1,
            pos=(1.2, 0, -0.03),
            command=self.move_right,
            frameColor=((.9, .9, .9, .9),
                        (0.9, 0.9, 0.9, 1),
                        (0.8, 0.8, 0.8, 1),
                        (0.2, 0.2, 0.2, 1)),
            state=DGG.DISABLED
        )

    def reset(self):
        super().reset()
        self.current_offset = 0
        self.left_button['state'] = DGG.DISABLED
        self.right_button['state'] = DGG.DISABLED

    def addition(self, add):
        super().addition(add)

        if len(self.collection) > len(positions):
            self.right_button['state'] = DGG.NORMAL

    def move_left(self):
        self.current_offset -= 1

        if self.current_offset < 1:
            self.left_button['state'] = DGG.DISABLED
        if self.current_offset + len(positions) < len(self.collection):
            self.right_button['state'] = DGG.NORMAL

        self.rearrange()

    def move_right(self):
        self.current_offset += 1

        if self.current_offset > 0:
            self.left_button['state'] = DGG.NORMAL
        if self.current_offset + len(positions) >= len(self.collection):
            self.right_button['state'] = DGG.DISABLED

        self.rearrange()
