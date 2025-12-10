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
            "hostID": int(f"{self.lobby.getLobbyID()}0{self.host.getUserID()}{self.host.getHostID()}")
        }
        host = {
            "lobbyID": self.lobby.getLobbyID(),
            "userID" : self.host.getUserID(),
            "hostID" : int(f"{self.lobby.getLobbyID()}0{self.host.getUserID()}{self.host.getHostID()}"),
            "username": "Host",
            "isPlayerReady": "true"
        }
        # lobby: lobbyID, hostID = host.hostID|| host: hostID: userID_lobbyID
        # lobby: hostID -> host: hostID -> userID
        # lobby:
        # hostID
        # user:
        # userID
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

    def playerJoins(self, lobbyID):
        self.player = Player()
        username = request.form['nickname']
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
            newPlayer = {
                "lobbyID": lobbyID,
                "userID" : self.player.getUserID(),
                "hostID" : 0,
                "username": self.player.getNickname(),
                "isPlayerReady": self.player.getStatus()
            }
            self.lobby.addPlayer(newPlayer)
            return newPlayer

    def getPlayer(self, username, lobbyID):
        for players in self.lobby.getPlayerList():
            if players["username"] == username and players["lobbyID"] == lobbyID:
                return players
        return None

    def removePlayer(self, lobbyID, userID):
        players = self.lobby.getPlayerList()
        for i, p in enumerate(players):
            if p["userID"] == userID and p["lobbyID"] == lobbyID:
                del players[i]
                return True
        return False

    def closeLobby(self, lobbyID):
        lobbies = self.createdLobbies
        players = self.lobby.getPlayerList()
        userID = request.form.get('userID')
        for i, l in enumerate(lobbies):
            for j, p in enumerate(players):
                if l["lobbyID"] == lobbyID and p["lobbyID"] == lobbyID and p["userID"] == userID:
                    del lobbies[i]
                    del players[j]
                    return True
        return False

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

