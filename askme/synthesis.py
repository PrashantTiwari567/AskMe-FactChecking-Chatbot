from __future__ import annotations
from typing import List
from .types import Evidence, Claim

def build_cited_answer(claims: List[Claim], evidence: List[Evidence]) -> str:
    if not claims:
        return "I couldn't find enough reliable evidence to answer."
    lines = []
    for c in claims:
        cites = []
        for idx in c.support_evidence_idx:
            if idx < len(evidence):
                cites.append(f"[{idx+1}]")
        sent = c.sentence
        tag = {
            "Verified": "(Verified)",
            "Uncertain": "(Uncertain)",
            "Unverifiable": "(Unverifiable)"
        }[c.label]
        lines.append(f"{sent} {' '.join(cites)} {tag}")
    return "\n".join(lines)

def bibliography(evidence: List[Evidence]) -> str:
    lines = []
    for i, e in enumerate(evidence, start=1):
        url = e.url or ""
        lines.append(f"[{i}] {e.title} — {e.source} — {url}")
    return "\n".join(lines)
