from aiogram.types import CopyTextButton, InlineKeyboardButton, InlineKeyboardMarkup

from config import settings
from app.tg.buttons.base import BotIKB, MenuCall

class HelpIKB(BotIKB):    
    def main(self):
        self.builder.button(text='📖 Гайд на бота', url=settings.docs_url)
        return self.builder.as_markup()