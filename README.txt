Python 3.x script which finds the max damage dealt by an ability in a given log set.

[DEPENDENCIES]
a. Python 3.x https://www.python.org/
b. TO DOWNLOAD CSV LOGS FROM https://www.fflogs.com:
	Allies > Damage Taken > Events > [DOWNLOAD CSV]
	*you may have to download multiple CSV files for a log
[USAGE]
1. Place CSV files into "inputs" folder. Make sure to remove demo.csv
2. Run "abilityDamageParser"
	--output.txt for pasting into spreadsheet
	--outputs formatted results to command line

BLACKLIST.json contains the names of events the parser ignores
Ignores "attack" casts by default
Format Example:
	{
		"event_name":"",
		"event_name2":"",
			...
		"event_nameN":""
	}
