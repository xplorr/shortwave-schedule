import requests
import json
from datetime import datetime

URL = "https://www1.s2.starcat.ne.jp/ndxc/pc/ns/userlist1.txt"
OUTPUT_FILE = "shortwaveschedule.js"

# Fetch the file
text = requests.get(URL).text
lines = text.splitlines()

# First line for comment header
first_line = lines[0].strip()
timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")
header_comment = f"// {first_line} (converted by XPloRR at {timestamp})"

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

# Write as nicely formatted JS file with comment header
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    f.write(header_comment + "\n\n")
    f.write("var shortWaveSchedule = [\n")
    for entry in data:
        f.write("  " + json.dumps(entry, ensure_ascii=False) + ",\n")
    f.write("];\n")
