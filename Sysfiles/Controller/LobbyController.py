from flask import request
from Sysfiles.Controller.QRCodeController import QrCodeController
from Sysfiles.Model.Lobby import Lobby
from Sysfiles.Model.Player import Player

class LobbyController:
    def __init__(self):
        self.player = None
        self.lobby = None
        self.qr = None
        self.settings = {
            "subject": [
                "Tiere",
                "Städte",
                "Flüsse"
            ],
            "GameLength": [
                5,
                10,
                15,
                20
            ],
            "maxPlayerCount": [
                5,
                10,
                15,
                20,
                25
            ]
        }
        self.createdLobbies = []

    def setLobbySettings(self):
        if self.lobby is None:
            return {}
        return self.settings

    def createLobby(self):
        self.lobby = Lobby()
        self.qr = QrCodeController(self.lobby.getLobbyID())
        createdLobby = {
            "lobbyID": self.lobby.getLobbyID(),
            "subjectName": self.lobby.setSubject(request.form.get('subject')),
            "generatedQRCode": self.qr.generateQrCode(),
            "maxPlayers": self.lobby.setMaxPlayers(request.form.get('maxPlayers')),
            "maxGameLength": self.lobby.setMaxGameLength(request.form.get('maxGameLength'))
        }
        self.createdLobbies.append(createdLobby)
        return createdLobby

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
            return [{}], 204
        return lobbyList

    def playerJoins(self):
        self.player = Player()
        playerList = []
        # self.player.setNickname(request.form['nickname']) <<<< swap when Testing
        self.player.setNickname(request.form.get('nickname'))
        self.player.setStatus(request.form.get('readyPlayer'))
        player = {
            "username": self.player.getNickname(),
            "isPlayerReady": self.player.getStatus()
        }
        playerList.append(player)
        if self.lobby is None:
            return [{}], 204
        self.lobby.addPlayer(player)
        return playerList, 200

    def getPlayerList(self):
        playerList = []
        if self.lobby is None or not self.lobby.playerList:
            return [{}], 204
        for data in self.lobby.playerList:
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