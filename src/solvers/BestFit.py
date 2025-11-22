from direct.directnotify.Notifier import Notifier
from direct.showbase.MessengerGlobal import messenger

from src.solvers.Solver import Solver


class BestFit(Solver):
    """
    Places each item in the least filled container that can contain it.
    """
    def __init__(self, dimension):
        super().__init__(dimension, "BestFit")

    def solve(self):
        if not super().solve():
            return False

        cur_bins = self.container_holder.collection

        for i,item in enumerate(self.item_holder.collection[:]):
            if not item.active:
                continue

            self.debug("==========================")
            self.debug(f"Placing {item}")
            self.debug("==========================")

            # find least filled container
            best_bin = None
            best_remain = 0
            if len(cur_bins) != 0:
                for cur_bin in cur_bins:
                    remain = cur_bin.get_remainder()
                    if best_remain < remain:
                        self.debug(f"Found {cur_bin} (was {best_remain})")
                        best_remain = remain
                        best_bin = cur_bin
            if not best_bin or not best_bin.can_add(item):
                self.debug("Creating new container")
                best_bin = self.container_holder.create_new_container()
                best_remain = best_bin.get_remainder()

            if best_bin.can_add(item):
                self.debug(f"Placing {item} in {best_bin}")
                messenger.send("item-clicked", [item])
                messenger.send("container-clicked", [best_bin])

        super().solve()

        return self.solved()