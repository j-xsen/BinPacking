from direct.directnotify.Notifier import Notifier
from direct.showbase.MessengerGlobal import messenger

from src.solvers.Solver import Solver


class FirstFitDecreasing(Solver):
    """
    Sort items in decreasing order by weight,
    then place each item in the first container that can contain it
    """
    def __init__(self, dimension):
        super().__init__(dimension,"FirstFitDecreasing")

    def solve(self):
        if not super().solve():
            return False

        for item in sorted(self.item_holder.collection, key=lambda x: int(x.weight), reverse=True):
            if not item.active:
                continue
            cur_bins = self.container_holder.collection
            item.show()
            self.debug("==========================")
            self.debug(f"Placing {item}")
            self.debug("==========================")
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

        super().solve()

        return self.solved()