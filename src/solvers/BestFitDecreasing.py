from direct.directnotify.Notifier import Notifier
from direct.showbase.MessengerGlobal import messenger


class BestFitDecreasing(Notifier):
    """
    Places each item in the least filled container that can contain it.
    """
    def __init__(self, item_holder, container_holder, problem):
        super().__init__("BestFitDecreasing")

        self.setDebug(True)

        self.item_holder = item_holder
        self.container_holder = container_holder
        self.problem = problem

    def solve(self):
        self.item_holder.deselect()
        self.container_holder.deselect()

        cur_bins = self.container_holder.collection
        for item in sorted(self.item_holder.collection, key=lambda x: int(x.weight), reverse=True):
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
                best_bin = self.container_holder.create_new_container()
                best_remain = best_bin.get_remainder()

            if best_bin.can_add(item):
                item.show()
                messenger.send("item-clicked", [item])
                messenger.send("container-clicked", [best_bin])

        self.item_holder.deselect()
        self.container_holder.deselect()