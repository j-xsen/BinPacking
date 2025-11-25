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
        if dimension:
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

    def set_dimension(self, dimension):
        if not isinstance(dimension.item_holder, ItemHolder):
            raise TypeError("item_holder must be an instance of ItemHolder")
        if not isinstance(dimension.container_holder, ContainerHolder):
            raise TypeError("container_holder must be an instance of ContainerHolder")
        self.item_holder = dimension.item_holder
        self.container_holder = dimension.container_holder
        self.problem = dimension.problem_loader.loaded_problem
        self.crowd_holder = dimension.crowd_holder

    def reset(self):
        for container in self.container_holder.collection:
            container.reset()
        for item in self.item_holder.collection:
            item.reset()
        self.start_time = 0

    def retrieve_data(self):
        df = pd.DataFrame(self.solution_data)
        sns.set_theme()
        sns.barplot(
            data=df,
            x='ID',
            y='Capacity',
            legend='full'
        )
        plt.show()

    def vary(self, sol=None):
        REMOVE_ITEM_CHANCE = 0.25
        PUT_BACK_CHANCE = 0.5
        END_VARY_CHANCE = 0.1
        if sol:
            use_sol = sol
        else:
            use_sol = self.solution_data
        if isinstance(use_sol, pd.DataFrame):
            if use_sol.empty:
                self.error("Solution data is empty")
        elif not use_sol:
            self.error(f"No solution data to vary. {use_sol}")
        else:
            done = False
            while not done:
                removed = None
                removed_from = None
                added_to = None
                for item in use_sol:
                    if not item['items']:
                        continue
                    if not removed:
                        if random.random() < REMOVE_ITEM_CHANCE:
                            self.debug(f"Removing from {item['items']}")
                            removed = min(item['items'])
                            item['items'].remove(removed)
                            item['sum'] -= int(removed)
                            item['Capacity'] = item['sum'] / int(self.problem.bin_capacity)
                            removed_from = item
                    else:
                        sum_items = 0
                        for i in item['items']:
                            sum_items += int(i)
                        maxim = int(self.problem.bin_capacity)
                        if sum_items + int(removed) <= maxim:
                            self.debug(f"Adding {removed} to {item}")
                            item['items'].append(removed)
                            item['sum'] += int(removed)
                            item['Capacity'] = item['sum'] / int(self.problem.bin_capacity)
                            added_to = item
                            break
                if removed and not added_to:
                    if random.random() < PUT_BACK_CHANCE:
                        # put back
                        self.debug(f"Putting back {removed} to {removed_from}")
                        removed_from['items'].append(removed)
                        removed_from['sum'] += int(removed)
                        removed_from['Capacity'] = removed_from['sum'] / int(self.problem.bin_capacity)
                    else:
                        # make new container
                        self.debug(f"Creating new container for {removed}")
                        use_sol.append({
                            'items': [removed],
                            'sum': int(removed),
                            'Capacity': int(removed)/int(self.problem.bin_capacity),})
                if random.random() < END_VARY_CHANCE:
                    done = True
            for s in use_sol:
                if len(s['items']) == 0:
                    self.debug(f"Removing empty container {s} from solution")
                    use_sol.remove(s)
            self.solution_data = use_sol


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

    def create_data_frame(self, end_time):
        # create dataframe for solution
        solution_data = []
        for container in self.container_holder.collection:
            items_in_container = [item.weight for item in container.collection]
            solution_data.append({
                'items': items_in_container,
                'sum': container.carrying,
                'Capacity': container.carrying / container.capacity,
                'time': end_time - self.start_time
            })
        if len(solution_data) == 0:
            self.warning("No solution data recorded yet.")
            return False
        self.solution_data=solution_data
        return pd.DataFrame(self.solution_data)

    def solved(self):
        if len(self.container_holder.collection)==0:
            self.warning("No solution data recorded yet.")
            return False
        end_time = time.perf_counter()

        # create dataframe for solution
        solution_data = self.create_data_frame(end_time)
        if not isinstance(solution_data, pd.DataFrame):
            return False
        self.solution_data = solution_data

        # perform variation on solution
        self.vary()

        # clean solution data
        new_solution = []
        for index, row in self.solution_data.iterrows():
            if row['items']:
                sum_items = 0
                for i in row['items']:
                    sum_items += int(i)
                maxim = int(self.problem.bin_capacity)
                if sum_items > maxim:
                    self.error(f"Container over capacity: {row['items']} with total {sum_items} > {maxim}")
                cap = sum_items / maxim
                row['Capacity'] = cap
                row['sum'] = sum_items
                new_solution.append(row)

        self.crowd_holder.addition(pd.DataFrame(new_solution))
        self.start_time = -1

        # adjust for variations
        self.crowd_holder.collection[-1].command()
        return True
