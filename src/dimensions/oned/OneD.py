from direct.gui.DirectButton import DirectButton
from panda3d.core import NodePath

from src.ProblemLoader import ProblemLoader
from src.solvers.Solvers import Solvers
from src.holders.ContainerHolder import ContainerHolder
from src.holders.ItemHolder import ItemHolder


class OneD(NodePath):
    def __init__(self):
        super().__init__('1DView')
        self.item_holder = ItemHolder()
        self.container_holder = ContainerHolder()

        camera.set_pos(101.66,-124.8,13.74)

        self.item_holder.reparent_to(self)
        self.container_holder.reparent_to(self)

        self.problem_loader = ProblemLoader(self.item_holder, self.container_holder)
        self.problem_loader.load("problem50")

        self.reset_button = DirectButton(
            text="Reset",
            scale=0.05,
            parent=base.a2dBottomLeft,
            pos=(0.2,0,0.075),
            command=self.reset
        )

        self.solvers = Solvers(self.item_holder, self.container_holder, self.problem_loader.loaded_problem)

    def reset(self):
        self.item_holder.reset()
        self.container_holder.reset()
        self.problem_loader.load("problem1")

    def render(self):
        return f"Rendering 1D view with data: {self.data}"