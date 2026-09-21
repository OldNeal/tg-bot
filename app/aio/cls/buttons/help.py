from app.aio.cls.buttons.base import BotIKB, MenuCall
from aiogram.types import CopyTextButton, InlineKeyboardButton, InlineKeyboardMarkup
from config import settings

class HelpIKB(BotIKB):    
    def main(self):
        self.builder.button(text='📖 Гайд на бота', url=settings.docs_url)
        return self.builder.as_markup()