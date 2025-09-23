import requests
import json

URL = "https://www1.s2.starcat.ne.jp/ndxc/pc/ns/userlist1.txt"
OUTPUT_FILE = "shortwaveschedule.js"

# Fetch the file
text = requests.get(URL).text
lines = text.splitlines()

# Skip first 4 header lines
lines = lines[4:]

data = []

for line in lines:
    if not line.strip():
        continue

    # Fixed-width parsing
    freq     = line[0:14].strip()
    start    = line[14:18].strip()
    end      = line[19:23].strip()
    ITU      = line[30:34].strip()
    station  = line[34:59].strip()
    language = line[59:63].strip()
    location = line[63:75].strip()
    days     = line[75:].strip()

    entry = {
        "freq": freq,
        "startTime": start,
        "endTime": end,
        "ITU": ITU,
        "station": station,
        "language": language,
        "location": location,
        "days": days
    }
    data.append(entry)

# Write as nicely formatted JS file
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    f.write("var shortWaveSchedule = [\n")
    for entry in data:
        f.write("  " + json.dumps(entry, ensure_ascii=False) + ",\n")
    f.write("];\n")
