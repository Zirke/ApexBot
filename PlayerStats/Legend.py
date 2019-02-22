from PlayerStats import Stat


class Legend:
    def __init__(self, legendName, stats):
        self.legendName = legendName
        self.stats = stats

    # Overwriting tostring
    def __repr__(self):
        return ">>>>>Legend name<<<<<: " + self.legendName + "\nStats: " + str(self.stats) +"\n"
