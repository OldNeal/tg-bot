import json

from app.redis.base import BaseStore, BaseHashs


class QuestionHashs(BaseHashs):
    MODERATION = '{namespace}:{chat_id}:{author_tg_id}:{message_id}'
    QUIZ_ACTIVE = 'quiz_active:{tg_id}:{question_id}'

    @classmethod
    def moderation(cls, namespace: str, chat_id: int, author_tg_id: int, message_id: int | None = None):
        key = f'{namespace}:{chat_id}:{author_tg_id}'
        return f'{key}:{message_id}' if message_id is not None else key

    @classmethod
    def quiz_active(cls, tg_id: int, question_id: int):
        return cls.QUIZ_ACTIVE.format(tg_id=tg_id, question_id=question_id)


class QuestionStore(BaseStore):
    hashs_cls = QuestionHashs
    hashs: type[QuestionHashs]

    async def pending_moderation(self, chat_id: int, namespaces: tuple[str, ...]):
        payloads = []
        for namespace in namespaces:
            pattern = f'{namespace}:{chat_id}:*'
            async for key in self.client.scan_iter(match=pattern):
                if key.count(':') < 3:
                    continue
                payload_text = await self.client.get(key)
                if not payload_text:
                    continue
                try:
                    payload = json.loads(payload_text)
                    if payload.get('status', 'pending') == 'pending' and payload['request']['question']:
                        payloads.append(payload)
                except (KeyError, TypeError, json.JSONDecodeError):
                    continue
        return sorted(payloads, key=lambda item: int(item.get('moderation_message_id', 0)))

    async def get_moderation(self, chat_id: int, author_tg_id: int, message_id: int, namespaces: tuple[str, ...]):
        for namespace in namespaces:
            payload = await self.client.get(self.hashs.moderation(namespace, chat_id, author_tg_id, message_id))
            if payload is not None:
                return payload
        # Legacy creation requests were stored without their moderation message id.
        if namespaces:
            return await self.client.get(self.hashs.moderation(namespaces[0], chat_id, author_tg_id))
        return None

    async def save_moderation(self, namespace: str, chat_id: int, payload: dict, ttl: int | None = None):
        key = self.hashs.moderation(
            namespace,
            chat_id,
            int(payload['author_tg_id']),
            int(payload['moderation_message_id']),
        )
        return await self.client.set(key, json.dumps(payload, ensure_ascii=False), ex=ttl)

    async def delete_active_quiz(self, tg_id: int, question_id: int):
        return await self.client.delete(self.hashs.quiz_active(tg_id, question_id))
