import time
from enum import Enum
import random

from direct.directnotify.Notifier import Notifier
from direct.gui.DirectButton import DirectButton
from direct.showbase.DirectObject import DirectObject

from src.solvers.Solver import Solver


class CrossoverTypes(Enum):
    ONE_POINT = 'one_point'


class MutationTypes(Enum):
    SCRAMBLE = 'scramble'


class Breeder(Solver):
    def __init__(self, crowd_control):
        super().__init__(None, "Breeder")
        Notifier.__init__(self, "Breeder")
        self.setDebug(True)
        self.btn = DirectButton(
            text="Breed",
            scale=0.07,
            pos=(-.875, 0, -.02),
            command=self.breed_x,
            extraArgs=[10],
            parent=crowd_control.frame,
        )
        self.crowd_control = crowd_control

    def breed_x(self, x, parent_pool_percent=0.5):
        self.set_dimension(base.dimension)
        crowd_copy = self.crowd_holder.collection.copy()
        sorted_crowd = sorted(
            crowd_copy,
            key=lambda c: int(c),
        )[: max(2, int(len(crowd_copy) * parent_pool_percent))]
        if len(sorted_crowd) < 2:
            self.warning("Not enough crowd members to breed from!")
            return
        new_crowds = []
        for _ in range(x):
            # pick parents
            parent_one = random.choice(sorted_crowd)
            parent_two = None
            while not parent_two:
                candidate = random.choice(sorted_crowd)
                if candidate != parent_one:
                    parent_two = candidate
            data = self.breed(parent_one, parent_two)
            new_crowds.append(data)
        self.crowd_holder.new_generation()
        for data in new_crowds:
            self.crowd_holder.addition(data)

    def breed(self, parent_one, parent_two):
        self.debug(f"Breeding {parent_one} and {parent_two}")
        # reset
        base.dimension.reset()

        self.start_time = time.perf_counter()

        # select crossover type
        crossover_type = random.choice(list(CrossoverTypes))
        # select mutation type
        mutation_type = random.choice(list(MutationTypes))

        self.debug(f"Crossover type: {crossover_type}, Mutation type: {mutation_type}")

        if crossover_type == CrossoverTypes.ONE_POINT:
            point = random.randint(1, max(len(parent_one.data["items"]),
                                          len(parent_two.data["items"])) - 1)
            self.debug(f"One-point crossover at point {point}")
            for idc, container in enumerate(parent_one.data["items"]):
                items_to_add = []
                if idc < point or idc >= len(parent_two.data["items"]):
                    items_to_add=container
                else:
                    items_to_add=parent_two.data["items"][idc]
                new_cont = base.dimension.container_holder.create_new_container()
                for item in items_to_add:
                    messenger.send("container-clicked", [new_cont])
                    messenger.send("item-clicked", [item])
        else:
            self.warning(f"Crossover type {crossover_type} not implemented")
            return False

        # crossover correction
        while base.dimension.item_holder.collection:
            item = base.dimension.item_holder.collection[0]
            if not item.active:
                continue
            placed = False
            for container in base.dimension.container_holder:
                if container.can_add(item):
                    self.debug(f"Placing item {item} into existing container {container}")
                    messenger.send("container-clicked", [container])
                    placed = True
                    break
            if not placed:
                self.debug(f"Creating new container for item {item}")
                new_cont = base.dimension.container_holder.create_new_container()
                messenger.send("container-clicked", [new_cont])
            messenger.send("item-clicked", [item])

        # remove duplicates
        items = self.problem.items.copy()
        while len(items) > 0:
            item = items[0]
            count_in_offspring = 0
            for container in base.dimension.container_holder.collection:
                count_in_offspring += container.collection.count(item)
            count_in_parents = 0
            for container in parent_one.data["items"]:
                count_in_parents += container.count(item)
            for container in parent_two.data["items"]:
                count_in_parents += container.count(item)
            if count_in_offspring > count_in_parents:
                # remove duplicates
                to_remove = count_in_offspring - count_in_parents
                self.debug(f"Removing {to_remove} duplicates of item {item} from offspring")
                for container in base.dimension.container_holder.collection:
                    while item in container.collection and to_remove > 0:
                        messenger.send("container-clicked", [container])
                        messenger.send("item-clicked", [item])
                        to_remove -= 1
                        if to_remove == 0:
                            break
            items = [i for i in items if i != item]

        end_time = time.perf_counter()
        new_data = self.create_data_frame(end_time)
        if new_data['sum'].sum() != parent_one.data['sum'].sum() and \
                new_data['sum'].sum() != parent_two.data['sum'].sum():
            self.error(f"Breeding resulted in invalid total sum of items!\n"
                         f"Parent one sum: {parent_one.data['sum'].sum()}\n"
                         f"Parent two sum: {parent_two.data['sum'].sum()}\n"
                         f"Offspring sum: {new_data['sum'].sum()}")

        base.dimension.deselect()

        return new_data