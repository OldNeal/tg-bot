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
local cooldown = redis.call('EXISTS', KEYS[1])
if cooldown == 1 then
    return 1
end

local candidate = cjson.decode(ARGV[1])
local candidate_set = {}
for _, gram in ipairs(candidate) do
    candidate_set[gram] = true
end

local history = redis.call('LRANGE', KEYS[2], 0, tonumber(ARGV[3]) - 1)
for _, encoded in ipairs(history) do
    local previous = cjson.decode(encoded)
    local previous_set = {}
    for _, gram in ipairs(previous) do
        previous_set[gram] = true
    end

    local intersection = 0
    local union = 0
    for gram, _ in pairs(candidate_set) do
        union = union + 1
        if previous_set[gram] then
            intersection = intersection + 1
        end
    end
    for gram, _ in pairs(previous_set) do
        if not candidate_set[gram] then
            union = union + 1
        end
    end

    if union > 0 and intersection / union >= tonumber(ARGV[5]) then
        return 2
    end
end

redis.call('SET', KEYS[1], '1', 'EX', tonumber(ARGV[2]))
redis.call('LPUSH', KEYS[2], ARGV[1])
redis.call('LTRIM', KEYS[2], 0, tonumber(ARGV[3]) - 1)
redis.call('EXPIRE', KEYS[2], tonumber(ARGV[4]))
return 0
"""

    _MESSAGE_INCR_UNTIL_SCRIPT = """
local count = redis.call('INCR', KEYS[1])
if count < tonumber(ARGV[1]) then
    return {count, 0}
end
redis.call('SET', KEYS[1], 0)
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