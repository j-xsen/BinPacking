from direct.showbase.MessengerGlobal import messenger


class Greedy:
    def __init__(self, item_holder, container_holder, problem):
        self.item_holder = item_holder
        self.container_holder = container_holder
        self.problem = problem

    def solve(self):
        cur_bins = self.container_holder.collection
        for item in self.item_holder.collection:
            if not item.active:
                continue
            messenger.send("item-clicked", [item])
            placed = False
            for bin in cur_bins:
                if bin.can_add(item):
                    messenger.send("container-clicked", [bin])
                    placed=True
                    continue
            if not placed:
                new_container = self.container_holder.create_new_container()
                if new_container.can_add(item):
                    messenger.send("container-clicked", [new_container])
