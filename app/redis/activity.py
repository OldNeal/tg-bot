from app.redis.base import BaseStore, BaseHashs

class ActivityHashs(BaseHashs):
    COOLDOWN = 'act:cd:{tg_id}'
    NGRAM_HISTORY = 'act:hist:{tg_id}'
    MESSAGE_COUNT = 'act:count:{tg_id}'

    @classmethod
    def cooldown(self, tg_id: int):
        return self.COOLDOWN.format(tg_id=tg_id)
    
    @classmethod
    def ngram_history(self, tg_id: int):
        return self.NGRAM_HISTORY.format(tg_id=tg_id)
    
    @classmethod
    def message_count(self, tg_id: int):
        return self.MESSAGE_COUNT.format(tg_id=tg_id)

class ActivityStore(BaseStore):
    hashs_cls = ActivityHashs
    hashs: type[ActivityHashs]

    _CHECK_AND_UPDATE_SCRIPT = """
-- _CHECK_AND_UPDATE_SCRIPT
local cooldown_sec  = tonumber(ARGV[2])
local history_size  = tonumber(ARGV[3])
local dedup_ttl_sec = tonumber(ARGV[4])
local jaccard       = tonumber(ARGV[5])

if redis.call('EXISTS', KEYS[1]) == 1 then
    return 1
end

local ok, candidate = pcall(cjson.decode, ARGV[1])
if not ok or type(candidate) ~= 'table' or #candidate == 0 then
    return redis.error_reply('ARGV[1] must be a non-empty JSON array')
end

local candidate_set, candidate_len = {}, 0
for _, gram in ipairs(candidate) do
    if not candidate_set[gram] then
        candidate_set[gram] = true
        candidate_len = candidate_len + 1
    end
end

if jaccard and jaccard > 0 and history_size and history_size > 0 then
    local history = redis.call('LRANGE', KEYS[2], 0, history_size - 1)
    for _, encoded in ipairs(history) do
        local decoded, previous = pcall(cjson.decode, encoded)
        if decoded and type(previous) == 'table' then
            local previous_set, previous_len = {}, 0
            for _, gram in ipairs(previous) do
                if not previous_set[gram] then
                    previous_set[gram] = true
                    previous_len = previous_len + 1
                end
            end

            local intersection = 0
            for gram in pairs(candidate_set) do
                if previous_set[gram] then
                    intersection = intersection + 1
                end
            end

            local union = candidate_len + previous_len - intersection
            if union > 0 and intersection / union >= jaccard then
                return 2
            end
        end
    end
end

redis.call('LPUSH', KEYS[2], ARGV[1])
if history_size and history_size > 0 then
    redis.call('LTRIM', KEYS[2], 0, history_size - 1)
end
if dedup_ttl_sec and dedup_ttl_sec > 0 then
    redis.call('EXPIRE', KEYS[2], dedup_ttl_sec)
end
if cooldown_sec and cooldown_sec > 0 then
    redis.call('SET', KEYS[1], '1', 'EX', cooldown_sec)
end
return 0
"""

    _MESSAGE_INCR_UNTIL_SCRIPT = """
local limit = tonumber(ARGV[1])
local ttl   = tonumber(ARGV[2])

local count = redis.call('INCR', KEYS[1])
if count == 1 and ttl > 0 then
    redis.call('EXPIRE', KEYS[1], ttl)
end

if count < limit then
    return {count, 0}
end

redis.call('SET', KEYS[1], 0, 'KEEPTTL')  -- сброс без потери TTL
return {count, 1}
"""

    async def check_and_update(
        self,
        tg_id: int,
        units: str,
        cooldown_sec: int,
        history_size: int,
        dedup_ttl_sec: int,
        dedup_jaccard: float,
    ) -> int:
        return await self.client.eval(
            self._CHECK_AND_UPDATE_SCRIPT,
            2,
            self.hashs.cooldown(tg_id),
            self.hashs.ngram_history(tg_id),
            units,
            cooldown_sec,
            history_size,
            dedup_ttl_sec,
            dedup_jaccard,
        )

    async def message_incr_until(self, tg_id: int, limit: int) -> tuple[int, bool]:
        result = await self.client.eval(
            self._MESSAGE_INCR_UNTIL_SCRIPT,
            1,
            self.hashs.message_count(tg_id),
            limit,
        )
        return int(result[0]), bool(result[1])