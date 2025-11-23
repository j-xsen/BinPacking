from direct.gui.DirectButton import DirectButton
from direct.gui.DirectLabel import DirectLabel
from direct.showbase.DirectObject import DirectObject

from src.holders.CarouselHolder import CarouselHolder
from src.holders.Container import Container
from src.holders.Holder import Holder


class ContainerHolder(CarouselHolder, DirectObject):
    def __init__(self):
        super().__init__(Container, (0, 0, 0.7), 1, 'ContainerHolder')

        self.capacity=5

        self.create_new_container_button = DirectButton(
            text="Create New Container",
            scale=0.07,
            pos=(0, 0, 0.88),
            command=self.create_new_container
        )

        self.container_number = DirectLabel(
            text="#0",
            parent=base.a2dTopLeft,
            scale=0.08,
            pos=(.4,0,-0.15),
            frameColor=(0,0,0,0),
            text_fg=(1,1,1,1),
        )

        self.accept("container-clicked", self.click_container)

    def click_container(self, item):
        super().on_item_clicked(item)

    def reset(self):
        super().reset()
        self.container_number.setText("#0")

    def addition(self, add):
        super().addition(add)

        self.container_number.setText(f"#{str(len(self.collection))}")

    def set_capacity(self, cap):
        self.capacity = cap

    def create_new_container(self):
        new_container = Container(capacity=self.capacity)
        self.addition(new_container)
        return new_container