from __future__ import annotations
from typing import List
from .types import Evidence
from .providers.wikipedia_provider import WikipediaProvider
from .providers.web_provider import WebProvider
from .providers.rss_provider import RSSProvider

class Retriever:
    def __init__(self):
        self.wp = WikipediaProvider()
        self.web = WebProvider()
        self.rss = RSSProvider()

    def gather(self, query: str, max_per_source: int = 5) -> List[Evidence]:
        ev: List[Evidence] = []
        ev += self.wp.get_evidence(query, max_results=2)
        ev += self.web.get_evidence(query, max_results=max_per_source)
        # ev += self.rss.get_evidence(query, max_results=3) Excluding for now 
        seen = set()
        out = []
        for e in ev:
            key = (e.url or e.title)
            if key in seen:
                continue
            seen.add(key)
            out.append(e)
        return out
