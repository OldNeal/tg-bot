from app.tg.text.base import BaseText
from app.tg.text.utils import TextHTML
from app.validate.core import AnswerInventory, AnswerItemChange, AnswerItems, ItemInfo


class ItemText(BaseText):
    @classmethod
    def _item_name(cls, item: ItemInfo):
        return f'{item.emodzi or "📦"} {TextHTML(item.name).escape()}'

    @classmethod
    def inventory(cls, data: AnswerInventory):
        if not data.items:
            return '🎒 Инвентарь пуст'

        page_text = (
            cls.page_text(data.page.number, data.page.max)
            if data.page else ''
        )
        return f'🎒 Инвентарь {page_text}'.rstrip()

    @classmethod
    def items(cls, data: AnswerItems):
        if not data.items:
            return '📦 Предметов нет'

        page_text = (
            cls.page_text(data.page.number, data.page.max)
            if data.page else ''
        )
        return f'📦 Предметы {page_text}'.rstrip()

    @classmethod
    def item_info(cls, item: ItemInfo):
        lines = [
            f'🏷 ID: {item.item_id}',
            f'🔖 Тег: {TextHTML(item.tag).escape()}',
            f'📃 Описание: {TextHTML(item.description).escape() if item.description and len(item.description) > 0 else '❌'}'
        ]
        if item.quantity is not None:
            lines.append(f'📦 В наличии: {item.quantity}')
        return f'{cls._item_name(item)}' + cls.html.separator().joined(lines).blockquote()

    @classmethod
    def enter_quantity(cls, action: str, item: ItemInfo):
        verb = 'выдать' if action == 'give' else 'забрать'
        return f'✒️ Введите количество предмета «{TextHTML(item.name).escape()}», которое нужно {verb}.'

    @classmethod
    def item_changed(cls, data: AnswerItemChange, action: str, quantity: int | None = None):
        purpose = data.purpose or data.user
        verb = 'Выдано' if action == 'give' else 'Отобрано'
        item = data.item
        text = (
            f'✅ {verb} {quantity or 1} шт. предмета '
            f'{cls._item_name(item)} для {cls.user_mention(purpose)}'
        )
        return text
