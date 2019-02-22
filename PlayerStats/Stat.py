class Stat:

    def __init__(self, statName, value, rank):
        self.statName = statName
        self.value = value
        self.rank = rank

    def getstatname(self):
        return self.statName

    def getvalue(self):
        return self.value

    def getrank(self):
        return self.rank
