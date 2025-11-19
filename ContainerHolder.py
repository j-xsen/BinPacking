from Container import Container
from Holder import Holder


class ContainerHolder(Holder):
    def __init__(self):
        super().__init__('ContainerHolder')

    def addition(self, add):
        if type(add) != Container:
            self.notify.warning("Only Container instances can be added to ContainerHolder")
            return
        self.notify.debug(f"Adding Container {add.get_name()} to ContainerHolder")
        add.reparent_to(self)
        self.collection.append(add)
        self.notify.debug(f"Container {add.get_name()} added to ContainerHolder")