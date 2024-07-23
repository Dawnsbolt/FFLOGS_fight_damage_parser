""" 
Script to convert a CSV of enemy casts into a clean timestring for spreadsheets where each line is of the form:
 TIME \t ABILITYNAME \n

SETTINGS.json contains the following:
    INPUT_FILENAME [filename]   -   name of the input file
    OUTPUT_FILENAME [filename]  -   name of the desired output file
    IGNORE_REPEATS [True/False] -   ignore consecutive events that occur within 1 second of each other
    IGNORE_UNKNOWN [True/False] -   ignore unknown_* events
    REPEAT_INTERVAL [int] -         time between repeated events allowed before they are considered to be repeats that should be ignored
                                    // Useful for ignoring spread mechanics which occur concurrently while allowing repeat raidwides through
Add event names you want to ignore to BLACKLIST.json
"""
import os, re, json
from dev.log import Log, LogFileNotFound

def main():
    # set CWD
    os.chdir(os.path.dirname(__file__))
    # load settings
    INPUT_FILENAME, OUTPUT_FILENAME, IGNORE_UNKNOWN, IGNORE_REPEATS, REPEAT_INTERVAL = loadSettings()
    # load blacklist
    blacklistFile = open("BLACKLIST.json")
    BLACKLIST = json.load(blacklistFile)
    blacklistFile.close()
    
    # file I/O
    results = open(OUTPUT_FILENAME, 'w', encoding="utf-8")
    # initialize generator
    try:
        myLog = Log(INPUT_FILENAME)
    except LogFileNotFound:
            print("Log file not found. Do you have a file named: \"" + INPUT_FILENAME + "\" in the same directory as this script?")
            input("Press ENTER to exit...")
            return -1

    # parse log
    previous_event = ''
    for event in myLog:
        seconds = int(event[0].split(":")[1].split(".")[0])
        if IGNORE_UNKNOWN and re.search('unknown_.*', event[1]) or event[1] in BLACKLIST:
            continue
        if IGNORE_REPEATS and previous_event == event[1] and seconds-previous_time < REPEAT_INTERVAL:
            previous_time = seconds
            continue
        if event[1] not in BLACKLIST:
            output_string = event[0] + '\t' + event[1] + '\t' + event[2] + '\n'
            print(output_string)
            results.write(output_string)
            previous_time = seconds
            previous_event = event[1]

def loadSettings():
    jsonFile = open('SETTINGS.json', 'r', encoding='utf-8')
    jsonObj = json.load(jsonFile)
    settings = [jsonObj["INPUT_FILENAME"], 
                jsonObj["OUTPUT_FILENAME"],
                jsonObj["IGNORE_UNKNOWN"].lower() == "true",
                jsonObj["IGNORE_REPEATS"].lower() == "true",
                int(jsonObj["REPEAT_INTERVAL"])]
    jsonFile.close()
    return settings

if __name__ == '__main__':
    main()