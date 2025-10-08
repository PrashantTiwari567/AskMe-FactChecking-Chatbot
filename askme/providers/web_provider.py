from __future__ import annotations
import requests
from ddgs import DDGS
from bs4 import BeautifulSoup
from datetime import datetime
from typing import List
from ..types import Evidence
from ..utils import clean_text, domain_from_url, now_utc

META_DATE_KEYS = [
    ("meta", {"property": "article:published_time"}),
    ("meta", {"name": "date"}),
    ("meta", {"itemprop": "datePublished"}),
    ("time", {}),
]

class WebProvider:
    provider_name = "web"

    def search(self, query: str, max_results: int = 5):
        with DDGS() as ddgs:
            return list(ddgs.text(query, region="us-en", max_results=max_results))

    def fetch_page_text(self, url: str):
        r = requests.get(url, timeout=20, headers={"User-Agent": "AskMe academic bot"})
        r.raise_for_status()
        html = r.text
        soup = BeautifulSoup(html, "html.parser")
        paragraphs = [p.get_text(" ", strip=True) for p in soup.find_all("p")][:30]
        text = " ".join(paragraphs)
        text = clean_text(text)[:3000]
        title = clean_text(soup.title.get_text()) if soup.title else url
        pub = None
        for tag, attrs in META_DATE_KEYS:
            el = soup.find(tag, attrs=attrs)
            if el:
                val = el.get("content") or el.get_text(strip=True)
                try:
                    pub = datetime.fromisoformat(val.replace("Z", "+00:00"))
                    break
                except Exception:
                    continue
        return text, pub, title

    def get_evidence(self, query: str, max_results: int = 5) -> List[Evidence]:
        items = self.search(query, max_results=max_results)
        ev: List[Evidence] = []
        for it in items:
            url = it.get("href") or it.get("url")
            if not url:
                continue
            try:
                text, pub, title = self.fetch_page_text(url)
                if not text:
                    continue
                ev.append(Evidence(
                    text=text,
                    title=title,
                    url=url,
                    source=domain_from_url(url),
                    provider=self.provider_name,
                    published=pub,
                    retrieved=now_utc(),
                    extra={"snippet": it.get("body") or it.get("snippet") or ""}
                ))
            except Exception:
                continue
        return ev
