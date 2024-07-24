import os, re
from math import floor
"""
LOG is an iterator which parses a CSV textfile into [TIMESTAMP, EVENT_NAME]
Iterates over lines which have a match of provided regex
"""
ROUND = 100
class Log:
    def __init__(self, INPUT_FILENAME):
        self.file = None
        self.previous_event = ''
        # Verify input file path
        if not os.path.isfile(INPUT_FILENAME):
            raise LogFileNotFound(INPUT_FILENAME)
        # Open input file
        self.file = open(INPUT_FILENAME, 'r', encoding="utf-8")
        self.regex = ""
    
    def __del__(self):
        if self.file and not self.file.closed:
            self.file.close()

    def __iter__(self):
        return self
    
    def __next__(self):
        line = next(self.file)
        while (not re.search(self.regex, line)):
            line = next(self.file)
        return line

class LogFileNotFound(FileNotFoundError):
    def __init__(self, EXPECTED_FILENAME):
        self.expected = EXPECTED_FILENAME
