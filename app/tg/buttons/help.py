from aiogram.types import CopyTextButton, InlineKeyboardButton, InlineKeyboardMarkup

from config import settings
from app.tg.buttons.base import BotIKB, MenuCall
from app.tg.callback.help import CmdListCall

class HelpIKB(BotIKB):    
    def main(self):
        self.builder.button(text='📖 Гайд на бота', url=settings.docs_url)
        self.builder.button(text='🕹️ Список команд', callback_data=CmdListCall(tg_id=self.tg_id))
        self.builder.button(text='📰 Газета Старого Нила', url=settings.news_url)
        self.builder.button(text='🔒 Политика конфиденциальности', url=settings.privacy_url)
        self.builder.button(text='📄 Пользовательское соглашение', url=settings.terms_url)
        self.builder.button(text='↩️ В главное меню', callback_data=MenuCall(where='main', tg_id=self.tg_id))
        return self.builder.adjust(1).as_markup()
    
    def cmds(self):
        self.builder.button(text='↩️ Назад', callback_data=MenuCall(where='help', tg_id=self.tg_id))
        return self.builder.adjust(1).as_markup()