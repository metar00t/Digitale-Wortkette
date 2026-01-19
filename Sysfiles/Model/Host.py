from Sysfiles.Model.Player import Player

class Host(Player):
    _hostID : int = 0

    def __init__(self):
        super().__init__()
        self.hostID = Host._hostID + 1
        Host._hostID += 1

    def getHostID(self):
        return self.hostID
