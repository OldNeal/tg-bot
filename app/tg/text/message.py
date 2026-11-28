from html import escape


class MessageText:
    @classmethod
    def organ(cls, action: str, payload: dict[str, str]):
        organ = escape(payload['organ_name'])
        actor = escape(payload.get('actor_name') or f"#{payload['actor_id']}")
        old = escape(payload.get('old_value') or 'не задан')
        new = escape(payload.get('new_value') or 'не задан')
        changes = {
            'rank': f'изменил ваш ранг: {old} → {new}',
            'titul': f'изменил ваш титул: {old} → {new}',
            'kick': 'исключил вас из организации',
            'give': 'передал вам владение организацией',
        }
        return f'🏛 Организация «{organ}»: {actor} {changes[action]}.'

    @classmethod
    def activity_points(cls, points: int, reason: str):
        return f'⚡ Получены очки активности: {points} ({escape(reason)})'

    @classmethod
    def item(
        cls,
        action: str,
        item_id: int,
        quantity: int,
        remaining: int,
        item_name: str | None = None,
        item_emodzi: str | None = None,
    ):
        verb = 'Выдано' if action == 'give' else 'Изъято'
        name = escape(item_name) if item_name else f'#{item_id}'
        item_label = f'{escape(item_emodzi)} {name}' if item_emodzi else name
        return (
            f'📦 {verb} {quantity} шт. предмета {item_label}. '
            f'Осталось в инвентаре: {remaining}'
        )
