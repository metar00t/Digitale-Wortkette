import time


class Helper:

    def __init__(self):
        self.entry = None

    def setEntry(self, entry):
        """
        Sets the Entry Object for further Processing
        :param entry: Entry Dictionary
        :type entry: dict
        """
        self.entry = entry

    def countdown(self):
        """
        Countdown Method for handling the Time left in the Game-Session
        """
        while self.entry["game"].getTime() > 0 and self.entry["timer_running"]:
            mins, secs = divmod(self.entry["game"].getTime(), 60)
            time.sleep(1)
            self.entry["game"].setTime(self.entry["game"].getTime() - 1)
        self.entry["timer_running"] = False
        self.entry["game"].callbackTimer()

    def normalize_word_list(self, wordList: list) -> list:
        """
        Normalize wordList so every entry has the structure:
        {"word": str, "username": str}
        """
        __DEFAULT_USERNAME__ = "Unbekannt"

        return [
            {
                "word": item["word"] if isinstance(item, dict) else item,
                "username": item["username"] if isinstance(item, dict) else __DEFAULT_USERNAME__
            }
            for item in wordList
        ]
