class Stat:

    def __init__(self, legendName, statName, value, rank):
        self.legendName = legendName
        self.statName = statName
        self.value = value
        self.rank = rank

    def __repr__(self):
        return "\n" + self.statName + "\nValue: " + str(self.value) + "\nRank: " + str(self.rank) + "\n"

    def getstatname(self):
        return self.statName

    def getvalue(self):
        return self.value

    def getrank(self):
        return self.rank
