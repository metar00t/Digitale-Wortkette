class Player:
    _userID : int = 0

    def __init__(self):
        self.nickname = ""
        self.status = ""
        self.userID = Player._userID + 1
        Player._userID += 1

    def setNickname(self, nickname : str):
        self.nickname = nickname

    def setStatus(self, status : bool):
        self.status = status

    def getNickname(self):
        return self.nickname

    def getStatus(self):
        return self.status

    def getUserID(self):
        return self.userID