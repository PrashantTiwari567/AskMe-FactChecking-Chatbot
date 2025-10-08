import re
from typing import Tuple
from dateparser import parse as dateparse

try:
    import pint
    _ureg = pint.UnitRegistry()
except Exception:
    _ureg = None

_ft_in_pattern = re.compile(r"(\d+)'\s*(\d+)?\"?")  # e.g., 5' 11"

def normalize_units(text: str) -> str:
    if not _ureg:
        return text
    def _conv(match):
        feet = float(match.group(1))
        inches = float(match.group(2) or 0)
        total_inches = feet * 12 + inches
        cm = (total_inches * _ureg.inch).to(_ureg.cm).magnitude
        return f"{feet} ft {inches} in (~{cm:.2f} cm)"
    text = _ft_in_pattern.sub(_conv, text)
    return text

def normalize_date(s: str) -> Tuple[str, str]:
    dt = dateparse(s)
    if not dt:
        return s, ""
    return dt.strftime("%Y-%m-%d"), dt.isoformat()
