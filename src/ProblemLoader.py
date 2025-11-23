import random


class Problem:
    def __init__(self, bin_capacity, items, name):
        self.bin_capacity = bin_capacity
        self.items = items
        self.name = name

    def __len__(self):
        return len(self.items)

    def __str__(self):
        return f"Problem(name={self.name}, bin_capacity={self.bin_capacity}, items={self.items})"

def load_problem(problem_name):
    problem_path = f"problems/{problem_name}.txt"
    try:
        with open(problem_path, 'r') as file:
            problem_data = file.read().splitlines()
            problem = Problem(
                bin_capacity=problem_data[0],
                items=list(map(str, problem_data[1].split())),
                name=problem_name
            )
        return problem
    except FileNotFoundError:
        raise Exception(f"Problem '{problem_name}' not found in directory 'problems/'.")


class ProblemLoader:
    def __init__(self, item_holder, container_holder):
        self.item_holder = item_holder
        self.container_holder = container_holder
        self.loaded_problem = None

    def load(self, problem):
        # get problem
        if type(problem) == str:
            problem = load_problem(problem)
        elif type(problem) != Problem:
            raise TypeError("Problem must be a string or Problem instance")

        # Clear existing items and containers
        self.item_holder.clear()
        self.container_holder.clear()

        # Load items
        for item_data in problem.items:
            if ":" in item_data:
                weight, value = map(int, item_data.split(":"))
                item = self.item_holder.create_new_valued_item(weight=weight, value=value)
            else:
                item = self.item_holder.create_new_item(weight=item_data)

        if ":" in problem.bin_capacity:
            capacity, count = map(int, problem.bin_capacity.split(":"))
            self.container_holder.set_capacity(capacity)
            for i in range(count):
                self.container_holder.create_new_container()
        else:
            capacity = int(problem.bin_capacity)
            self.container_holder.set_capacity(capacity)

        # Rearrange holders to reflect new data
        self.item_holder.rearrange()
        self.container_holder.rearrange()

        self.loaded_problem = problem
