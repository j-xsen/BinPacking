from direct.directnotify.DirectNotifyGlobal import directNotify
from direct.showbase.ShowBase import ShowBase

from panda3d.core import loadPrcFileData, GeomNode, CollisionRay, CollisionTraverser, CollisionHandlerQueue, \
    CollisionNode

from src.dimensions.oned.OneD import OneD

# loadPrcFileData("", "want-directtools #t")
# loadPrcFileData("", "want-tk #t")
loadPrcFileData("", "window-title Bin Packing Visualization")
loadPrcFileData("", "win-origin 100 100")
loadPrcFileData("", "default-directnotify-level warning")

# warning level
loadPrcFileData("", "notify-level-EventManager warning")
loadPrcFileData("", "notify-level-Messenger warning")
loadPrcFileData("", "notify-level-ShowBase warning")

class BinPacking(ShowBase):
    def __init__(self):
        super().__init__()
        base.disableMouse()

        self.notify = directNotify.newCategory("BinPacking")

        # window set up
        self.title = "Bin Packing Visualization"
        self.set_background_color(0, 0, 0.2, 1)
        # self.accept("mouse1", self.on_mouse_click)

        self.item_selected = None

        # dimension
        one_dimension = OneD()
        one_dimension.reparent_to(render)
        self.dimension = one_dimension

        self.accept("holder-updated", self.on_holder_update)

        # exit
        self.accept("escape", self.userExit)

    def on_holder_update(self):
        if self.dimension.item_holder.selected and self.dimension.container_holder.selected:
            # check if valid
            if self.dimension.container_holder.selected.can_add(self.dimension.item_holder.selected):
                self.notify.debug(f"Moving Item {self.dimension.item_holder.selected.get_name()}"
                                  f" ({self.dimension.item_holder.selected.weight}) to Container"
                                  f" {self.dimension.container_holder.selected.get_name()}")
                self.dimension.container_holder.selected.addition(self.dimension.item_holder.selected)
                self.dimension.item_holder.subtraction(self.dimension.item_holder.selected)
                messenger.send("holder-updated")
            else:
                self.dimension.container_holder.selected.deselect()
                self.dimension.container_holder.rearrange()

    def on_mouse_click(self):
        if not base.mouseWatcherNode.has_mouse():
            return None
        picker_node = CollisionNode('mouseRay')
        picker_np = camera.attach_new_node(picker_node)
        picker_node.set_from_collide_mask(GeomNode.get_default_collide_mask())
        picker_ray = CollisionRay()
        picker_node.add_solid(picker_ray)
        my_traverser = CollisionTraverser('traverser')
        my_handler = CollisionHandlerQueue()
        my_traverser.add_collider(picker_np, my_handler)

        m_pos = base.mouseWatcherNode.get_mouse()
        picker_ray.set_from_lens(base.camNode, m_pos.get_x(), m_pos.get_y())

        my_traverser.traverse(render)

        if my_handler.get_num_entries() > 0:
            my_handler.sort_entries()
            picked_obj = my_handler.get_entry(0).get_into_node_path()
            picked_item = picked_obj.find_net_tag("item")
            if not picked_item.is_empty():
                self.item_selected = picked_item
                self.notify.debug(f"Item {picked_item.get_name()} clicked")
            else:
                picked_item = picked_obj.find_net_tag("container")
                if not picked_item.is_empty() and self.item_selected:
                    container = self.dimension.container_holder.get(picked_item)
                    if container:
                        self.notify.debug(f"Placing Item {self.item_selected.get_name()} into Container {picked_item.get_name()}")
                        container.add_item(self.item_selected)
                        self.dimension.item_holder.subtraction(self.item_selected)
                        self.item_selected.deselect()
                        self.item_selected = None
                    else:
                        self.notify.warning(f"Container {picked_item} not found in ContainerHolder")
        picker_np.remove_node()
        return None

bin_packing_app = BinPacking()
bin_packing_app.run()
