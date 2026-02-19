import threading
import time

from Sysfiles.Model.Game import Game


class GameController:
    def __init__(self, lobbyController):
        self.lobbyController = lobbyController
        # List of dicts: {"lobbyID": int, "game": Game, "wordList": list, "timer_running": bool}
        self.gameList = []

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
        max_length = int(lobby_data.get("maxGameLength")) * 60
        entry["game"].setTime(max_length)

        if entry["timer_running"]:
            return {"message": "Timer already running for this lobby"}

        entry["timer_running"] = True

        def countdown():
            while entry["game"].getTime() > 0 and entry["timer_running"]:
                mins, secs = divmod(entry["game"].getTime(), 60)
                # Optional
                print(f"Lobby {lobbyID} - Time remaining: {mins:02d}:{secs:02d}")
                time.sleep(1)
                entry["game"].setTime(entry["game"].getTime() - 1)
            entry["timer_running"] = False
            entry["game"].callbackTimer()
            print(f"Lobby {lobbyID} - Time's up!")

        # Start in a daemon thread
        timer_thread = threading.Thread(target=countdown, daemon=True)
        timer_thread.start()

        return {"message": "Timer started"}

    def gameSession(self, lobbyID):
        """Get game session for a lobby, creating if needed."""
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
            recentWord = ""
            username = ""
        elif isinstance(recentWordEntry, dict):
            # get dict with "word" and "username"
            recentWord = recentWordEntry["word"]
            username = recentWordEntry["username"]
        else:
            recentWord = ""
            username = "Unknown"

        return {
            "gameID": game.getGameID(),
            "chosenSubject": (
                lobby_data.get("subjectName", "Default") if lobby_data else "Default"
            ),
            "isTimeUp": game.getIsTimeUp(),
            "time": game.getTime(),
            "currentLetter": recentWord[-1:],
            "usedWords": [
                entry["word"] if isinstance(entry, dict) else entry
                for entry in wordList
            ],
            "previousWord": {"username": username, "wordUsed": recentWord},
        }

    def isInputValid(self, chosenWord: str, lobbyID: int) -> bool:
        """Validate input for a specific lobby."""
        entry = self.get_game_entry(lobbyID)
        wordList = entry["wordList"]

        chosenWord = chosenWord.strip()
        if not chosenWord:
            return False

        # Handle dict format: extract "word" from each entry
        if chosenWord.lower() in (entry["word"].lower() for entry in wordList):
            return False

        if not wordList:
            return True

        # Get the actual word from the dict
        previousWord = wordList[-1]["word"]
        return chosenWord[0].lower() == previousWord[-1].lower()

    def addWord(self, word: str, lobbyID: int, userID: int) -> None:
        """Add word to a specific lobby."""
        entry = self.get_game_entry(lobbyID)

        player = self.getPlayer(lobbyID, userID)
        username = player if player else "Unknown"

        entry["wordList"].append({"word": word, "username": username})

    def updateTurnOrder(self, lobbyID: int):
        """Update turn order for a specific lobby."""
        gamePlayerList = self.lobbyController.getListOfPlayers(lobbyID)
        gamePlayerList.append(
            gamePlayerList.pop(gamePlayerList.index(gamePlayerList[0]))
        )
        return gamePlayerList

    # remove Game Entries when Lobby closes
    def removeGame(self, lobbyID: int) -> bool:
        """Remove game entry for a lobby (e.g., when lobby closes)."""
        for i, entry in enumerate(self.gameList):
            if entry["lobbyID"] == lobbyID:
                del self.gameList[i]
                return True
        return False
