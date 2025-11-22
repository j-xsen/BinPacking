import time

import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt

from src.holders.ContainerHolder import ContainerHolder
from src.holders.ItemHolder import ItemHolder


class Solver:
    def __init__(self, item_holder, container_holder, problem, crowd_holder):
        if not isinstance(item_holder, ItemHolder):
            raise TypeError("item_holder must be an instance of ItemHolder")
        if not isinstance(container_holder, ContainerHolder):
            raise TypeError("container_holder must be an instance of ContainerHolder")
        self.item_holder = item_holder
        self.container_holder = container_holder
        self.problem = problem
        self.crowd_holder = crowd_holder
        self.solution_data = []
        self.start_time = -1

    def reset(self):
        for container in self.container_holder.collection:
            container.reset()
        for item in self.item_holder.collection:
            item.reset()
        self.start_time = 0

    def retrieve_data(self):
        df = pd.DataFrame(self.solution_data)
        print(f"Mean: {df['Capacity'].mean()}")
        sns.set_theme()
        sns.barplot(
            data=df,
            x='ID',
            y='Capacity',
            legend='full'
        )
        plt.show()

    def solve(self):
        if self.start_time == -1:
            self.start_time = time.perf_counter()
        if hasattr(self.item_holder,"collection") and len(self.item_holder.collection)==0:
            return False
        self.item_holder.deselect()
        self.container_holder.deselect()
        return True

    def solved(self):
        end_time = time.perf_counter()
        # Log the solution
        solution_data = []
        count=0
        for container in self.container_holder.collection:
            items_in_container = [item.weight for item in container.collection]
            solution_data.append({
                'ID': count,
                'items': items_in_container,
                'Capacity': container.carrying/container.capacity,
                'time': end_time - self.start_time
            })
            count+=1
        self.solution_data = solution_data
        self.crowd_holder.addition(pd.DataFrame(self.solution_data))
