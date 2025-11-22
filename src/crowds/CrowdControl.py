from direct.gui.DirectFrame import DirectFrame
from panda3d.core import NodePath


class CrowdControl(NodePath):
    def __init__(self):
        super().__init__("CrowdButtons")
        self.frame = DirectFrame(
            frameColor=(0.8, 0.8, 0.8, 1),
            frameSize=(-1, 1, -.05, .05),
            pos=(0, 0, -.2),
            text="Crowd Control",
            text_scale=0.05,
            text_pos=(-.8, 0.06),
            text_fg=(1,1,1, 1),
        )
