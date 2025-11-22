import random

from direct.task.TaskManagerGlobal import taskMgr
from panda3d.core import NodePath, LVecBase4f

from src.geom.Square import Square


class Cube(NodePath):
    def __init__(self, side_length, width_length=None, height_length=None):
        self.uid = random.randint(1000, 9999)
        super().__init__('cube')

        # Create six faces
        self.faces = [Square(side_length) for _ in range(6)]

        # Half the side length for positioning
        self.side_length = side_length

        # Orient and position each face
        # Front
        self.faces[0].set_pos(0, self.side_length, 0)
        self.faces[0].set_color(LVecBase4f(1, 0, 0, 1))  # Red
        self.faces[0].set_h(180)
        # Back
        self.faces[1].set_h(0)
        self.faces[1].set_pos(0, -self.side_length, 0)
        self.faces[1].set_color(LVecBase4f(0, 1, 0, 1))  # Green
        # Right
        self.faces[2].set_h(90)
        self.faces[2].set_pos(self.side_length, 0, 0)
        self.faces[2].set_color(LVecBase4f(0, 0, 1, 1))  # Blue
        # Left
        self.faces[3].set_h(-90)
        self.faces[3].set_pos(-self.side_length, 0, 0)
        self.faces[3].set_color(LVecBase4f(1, 1, 0, 1))  # Yellow
        # Top
        self.faces[4].set_p(-90)
        self.faces[4].set_pos(0, 0, self.side_length)
        self.faces[4].set_color(LVecBase4f(1, 0, 1, 1))  # Magenta
        # Bottom
        self.faces[5].set_p(90)
        self.faces[5].set_pos(0, 0, -self.side_length)
        self.faces[5].set_color(LVecBase4f(0, 1, 1, 1))  # Cyan

        # Attach all faces to the cube node
        for face in self.faces:
            face.reparent_to(self)

        # spin
        # taskMgr.add(self.move, f"move-{self.uid}")

    def delete(self):
        taskMgr.remove("move")
        self.remove_node()

    def move(self, task):
        if not self.is_empty():
            self.set_h(self.get_h() + .6)
        return task.cont

    def volume(self):
        return self.side_length ** 3

    def surface_area(self):
        return 6 * (self.side_length ** 2)