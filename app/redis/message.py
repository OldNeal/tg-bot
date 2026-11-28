from collections.abc import AsyncIterator

from app.redis.base import BaseHashs, BaseStore


class MessageHashs(BaseHashs):
    TELEGRAM = 'message:telegram:*'
    GET_ACTIVITY_POINT = 'message:telegram:notify:get-activity-point'
    ITEM = 'message:telegram:notify:item:{action}'
    ORGAN = 'message:telegram:notify:organ:{action}'

    @classmethod
    def organ(cls, action: str):
        if action not in {'rank', 'titul', 'kick', 'give'}:
            raise ValueError('Unknown organization notification action')
        return cls.ORGAN.format(action=action)

    @classmethod
    def item(cls, action: str):
        if action not in {'give', 'take'}:
            raise ValueError("action must be 'give' or 'take'")
        return cls.ITEM.format(action=action)


class MessageStore(BaseStore):
    hashs_cls = MessageHashs
    hashs: type[MessageHashs]

    # Core can replace a notification while Telegram is sending the old one.
    _DELETE_IF_UNCHANGED = """
if redis.call('TYPE', KEYS[1]).ok ~= 'hash' then
    return 0
end
if redis.call('HLEN', KEYS[1]) * 2 ~= #ARGV then
    return 0
end
for i = 1, #ARGV, 2 do
    if redis.call('HGET', KEYS[1], ARGV[i]) ~= ARGV[i + 1] then
        return 0
    end
end
return redis.call('DEL', KEYS[1])
"""

    async def pending(self) -> AsyncIterator[tuple[str, dict[str, str]]]:
        async for key in self.client.scan_iter(match=self.hashs.TELEGRAM, _type='hash'):
            payload = await self.client.hgetall(key)
            if payload:
                yield key, payload

    async def delete_if_unchanged(self, key: str, payload: dict[str, str]):
        fields = [value for pair in payload.items() for value in pair]
        return await self.client.eval(self._DELETE_IF_UNCHANGED, 1, key, *fields)
