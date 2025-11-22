from direct.showbase.MessengerGlobal import messenger


class FirstFit:
    """
    Places each item in the first container that can contain it.
    """
    def __init__(self, item_holder, container_holder, problem):
        self.item_holder = item_holder
        self.container_holder = container_holder
        self.problem = problem

    def solve(self):
        self.item_holder.deselect()
        self.container_holder.deselect()
        for item in self.item_holder.collection:
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