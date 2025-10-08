import re, tldextract
from datetime import datetime


def domain_from_url(url: str) -> str:
if not url:
return ""
tld = tldextract.extract(url)
return ".".join(part for part in [tld.domain, tld.suffix] if part)


def clean_text(s: str) -> str:
s = re.sub(r"\s+", " ", s or "").strip()
return s


def extract_numbers(sentence: str):
# Returns list of floats found in text (simple heuristic)
nums = re.findall(r"(?:(?:\d+\.\d+)|(?:\d+))(?:\s*(?:million|billion|thousand|k|m|bn))?", sentence.lower())
out = []
for n in nums:
val = n
mult = 1
if n.endswith("million") or n.endswith(" m"):
val = n.split()[0]; mult = 1_000_000
elif n.endswith("billion") or n.endswith(" bn"):
val = n.split()[0]; mult = 1_000_000_000
elif n.endswith("thousand") or n.endswith(" k"):
val = n.split()[0]; mult = 1_000
try:
out.append(float(val) * mult)
except: # ignore parse errors
pass
return out


def now_utc():
return datetime.utcnow()