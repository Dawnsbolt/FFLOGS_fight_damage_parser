Python 3.x script used to convert an FFLOGs CSV of enemy casts into a clean timestring for spreadsheets where each line is of the form:
	[time]	[event_name]

[DEPENDENCIES]
Requires Python 3.x - https://www.python.org/
TO DOWNLOAD CSV LOGS FROM https://www.fflogs.com:
	Enemies > Casts > Events > [DOWNLOAD CSV]
	* Include All Begin Casts can be used to add a duplicate line event for start of casts; Default is when cast is complete
[USAGE]
	1. Place your input file [DEFAULT="in.csv"]in same directory as the script
	2. Configure SETTINGS.json and BLACKLIST.json
	3. Run ffSpreadsheetCAST.py
	4. Output should be [OUTPUT_FILENAME].txt within the directory script was run

[CONFIGURATION]
SETTINGS.json contains the following:
	INPUT_FILENAME [filename]   -   name of the input file
	OUTPUT_FILENAME [filename]  -   name of the desired output file
	IGNORE_REPEATS [True/False] -   ignore consecutive repeated events (eg spread mechanics);
	IGNORE_UNKNOWN [True/False] -   ignore unknown_* events
	REPEAT_INTERVAL [int] - minimum time allowed between repeated events before they are ignored

BLACKLIST.json contains the names of events the parser ignores
Ignores "attack" casts by default
Format Example:
	{
		"event_name":"",
		"event_name2":"",
			...
		"event_nameN":""
	}
