from __future__ import annotations
from typing import List, Dict, Tuple
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from collections import defaultdict
from .types import Evidence, Claim
from .utils import extract_numbers
from .config import settings

def _cluster_sentences(sentences: List[str]) -> List[List[int]]:
    if not sentences:
        return []
    vec = TfidfVectorizer(ngram_range=(1,2), min_df=1).fit(sentences)
    X = vec.transform(sentences)
    S = cosine_similarity(X)
    n = len(sentences)
    parent = list(range(n))
    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x
    def union(a,b):
        ra, rb = find(a), find(b)
        if ra!=rb:
            parent[rb]=ra
    thr = settings.verification_similarity
    for i in range(n):
        for j in range(i+1, n):
            if S[i,j] >= thr:
                union(i,j)
    clusters = defaultdict(list)
    for i in range(n):
        clusters[find(i)].append(i)
    return list(clusters.values())

def _cluster_domains(cluster: List[int], sent2src: Dict[int, str]) -> int:
    return len(set(sent2src[i] for i in cluster))

def _numbers_conflict(sentences: List[str]) -> bool:
    numbers = [extract_numbers(s) for s in sentences]
    flat = [num for sub in numbers for num in sub]
    if len(flat) <= 1:
        return False
    lo, hi = min(flat), max(flat)
    if lo == 0:
        return (hi > 0)
    return (hi - lo) / max(abs(hi), 1.0) > settings.numeric_tolerance_pct

def verify_sentences(sentences: List[str], evidence: List[Evidence]) -> List[Claim]:
    sent_map: List[Tuple[int, str]] = []
    for idx, s in enumerate(sentences):
        src_domain = evidence[idx].source if idx < len(evidence) else ""
        sent_map.append((idx, src_domain))
    sent2src = {i: src for i,src in enumerate([m[1] for m in sent_map])}
    clusters = _cluster_sentences(sentences)
    claims: List[Claim] = []
    for cluster in clusters:
        domain_count = _cluster_domains(cluster, sent2src)
        sents = [sentences[i] for i in cluster]
        label = "Unverifiable"
        notes = None
        score = 0.0
        if domain_count >= settings.min_verified_sources:
            if _numbers_conflict(sents):
                label = "Uncertain"
                notes = "Conflicting numeric values across sources"
            else:
                label = "Verified"
                score = 1.0
        elif domain_count == 1 and len(cluster) > 1:
            label = "Uncertain"
            notes = "Only one unique source domain"
        else:
            label = "Unverifiable"
        rep = sents[0]
        claims.append(Claim(
            sentence=rep,
            support_evidence_idx=[i for i in cluster],
            label=label,
            notes=notes,
            score=score
        ))
    return claims
