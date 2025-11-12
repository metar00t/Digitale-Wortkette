from sysfiles.Controller.QRCodeController import QrCodeController
from sysfiles.Model.Lobby import *
from sysfiles.Model.Player import Player

class LobbyController:
    def __init__(self):
        self.player = None
        self.lobby = None
        self.createdLobbies = []
        self.qr = None

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

    def getConnectedPlayers(self):
        self.player = Player()
        return {
            "username" : self.player.getNickname(),
            "readyPlayer" : self.player.getStatus()
        }

    def getLobbySettings(self):
        if self.lobby is None:
            return {}
        return {
            "chosenSubjectName" : self.lobby.getSubject(),
            "chosenGameLength" : self.lobby.getMaxGameLength(),
            "chosenMaxPlayer" : self.lobby.getMaxPlayers()
        }
