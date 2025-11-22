import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt


class Solver:
    def __init__(self, item_holder, container_holder, problem):
        self.item_holder = item_holder
        self.container_holder = container_holder
        self.problem = problem

        self.solution_data = []

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
        pass

    def solved(self):
        # Log the solution
        solution_data = []
        count=0
        for container in self.container_holder.collection:
            items_in_container = [item.uid for item in container.collection]
            solution_data.append({
                'ID': count,
                'items': items_in_container,
                'Capacity': container.carrying/container.capacity,
            })
            count+=1
        self.solution_data = solution_data

        self.retrieve_data()
