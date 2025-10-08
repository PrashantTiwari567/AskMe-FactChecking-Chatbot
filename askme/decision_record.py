import json, os
from datetime import datetime
from .types import Evidence, Claim

def write_decision_record(query: str, claims: list[Claim], evidence: list[Evidence], out_dir: str = "data/cache") -> str:
    os.makedirs(out_dir, exist_ok=True)
    payload = {
        "query": query,
        "timestamp": datetime.utcnow().isoformat(),
        "claims": [c.model_dump() for c in claims],
        "evidence": [e.model_dump() for e in evidence],
    }
    path = os.path.join(out_dir, f"decision_{int(datetime.utcnow().timestamp())}.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2, default=str)
    return path
