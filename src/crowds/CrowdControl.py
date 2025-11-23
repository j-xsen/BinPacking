import numpy
from direct.directnotify.Notifier import Notifier
from direct.gui.DirectButton import DirectButton
from direct.gui.DirectFrame import DirectFrame
from panda3d.core import NodePath

from src.crowds.Breeder import Breeder


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

        breeder = Breeder(self)

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
        return True

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
                matrix[i][j] = matrix[i][j] / len(items)
