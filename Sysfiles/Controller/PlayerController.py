from flask import request

from Sysfiles.Model.Player import Player

class PlayerController:
    def __init__(self, lobbyController):
        self.player = None
        self.lobbyController = lobbyController

    def playerJoins(self, lobbyID, userID):
        self.player = Player()
        username = request.form['nickname']
        if username.strip() == "":
            return {"message": "Bitte gib einen Usernamen ein"}
        status = request.form.get('isPlayerReady')
        self.player.setNickname(username)
        self.player.setStatus(status)
        playerAlreadyExists = self.getPlayer(userID, lobbyID)
        if playerAlreadyExists:
            return self.updatePlayer(lobbyID, userID, username, status)
        else:
            newPlayer = {
                "lobbyID": lobbyID,
                "userID": self.player.getUserID(),
                "hostID": 0,
                "username": self.player.getNickname(),
                "isPlayerReady": self.player.getStatus()
            }
            self.lobbyController.addPlayer(newPlayer)
            return newPlayer

    def getPlayer(self, userID, lobbyID):
        for players in self.lobbyController.playerList:
            if players["userID"] == userID and players["lobbyID"] == lobbyID:
                return True
        return False

    def updatePlayer(self, lobbyID, userID, username, status):
 #       self.player = Player()
        updatedPlayer = None
        for players in self.lobbyController.playerList:
            if players["userID"] == userID and players["lobbyID"] == lobbyID:
                players["isPlayerReady"] = status
                players["username"] = username
                updatedPlayer = {
                    "lobbyID": lobbyID,
                    "userID": players["userID"],
                    "hostID": 0,
                    "username": players["username"],
                    "isPlayerReady": status
                }
        return updatedPlayer

    def removePlayer(self, lobbyID, userID):
#        self.player = Player()
        players = self.lobbyController.playerList
        for i, p in enumerate(players):
            if p["userID"] == userID and p["lobbyID"] == lobbyID:
                del players[i]
                return True
        return False