import time

from Sysfiles.Model.Game import Game

class GameController:
    def __init__(self, playerController):
        self.playerController = playerController
        self.game = Game()
        self.wordList = []

    # Setting the Status of the Game Session to true
    def setGameStatus(self,lobbyID:int):
        for data in self.playerController.lobbyController.createdLobbies:
            if lobbyID == data["lobbyID"]:
                data["hasGameStarted"] = True
                break
        self.game.setTime(int(self.playerController.lobbyController.lobby.getMaxGameLength()) * 60)

    def timer(self):
        while self.game.getTime() > 0:
            time.sleep(1)
            self.game.setTime(self.game.getTime() - 1)
        return {"message": "Time's up"}


    def gameSession(self):
        currentWordList = self.wordList
        recentWord = currentWordList[-1] if currentWordList else ""
        self.timer()
        return {
            "chosenSubject": self.playerController.lobbyController.lobby.getSubject(),
            "time": self.game.getTime(),
            "currentLetter": recentWord[:1],
            "usedWords" : self.wordList,
            "previousWord": {
                "wordUsed": recentWord,
                "username": self.playerController.lobbyController.player.getNickname()
            },
       #     "playerStatus": [
         #       "connected",
          #      "disconnected"
           # ]
        }

    def isInputValid(self, chosenWord: str) -> bool:
        chosenWord = chosenWord.strip()

        if not chosenWord:
            return False

        if chosenWord.lower() in (word.lower() for word in self.wordList):
            return False

        if not self.wordList:
            return True

        previousWord = self.wordList[-1]
        return chosenWord[0].lower() == previousWord[-1].lower()

    def addWord(self, word:str) -> None:
        self.wordList.append(word)


    def updateTurnOrder(self,lobbyID:int):
        gamePlayerList = self.playerController.lobbyController.getListOfPlayers(lobbyID)
        gamePlayerList.append(gamePlayerList.pop(gamePlayerList.index(gamePlayerList[0])))
        return gamePlayerList