import random, string

from flask import request
from Sysfiles.Controller.QRCodeController import QrCodeController
from Sysfiles.Model.Lobby import Lobby
from Sysfiles.Model.Player import Player

class LobbyController:
    def __init__(self):
        self.player = None
        self.lobby = None
        self.qr = None
        self.createdLobbies = []

    def createLobby(self):
        self.lobby = Lobby()
        self.qr = QrCodeController(self.lobby.getLobbyID())
        createdLobby = {
            "lobbyID": self.lobby.getLobbyID(),
            "subjectName": [
                "Tiere",
                "Staedte",
                "Fluesse"
            ],
            "generatedQRCode": self.qr.generateQrCode(),
            "maxPlayers": [
                5,
                10,
                15,
                20,
                25
            ],
            "maxGameLength": [
                5,
                10,
                15,
                20
            ]
        }
        return createdLobby

    def saveCurrentLobby(self):
        lobbyID = self.lobby.getLobbyID()
        updatedLobby = {
            "lobbyID": lobbyID,
            "chosenSubjectName": request.form.get('subjectName'),
            "chosenMaxPlayers": request.form.get('maxPlayers'),
            "chosenMaxGameLength": request.form.get('maxGameLength')
        }
        self.createdLobbies.append(updatedLobby)
        return updatedLobby

    def getLobbyList(self):
        lobbyList = []
        for data in self.createdLobbies:
            lobbyInfo = {
                "lobbyID": data["lobbyID"],
                "subjectName": data["chosenSubjectName"],
                "maxPlayers": data["chosenMaxPlayers"]
            }
            lobbyList.append(lobbyInfo)
        if self.lobby is None or not lobbyList:
            return [{}], 204
        return lobbyList

    def playerJoins(self):
        self.player = Player()
        playerList = []
        # self.player.setNickname(request.form['nickname']) <<<< swap when Testing
        self.player.setNickname(request.form.get('nickname'))
        self.player.setStatus(False)
        player = {
            "username": self.player.getNickname(),
            "isPlayerReady": self.player.getStatus()
        }
        playerList.append(player)
        if self.lobby is None:
            return [{}], 204
        self.lobby.addPlayer(player)
        return playerList, 201

    def getPlayerList(self):
        playerList = []
        if self.lobby is None or not self.lobby.playerList:
            return [{}], 204
        for data in self.lobby.getPlayerList():
            playerInfo = {
                "username": data["username"],
                "isPlayerReady": data["isPlayerReady"]
            }
            playerList.append(playerInfo)
        return playerList, 200

    def getChosenLobbySettings(self):
        if self.lobby is None:
            return {}, 204
        return {
            "chosenSubjectName": self.lobby.getSubject(),
            "chosenGameLength": self.lobby.getMaxGameLength(),
            "chosenMaxPlayer": self.lobby.getMaxPlayers()
        }

    def setGameStatus(self):
        return {
            "hasGameStarted" : bool,
            "firstLetter" : random.choice(string.ascii_letters)
        }

    def gameSession(self):
        if self.lobby is None and self.player is None:
            return {}, 204
        currentWordList = self.lobby.getWordList()
        if not currentWordList:
            return {}, 204
        currentWord = currentWordList[-1]
        return {
            "chosenSubject" : self.lobby.getSubject(),
            "timer" : float,
            "currentLetter" : currentWord[:1],
            "previousWords" : {
                "wordUsed" : currentWord,
                "username" : self.player.getNickname()
            },
            "playerStatus" : [
                "disconnected",
                "selected",
                "next",
                "connected",
                "suspend round"
            ],
            "wordsPerMinute" : float,
            "usableWord" : bool
        }

    def checkInput(self):
        # request.form['wordInput']
        # request.form.get('wordInput')
        chosenWord = request.form['wordInput']
        currentWordList = self.lobby.getWordList()
        for checkWord in currentWordList:
            if checkWord == chosenWord:
                break
            return chosenWord

    def addWord(self, word):
        return self.lobby.setCurrentWord(word)