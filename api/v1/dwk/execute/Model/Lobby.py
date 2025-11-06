class Lobby:
    def __init__(self, lobbyID, hostName, subject, playerCount):
        self.lobbyID = lobbyID
        self.hostName = hostName
        self.subject = subject
        self.playerCount = playerCount

    def setLobbyID(self, lobbyID):
        self.lobbyID = lobbyID

    def getLobbyInfo(self):
        return {
            "lobbyID": self.lobbyID,
            "hostName" : self.hostName,
            "subject" : self.subject,
            "playerCount" : self.playerCount
        }

    def createNewLobby(self, img, qrString, maxPlayers, maxGameLength):
        return {
            "lobbyID" : self.lobbyID,
            "img" : img,
            "subjectName" : self.subject,
            "generatedQRCode" : qrString,
            "maxPlayers" : maxPlayers,
            "maxGameLength" : maxGameLength
        }