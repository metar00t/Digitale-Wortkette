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
                "Flüsse",
                "Programmiersprachen",
                "IDE",
                "Hardware"
            ],
            "generatedQRCode": self.qr.generateQrCode(),
            "maxPlayers": [
                5,
                10,
                15,
                20,
                25,
                30,
                35
            ],
            "maxGameLength": [
                5,
                10,
                15,
                20,
                25,
                30
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
            return None
        return lobbyList

    def playerJoins(self, lobbyID):
        self.player = Player()
        username = request.form['nickname']
        #username = request.form.get('nickname')
        if username.strip() == "":
            return {"message" : "Bitte gib einen Usernamen ein"}
        status = request.form.get('isPlayerReady')
        self.player.setNickname(username)
        self.player.setStatus(status)
        if self.lobby is None:
            return {}
        playerAlreadyExists = self.getPlayer(username, lobbyID)
        if playerAlreadyExists:
            self.updatePlayerStatus(lobbyID, username, status)
            return self.lobby.getPlayerList()
        else:
            player = {
                "lobbyID": lobbyID,
                "username": self.player.getNickname(),
                "isPlayerReady": self.player.getStatus()
            }
            self.lobby.addPlayer(player)
            return self.lobby.getPlayerList()

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
            return {}, 204
        for data in self.lobby.getPlayerList():
            if lobbyID == data['lobbyID']:
                playerInfo = {
                    "lobbyID": data["lobbyID"],
                    "username": data["username"],
                    "isPlayerReady": data["isPlayerReady"]
                }
                playerList.append(playerInfo)
        return playerList

    def isPlayerLimitReached(self, lobbyID):
        foundLobby = None
        for l in self.createdLobbies:
            if l["lobbyID"] == lobbyID:
                foundLobby = l
                break

        if foundLobby is None:
            return False

        maxPlayers = int(foundLobby["maxPlayers"])

        count = 0
        for player in self.lobby.getPlayerList():
            if player["lobbyID"] == lobbyID:
                count += 1

        if count >= maxPlayers:
            return True
        else:
            return False

