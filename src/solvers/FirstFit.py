from direct.showbase.MessengerGlobal import messenger

from src.solvers.Solver import Solver


class FirstFit(Solver):
    """
    Places each item in the first container that can contain it.
    """
    def __init__(self, item_holder, container_holder, problem):
        super().__init__(item_holder, container_holder, problem)

    def solve(self):
        self.item_holder.deselect()
        self.container_holder.deselect()
        for i,item in enumerate(self.item_holder.collection[:]):
            cur_bins = self.container_holder.collection
            if not item.active:
                continue
            messenger.send("item-clicked", [item])
            placed = False
            for cur_bin in cur_bins:
                if placed:
                    break
                if cur_bin.can_add(item):
                    messenger.send("container-clicked", [cur_bin])
                    placed=True
                    continue
            if not placed:
                new_container = self.container_holder.create_new_container()
                if new_container.can_add(item):
                    messenger.send("container-clicked", [new_container])
        self.item_holder.deselect()
        self.container_holder.deselect()

        self.solved()