from direct.showbase.MessengerGlobal import messenger
from panda3d.core import NodePath


class GreedyValue(NodePath):
    """
    For knapsack problem (variation of bin packing),
     a constant number of containers,
     places each item in order of decreasing value/weight ratio
    """
    def __init__(self, item_holder, container_holder, problem):
        super().__init__('GreedyValueSolver')
        self.notify = directNotify.newCategory("GreedyValue")
        self.item_holder = item_holder
        self.container_holder = container_holder
        self.problem = problem

    def solve(self):
        if len(self.container_holder.collection) == 0:
            self.notify.warning("No containers available to place items in.")
            return

        self.item_holder.deselect()
        self.container_holder.deselect()

        if hasattr(self.item_holder.collection[0], 'value') is False or hasattr(self.item_holder.collection[0], 'weight') is False:
            self.notify.warning("Items do not have 'value' or 'weight' attributes required for GreedyValue solver.")
            return

        for item in sorted(self.item_holder.collection, key=lambda x: x.value / x.weight, reverse=True):
            if not item.active:
                continue
            messenger.send("item-clicked", [item])
            for cur_bin in self.container_holder.collection:
                if cur_bin.can_add(item):
                    messenger.send("container-clicked", [cur_bin])
                    break

        self.item_holder.deselect()
        self.container_holder.deselect()