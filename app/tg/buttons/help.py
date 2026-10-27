from aiogram.types import CopyTextButton, InlineKeyboardButton, InlineKeyboardMarkup

from config import settings
from app.tg.buttons.base import BotIKB, MenuCall

class HelpIKB(BotIKB):    
    def main(self):
        self.builder.button(text='📖 Гайд на бота', url=settings.docs_url)
        self.builder.button(text='↩️ В главное меню', callback_data=MenuCall(where='main', tg_id=self.tg_id))
        return self.builder.adjust(1).as_markup()