
class User(dict):
    def __init__(self, name, password, color, scoreList, timePlayed):
        self.name = name
        self.password = password
        self.color = color
        self.scoreList = scoreList

        #Statistixxxxxcs
        self.timePlayed = timePlayed

        dict.__init__(self, name = name, password = password, color = color, scoreList = scoreList, timePlayed = self.timePlayed)
        
    def edit(self, newUsername, newPassword, newColor):
        self.name = newUsername
        self.password = newPassword
        self.color = newColor

    def newScore(self, score, time):
        self.scoreList.append(score)
        self.timePlayed += time

    def save(self):
        ret = ""
        ret += "name:" + self.name + "/n"
        ret += "name:" + self.password + "/n"
        ret += "name:" + self.color + "/n"
        ret += "name:" + self.scoreList + "/n"
        
    def __setitem__(self, key, value):
        super(User, self).__setitem__(key, value)
