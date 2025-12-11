from flask import request

from Sysfiles.Controller.QRCodeController import QrCodeController
from Sysfiles.Model.Host import Host
from Sysfiles.Model.Lobby import Lobby
from Sysfiles.Model.Player import Player


class LobbyController:
    def __init__(self):
        self.host = None
        self.player = None
        self.lobby = None
        self.qr = None
        self.createdLobbies = []

    def createLobby(self):
        self.lobby = Lobby()
        self.host = Host()
        self.qr = QrCodeController(f"/api/v1/dwk/lobby/{self.lobby.getLobbyID()}/join")
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
            ],
            "hostID": int(f"{self.lobby.getLobbyID()}0{self.host.getUserID()}{self.host.getHostID()}"),
            "userID": self.host.getUserID()
        }
        host = {
            "lobbyID": self.lobby.getLobbyID(),
            "userID" : self.host.getUserID(),
            "hostID" : int(f"{self.lobby.getLobbyID()}0{self.host.getUserID()}{self.host.getHostID()}"),
            "username": "Host",
            "isPlayerReady": "true"
        }
        self.lobby.addPlayer(host)
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

    def playerJoins(self, lobbyID, userID):
        self.player = Player()
        username = request.form['nickname']
        if username.strip() == "":
            return {"message" : "Bitte gib einen Usernamen ein"}
        status = request.form.get('isPlayerReady')
        self.player.setNickname(username)
        self.player.setStatus(status)
        if self.lobby is None:
            return {}
        playerAlreadyExists = self.getPlayer(userID, lobbyID)
        if playerAlreadyExists:
            return self.updatePlayer(lobbyID, userID, username, status)
        else:
            newPlayer = {
                "lobbyID": lobbyID,
                "userID" : self.player.getUserID(),
                "hostID" : 0,
                "username": self.player.getNickname(),
                "isPlayerReady": self.player.getStatus()
            }
            self.lobby.addPlayer(newPlayer)
            return newPlayer

    def getPlayer(self, userID, lobbyID):
        for players in self.lobby.getPlayerList():
            if players["userID"] == userID and players["lobbyID"] == lobbyID:
                return True
        return False

    def updatePlayer(self, lobbyID, userID, username, status):
        updatedPlayer = None
        for players in self.lobby.getPlayerList():
            if players["userID"] == userID and players["lobbyID"] == lobbyID:
                players["isPlayerReady"] = status
                players["username"] = username
                updatedPlayer = {
                "lobbyID": lobbyID,
                "userID" : players["userID"],
                "hostID" : 0,
                "username": players["username"],
                "isPlayerReady": status
            }
        return updatedPlayer

    def removePlayer(self, lobbyID, userID):
        players = self.lobby.getPlayerList()
        for i, p in enumerate(players):
            if p["userID"] == userID and p["lobbyID"] == lobbyID:
                del players[i]
                return True
        return False

    def closeLobby(self, lobbyID, hostID):
        lobbies = self.createdLobbies
        players = self.lobby.getPlayerList()
        for i, l in enumerate(lobbies):
            for j, p in enumerate(players):
                if l["lobbyID"] == lobbyID and p["lobbyID"] == lobbyID and p["hostID"] == hostID:
                    del lobbies[i]
                    del players[j]
                    return True
        return False


    def getPlayerList(self, lobbyID):
        playerList = []
        if self.lobby is None or not self.lobby.playerList:
            return {}, 204
        for data in self.lobby.getPlayerList():
            if lobbyID == data['lobbyID']:
                playerInfo = {
                    "lobbyID": data["lobbyID"],
                    "userID": data["userID"],
                    "hostID": data["hostID"],
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

