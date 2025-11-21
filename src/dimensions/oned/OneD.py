from panda3d.core import NodePath

from src.holders.ContainerHolder import ContainerHolder
from src.holders.ItemHolder import ItemHolder


class OneD(NodePath):
    def __init__(self):
        super().__init__('1DView')
        self.item_holder = ItemHolder()
        self.container_holder = ContainerHolder()

        camera.set_pos(101.66,-124.8,13.74)

        self.item_holder.reparent_to(self)
        self.item_holder.create_new_item()
        self.container_holder.reparent_to(self)
        self.container_holder.create_new_container()

    def render(self):
        return f"Rendering 1D view with data: {self.data}"