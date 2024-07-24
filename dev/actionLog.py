from dev.log import Log
class actionLog(Log):
    def __init__(self, input):
        super().__init__(input)
        self.regex = "prepares"
    def __next__(self):
        return super().__next__().split("  ")[1]