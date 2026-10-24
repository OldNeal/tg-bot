from aiogram.types import InlineKeyboardButton

from app.validate.api import AnswerNewsPaperInfoReaders, AnswerReaderInfo, NewsPaperInfo, ForButtons
from app.tg.buttons.base import BotIKB
from app.tg.callback.news_paper import (
    NewsPaperInfoCall,
    NewsPaperInfoDescCall,
    NewsPaperActionCall,
    NewsPaperCreateCall,
    NewsPaperFireEditorCall,
    NewsPaperGiveCall,
    NewsPaperMakeEditorCall,
    NewsPaperCaptureCall,
    NewsPaperMenuCall,
    NewsPaperNotifyCall,
    NewsPaperPageCall,
    NewsPaperSearchCall,
    NewsPaperSubscribeCall,
    NewsPaperSettingsCall,
    NewsPaperSettingsDefaultCall,
    NewsPaperSettingsRedactCall,
    NewsPaperUnsubscribeCall,
    ReaderCall,
)


class NewsPaperIKB(BotIKB):
    def news_papers(
        self,
        news_papers: list[NewsPaperInfo],
        page: int,
        max_page: int,
        mode: str = 'search',
        back_to_menu: bool = False
    ):
        for news_paper in news_papers:
            label = f'{news_paper.emodzi or "📰"} {news_paper.name}'
            callback_data = (
                NewsPaperActionCall(
                    action=mode,
                    news_paper_id=news_paper.id,
                    tg_id=self.tg_id,
                )
                if mode in {'subscribe', 'unsubscribe', 'notify', 'make_editor', 'fire_editor'}
                else NewsPaperInfoCall(news_paper_id=news_paper.id, tg_id=self.tg_id)
            )
            self.builder.button(text=label[:64], icon_custom_emoji_id=news_paper.custom_emodzi_id, callback_data=callback_data)
        self.builder.adjust(1)

        pages = []
        if page > 0:
            pages.append(InlineKeyboardButton(text='⬅️', callback_data=NewsPaperPageCall(page=page - 1, mode=mode, tg_id=self.tg_id).pack()))
        if page < max_page - 1:
            pages.append(InlineKeyboardButton(text='➡️', callback_data=NewsPaperPageCall(page=page + 1, mode=mode, tg_id=self.tg_id).pack()))
        if pages:
            self.builder.row(*pages)

        if mode == 'search':
            self.builder.row(InlineKeyboardButton(text='✒️ Ввести запрос еще раз', callback_data=NewsPaperSearchCall(tg_id=self.tg_id).pack()))
        elif mode == 'editors':
            self.builder.row(InlineKeyboardButton(text='➕ Создать газету', callback_data=NewsPaperCreateCall(tg_id=self.tg_id).pack()))
        if back_to_menu:
            self.builder.row(InlineKeyboardButton(text='↩️ Назад в меню', callback_data=NewsPaperMenuCall(tg_id=self.tg_id).pack()))
        return self.builder.as_markup()

    def news_paper_info(
        self,
        news_paper_id: int,
        for_buttons: ForButtons,
        mode: str = 'search',
        page: int = 0,
    ):
        self.builder.button(text='🪶 Описание', callback_data=NewsPaperInfoDescCall(news_paper_id=news_paper_id, tg_id=self.tg_id))
        self.builder.button(text='🗞 Читатели', callback_data=NewsPaperPageCall(news_paper_id=news_paper_id, page=0, mode='readers', tg_id=self.tg_id))
        if for_buttons.is_redact_setting:
            self.builder.button(text='⚙️ Настройки', callback_data=NewsPaperSettingsCall(news_paper_id=news_paper_id, tg_id=self.tg_id))
        if for_buttons.is_news:
            self.builder.button(text='📣 Выпустить новость', callback_data=NewsPaperNotifyCall(news_paper_id=news_paper_id, tg_id=self.tg_id))
        if for_buttons.is_capture:
            self.builder.button(text='👑 Захватить газету', callback_data=NewsPaperCaptureCall(news_paper_id=news_paper_id, tg_id=self.tg_id))
        if for_buttons.is_reader:
            self.builder.button(text='🔕 Отписаться', callback_data=NewsPaperUnsubscribeCall(news_paper_id=news_paper_id, tg_id=self.tg_id))
        else:
            self.builder.button(text='🔔 Подписаться', callback_data=NewsPaperSubscribeCall(news_paper_id=news_paper_id, tg_id=self.tg_id))
        self.builder.button(text='↩️ Назад', callback_data=NewsPaperPageCall(page=page, mode=mode, tg_id=self.tg_id))
        return self.builder.adjust(2, 1).as_markup()

    def readers(self, readers: list[AnswerReaderInfo], news_paper_id: int, page: int, max_page: int):
        for reader in readers:
            self.builder.button(text=f'{reader.user.fullname or reader.user.username} ({reader.reader.rank_name})', callback_data=ReaderCall(purpose_tg_id=reader.user.tg_id, news_paper_id=news_paper_id, tg_id=self.tg_id))
        self.builder.adjust(1)
        pages = []
        if page > 0:
            pages.append(InlineKeyboardButton(
                text='⬅️',
                callback_data=NewsPaperPageCall(
                    page=page - 1,
                    mode='readers',
                    news_paper_id=news_paper_id,
                    tg_id=self.tg_id,
                ).pack(),
            ))
        if page < max_page - 1:
            pages.append(InlineKeyboardButton(
                text='➡️',
                callback_data=NewsPaperPageCall(
                    page=page + 1,
                    mode='readers',
                    news_paper_id=news_paper_id,
                    tg_id=self.tg_id,
                ).pack(),
            ))
        if pages:
            self.builder.row(*pages)
        self.builder.row(InlineKeyboardButton(
            text='↩️ К газете',
            callback_data=NewsPaperInfoCall(
                news_paper_id=news_paper_id,
                tg_id=self.tg_id,
            ).pack(),
        ))
        return self.builder.as_markup()

    def create(self, news_paper_id: int):
        return self.builder.button(
            text='📰 Открыть карточку',
            callback_data=NewsPaperInfoCall(
                news_paper_id=news_paper_id,
                tg_id=self.tg_id,
            ),
        ).as_markup()

    def settings_values(self, news_paper_id: int):
        self.builder.button(text='✒️ Изменить', callback_data=NewsPaperSettingsRedactCall(news_paper_id=news_paper_id, tg_id=self.tg_id))
        self.builder.button(text='🔩 Сбросить', callback_data=NewsPaperSettingsDefaultCall(news_paper_id=news_paper_id, tg_id=self.tg_id))
        self.builder.button(text='↩️ Назад', callback_data=NewsPaperInfoCall(news_paper_id=news_paper_id, tg_id=self.tg_id))
        return self.builder.adjust(1).as_markup()

    def back_to_settings(self, news_paper_id: int):
        self.builder.button(text='↩️ Назад', callback_data=NewsPaperSettingsCall(news_paper_id=news_paper_id, tg_id=self.tg_id))
        return self.builder.as_markup()

    def reader(
        self,
        news_paper_id: int,
        page: int,
        purpose_tg_id: int,
        for_buttons: ForButtons,
    ):  
        if purpose_tg_id != self.tg_id:
            if for_buttons.is_redact_rank:
                self.builder.button(
                    text='➖ Снять с поста редактора',
                    callback_data=NewsPaperFireEditorCall(
                        purpose_tg_id=purpose_tg_id,
                        news_paper_id=news_paper_id,
                        tg_id=self.tg_id,
                    ),
                )
                self.builder.button(
                    text='➕ Сделать редактором',
                    callback_data=NewsPaperMakeEditorCall(
                        purpose_tg_id=purpose_tg_id,
                        news_paper_id=news_paper_id,
                        tg_id=self.tg_id,
                    ),
                )
            if for_buttons.is_give:
                self.builder.button(
                    text='👑 Передать газету',
                    callback_data=NewsPaperGiveCall(
                        purpose_tg_id=purpose_tg_id,
                        news_paper_id=news_paper_id,
                        tg_id=self.tg_id,
                    ),
                )
        self.builder.button(text='↩️ Назад', callback_data=NewsPaperPageCall(news_paper_id=news_paper_id, page=page, mode='readers', tg_id=self.tg_id))
        return self.builder.adjust(2, 1, 1).as_markup()

    def give_news_paper(self, news_paper_id: int, purpose_tg_id: int):
        self.builder.button(
            text='✅ Да',
            callback_data=NewsPaperGiveCall(
                accert=True,
                purpose_tg_id=purpose_tg_id,
                news_paper_id=news_paper_id,
                tg_id=self.tg_id,
            ),
        )
        self.builder.button(
            text='❌ Нет',
            callback_data=NewsPaperGiveCall(
                cancel=True,
                purpose_tg_id=purpose_tg_id,
                news_paper_id=news_paper_id,
                tg_id=self.tg_id,
            ),
        )
        return self.builder.adjust(2).as_markup()

    def confirm_unsubscribe(self, news_paper_id: int):
        self.builder.button(
            text='✅ Да',
            callback_data=NewsPaperUnsubscribeCall(
                accert=True,
                news_paper_id=news_paper_id,
                tg_id=self.tg_id,
            ),
        )
        self.builder.button(
            text='❌ Нет',
            callback_data=NewsPaperUnsubscribeCall(
                cancel=True,
                news_paper_id=news_paper_id,
                tg_id=self.tg_id,
            ),
        )
        return self.builder.adjust(2).as_markup()

    def back_to_menu(self):
        self.builder.button(text='↩️ Назад в меню', callback_data=NewsPaperMenuCall(tg_id=self.tg_id))
        return self.builder.as_markup()

    def back_to_info(self, news_paper_id: int):
        self.builder.button(text='↩️ Назад', callback_data=NewsPaperInfoCall(news_paper_id=news_paper_id, tg_id=self.tg_id))
        return self.builder.as_markup()

    def back_to_reader(self, news_paper_id: int, purpose_tg_id: int):
        self.builder.button(text='↩️ Назад', callback_data=ReaderCall(purpose_tg_id=purpose_tg_id, news_paper_id=news_paper_id, tg_id=self.tg_id))
        return self.builder.as_markup()
    
    def menu(self):
        self.builder.button(text='📝 Меню редактора', callback_data=NewsPaperPageCall(page=0, mode='editors', tg_id=self.tg_id))
        self.builder.button(text='🗞 Меню читателя', callback_data=NewsPaperPageCall(page=0, mode='list', tg_id=self.tg_id))
        self.builder.button(text='🔎 Найти газету', callback_data=NewsPaperSearchCall(tg_id=self.tg_id))
        self.builder.button(text='📜 Все газеты', callback_data=NewsPaperPageCall(page=0, mode='all', tg_id=self.tg_id))
        return self.builder.adjust(1).as_markup()
