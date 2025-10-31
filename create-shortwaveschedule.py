import requests
import json
from datetime import datetime

AOKI_URL = "https://www1.m2.mediacat.ne.jp/binews/us/nz/userlist1.txt"
AOKI_OUTPUT_FILE = "shortwaveschedule.js"

def utc_timestamp():
    return datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")

def write_with_header(filename, header_text, content):
    with open(filename, "w", encoding="utf-8") as f:
        f.write(header_text + "\n\n")
        f.write(content)

print("Fetching AOKI shortwave schedule...")

try:
    response = requests.get(AOKI_URL, timeout=30)
    if response.status_code != 200 or not response.text.strip():
        raise ValueError("Source unavailable or empty.")
    aoki_text = response.text
except Exception as e:
    print(f"❌ AOKI source unavailable: {e}")
    print("Skipping conversion to avoid overwriting local file.")
    exit(0)

aoki_lines = aoki_text.splitlines()
if len(aoki_lines) < 5:
    print("❌ AOKI data too short or invalid.")
    print("Skipping conversion to avoid overwriting local file.")
    exit(0)

first_line = aoki_lines[0].strip()
timestamp = utc_timestamp()
header_comment = f"// {first_line} (AOKI Database converted by XPloRR at {timestamp})"

# Skip first 4 header lines
aoki_lines = aoki_lines[4:]

data = []
for line in aoki_lines:
    if not line.strip():
        continue

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

aoki_js = "var shortWaveSchedule = [\n"
for entry in data:
    aoki_js += "  " + json.dumps(entry, ensure_ascii=False) + ",\n"
aoki_js += "];\n"

write_with_header(AOKI_OUTPUT_FILE, header_comment, aoki_js)
print(f"✅ Wrote {AOKI_OUTPUT_FILE}")
