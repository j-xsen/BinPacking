from direct.gui.DirectButton import DirectButton
from direct.gui.DirectFrame import DirectFrame
from panda3d.core import NodePath
from pandas import DataFrame

from src.crowds.Crowd import Crowd
from src.crowds.CrowdControl import CrowdControl
from src.holders.CarouselHolder import CarouselHolder
from src.holders.Holder import positions
from direct.gui import DirectGuiGlobals as DGG


class CrowdHolder(CarouselHolder):
    def __init__(self):
        super().__init__(Crowd, (0, 0, 0), 1)
        self._time = 0
        self.crowd_buttons = CrowdControl(self)
        self.past_generations = []

    @property
    def time(self):
        return self._time
    @time.setter
    def time(self, value):
        self._time = value

    def addition(self, add):
        if isinstance(add, DataFrame):
            add = Crowd(add)
        if not add:
            self.notify.error("Cannot add None to Holder")
            return
        if not isinstance(add, self.item_type):
            self.notify.warning(f"Only {self.item_type.__name__} instances can be added to Holder")
            return
        add.reparent_to(self.frame)
        self.collection.append(add)
        self.rearrange()
        if len(self.collection) > len(positions):
            self.right_button['state'] = DGG.NORMAL

    def new_generation(self):
        prev_collection = self.collection.copy()
        self.notify.debug(f"Appending generation with {len(prev_collection)} crowds")
        for i in prev_collection:
            i.hide()
        self.past_generations.append(prev_collection)
        self.notify.debug(f"Past generations: {self.past_generations[-1]}")
        self.collection.clear()
        self.rearrange()
