import random

class Lobby:
    _maxLobbyID = 0
    _lobbyList = []

    def __init__(self):
        self.lobbyID = Lobby._maxLobbyID
        Lobby._maxLobbyID += 1
        Lobby._lobbyList.append(self.lobbyID)
        self.subject = ""
        self.maxPlayers = 0
        self.maxGameLength = 0
        self.playerList = []
        self.wordList = []

    def setSubject(self, subject):
        self.subject = subject

    def setMaxPlayers(self, maxPlayers):
        self.maxPlayers = maxPlayers

    def setMaxGameLength(self, maxGameLength):
        self.maxGameLength = maxGameLength

    def getLobbyID(self):
        return self.lobbyID

    def getSubject(self):
        return self.subject

    def getMaxPlayers(self):
        return self.maxPlayers

    def getMaxGameLength(self):
        return self.maxGameLength

    def addPlayer(self, player):
        self.playerList.append(player)

    def getPlayerList(self):
        return self.playerList

    def setCurrentWord(self, word):
        self.wordList.append(word)

    def getWordList(self):
        return self.wordList