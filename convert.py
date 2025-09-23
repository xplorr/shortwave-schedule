import requests
import re

URL = "https://www1.s2.starcat.ne.jp/ndxc/pc/ns/userlist1.txt"
OUTPUT_FILE = "shortwaveschedule.js"

# Fetch the file
text = requests.get(URL).text
lines = text.splitlines()

# Skip first 4 lines
lines = lines[4:]

data = []

for line in lines:
    if not line.strip():
        continue
    
    # Fixed-width parsing based on your snapshot
    freq = line[0:8].strip()
    time = line[8:21].strip()
    ITU  = line[21:26].strip()
    station = line[26:55].strip()
    lang = line[55:59].strip()
    location = line[59:71].strip()
    days = line[71:].strip()

    # Split start and end time
    match = re.match(r"(\d{4})-(\d{4})", time)
    if match:
        start, end = match.groups()
    else:
        start, end = "", ""

    entry = {
        "freq": freq,
        "startTime": start,
        "endTime": end,
        "ITU": ITU,
        "station": station,
        "language": lang,
        "Location": location,
        "days": days
    }
    data.append(entry)

# Write as JS file
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    f.write("var shortWaveSchedule = ")
    f.write(str(data).replace("'", '"'))  # JSON-like
    f.write(";\n")
