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

def main():
    # set CWD
    os.chdir(os.path.dirname(__file__))
    # load settings
    OUTPUT_FILENAME, IGNORE_UNKNOWN, INCLUDE_REPEATS, REPEAT_INTERVAL = loadSettings()
    # load blacklist
    blacklistFile = open("BLACKLIST.json")
    BLACKLIST = json.load(blacklistFile)
    blacklistFile.close()
    
    # file I/O
    results = open(OUTPUT_FILENAME, 'w', encoding="utf-8")

    # iterate through "input" directory
    input_directory = os.path.join(os.getcwd(), "inputs")
    os.chdir(input_directory)
    for file in os.listdir(input_directory):
        try:
            myLog = Log(file)
            print(file)
        except LogFileNotFound:
                print("Log file not found. Do you have a file named: \"" + file + "\" in the same directory as this script?")
                input("Press ENTER to exit...")
                return -1

        # parse log
        previous_time = ''
        previous_event = ''
        max_dmg = 0
        for event in myLog:
            seconds = int(event[0].split(":")[1].split(".")[0])
            if IGNORE_UNKNOWN and re.search('unknown_.*', event[1]) or event[1] in BLACKLIST:
                continue
            if INCLUDE_REPEATS and event[1] not in BLACKLIST:
                output_string = event[0] + '\t' + event[1] + '\t' + event[2] + '\n'
                print(output_string)
                results.write(output_string)
                continue
            if event[1] not in BLACKLIST:
                if previous_event == '':
                    previous_time = event[0]
                    previous_event = event[1]
                    max_dmg = event[2]
                if previous_event == event[1]:
                    max_dmg = max(max_dmg, event[2])
                    continue
                else:
                    output_string = previous_time + '\t' + previous_event + '\t' + str(max_dmg) + '\n'
                    print(output_string)
                    results.write(output_string)
                    previous_time = event[0]
                    previous_event = event[1]
                    max_dmg = event[2]
        output_string = previous_time + '\t' + previous_event + '\t' + str(max_dmg) + '\n'
        print(output_string)
        results.write(output_string)

def loadSettings():
    jsonFile = open('SETTINGS.json', 'r', encoding='utf-8')
    jsonObj = json.load(jsonFile)
    settings = [jsonObj["OUTPUT_FILENAME"],
                jsonObj["IGNORE_UNKNOWN"].lower() == "true",
                jsonObj["INCLUDE_REPEATS"].lower() == "true",
                int(jsonObj["REPEAT_INTERVAL"])]
    jsonFile.close()
    return settings

if __name__ == '__main__':
    main()