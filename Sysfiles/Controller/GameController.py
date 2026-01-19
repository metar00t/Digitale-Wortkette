import random
import string

from flask import request


class GameController:
    def __init__(self, playerController):
        self.playerController = playerController
        self.wordList = []


    def setGameStatus(self):
        return {
            "hasGameStarted": bool,
            "firstLetter": random.choice(string.ascii_letters)
        }


    def setPlayerOrder(self):
        playerList = self.playerController.lobbyController.playerList
        for player in playerList:
            pass


    def gameSession(self):
        currentWordList = self.wordList
        if not currentWordList:
            return {}, 204
        currentWord = currentWordList[-1]
        return {
            "chosenSubject": self.playerController.lobby.getSubject(),
            "timer": self.playerController.lobby.getMaxGameLength(),
            "currentLetter": currentWord[:1],
            "previousWords": {
                "wordUsed": currentWord,
                "username": self.playerController.player.getNickname()
            },
            "playerStatus": [
                "disconnected",
                "selected",
                "next",
                "connected",
                "suspend round"
            ],
            "wordsPerMinute": float # To be determined if still being used
        }


    def checkInput(self):
        # request.form['wordInput']
        # request.form.get('wordInput')
        chosenWord = request.form['wordInput']
        currentWord = self.wordList
        lastWord = self.wordList[-1]
        for checkWord in currentWord:
            if checkWord == chosenWord:
                return {"message":"Dieses Wort wurde bereits verwendet"}
            return chosenWord


    def addWord(self, word):
        self.wordList.append(word)


    def getWordList(self):
        return self.wordList

