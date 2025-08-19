## Example: es.exe CSV Output

Command

```
PS D:\github\everything\pyeverything\bin> .\es.exe -p windows system32 drivers etc hosts -efu
```

Output

```csv
Filename,Size,Date Modified,Date Created,Attributes
"C:\Windows\System32\drivers\etc\hosts",959,133595279726435345,132201836974398552,8224
"C:\Windows\System32\drivers\etc\hosts.ics",438,133627481374926156,133033990216207556,8224
"C:\Windows\System32\drivers\etc\hosts_PowerToysBackup_20230302105429",1620,133178157426066816,133221956690693612,8224
"C:\Windows\System32\drivers\etc\lmhosts.sam",3683,132201835641223246,132201836974398552,8224
```

Notes

- Header: The first line is a CSV header. Column names are not quoted.
- Rows: Each subsequent line represents one file.
- Full path: The first column, “Filename”, contains the full path and is quoted.
- Size: Integer byte size.
- Timestamps: “Date Modified” and “Date Created” are Windows FILETIME values (100‑ns since 1601‑01‑01 UTC).
- Attributes: Numeric file attributes bitmask.

About `-efu`

- `-efu` is a single command‑line option. Treat it as one token; it produces the CSV format shown above with FILETIME timestamps, matching the example output.

Tips

- Grouping: `es.exe` accepts grouped short options (e.g., `-efu`).
- Full paths in text mode: Use `-p` to print full paths when not exporting CSV (text mode).

