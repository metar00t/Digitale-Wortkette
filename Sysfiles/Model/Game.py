class Game:
    _maxGameID: int = 0
    _gameList = []

    def __init__(self):
        self.gameID = Game._maxGameID + 1
        Game._maxGameID += 1
        Game._gameList.append(self.gameID)
        self.time = 0
        self.isTimeUp: bool = False

    def setTime(self, time):
        self.time = time

    def getTime(self):
        return self.time

    def getGameID(self):
        return self.gameID

    def callbackTimer(self):
        self.isTimeUp = True

    def getIsTimeUp(self):
        return self.isTimeUp
