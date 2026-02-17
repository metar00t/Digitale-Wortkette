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

    def timer(self):
        while self.game.getTime():
            mins,secs = divmod(self.game.getTime(),60)
            timer = '{:02d}:{:02d}'.format(mins, secs)
            time.sleep(1)
            timer -= 1
            self.game.setTime(timer)
        return {"message":"Time's up"}


    def gameSession(self):
        currentWordList = self.wordList
        recentWord = currentWordList[-1]
        self.game.setTime(self.playerController.lobby.getMaxGameLength()*60)
        return {
            "chosenSubject": self.playerController.lobby.getSubject(),
            "time": self.game.getTime(),
            "currentLetter": recentWord[:1],
            "usedWords" : self.wordList,
            "previousWord": {
                "wordUsed": recentWord,
                "username": self.playerController.player.getNickname()
            },
       #     "playerStatus": [
         #       "connected",
          #      "disconnected"
           # ]
        }


    def doesWordAlreadyExist(self, chosenWord) -> bool:
        currentWord = self.wordList
        for checkWord in currentWord:
            if checkWord == chosenWord:
                return False
        return True


    def addWord(self, word:str) -> None:
        self.wordList.append(word)


    def updateTurnOrder(self,lobbyID:int):
        gamePlayerList = self.playerController.lobbyController.getListOfPlayers(lobbyID)
        gamePlayerList.append(gamePlayerList.pop(gamePlayerList.index(gamePlayerList[0])))
        return gamePlayerList