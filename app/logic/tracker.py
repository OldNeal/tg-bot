import hashlib, json, unicodedata
from typing import Literal

from app.exception.activity import (
    ActivityCooldownError,
    ActivityDuplicateError,
    ActivityLowDiversityError,
    ActivityMessageTooShortError,
    ActivityMessagePerRequestError
)
from app.redis.store import store as redis_store

COOLDOWN_SEC = 60
MIN_UNIQUE_UNITS = 3      # минимум уникальных n-грамм в сообщении
DEDUP_TTL_SEC = 90
DEDUP_JACCARD = 0.7
HISTORY_SIZE = 10
MIN_TEXT_LEN = 3
NGRAM_N = 3               # длина n-граммы
ACTIVITY_MESSAGES_PER_REQUEST = 10
EXCEPTION_LEVEL: Literal['trace', 'debug', 'info', 'success', 'warning', 'error', 'critical'] = 'trace'

class ActivityTracker:
    store = redis_store
    _cache: dict[str, set[str]] = {}
    
    def char_ngrams(self, text: str, n: int = NGRAM_N) -> set[str]:
        """Нормализует текст и строит символьные n-граммы для сравнения.

        Комбинируемые знаки сохраняются, а для письменностей без пробелов
        используются более короткие n-граммы.
        """
        if not text:
            return set()
    
        t = unicodedata.normalize("NFKC", text).casefold()
        t = "".join(
            ch
            if ch.isalnum() or unicodedata.category(ch).startswith("M") or ch.isspace()
            else " "
            for ch in t
        )
        t = " ".join(t.split())  # схлопнуть пробелы, обрезать края
    
        if not t:
            return set()
        if n == NGRAM_N and any(
            unicodedata.name(ch, "").startswith(
                ("CJK UNIFIED IDEOGRAPH", "CJK COMPATIBILITY IDEOGRAPH",
                 "HIRAGANA", "KATAKANA", "HANGUL", "THAI", "LAO", "KHMER")
            )
            for ch in t
        ):
            n = 2
        if len(t) < n:
            return {t}
    
        return {t[i:i + n] for i in range(len(t) - n + 1)}
    
    def _cached_ngrams(self, text: str) -> set[str]:
        key = hashlib.md5(text.encode("utf-8")).hexdigest()
        if key in self._cache:
            return self._cache[key]
        grams = self.char_ngrams(text)
        self._cache[key] = grams
        if len(self._cache) > 10_000:
            self._cache.clear()
        return grams
    
    async def check(self, tg_id: int, text: str):
        text = (text or "").strip()
        if len(text) < MIN_TEXT_LEN:
            raise ActivityMessageTooShortError(level=EXCEPTION_LEVEL)
        units = self._cached_ngrams(text)
        if len(units) < MIN_UNIQUE_UNITS:
            raise ActivityLowDiversityError(level=EXCEPTION_LEVEL)
        result = await self.store.activity.check_and_update(
            tg_id,
            json.dumps(sorted(units), ensure_ascii=False),
            COOLDOWN_SEC,
            HISTORY_SIZE,
            DEDUP_TTL_SEC,
            DEDUP_JACCARD,
        )
        if result == 1:
            raise ActivityCooldownError(level=EXCEPTION_LEVEL)
        if result == 2:
            raise ActivityDuplicateError(level=EXCEPTION_LEVEL)
        if result != 0:
            raise RuntimeError(f"Unexpected activity check result: {result}")
        return units

    async def message_per_request(self, tg_id: int):
        activity_count, limit_reached = await self.store.activity.message_incr_until(
            tg_id,
            ACTIVITY_MESSAGES_PER_REQUEST,
        )
        if not limit_reached:
            raise ActivityMessagePerRequestError(level=EXCEPTION_LEVEL, activity_count=activity_count)
        return activity_count

tracker = ActivityTracker()