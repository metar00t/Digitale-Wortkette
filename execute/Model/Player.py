from flask import request

class Player:
    _usedNicknames = []
    _userID = 0

    def __init__(self):
        self.nickname = request.form['nickname']
        self.status = request.form.get('readyPlayer')
        self.userID = Player._userID + 1
        Player._userID += 1
        Player._usedNicknames.append(self.nickname)

    def getNickname(self):
        return self.nickname

    def getStatus(self):
        return self.status