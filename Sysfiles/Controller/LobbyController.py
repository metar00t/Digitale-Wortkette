import random
import string

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
                "Städte",
                "Flüsse"
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
        self.createdLobbies.append(createdLobby)
        return createdLobby

    def saveCurrentLobby(self):
        lobbyID = self.lobby.getLobbyID()
        chosenSubject = request.form.get('subjectName')
        chosenMaxPlayers = request.form.get('maxPlayers')
        chosenMaxGameLength = request.form.get('maxGameLength')
        for lobbies in self.createdLobbies:
            if lobbyID == lobbies["lobbyID"]:
                if chosenSubject is not None:
                    lobbies["subjectName"] = chosenSubject
                    self.lobby.setSubject(chosenSubject)
                if chosenMaxPlayers is not None:
                    lobbies["maxPlayers"] = chosenMaxPlayers
                    self.lobby.setMaxPlayers(chosenMaxPlayers)
                if chosenMaxGameLength is not None:
                    lobbies["maxGameLength"] = chosenMaxGameLength
                    self.lobby.setMaxGameLength(chosenMaxGameLength)
                break

    def getChosenLobbySettings(self, lobbyID):
        for lobbies in self.createdLobbies:
            if lobbyID == lobbies["lobbyID"]:
                return {
                    "chosenSubject": lobbies["subjectName"],
                    "chosenMaxPlayers": lobbies["maxPlayers"],
                    "chosenMaxGameLength": lobbies["maxGameLength"]
                }
        return {}

    def getLobbyList(self):
        lobbyList = []
        for data in self.createdLobbies:
            lobbyInfo = {
                "lobbyID": data["lobbyID"],
                "subjectName": data["subjectName"],
                "maxPlayers": data["maxPlayers"]
            }
            lobbyList.append(lobbyInfo)
        if self.lobby is None or not lobbyList:
            return {}, 204
        return lobbyList

    def playerJoins(self, lobbyID):
        self.player = Player()
        username = request.form['nickname']
        self.player.setNickname(username)
        status = request.form['isPlayerReady']
        self.player.setStatus(status)
        if self.lobby is None:
            return [{}], 204
        playerAlreadyExists = self.getPlayer(username, lobbyID)
        if playerAlreadyExists:
            self.updatePlayerStatus(lobbyID, username, status)
            return self.lobby.getPlayerList(), 201
        else:
            player = {
                "lobbyID": lobbyID,
                "username": self.player.getNickname(),
                "isPlayerReady": self.player.getStatus()
            }
            self.lobby.addPlayer(player)
            return self.lobby.getPlayerList(), 201

    def getPlayer(self, username, lobbyID):
        for players in self.lobby.getPlayerList():
            if players["username"] == username and players["lobbyID"] == lobbyID:
                return players
        return None

    def updatePlayerStatus(self, lobbyID, username, status):
        for players in self.lobby.getPlayerList():
            if players["username"] == username and players["lobbyID"] == lobbyID:
                players["isPlayerReady"] = status
                return

    def getPlayerList(self, lobbyID):
        playerList = []
        if self.lobby is None or not self.lobby.playerList:
            return [{}], 204
        for data in self.lobby.getPlayerList():
            playerInfo = {
                "lobbyID": data["lobbyID"],
                "username": data["username"],
                "isPlayerReady": data["isPlayerReady"]
            }
            playerList.append(playerInfo)
        return playerList, 200

    def setGameStatus(self):
        return {
            "hasGameStarted": bool,
            "firstLetter": random.choice(string.ascii_letters)
        }

    def gameSession(self):
        if self.lobby is None and self.player is None:
            return {}, 204
        currentWordList = self.lobby.getWordList()
        if not currentWordList:
            return {}, 204
        currentWord = currentWordList[-1]
        return {
            "chosenSubject": self.lobby.getSubject(),
            "timer": float,
            "currentLetter": currentWord[:1],
            "previousWords": {
                "wordUsed": currentWord,
                "username": self.player.getNickname()
            },
            "playerStatus": [
                "disconnected",
                "selected",
                "next",
                "connected",
                "suspend round"
            ],
            "wordsPerMinute": float,
            "usableWord": bool
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

    def getCurrentLobbyID(self):
        return self.lobby.getLobbyID()
