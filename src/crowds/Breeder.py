import random

from direct.directnotify.Notifier import Notifier
from direct.gui.DirectButton import DirectButton
from direct.showbase.DirectObject import DirectObject

crossover_types = ['one_point', 'two_point', 'uniform']
mutation_types = ['swap', 'scramble']


class Breeder(DirectObject, Notifier):
    def __init__(self, crowd_control):
        super().__init__()
        Notifier.__init__(self, "Breeder")
        self.setDebug(True)
        self.btn = DirectButton(
            text="Breed",
            scale=0.07,
            pos=(-.875, 0, -.02),
            command=self.breed_x,
            extraArgs=[2],
            parent=crowd_control.frame,
        )
        self.crowd_control = crowd_control

    def breed_x(self, x, parent_pool_percent=0.3):
        crowd_copy = base.dimension.crowd_holder.collection.copy()
        sorted_crowd = sorted(
            crowd_copy,
            key=lambda c: int(c),
        )[: max(2, int(len(crowd_copy) * parent_pool_percent))]
        for _ in range(x):
            # pick parents
            parent_one = random.choice(sorted_crowd)
            parent_two = None
            while not parent_two:
                candidate = random.choice(sorted_crowd)
                if candidate != parent_one:
                    parent_two = candidate
            self.breed(parent_one, parent_two)

    def breed(self, parent_one, parent_two):
        self.debug(f"Breeding {parent_one} and {parent_two}")
        pass