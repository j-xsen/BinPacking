from direct.directnotify.DirectNotifyGlobal import directNotify
from direct.showbase.ShowBase import ShowBase

from Container import Container
from ContainerHolder import ContainerHolder
from Item import Item
from ItemHolder import ItemHolder


from panda3d.core import loadPrcFileData, GeomNode, CollisionRay, CollisionTraverser, CollisionHandlerQueue, \
    CollisionNode

# loadPrcFileData("", "want-directtools #t")
# loadPrcFileData("", "want-tk #t")
loadPrcFileData("", "window-title Bin Packing Visualization")
loadPrcFileData("", "win-origin 100 100")
loadPrcFileData("", "default-directnotify-level debug")

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

        self._item_selected = None

        container_one = Container(side_length=4)

        self.container_holder = ContainerHolder()
        self.container_holder.addition(container_one)
        self.container_holder.set_pos(0,80,0)
        self.container_holder.reparent_to(render)

        item_one = Item(side_length=1, weight=1)

        self.item_holder = ItemHolder()
        self.item_holder.addition(item_one)
        self.item_holder.set_pos(0,80,-10)
        self.item_holder.reparent_to(render)

        self.accept("mouse1", self.on_mouse_click)

        # exit
        self.accept("escape", self.userExit)

    @property
    def item_selected(self):
        if self._item_selected is None:
            return None
        return self._item_selected
    @item_selected.setter
    def item_selected(self, value):
        value = self.item_holder.get(value)

        if not value:
            self.notify.warning("No item selected")
            return

        # no item selected, fill
        if not self._item_selected:
            if value is None:
                self.notify.warning(f"Selected item {value} not found in ItemHolder")
                return
            value.select()
            self._item_selected = value
        # item selected, toggle
        else:
            # deselect if same item
            if value == self._item_selected:
                value.deselect()
                self._item_selected = None
            # select if new item
            else:
                self._item_selected.deselect()
                value.select()
                self._item_selected = value

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
            else:
                picked_item = picked_obj.find_net_tag("container")
                if not picked_item.is_empty() and self.item_selected:
                    container = self.container_holder.get(picked_item)
                    if container:
                        self.notify.debug(f"Placing Item {self.item_selected.get_name()} into Container {picked_item.get_name()}")
                        container.add_item(self.item_selected)
                        self.item_holder.subtraction(self.item_selected)
                        self.item_selected.deselect()
                        self._item_selected = None
                    else:
                        self.notify.warning(f"Container {picked_item} not found in ContainerHolder")
        picker_np.remove_node()
        return None

bin_packing_app = BinPacking()
bin_packing_app.run()
