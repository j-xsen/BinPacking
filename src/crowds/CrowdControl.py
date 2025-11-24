import numpy
from direct.directnotify.Notifier import Notifier
from direct.gui.DirectButton import DirectButton
from direct.gui.DirectFrame import DirectFrame
from panda3d.core import NodePath

from src.crowds.Breeder import Breeder

import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np


class CrowdControl(NodePath, Notifier):
    def __init__(self, crowd_holder):
        super().__init__("CrowdButtons")
        Notifier.__init__(self, "CrowdControl")
        self.setDebug(True)
        self.crowd_holder = crowd_holder
        self.frame = DirectFrame(
            frameColor=(0.8, 0.8, 0.8, 1),
            frameSize=(-1, 1, -.05, .05),
            pos=(0, 0, -.2),
            text="Crowd Control",
            text_scale=0.05,
            text_pos=(-.8, 0.06),
            text_fg=(1,1,1, 1),
        )

        self.breeder = Breeder(self)

        create_agreement_matrix_button = DirectButton(
            parent=self.frame,
            text="Create Agreement Matrix",
            scale=0.05,
            pos=(0, 0, 0),
            command=self.create_agreement_matrix
        )

    def __len__(self):
        return len(self.crowd_holder.collection)

    def verify_start(self):
        if len(self.crowd_holder.collection) < 2:
            self.debug("At least two crowd members are required to verify agreement.")
            return False
        if not hasattr(self.breeder,'dimension'):
            self.breeder.set_dimension(base.dimension)
        return True

    def show_agreement_matrix(self, matrix, index_to_item):
        sorted_indices = sorted(range(len(index_to_item)), key=lambda i: int(index_to_item[i]))
        matrix_sorted = matrix[np.ix_(sorted_indices, sorted_indices)]
        sorted_labels = [index_to_item[i] for i in sorted_indices]
        annot = np.where(matrix_sorted==0, "", np.round(matrix_sorted, 2).astype(str))
        hm = sns.heatmap(matrix_sorted, annot=annot, fmt="")

        hm.set_xticklabels(sorted_labels)
        hm.set_yticklabels(sorted_labels)

        plt.title("Agreement Matrix")
        plt.xlabel("Items")
        plt.ylabel("Items")
        plt.show()

    def create_data_from_matrix(self, matrix, index_to_item):
        base.dimension.reset()
        while len(base.dimension.item_holder)!=0:
            item = base.dimension.item_holder.collection[0]
            placed = False
            for container in base.dimension.container_holder:
                if container.can_add(item):
                    # check agreement values
                    agreement_sum = 0.0
                    for other_item in container:
                        idx_i = None
                        idx_j = None
                        for idx, it in index_to_item.items():
                            if it == item:
                                idx_i = idx
                            if it == other_item:
                                idx_j = idx
                        if idx_i is not None and idx_j is not None:
                            agreement_sum += matrix[idx_i][idx_j]
                    messenger.send("container-clicked", [container])
                    messenger.send("item-clicked", [item])
                    placed=True
                    break
            if not placed:
                new_container = base.dimension.container_holder.create_new_container()
                messenger.send("container-clicked", [new_container])
                messenger.send("item-clicked", [item])
        self.debug(f"Created new data from agreement matrix with {len(base.dimension.container_holder)} containers.")
        self.breeder.solved()

    def create_agreement_matrix(self):
        if not self.verify_start():
            return
        items = list(dict.fromkeys(base.dimension.problem_loader.loaded_problem.items))
        matrix = numpy.zeros((len(items), len(items)), dtype=float)
        item_to_index = {item: idx for idx, item in enumerate(items)}
        # go through every crowd
        for crowd in self.crowd_holder.collection:
            # every item
            for item_i in items:
                container_i = None
                # go through every container
                for container in crowd.data["items"]:
                    # check if item is in container
                    if item_i in container:
                        # container
                        container_i = container
                        break
                # item not found
                if container_i is None:
                    continue
                # item is found
                # check every other item in the same bin
                # except vertices
                for jdx, item_j in enumerate(items):
                    if item_j == item_i:
                        continue
                    if item_j in container_i:
                        matrix[item_to_index[item_i], item_to_index[item_j]] += 1
                        matrix[item_to_index[item_j], item_to_index[item_i]] += 1
        # normalize
        rows, cols = matrix.shape
        for i in range(rows):
            for j in range(cols):
                cur = matrix[i][j]
                if matrix[i][j] / (len(crowd)*1) > 1:
                    self.warning(f"Agreement value {cur} for items {items[i]} and {items[j]} exceeds 1 after normalization.")
                matrix[i][j] = matrix[i][j] / (len(crowd)*1)
        index_to_item = {idx: item for item, idx in item_to_index.items()}
        self.show_agreement_matrix(matrix,index_to_item)
        self.create_data_from_matrix(matrix, index_to_item)
