import threading
import time

from Sysfiles.Model.Game import Game
from Sysfiles.Helper.Helper import Helper


class GameController:
    def __init__(self, lobbyController):
        self.lobbyController = lobbyController
        # List of dicts: {"lobbyID": int, "game": Game, "wordList": list, "timer_running": bool}
        self.gameList = []
        self.turnOrder = []
        self.helper = Helper()

    def get_game_entry(self, lobbyID):
        """Helper to get or create a game entry for a lobbyID."""
        for entry in self.gameList:
            if entry["lobbyID"] == lobbyID:
                return entry
        # Create new entry if not found
        new_entry = {
            "lobbyID": lobbyID,
            "game": Game(),
            "wordList": [],
            "timer_running": False,
        }
        self.gameList.append(new_entry)
        return new_entry

    def getPlayer(self, lobbyID: int, userID: int):
        """
        Filter and get player dict by userID and lobbyID, like PlayerController's updatePlayer logic.
        :param lobbyID: ID of Lobby
        :type lobbyID: int
        :param userID: ID of User
        :type userID: int
        :return: Player dict or None if not found
        :rtype: dict or None
        """
        for player in self.lobbyController.playerList:
            if player["userID"] == userID and player["lobbyID"] == lobbyID:
                return player["username"]
        return None

    def timer(self, lobbyID):
        """Start a non-blocking timer for a specific lobby."""
        entry = self.get_game_entry(lobbyID)
        lobby_data = None
        for lobby in self.lobbyController.createdLobbies:
            if lobby["lobbyID"] == lobbyID:
                lobby_data = lobby
                break
        if not lobby_data:
            return {"message": "Lobby not found"}

        # Convert minutes to seconds
        max_length = int(lobby_data.get("maxGameLength")[0]) * 60
        entry["game"].setTime(max_length)

        if entry["timer_running"]:
            return {"message": "Timer already running for this lobby"}

        entry["timer_running"] = True

        self.helper.setEntry(entry)
        self.helper.countdown()

        # Start in a daemon thread
        timer_thread = threading.Thread(
            target=self.helper.countdown, daemon=True)
        timer_thread.start()

        return {"message": "Timer started"}

    def setStartingTurnOrder(self, lobbyID: int):
        self.turnOrder = self.lobbyController.getListOfPlayers(lobbyID)

    def getTurnOrder(self):
        return self.turnOrder

    def gameSession(self, lobbyID):
        """Get game session for a lobby, creating a new game session if needed."""
        # Constants for Default Fallback Values
        __DEFAULT_SUBJECTNAME__: str = "Tiere"
        __DEFAULT_USERNAME__: str = "Unbekannt"
        __DEFAULT_WORDENTRY__: str = ""

        entry = self.get_game_entry(lobbyID)

        # Start timer only if not running
        if not entry["timer_running"]:
            self.timer(lobbyID)

        game = entry["game"]
        wordList = entry["wordList"]
        lobby_data = None
        for lobby in self.lobbyController.createdLobbies:
            if lobby["lobbyID"] == lobbyID:
                lobby_data = lobby
                break

        currentWordList = wordList
        recentWordEntry = currentWordList[-1] if currentWordList else None

        # Handle both old string entries and new dict entries
        if recentWordEntry is None:
            recentWord = __DEFAULT_WORDENTRY__
            username = __DEFAULT_USERNAME__
        elif isinstance(recentWordEntry, dict):
            # get dict with "word" and "username"
            recentWord = recentWordEntry["word"]
            username = recentWordEntry["username"]
        else:
            recentWord = __DEFAULT_WORDENTRY__
            username = __DEFAULT_USERNAME__

        return {
            "gameID": game.getGameID(),
            "chosenSubject": (
                lobby_data.get(
                    "subjectName", __DEFAULT_SUBJECTNAME__) if lobby_data else __DEFAULT_SUBJECTNAME__
            ),
            "isTimeUp": game.getIsTimeUp(),
            "time": game.getTime(),
            "turnOrder": self.getTurnOrder(),
            "currentLetter": recentWord[-1:],
            "usedWords": [  # Conditional Expression for extracting the value associated with the key
                {
                    "word": entry["word"] if isinstance(entry, dict) else entry,
                    "username": entry["username"] if isinstance(entry, dict) else None
                }
                for entry in wordList
            ],
            "previousWord": {"username": username, "wordUsed": recentWord},
        }

    def isInputValid(self, chosenWord: str, lobbyID: int) -> bool:
        """Validate input for a specific lobby."""
        entry = self.get_game_entry(lobbyID)
        wordList = entry["wordList"]

        chosenWord = chosenWord.strip()
        # No Whitespace allowed :(
        if not chosenWord:
            return False

        # applies to the first round (Host starts the game)
        if not wordList:
            return True

        # Handle dict format: extract "word" from each entry
        if chosenWord.lower() in (entry["word"].lower() for entry in wordList):
            return False

        # Get the actual word from the dict
        previousWord = wordList[-1]["word"]
        return chosenWord[0].lower() == previousWord[-1].lower()

    def addWord(self, word: str, lobbyID: int, userID: int) -> None:
        """Add word to a specific lobby."""
        entry = self.get_game_entry(lobbyID)

        player = self.getPlayer(lobbyID, userID)
        username = player if player else "Unknown"

        entry["wordList"].append({"word": word, "username": username})

    def updateTurnOrder(self):
        """Update turn order for a specific lobby."""
        self.turnOrder.append(
            self.turnOrder.pop(self.turnOrder.index(self.turnOrder[0]))
        )

    from collections import Counter

    def getGameStats(self, lobbyID: int) -> dict:
        """
        Compute game statistics for a specific lobby.
        Returns a dictionary with:
        - words per player
        - total words
        - longest word(s)
        - shortest word(s)
        - player(s) with most words
        """
        entry = self.get_game_entry(lobbyID)
        wordList = entry["wordList"]
    
        # Count words per player
        playerCounts = Counter(item["username"] for item in wordList)
    
        # Total number of words
        totalWords = len(wordList)
    
        # Longest word(s)
        longestWordLength = max((len(item["word"]) for item in wordList), default=0)
        longestWords = [item["word"] for item in wordList if len(item["word"]) == longestWordLength]
    
        # Shortest word(s)
        shortestWordLength = min((len(item["word"]) for item in wordList), default=0)
        shortestWords = [item["word"] for item in wordList if len(item["word"]) == shortestWordLength]
    
        # Player(s) with most words
        if playerCounts:
            maxCount = max(playerCounts.values())
            mostWordsPlayers = [username for username, count in playerCounts.items() if count == maxCount]
        else:
            mostWordsPlayers = []
    
        return {
            "wordsPerPlayer": dict(playerCounts),
            "totalWords": totalWords,
            "longestWords": longestWords,
            "shortestWords": shortestWords,
            "mostWordsPlayers": mostWordsPlayers
        }