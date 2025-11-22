from direct.gui.DirectButton import DirectButton
from direct.gui.DirectFrame import DirectFrame

from src.solvers.BestFit import BestFit
from src.solvers.BestFitDecreasing import BestFitDecreasing
from src.solvers.FirstFitDecreasing import FirstFitDecreasing
from src.solvers.GreedyValue import GreedyValue
from src.solvers.FirstFit import FirstFit
from src.solvers.WorstFit import WorstFit


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

        first_fit = FirstFit(item_holder, container_holder, problem)
        self.first_fit = DirectButton(
            parent=self.frame,
            text="First Fit",
            scale=0.05,
            pos=(-0.4, 0, 0),
            command=first_fit.solve
        )

        first_fit_decreasing = FirstFitDecreasing(item_holder, container_holder, problem)
        self.first_fit_decreasing = DirectButton(
            parent=self.frame,
            text="First Fit Decreasing",
            scale=0.05,
            pos=(-0.4, 0, -.07),
            command=first_fit_decreasing.solve
        )

        # greedy_value = GreedyValue(item_holder, container_holder, problem)
        # self.greedy_value = DirectButton(
        #     parent=self.frame,
        #     text="Greedy Value",
        #     scale=0.05,
        #     pos=(0.4, 0, 0),
        #     command=greedy_value.solve
        # )
        # self.greedy_value.hide()

        best_fit = BestFit(item_holder, container_holder, problem)
        self.best_fit = DirectButton(
            parent=self.frame,
            text="Best Fit",
            scale=0.05,
            pos=(0.4, 0, 0),
            command=best_fit.solve
        )

        best_fit_decreasing = BestFitDecreasing(item_holder, container_holder, problem)
        self.best_fit_decreasing = DirectButton(
            parent=self.frame,
            text="Best Fit Decreasing",
            scale=0.05,
            pos=(0.4, 0, -.07),
            command=best_fit_decreasing.solve
        )

        worst_fit = WorstFit(item_holder, container_holder, problem)
        self.worst_fit = DirectButton(
            parent=self.frame,
            text="Worst Fit",
            scale=0.05,
            pos=(0, 0, 0),
            command=worst_fit.solve
        )
