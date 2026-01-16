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
        self.playerList = []

    def createLobby(self):
        self.lobby = Lobby()
        self.host = Host()
        self.player = Player()
        self.qr = QrCodeController(f"dwk://player/{self.lobby.getLobbyID()}/join")
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
            "userID": self.host.getUserID(),
            "hostID": int(f"{self.lobby.getLobbyID()}0{self.host.getUserID()}{self.host.getHostID()}"),
            "username": "Host",
            "isPlayerReady": "true"
        }
        self.playerList.append(host)
        self.createdLobbies.append(createdLobby)
        return createdLobby

    def addPlayer(self, player):
        self.playerList.append(player)

    def updateLobby(self):
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

    def closeLobby(self, lobbyID, hostID):
        lobbies = self.createdLobbies
        players = self.playerList
        for i, l in enumerate(lobbies):
            for j, p in enumerate(players):
                if l["lobbyID"] == lobbyID and p["lobbyID"] == lobbyID and p["hostID"] == hostID:
                    del lobbies[i]
                    del players[j]
                    return True
        return False

    def isPlayerLimitReached(self, lobbyID):
        foundLobby = None
        for l in self.createdLobbies:
            if l["lobbyID"] == lobbyID:
                foundLobby = l
                break

        if foundLobby is None:
            return False

        maxPlayers = foundLobby["maxPlayers"]

        count = 0
        for player in self.playerList:
            if player["lobbyID"] == lobbyID:
                count += 1

        if count >= int(maxPlayers):
            return True
        else:
            return False

    def getListOfPlayers(self, lobbyID):
        playerList = []
        for data in self.playerList:
            if lobbyID == data["lobbyID"]:
                playerInfo = {
                    "lobbyID": data["lobbyID"],
                    "userID": data["userID"],
                    "hostID": data["hostID"],
                    "username": data["username"],
                    "isPlayerReady": data["isPlayerReady"]
                }
                playerList.append(playerInfo)
        return playerList
