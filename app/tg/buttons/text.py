from typing import Literal
from aiogram.types import InlineKeyboardButton

class TextKeyboardButton(InlineKeyboardButton):
    def pack(self):
        if self.url:
            return f'<tg-button type="url" style="{self.style or 'primary'}" url="{self.url}">{self.text}</tg-button>'
        if self.callback_data:
            return f'<tg-button type="callback_data" style="{self.style or 'primary'}" data="{self.callback_data}">{self.text}</tg-button>'
        if self.copy_text:
            return f'<tg-button type="copy_text" style="{self.style or 'primary'}" text="{self.copy_text}">{self.text}</tg-button>'
        
class TextKeyboardMarkup:
    def __init__(self, buttons: list[TextKeyboardButton], align: Literal["left", "center", "right"] = 'left'):
        self.buttons = buttons
        self.align = align

    def as_makrup(self):
        return f'<tg-button-row align="{self.align}">{' '.join([b.pack() for b in self.buttons if b.pack()])}</tg-button-row>'
