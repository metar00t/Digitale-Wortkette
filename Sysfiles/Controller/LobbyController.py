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
            "subjectName": self.lobby.setSubject(request.form.get('subject')),
            "generatedQRCode": self.qr.generateQrCode(),
            "maxPlayers": self.lobby.setMaxPlayers(request.form.get('maxPlayers')),
            "maxGameLength" : self.lobby.setMaxGameLength(request.form.get('maxGameLength'))
        }
        self.createdLobbies.append(createdLobby)
        return createdLobby

    def getLobbyList(self):
        lobbyList = []
        for data in self.createdLobbies:
            lobbyInfo = {
                "lobbyID" : data["lobbyID"],
                "subjectName" : data["subjectName"],
                "maxPlayers" : data["maxPlayers"]
            }
            lobbyList.append(lobbyInfo)
        return lobbyList

    def playerJoins(self):
        self.player = Player()
       # self.player.setNickname(request.form['nickname'])
        self.player.setNickname(request.form.get('nickname'))
        self.player.setStatus(request.form.get('readyPlayer'))
        playerList = []
        player = {
            "username" : self.player.getNickname(),
            "isPlayerReady" : self.player.getStatus()
        }
        self.lobby.addPlayer(player)
        playerList.append(player)
        return playerList

    def getPlayerList(self):
        playerList = []
        if self.lobby is None:
            return [{}]
        elif not self.lobby.playerList:
            return [{}]
        for data in self.lobby.playerList:
            playerInfo = {
                "username" : data["username"],
                "isPlayerReady" : data["isPlayerReady"]
            }
            playerList.append(playerInfo)
        return playerList


    def getLobbySettings(self):
        if self.lobby is None:
            return {}
        return {
            "chosenSubjectName" : self.lobby.getSubject(),
            "chosenGameLength" : self.lobby.getMaxGameLength(),
            "chosenMaxPlayer" : self.lobby.getMaxPlayers()
        }
