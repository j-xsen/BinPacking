import random
import time

from direct.gui.DirectButton import DirectButton
from direct.gui.DirectFrame import DirectFrame

from src.solvers.BestFit import BestFit
from src.solvers.BestFitDecreasing import BestFitDecreasing
from src.solvers.FirstFit import FirstFit
from src.solvers.FirstFitDecreasing import FirstFitDecreasing
from src.solvers.WorstFit import WorstFit


class Solvers:
    def __init__(self, dimension):
        self.frame = DirectFrame(
            frameColor=(0.8, 0.8, 0.8, 1),
            frameSize=(-0.75, 0.75, -0.1, 0.1),
            pos=(0, 0, -.45),
            text="Solvers",
            text_scale=0.05,
            text_pos=(-0.65, 0.06),
        )

        self.dimension = dimension

        first_fit = FirstFit(dimension)
        self.first_fit = DirectButton(
            parent=self.frame,
            text="First Fit",
            scale=0.05,
            pos=(-0.4, 0, 0),
            command=first_fit.solve
        )

        first_fit_decreasing = FirstFitDecreasing(dimension)
        self.first_fit_decreasing = DirectButton(
            parent=self.frame,
            text="First Fit Decreasing",
            scale=0.05,
            pos=(-0.4, 0, -.07),
            command=first_fit_decreasing.solve
        )

        best_fit = BestFit(dimension)
        self.best_fit = DirectButton(
            parent=self.frame,
            text="Best Fit",
            scale=0.05,
            pos=(0.4, 0, 0),
            command=best_fit.solve
        )

        best_fit_decreasing = BestFitDecreasing(dimension)
        self.best_fit_decreasing = DirectButton(
            parent=self.frame,
            text="Best Fit Decreasing",
            scale=0.05,
            pos=(0.4, 0, -.07),
            command=best_fit_decreasing.solve
        )

        worst_fit = WorstFit(dimension)
        self.worst_fit = DirectButton(
            parent=self.frame,
            text="Worst Fit",
            scale=0.05,
            pos=(0, 0, 0),
            command=worst_fit.solve
        )

        self.solvers = [first_fit, first_fit_decreasing,
                        best_fit, best_fit_decreasing,
                        worst_fit]

        gen_ten = DirectButton(
            parent=self.frame,
            text="Run 10 times",
            scale=0.05,
            pos=(0, 0, .1),
            command=self.generate_x,
            extraArgs=[10]
        )

    def generate_x(self, x):
        start = time.perf_counter()
        for _ in range(x):
            new_solver = random.choice(self.solvers)
            new_solver.solve()
            self.dimension.reset()
        end = time.perf_counter()
        self.dimension.crowd_holder.time = end - start
