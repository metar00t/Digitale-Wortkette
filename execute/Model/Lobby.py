from flask import request
import random

class Lobby:
    _maxLobbyID = 0
    _lobbyList = []

    def __init__(self):
        self.lobbyID = Lobby._maxLobbyID + 1
        Lobby._maxLobbyID += 1
        Lobby._lobbyList.append(self.lobbyID)
        self.lobbyCode = random.randint(0 , 999)
        self.subject = ""
        self.maxPlayers = 0
        self.maxGameLength = 0

    def setSubject(self):
        self.subject = request.form.get('subject')

    def setMaxPlayers(self):
        self.maxPlayers = request.form.get('maxPlayers')

    def setMaxGameLength(self):
        self.maxGameLength = request.form.get('maxGameLength')

    def getLobbyID(self):
        return self.lobbyID

    def getLobbyCode(self):
        return self.lobbyCode

    def getHostName(self):
        return self.hostName

    def getSubject(self):
        return self.subject

    def getMaxPlayers(self):
        return self.maxPlayers

    def getMaxGameLength(self):
        return self.maxGameLength