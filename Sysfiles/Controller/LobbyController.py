from typing import Any

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

    def createLobby(self, auth_manager_object) -> dict[str, int]:
        """
        Create a new Lobby
        :return: Lobby Object
        :rtype: dict[str,int]
        """
        self.lobby = Lobby()
        self.host = Host()
        self.player = Player()
        self.qr = QrCodeController(f"dwk://player/{self.lobby.getLobbyID()}/join")
        auth_token = auth_manager_object.auth_token(
            subject= self.host.getUserID(),
            scope={"Host": True}
        )
        createdLobby : dict[str,int] = {
            "lobbyID": self.lobby.getLobbyID(),
            "hasGameStarted": False,
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
        host : dict[str,int] = {
            "lobbyID": self.lobby.getLobbyID(),
            "userID": self.host.getUserID(),
            "hostID": int(f"{self.lobby.getLobbyID()}0{self.host.getUserID()}{self.host.getHostID()}"),
            "username": "Host",
            "isPlayerReady": "true",
            "auth_token" : auth_token.signed
        }
        self.playerList.append(host)
        self.createdLobbies.append(createdLobby)
        return createdLobby

    def addPlayer(self, player: dict[str, int]) -> None:
        """
        Add Player to Lobby
        :param player: Player Object
        :type player: dict[str,int]
        :return: Nothing
        :rtype: None
        """
        self.playerList.append(player)

    def updateLobby(self) -> None:
        """
        Updates the Lobby Metadata
        :return: Nothing
        :rtype: None
        """
        lobbyID = self.lobby.getLobbyID()
        chosenSubject = request.form.get('subjectName')
        chosenMaxPlayers = request.form.get('maxPlayers')
        chosenMaxGameLength = request.form.get('maxGameLength')
        hasGameStarted = request.form.get('hasGameStarted')
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
                if hasGameStarted is not None:
                    lobbies["hasGameStarted"] = hasGameStarted
                break

    def getChosenLobbySettings(self, lobbyID: int) -> dict[str, int]:
        """
        Get the current LobbySettings
        :param lobbyID: ID of Lobby
        :type lobbyID: int
        :return: LobbySettings
        :rtype: dict[str,int]
        """
        for lobbies in self.createdLobbies:
            if lobbyID == lobbies["lobbyID"]:
                return {
                    "chosenSubject": lobbies["subjectName"],
                    "chosenMaxPlayers": lobbies["maxPlayers"],
                    "chosenMaxGameLength": lobbies["maxGameLength"],
                    "hasGameStarted": lobbies["hasGameStarted"]
                }
        return {}

    def getLobbyList(self) -> list[Any] | None:
        """
        Get the current Lobbies
        :return: List of active Lobbies
        :rtype: list[Any]
        """
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

    def closeLobby(self, lobbyID: int, hostID: int) -> bool:
        """
        Close Lobby
        :param lobbyID: ID of Lobby
        :type lobbyID: int
        :param hostID: ID of Host
        :type hostID: int
        :return: Response if the operation was successful or not
        :rtype: bool
        """
        lobbies = self.createdLobbies
        players = self.playerList
        for i, l in enumerate(lobbies):
            for j, p in enumerate(players):
                if l["lobbyID"] == lobbyID and p["lobbyID"] == lobbyID and p["hostID"] == hostID:
                    del lobbies[i]
                    del players[j]
                    return True
        return False

    def isPlayerLimitReached(self, lobbyID: int) -> bool:
        """
        Player Limit Validation
        :param lobbyID: ID of Lobby
        :type lobbyID: int
        :return: True if PlayerLimit has been reached and False if not
        :rtype: bool
        """
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

    def getListOfPlayers(self, lobbyID: int) -> list[Any]:
        """
        Get List of Players in Lobby
        :param lobbyID: ID of Lobby
        :type lobbyID: int
        :return: List of Players in Lobby
        :rtype: list[Any]
        """
        playerList = []
        for data in self.playerList:
            if lobbyID == data["lobbyID"]:
                playerInfo = {
                    "lobbyID": data["lobbyID"],
                    "userID": data["userID"],
                    "hostID": data["hostID"],
                    "username": data["username"],
                    "isPlayerReady": data["isPlayerReady"],
                    "auth_token": data["auth_token"]
                }
                playerList.append(playerInfo)
        return playerList
