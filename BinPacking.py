from direct.directnotify.DirectNotifyGlobal import directNotify
from direct.showbase.ShowBase import ShowBase
from panda3d.core import loadPrcFileData

from src.dimensions.oned.OneD import OneD

# loadPrcFileData("", "want-directtools #t")
# loadPrcFileData("", "want-tk #t")
loadPrcFileData("", "window-title Bin Packing Visualization")
loadPrcFileData("", "win-origin 100 100")
loadPrcFileData("", "default-directnotify-level debug")

# warning level
loadPrcFileData("", "notify-level-EventManager warning")
loadPrcFileData("", "notify-level-Messenger warning")
loadPrcFileData("", "notify-level-ShowBase warning")

# bin packing
loadPrcFileData("", "notify-level-BinPacking warning")
loadPrcFileData("", "notify-level-ItemHolder debug")


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
            ise = self.dimension.item_holder.selected
            cs = self.dimension.container_holder.selected
            # check if valid
            if self.dimension.container_holder.selected.can_add(ise):
                self.notify.debug(f"Moving {ise} to"
                                  f" {cs}")
                self.dimension.container_holder.selected.addition(ise)
                self.dimension.item_holder.subtraction(ise)
                messenger.send("holder-updated")
            else:
                self.notify.debug(f"Cannot add {ise} to {cs}")
                self.dimension.container_holder.selected.deselect()
                self.dimension.item_holder.selected.deselect()
                self.dimension.container_holder.rearrange()


bin_packing_app = BinPacking()
bin_packing_app.run()
