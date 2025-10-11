import requests
from datetime import datetime

KIWI_URL = "http://rx.linkfanel.net/kiwisdr_com.js"
KIWI_OUTPUT_FILE = "kiwiservers.js"

def utc_timestamp():
    return datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")

def write_with_header(filename, header_text, content):
    with open(filename, "w", encoding="utf-8") as f:
        f.write(header_text + "\n\n")
        f.write(content)

print("Fetching KiwiSDR server list...")

try:
    response = requests.get(KIWI_URL, timeout=30)
    if response.status_code != 200 or not response.text.strip():
        raise ValueError("Source unavailable or empty.")
    kiwi_text = response.text
except Exception as e:
    print(f"❌ Kiwi source unavailable: {e}")
    print("Skipping copy to avoid overwriting local file.")
    exit(0)

timestamp = utc_timestamp()
header = f"// Updated by XPloRR at {timestamp}"

write_with_header(KIWI_OUTPUT_FILE, header, kiwi_text)
print(f"✅ Wrote {KIWI_OUTPUT_FILE}")
