from flask import request

from Sysfiles.Model.Player import Player


class PlayerController:
    def __init__(self, lobbyController):
        self.player = None
        self.lobbyController = lobbyController


    def playerJoins(self, lobbyID : int, userID : int) -> dict[str,int] | dict[str,str]:
        """
        Adds Player to the chosen Lobby
        :param lobbyID: ID of chosen Lobby
        :type lobbyID: int
        :param userID: ID of the joining User
        :type userID: int
        :return: Player Object or Error-Message
        :rtype: dict[str,int] | dict[str,str]
        """
        self.player = Player()
        username = request.form['nickname']
        status = request.form.get('isPlayerReady')
        if username.strip() == "":
            return {"message": "Bitte gib einen Usernamen ein"}
        self.player.setNickname(username)
        self.player.setStatus(status)
        playerExists : bool = self.hasPlayer(userID, lobbyID)
        if playerExists:
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


    def hasPlayer(self, userID : int, lobbyID : int) -> bool:
        """
        Checks if Player already exists in the current Lobby
        :param userID: ID of User
        :type userID: int
        :param lobbyID: ID of Lobby
        :type lobbyID: int
        :return: True if Player exists and False if not
        :rtype: bool
        """
        for players in self.lobbyController.playerList:
            if players["userID"] == userID and players["lobbyID"] == lobbyID:
                return True
        return False


    def updatePlayer(self, lobbyID : int, userID : int, username : str, status : bool) -> dict[str,int]:
        """
        Updates the Player
        :param lobbyID: ID of Lobby
        :type lobbyID: int
        :param userID: ID of User
        :type userID: int
        :param username: Username to Change
        :type username: str
        :param status: Status of Player
        :type status: bool
        :return: Updated Player
        :rtype: dict[str,int]
        """
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


    def removePlayer(self, lobbyID : int, userID : int) -> bool:
        """
        Removes Player from Lobby
        :param lobbyID: ID of Lobby
        :type lobbyID:
        :param userID: ID of User
        :type userID:
        :return: Response if success or fail
        :rtype: bool
        """
        players = self.lobbyController.playerList
        for i, p in enumerate(players):
            if p["userID"] == userID and p["lobbyID"] == lobbyID:
                del players[i]
                return True
        return False
