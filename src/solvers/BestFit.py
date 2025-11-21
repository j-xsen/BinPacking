from direct.showbase.MessengerGlobal import messenger


class BestFit:
    def __init__(self, item_holder, container_holder, problem):
        self.item_holder = item_holder
        self.container_holder = container_holder
        self.problem = problem

    def solve(self):
        self.item_holder.deselect()
        self.container_holder.deselect()

        cur_bins = self.container_holder.collection
        for item in self.item_holder.collection:
            if not item.active:
                continue
            print(f"Checking item {item}")
            # find least filled container
            best_bin = None
            best_remain = 0
            if len(cur_bins) != 0:
                for cur_bin in cur_bins:
                    remain = cur_bin.get_remainder()
                    if best_remain < remain:
                        best_remain = remain
                        best_bin = cur_bin
            if not best_bin or not best_bin.can_add(item):
                best_bin = self.container_holder.create_new_container()
                best_remain = best_bin.get_remainder()
                print(f"best_remain {best_remain}")

            if best_bin.can_add(item):
                messenger.send("item-clicked", [item])
                messenger.send("container-clicked", [best_bin])

        self.item_holder.deselect()
        self.container_holder.deselect()