class User:
    def __init__(self, nickname):
        self.nickname = nickname

    def getnickname(self):
        return {
            "username" : self.nickname
        }