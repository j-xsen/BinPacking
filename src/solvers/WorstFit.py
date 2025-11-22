from direct.directnotify.Notifier import Notifier
from direct.showbase.MessengerGlobal import messenger

from src.solvers.Solver import Solver


class WorstFit(Notifier, Solver):
    """
    Places each item in the most filled container that can still contain it.
    """
    def __init__(self, item_holder, container_holder, problem, crowd_holder):
        super().__init__("WorstFit")
        Solver.__init__(self, item_holder, container_holder, problem, crowd_holder)
        self.setDebug(False)

    def solve(self):
        if not super().solve():
            return False

        cur_bins = self.container_holder.collection
        for i,item in enumerate(self.item_holder.collection[:]):
            if not item.active:
                continue

            self.debug("==========================")
            self.debug(f"Placing item {item} of weight {item.weight}")
            self.debug("==========================")

            # find most filled container
            best_bin = None
            if len(cur_bins) != 0:
                best_remain = float('inf')
                for cur_bin in cur_bins:
                    remain = cur_bin.get_remainder()
                    if int(remain) >= int(item.weight) and best_remain > remain:
                        self.debug(f"Found {cur_bin} (was {best_remain})")
                        best_remain = remain
                        best_bin = cur_bin
                    else:
                        self.debug(f"{cur_bin} cannot fit {item}")
            if not best_bin or not best_bin.can_add(item):
                best_bin = self.container_holder.create_new_container()

            if best_bin.can_add(item):
                messenger.send("item-clicked", [item])
                messenger.send("container-clicked", [best_bin])

        super().solve()

        return self.solved()