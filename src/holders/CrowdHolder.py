from direct.gui.DirectButton import DirectButton
from direct.gui.DirectFrame import DirectFrame
from direct.gui.DirectLabel import DirectLabel
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

        self.avg_containers_per_crowd_label = DirectLabel(
            parent=self.frame,
            text="Avg Containers/Solution: 0",
            scale=0.05,
            text_fg=(1, 1, 1, 1),
            frameColor=(0, 0, 0, 0),
            pos=(-.8, 0, 0.12),
        )
        self.solution_number_label = DirectLabel(
            parent=self.frame,
            text="Solutions#: 0",
            scale=0.05,
            text_fg=(1, 1, 1, 1),
            frameColor=(0, 0, 0, 0),
            pos=(.5, 0, 0.12),
        )
        self._gen_count = 0
        self.gen_count_label = DirectLabel(
            parent=self.frame,
            text="Generation 0",
            scale=0.05,
            text_fg=(1, 1, 1, 1),
            frameColor=(0, 0, 0, 0),
            pos=(1, 0, 0.12),
        )
        self.show_generated_graph_btn = DirectButton(
            parent=self.frame,
            text="Show Generation Graph",
            scale=0.05,
            pos=(0, 0, 0.12),
            command=self.show_generation_graph,
        )

    @property
    def time(self):
        return self._time
    @time.setter
    def time(self, value):
        self._time = value

    def rearrange(self):
        super().rearrange()
        if len(self.collection) > 0:
            total_containers = sum(len(crowd) for crowd in self.collection)
            avg = total_containers / len(self.collection)
        else:
            avg = 0
        self.avg_containers_per_crowd_label['text'] = f"Avg Containers/Crowd: {avg:.2f}"
        self.solution_number_label['text'] = f"Solutions#: {len(self.collection)}"
        self.gen_count_label['text'] = f"Generation {len(self.past_generations)}"

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

    def show_generation_graph(self):
        import matplotlib.pyplot as plt

        generations = list(range(len(self.past_generations)))
        avg_containers = []
        for generation in self.past_generations:
            if len(generation) > 0:
                total_containers = sum(len(crowd) for crowd in generation)
                avg = total_containers / len(generation)
            else:
                avg = 0
            avg_containers.append(avg)

        plt.plot(generations, avg_containers, marker='o')
        plt.title('Average Containers per Crowd over Generations')
        plt.xlabel('Generation')
        plt.ylabel('Average Containers per Crowd')
        plt.xticks(generations)
        plt.grid()
        plt.show()
