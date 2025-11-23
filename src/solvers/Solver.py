import random
import time

import pandas as pd
import seaborn as sns
from direct.directnotify.Notifier import Notifier
from matplotlib import pyplot as plt

from src.holders.ContainerHolder import ContainerHolder
from src.holders.ItemHolder import ItemHolder


class Solver(Notifier):
    def __init__(self, dimension, name="Solver"):
        if not isinstance(dimension.item_holder, ItemHolder):
            raise TypeError("item_holder must be an instance of ItemHolder")
        if not isinstance(dimension.container_holder, ContainerHolder):
            raise TypeError("container_holder must be an instance of ContainerHolder")
        super().__init__(name)
        self.item_holder = dimension.item_holder
        self.container_holder = dimension.container_holder
        self.problem = dimension.problem_loader.loaded_problem
        self.crowd_holder = dimension.crowd_holder
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

    def vary(self):
        REMOVE_ITEM_CHANCE = 0.25
        PUT_BACK_CHANCE = 0.5
        END_VARY_CHANCE = 0.1
        if not self.solution_data:
            self.warning("No solution data to vary.")
        else:
            done = False
            while not done:
                removed = None
                removed_from = None
                added_to = None
                for item in self.solution_data:
                    if not item['items']:
                        continue
                    if not removed:
                        if random.random() < REMOVE_ITEM_CHANCE:
                            self.debug(f"Removing from {item['items']}")
                            removed = min(item['items'])
                            item['items'].remove(removed)
                            removed_from = item
                    else:
                        sum_items = 0
                        for i in item['items']:
                            sum_items += int(i)
                        maxim = int(self.problem.bin_capacity)
                        if sum_items + int(removed) <= maxim:
                            self.debug(f"Adding {removed} to {item}")
                            item['items'].append(removed)
                            added_to = item
                            break
                if removed and not added_to:
                    if random.random() < PUT_BACK_CHANCE:
                        # put back
                        self.debug(f"Putting back {removed} to {removed_from}")
                        removed_from['items'].append(removed)
                    else:
                        # make new container
                        self.debug(f"Creating new container for {removed}")
                        self.solution_data.append({
                            'items': [removed],
                            'Capacity': int(removed)/int(self.problem.bin_capacity),})
                if random.random() < END_VARY_CHANCE:
                    done = True


    def solve(self):
        if hasattr(self.item_holder,"collection") and len(self.item_holder.collection)==0\
                and len(self.container_holder.collection)==0:
            self.warning(f"No items to solve for in {self.item_holder}")
            return False
        if self.start_time == -1:
            self.start_time = time.perf_counter()
        self.item_holder.deselect()
        self.container_holder.deselect()
        return True

    def solved(self):
        if len(self.container_holder.collection)==0:
            self.warning("No solution data recorded yet.")
            return False
        end_time = time.perf_counter()

        # create dataframe for solution
        solution_data = []
        for container in self.container_holder.collection:
            items_in_container = [item.weight for item in container.collection]
            solution_data.append({
                'items': items_in_container,
                'sum': container.carrying,
                'Capacity': container.carrying/container.capacity,
                'time': end_time - self.start_time
            })
        if len(solution_data)==0:
            self.warning("No solution data recorded yet.")
            return False
        self.solution_data = solution_data

        # perform variation on solution
        self.vary()

        # clean solution data
        new_solution = []
        for s in solution_data:
            if s['items']:
                sum_items = 0
                for i in s['items']:
                    sum_items += int(i)
                maxim = int(self.problem.bin_capacity)
                if sum_items > maxim:
                    self.error(f"Container over capacity: {s['items']} with total {sum_items} > {maxim}")
                cap = sum_items / maxim
                s['Capacity'] = cap
                s['sum'] = sum_items
                new_solution.append(s)

        self.crowd_holder.addition(pd.DataFrame(new_solution))
        self.start_time = -1

        # adjust for variations
        self.crowd_holder.collection[-1].command()
        return True
