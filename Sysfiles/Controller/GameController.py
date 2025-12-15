import random
import string

from flask import request


class GameController:
    def setGameStatus(self):
        return {
            "hasGameStarted": bool,
            "firstLetter": random.choice(string.ascii_letters)
        }

    def gameSession(self):
        if self.lobby is None and self.player is None:
            return {}, 204
        currentWordList = self.lobby.getWordList()
        if not currentWordList:
            return {}, 204
        currentWord = currentWordList[-1]
        return {
            "chosenSubject": self.lobby.getSubject(),
            "timer": float,
            "currentLetter": currentWord[:1],
            "previousWords": {
                "wordUsed": currentWord,
                "username": self.player.getNickname()
            },
            "playerStatus": [
                "disconnected",
                "selected",
                "next",
                "connected",
                "suspend round"
            ],
            "wordsPerMinute": float,
            "usableWord": bool
        }

    def checkInput(self):
        # request.form['wordInput']
        # request.form.get('wordInput')
        chosenWord = request.form['wordInput']
        currentWordList = self.lobby.getWordList()
        for checkWord in currentWordList:
            if checkWord == chosenWord:
                break
            return chosenWord

    def addWord(self, word):
        return self.lobby.setCurrentWord(word)