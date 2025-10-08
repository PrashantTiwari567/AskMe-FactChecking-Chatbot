import pandas as pd
from typing import List
from .types import AskResponse


# Very simple baseline evaluation: checks whether at least one Verified claim was produced
# and whether citations exist. Extend as needed for your course.


def score_responses(responses: List[AskResponse]) -> pd.DataFrame:
rows = []
for r in responses:
has_verified = any(c.label == "Verified" for c in r.claims)
has_citations = len(r.evidence) > 0
rows.append({
"query": r.query,
"verified_claim": int(has_verified),
"has_citations": int(has_citations),
"num_sources": len(r.evidence),
})
return pd.DataFrame(rows)