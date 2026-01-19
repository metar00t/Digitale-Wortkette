class Lobby:
    _maxLobbyID : int = 0
    _lobbyList = []

    def __init__(self):
        self.lobbyID = Lobby._maxLobbyID + 1
        Lobby._maxLobbyID += 1
        Lobby._lobbyList.append(self.lobbyID)
        self.subject = ""
        self.maxPlayers = 0
        self.maxGameLength = 0

    def setSubject(self, subject : str):
        self.subject = subject

    def setMaxPlayers(self, maxPlayers : int):
        self.maxPlayers = maxPlayers

    def setMaxGameLength(self, maxGameLength : int):
        self.maxGameLength = maxGameLength

    def getLobbyID(self):
        return self.lobbyID

    def getSubject(self):
        return self.subject

    def getMaxPlayers(self):
        return self.maxPlayers

    def getMaxGameLength(self):
        return self.maxGameLength
