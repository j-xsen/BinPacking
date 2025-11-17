from panda3d.core import GeomVertexFormat, GeomVertexData, Geom, GeomVertexWriter, LVecBase3f, LVecBase4f, GeomNode, \
    NodePath, GeomTriangles


class Square(NodePath):
    def __init__(self, side_length):
        NodePath.__init__(self, "Square")
        self.side_length = side_length

        v_format = GeomVertexFormat.get_v3c4()

        v_data = GeomVertexData("Square", v_format, Geom.UHStatic)
        v_data.unclean_set_num_rows(4)
        vertex_writer = GeomVertexWriter(v_data, "vertex")
        color_writer = GeomVertexWriter(v_data, "color")

        vertex_writer.set_data3f(LVecBase3f(-side_length,0,side_length))
        color_writer.set_data4f(LVecBase4f(1, 1, 1, 1))

        vertex_writer.set_data3f(LVecBase3f(side_length,0,side_length))
        color_writer.set_data4f(LVecBase4f(1, 1, 1, 1))

        vertex_writer.set_data3f(LVecBase3f(-side_length,0,-side_length))
        color_writer.set_data4f(LVecBase4f(1, 1, 1, 1))

        vertex_writer.set_data3f(LVecBase3f(side_length,0,-side_length))
        color_writer.set_data4f(LVecBase4f(1, 1, 1, 1))

        tris = GeomTriangles(Geom.UHStatic)
        tris.add_vertices(2, 1, 0)
        tris.add_vertices(2, 3, 1)

        geom = Geom(v_data)
        geom.add_primitive(tris)
        geom_node = GeomNode("SquareGeomNode")
        geom_node.add_geom(geom)
        self.attach_new_node(geom_node)

    def area(self):
        return self.side_length ** 2

    def perimeter(self):
        return 4 * self.side_length