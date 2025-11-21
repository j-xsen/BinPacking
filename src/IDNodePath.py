import random

from panda3d.core import NodePath


class IDNodePath(NodePath):
    def __init__(self, name="IDNodePath"):
        super().__init__(name)
        self.uid = random.randint(1000, 9999)
