from direct.task.TaskManagerGlobal import taskMgr
from panda3d.core import NodePath, LVecBase4f

from Square import Square


class Cube(NodePath):
    def __init__(self, side_length):
        super().__init__('cube')

        # Create six faces
        self.faces = [Square(side_length) for _ in range(6)]

        # Half the side length for positioning
        half = side_length

        # Orient and position each face
        # Front
        self.faces[0].set_pos(0, half, 0)
        self.faces[0].set_color(LVecBase4f(1, 0, 0, 1))  # Red
        self.faces[0].set_h(180)
        # Back
        self.faces[1].set_h(0)
        self.faces[1].set_pos(0, -half, 0)
        self.faces[1].set_color(LVecBase4f(0, 1, 0, 1))  # Green
        # Right
        self.faces[2].set_h(90)
        self.faces[2].set_pos(half, 0, 0)
        self.faces[2].set_color(LVecBase4f(0, 0, 1, 1))  # Blue
        # Left
        self.faces[3].set_h(-90)
        self.faces[3].set_pos(-half, 0, 0)
        self.faces[3].set_color(LVecBase4f(1, 1, 0, 1))  # Yellow
        # Top
        self.faces[4].set_p(-90)
        self.faces[4].set_pos(0, 0, half)
        self.faces[4].set_color(LVecBase4f(1, 0, 1, 1))  # Magenta
        # Bottom
        self.faces[5].set_p(90)
        self.faces[5].set_pos(0, 0, -half)
        self.faces[5].set_color(LVecBase4f(0, 1, 1, 1))  # Cyan

        # Attach all faces to the cube node
        for face in self.faces:
            face.reparent_to(self)

        # spin
        taskMgr.add(self.move, "move")

    def move(self, task):
        self.set_h(self.get_h() + 1)
        return task.cont

    def volume(self):
        return self.side_length ** 3

    def surface_area(self):
        return 6 * (self.side_length ** 2)