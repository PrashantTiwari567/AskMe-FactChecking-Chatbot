import feedparser
import requests, io
from datetime import datetime
from ..types import Evidence
from ..utils import domain_from_url, clean_text, now_utc

class RSSProvider:
    provider_name = "rss"

    def get_evidence(self, query: str, max_results: int = 5):
        import urllib.parse as up
        url = f"https://news.google.com/rss/search?q={up.quote(query)}&hl=en-US&gl=US&ceid=US:en"
        try:
            # Fetch RSS with 10-second timeout
            r = requests.get(url, timeout=10, headers={"User-Agent": "AskMe academic bot"})
            r.raise_for_status()

           
            data = r.text
            if isinstance(data, bytes):  # rare case
                data = data.decode("utf-8", errors="ignore")

        except Exception as e:
            print("⚠️ RSS timeout or fetch error:", e)
            return []

       
        feed = feedparser.parse(io.StringIO(str(data)))

        ev = []
        for entry in feed.entries[:max_results]:
            ev.append(Evidence(
                text=clean_text((entry.get('summary') or entry.get('title') or '')[:3000]),
                title=clean_text(entry.get('title') or ''),
                url=entry.get('link'),
                source=domain_from_url(entry.get('link') or ''),
                provider=self.provider_name,
                published=None,
                retrieved=now_utc(),
            ))
        return ev
