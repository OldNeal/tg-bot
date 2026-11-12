import hashlib, json, unicodedata

from app.exception.activity import (
    ActivityCooldownError,
    ActivityDuplicateError,
    ActivityLowDiversityError,
    ActivityMessageTooShortError,
    ActivityMessagePerRequestError
)
from app.redis.store import store as redis_store

# --- настройки ---
COOLDOWN_SEC = 60
MIN_UNIQUE_UNITS = 3      # минимум уникальных n-грамм в сообщении
DEDUP_TTL_SEC = 90
DEDUP_JACCARD = 0.7
HISTORY_SIZE = 10
MIN_TEXT_LEN = 3
NGRAM_N = 3               # длина n-граммы
ACTIVITY_MESSAGES_PER_REQUEST = 10
EXCEPTION_LEVEL = 'trace'

class ActivityTracker:
    store = redis_store
    _cache: dict[str, set[str]] = {}
    
    def char_ngrams(self, text: str, n: int = NGRAM_N) -> set[str]:
        """Языко-независимые символьные n-граммы.
    
        - NFKC-нормализация (композиция диакритики)
        - lower() (регистр)
        - оставляем буквы/цифры/пробелы, пунктуацию и эмодзи выкидываем
        - схлопываем пробелы в один
        - режем на n-граммы
        """
        if not text:
            return set()
    
        t = unicodedata.normalize("NFKC", text).lower()
        t = "".join(ch if ch.isalnum() or ch.isspace() else " " for ch in t)
        t = " ".join(t.split())  # схлопнуть пробелы, обрезать края
    
        if not t:
            return set()
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
    
    def jaccard(self, a: set[str], b: set[str]) -> float:
        if not a or not b:
            return 0.0
        return len(a & b) / len(a | b)

    async def check(self, tg_id: int, text: str):
        text = (text or "").strip()
        if len(text) < MIN_TEXT_LEN:
            raise ActivityMessageTooShortError(level=EXCEPTION_LEVEL)
        units = self._cached_ngrams(text)
        if len(units) < MIN_UNIQUE_UNITS:
            raise ActivityLowDiversityError(level=EXCEPTION_LEVEL)
        if await self.store.activity.exist_cooldown(tg_id):
            raise ActivityCooldownError(level=EXCEPTION_LEVEL)
        raw = await self.store.activity.get_lrange_history(tg_id, HISTORY_SIZE)
        for item in raw:
            prev = set(json.loads(item))
            if self.jaccard(units, prev) >= DEDUP_JACCARD:
                raise ActivityDuplicateError(level=EXCEPTION_LEVEL)
        await self.store.activity.update(tg_id, COOLDOWN_SEC, list(units), HISTORY_SIZE, DEDUP_TTL_SEC)
        return units

    async def message_per_request(self, tg_id: int):
        activity_count = await self.store.activity.message_incr(tg_id)
        if activity_count < ACTIVITY_MESSAGES_PER_REQUEST:
            raise ActivityMessagePerRequestError(level=EXCEPTION_LEVEL, activity_count=activity_count)
        await self.store.activity.message_incr(tg_id, -activity_count)
        return activity_count

tracker = ActivityTracker()