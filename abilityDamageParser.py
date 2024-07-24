""" 
Script to convert a CSV of enemy casts into a clean timestring for spreadsheets where each line is of the form:
 TIME \t ABILITYNAME \n

SETTINGS.json contains the following:
    INPUT_FILENAME [filename]   -   name of the input file
    OUTPUT_FILENAME [filename]  -   name of the desired output file
    INCLUDE_REPEATS [True/False] -  includes repeated damage events (ie spread mechanics which resolve simultaneously)
    IGNORE_UNKNOWN [True/False] -   ignore unknown_* events
    REPEAT_INTERVAL [int] -         time between repeated events allowed before they are considered to be repeats that should be ignored
                                    // Useful for ignoring spread mechanics which occur concurrently while allowing repeat raidwides through
Add event names you want to ignore to BLACKLIST.json
"""
import os, re, json
from dev.log import Log, LogFileNotFound
from dev.actionLog import actionLog
from dev.damageLog import damageLog
def main():
    # set CWD
    os.chdir(os.path.dirname(__file__))
    # load blacklist
    blacklistFile = open("BLACKLIST.json")
    BLACKLIST = json.load(blacklistFile)
    blacklistFile.close()
    
    # file I/O
    results = open("output.txt", 'w', encoding="utf-8")
    input_directory = os.path.join(os.getcwd(), "inputs")
    os.chdir(input_directory)
    # generate Ability Dictionary
    ACTIONS = {}
    directory_list = os.listdir(input_directory)
    for file in directory_list:
        try:
            actionEvents = actionLog(file)
        except LogFileNotFound:
                print("Log file not found. actionLog could not be initialized. Do you have a file named: \"" + file + "\" in the same directory as this script?")
                input("Press ENTER to exit...")
                return -1
        # parse log
        for event in actionEvents:
            if event in BLACKLIST or event in ACTIONS: continue
            else: ACTIONS.update({event:"0"})
    
    # parse for ability damage
    for file in directory_list:
        try:
            damageEvents = damageLog(file)
        except LogFileNotFound:
            print("Log file not found. damageLog could not be initialized. Do you have a file named: \"" + file + "\" in the same directory as this script?")
            input("Press ENTER to exit...")
            return -1

if __name__ == '__main__':
    main()