""" 
Python 3.x script used to quickly analyze an FFLOGs Damage Taken Event log to find the maximum amount of damage an unmitigated cast would do.
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
        # parse log for unique action names
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
        
        # parse log for max damage
        for raw_event in damageEvents:
            for ability in ACTIONS:
                if re.search(ability, raw_event):
                    unmitigatedString= re.search("U: \d+", raw_event).group()
                    unmitigatedDMG = re.search("\d+", unmitigatedString).group()
                    ACTIONS.update({ability:str(max(ACTIONS[ability], unmitigatedDMG))})

    # output
    print("{:20} |\t {:7}".format(*["EVENT NAME", "MAX DAMAGE"]))
    print("{:20} |\t {:7}".format(*["-"*20, "-"*7]))
    for ability in ACTIONS:
        if int(ACTIONS[ability]) > 0:
            print("{:20} |\t {:7}".format(*[ability, ACTIONS[ability]]))
            results.write(ability +'\t'+ ACTIONS[ability] + '\n')
    results.close()
if __name__ == '__main__':
    main()
