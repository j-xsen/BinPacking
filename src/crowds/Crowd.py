from direct.directnotify.Notifier import Notifier
from direct.gui.DirectButton import DirectButton
from panda3d.core import NodePath
from direct.gui import DirectGuiGlobals as DGG


class Crowd(NodePath, Notifier):
    def __init__(self, data):
        if data.empty:
            raise ValueError("Cannot create Crowd with empty data")
        super().__init__("Crowd")
        Notifier.__init__(self, "Crowd")
        self.time = data.get("time", None)[0]
        data.drop("time",axis=1,inplace=True)
        self.data = data
        self.active = True
        self.frame=DirectButton(
            relief=DGG.RIDGE,
            borderWidth=(0.02, 0.02),
            frameSize=(-0.1, 0.1, -0.1, 0.1),
            pos=(0, 0, 0),
            parent=self,
            command=self.command,
            text=f"{data["Capacity"].mean():.2f}\n#{data.shape[0]}",
            text_scale=0.06,
        )
    def __str__(self):
        return f"Crowd ({self.data.shape[0]} bins, time={self.time:.5f}s, capacity%={self.data['Capacity'].mean():.2f})"
    def __len__(self):
        return int(self)
    def __int__(self):
        return int(self.data.shape[0])
    def command(self):
        self.debug(self.data)
        self.debug(f"in {self.time:.5f}s")
        base.dimension.reset()
        for idx, cur_bin in self.data.iterrows():
            for cur_item in cur_bin["items"]:
                messenger.send("container-clicked", [cur_bin])
                messenger.send("item-clicked", [cur_item])
        base.dimension.deselect()



