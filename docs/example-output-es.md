# Example Command line
PS D:\github\everything\pyeverything\bin> .\es.exe -p windows system32 drivers etc hosts -efu

# Example output
Filename,Size,Date Modified,Date Created,Attributes
"C:\Windows\System32\drivers\etc\hosts",959,133595279726435345,132201836974398552,8224
"C:\Windows\System32\drivers\etc\hosts.ics",438,133627481374926156,133033990216207556,8224
"C:\Windows\System32\drivers\etc\hosts_PowerToysBackup_20230302105429",1620,133178157426066816,133221956690693612,8224
"C:\Windows\System32\drivers\etc\lmhosts.sam",3683,132201835641223246,132201836974398552,8224

# Note
The first line is header line.
Columns name is not double-quoted.
Each trailing line represents a file.
Path string is double-quoted.
timestamp is Windows FILETIME format.

