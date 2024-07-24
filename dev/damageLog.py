from dev.log import Log
class damageLog(Log):
    def __init__(self, input):
        super().__init__(input)
        self.regex = "U: [0-9]+, M: [0-9]+"
    