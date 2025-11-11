from execute.Controller.QRCodeController import QrCodeController
from execute.Model.Lobby import *
from execute.Model.Player import Player

class LobbyController:
    def __init__(self):
        self.player = None
        self.lobby = Lobby()
        self.qr = QrCodeController(self.lobby.lobbyCode)

    def createLobby(self):
        return {
            "lobbyID": self.lobby.lobbyID,
            "subjectName": self.lobby.setSubject(),
            "generatedQRCode": self.qr.setQrCode(),
            "maxPlayers": self.lobby.setMaxPlayers(),
            "maxGameLength" : self.lobby.setMaxGameLength()
        }

    def getLobbyInfo(self):
        return {
            "lobbyID" : self.lobby.getLobbyID(),
            "subjectName" : self.lobby.getSubject(),
            "generatedQRCode" : self.qr.getQrCode(),
            "maxPlayers" : self.lobby.getMaxPlayers()
        }

    def getConnectedPlayers(self):
        self.player = Player()
        return {
            "username" : self.player.getNickname(),
            "readyPlayer" : self.player.getStatus()
        }

    def getLobbySettings(self):
        return {
            "chosenSubjectName" : self.lobby.getSubject(),
            "chosenGameLength" : self.lobby.getMaxGameLength(),
            "chosenMaxPlayer" : self.lobby.getMaxPlayers()
        }