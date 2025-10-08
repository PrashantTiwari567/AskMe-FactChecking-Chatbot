from pydantic import BaseModel

class Settings(BaseModel):
    user_agent: str = "AskMeBot/0.1 (academic project)"
    max_results: int = 5
    max_chars_per_source: int = 3000
    verification_similarity: float = 0.60
    numeric_tolerance_pct: float = 0.10  # 10% tolerance
    prefer_recent_days: int = 60
    min_verified_sources: int = 2

settings = Settings()
