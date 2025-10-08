from __future__ import annotations
import requests
from typing import List
from ..types import Evidence
from ..utils import clean_text, domain_from_url, now_utc

WIKI_API = "https://en.wikipedia.org/w/api.php"
WIKI_SUMMARY = "https://en.wikipedia.org/api/rest_v1/page/summary/{}"

class WikipediaProvider:
    provider_name = "wikipedia"

    def search_titles(self, query: str, limit: int = 3) -> List[str]:
        params = {
            "action": "query",
            "list": "search",
            "format": "json",
            "srsearch": query,
            "srlimit": limit,
        }
        headers = {"User-Agent": "AskMeBot/0.1 (Academic Project; contact: student@example.com)"}
        r = requests.get(WIKI_API, params=params, headers=headers, timeout=15)

        r.raise_for_status()
        data = r.json()
        return [item["title"] for item in data.get("query", {}).get("search", [])]

    def fetch_summary(self, title: str) -> Evidence:
        url = WIKI_SUMMARY.format(requests.utils.quote(title.replace(" ", "_")))
        headers = {
         "accept": "application/json",
           "User-Agent": "AskMeBot/0.1 (Academic Project; contact: student@example.com)"
         }
        r = requests.get(url, timeout=15, headers=headers)

        r.raise_for_status()
        j = r.json()
        summary = clean_text(j.get("extract") or "")
        page_url = j.get("content_urls", {}).get("desktop", {}).get("page")
        return Evidence(
            text=summary[:3000],
            title=j.get("title") or title,
            url=page_url,
            source=domain_from_url(page_url) or "wikipedia.org",
            provider=self.provider_name,
            published=None,
            retrieved=now_utc(),
        )

    def get_evidence(self, query: str, max_results: int = 2) -> List[Evidence]:
        ev: List[Evidence] = []
        for t in self.search_titles(query, limit=max_results):
            try:
                ev.append(self.fetch_summary(t))
            except Exception:
                continue
        return ev
