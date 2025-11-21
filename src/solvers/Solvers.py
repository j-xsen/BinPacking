from direct.gui.DirectButton import DirectButton
from direct.gui.DirectFrame import DirectFrame

from src.solvers.BestFit import BestFit
from src.solvers.GreedyValue import GreedyValue
from src.solvers.GreedyWeight import GreedyWeight


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

        greedy_weight = GreedyWeight(item_holder, container_holder, problem)
        self.greedy = DirectButton(
            parent=self.frame,
            text="Greedy Weight Solver",
            scale=0.05,
            pos=(-0.4, 0, 0),
            command=greedy_weight.solve
        )

        greedy_value = GreedyValue(item_holder, container_holder, problem)
        self.greedy_value = DirectButton(
            parent=self.frame,
            text="Greedy Value Solver",
            scale=0.05,
            pos=(0.4, 0, 0),
            command=greedy_value.solve
        )
        self.greedy_value.hide()

        best_fit = BestFit(item_holder, container_holder, problem)
        self.best_fit = DirectButton(
            parent=self.frame,
            text="Best Fit Solver",
            scale=0.05,
            pos=(0.4, 0, 0),
            command=best_fit.solve
        )
