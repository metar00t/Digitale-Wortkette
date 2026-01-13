class Player:
    _userID = 0

    def __init__(self):
        self.nickname = ""
        self.status = ""
        self.userID = Player._userID + 1
        Player._userID += 1

    def setNickname(self, nickname):
        self.nickname = nickname

    def setStatus(self, status):
        self.status = status

    def getNickname(self):
        return self.nickname

    def getStatus(self):
        return self.status

    def getUserID(self):
        return self.userID