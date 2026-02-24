import time


class Helper:

    def countdown(self, entry):
        while entry["game"].getTime() > 0 and entry["timer_running"]:
            mins, secs = divmod(entry["game"].getTime(), 60)
            time.sleep(1)
            entry["game"].setTime(entry["game"].getTime() - 1)
        entry["timer_running"] = False
        entry["game"].callbackTimer()
