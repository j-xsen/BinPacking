from direct.directnotify.Notifier import Notifier
from direct.showbase.MessengerGlobal import messenger


class FirstFitDecreasing(Notifier):
    """
    Sort items in decreasing order by weight,
    then place each item in the first container that can contain it
    """
    def __init__(self, item_holder, container_holder, problem):
        super().__init__("FirstFitDecreasing")
        self.setDebug(True)
        self.item_holder = item_holder
        self.container_holder = container_holder
        self.problem = problem

    def solve(self):
        self.item_holder.deselect()
        self.container_holder.deselect()

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

        self.item_holder.deselect()
        self.container_holder.deselect()