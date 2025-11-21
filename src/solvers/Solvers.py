from direct.gui.DirectButton import DirectButton
from direct.gui.DirectFrame import DirectFrame

from src.solvers.Greedy import Greedy


class Solvers:
    def __init__(self, item_holder, container_holder, problem):
        self.frame = DirectFrame(
            frameColor=(0.8, 0.8, 0.8, 1),
            frameSize=(-0.75, 0.75, -0.1, 0.1),
            pos=(0, 0, -.45),
            text="Solvers",
            text_scale=0.05,
            text_pos=(-0.65, 0.06),
        )

        greedy = Greedy(item_holder, container_holder, problem)
        self.greedy = DirectButton(
            parent=self.frame,
            text="Greedy Solver",
            scale=0.05,
            pos=(-0.5, 0, 0),
            command=greedy.solve
        )
