from direct.gui.DirectButton import DirectButton
from direct.showbase.DirectObject import DirectObject

from src.holders.Container import Container
from src.holders.Holder import Holder


class ContainerHolder(Holder, DirectObject):
    def __init__(self):
        super().__init__(Container, (0, 0, 0.7), 1, 'ContainerHolder')

        self.create_new_container_button = DirectButton(
            text="Create New Container",
            scale=0.07,
            pos=(0, 0, 0.88),
            command=self.create_new_container
        )

        self.accept("container-clicked", self.on_item_clicked)

    def create_new_container(self):
        new_container = Container(capacity=5)
        self.addition(new_container)