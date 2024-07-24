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

### HELPER METHODS ###

"""
Splits str separated by , returns list [TIME, EVENT]
tokens[0] = RAW_TIME
tokens[1] = RAW_EVENT
INPUT_LINE is just a string
"""
def generate_tokens(input_line):
    tokens = input_line.split(',')
    return [tokens[0], str.strip(tokens[1])]

def parse_event_dmg(event_input):
    print(event_input.split("  "))
    raw_dmg_string = re.search("U: [0-9]+", event_input)
    unmitigated_dmg = re.search("\d+", str(raw_dmg_string.group())).group()
    ability_name = event_input
    return ability_name, unmitigated_dmg
    
def parse_time(time_input):
    clean_time = time_input.replace("\"", '') #clean timestamp input
    time_tokens = clean_time.split('.')
    main_timestamp = time_tokens[0]
    rounded_sub = str(floor(int(time_tokens[1])/ROUND)) +'00'
    return main_timestamp + '.' + rounded_sub[0:3]