from aiogram.types import InlineKeyboardButton

from config import settings
from app.tg.buttons.base import BotIKB, MenuCall
from app.tg.callback.question import (
    QuestionCreateCall,
    QuestionModerationCall,
    QuestionMenuCall,
    QuestionPageCall,
    QuestionQuizAnswerCall,
    QuestionSelectCall,
)
from app.api.schemas import Question, QuestionAnswer


class QuestionIKB(BotIKB):
    def menu(self):
        self.builder.button(
            text='🎲 Ответить на случайный вопрос',
            callback_data=QuestionMenuCall(action='random', tg_id=self.tg_id),
        )
        self.builder.button(
            text='📝 Мои вопросы',
            callback_data=QuestionMenuCall(action='mine', tg_id=self.tg_id),
        )
        self.builder.button(
            text='📊 Моя статистика',
            callback_data=QuestionMenuCall(action='userstats', tg_id=self.tg_id),
        )
        self.builder.button(
            text='➕ Создать вопрос',
            callback_data=QuestionMenuCall(action='create', tg_id=self.tg_id),
        )
        self.builder.button(
            text='↩️ В главное меню',
            callback_data=MenuCall(where='main', tg_id=self.tg_id),
        )
        return self.builder.adjust(1, 1, 2, 1).as_markup()

    def back_to_menu(self):
        self.builder.button(
            text='↩️ К меню вопросов',
            callback_data=QuestionMenuCall(action='menu', tg_id=self.tg_id),
        )
        return self.builder.as_markup()

    def question_list(
        self,
        questions: list[Question],
        page: int,
        max_page: int,
    ):
        for index, question in enumerate(questions):
            label = question.body[:40]
            if len(question.body) > 40:
                label += '…'
            self.builder.button(
                text=label,
                callback_data=QuestionSelectCall(
                    page=page,
                    index=index,
                    tg_id=self.tg_id,
                ),
            )
        self.builder.adjust(1)

        pages = []
        if page > 0:
            pages.append(InlineKeyboardButton(
                text='⬅️',
                callback_data=QuestionPageCall(
                    page=page - 1,
                    tg_id=self.tg_id,
                ).pack(),
            ))
        if page < max_page - 1:
            pages.append(InlineKeyboardButton(
                text='➡️',
                callback_data=QuestionPageCall(
                    page=page + 1,
                    tg_id=self.tg_id,
                ).pack(),
            ))
        if pages:
            self.builder.row(*pages)

        self.builder.button(
            text='↩️ К меню вопросов',
            callback_data=QuestionMenuCall(action='menu', tg_id=self.tg_id),
        )
        return self.builder.adjust(1).as_markup()

    def question(self, page: int = 0):
        self.builder.button(
            text='↩️ К моим вопросам',
            callback_data=QuestionMenuCall(action='mine', page=page, tg_id=self.tg_id),
        )
        return self.builder.adjust(1).as_markup()

    def quiz(self, question_id: int, answers: list[QuestionAnswer]):
        for index, answer in enumerate(answers, start=1):
            self.builder.button(
                text=str(index),
                callback_data=QuestionQuizAnswerCall(
                    question_id=question_id,
                    answer_id=answer.answer_id,
                    tg_id=self.tg_id,
                ),
            )
        self.builder.adjust(len(answers))
        self.builder.row(
            InlineKeyboardButton(
                text='🎲 Другой вопрос',
                callback_data=QuestionMenuCall(
                    action='random',
                    tg_id=self.tg_id,
                ).pack(),
            ),
            InlineKeyboardButton(
                text='↩️ К меню',
                callback_data=QuestionMenuCall(
                    action='menu',
                    tg_id=self.tg_id,
                ).pack(),
            ),
            width=1
        )
        return self.builder.as_markup()

    def quiz_result(self):
        self.builder.button(
            text='🎲 Другой вопрос',
            callback_data=QuestionMenuCall(action='random', tg_id=self.tg_id),
        )
        self.builder.button(
            text='↩️ К меню вопросов',
            callback_data=QuestionMenuCall(action='menu', tg_id=self.tg_id),
        )
        return self.builder.adjust(1).as_markup()

    def create_confirmation(self):
        labels = {
            'body': '❔ Изменить вопрос',
            'description': '📜 Изменить описание',
            'correct_answers': '✏️ Изменить правильные ответы',
            'incorrect_answers': '✏️ Изменить неправильные ответы',
        }
        for field, text in labels.items():
            self.builder.button(
                text=text,
                callback_data=QuestionCreateCall(
                    action='edit',
                    field=field,
                    tg_id=self.tg_id,
                ),
            )
        self.builder.button(
            text='✅ Создать вопрос',
            callback_data=QuestionCreateCall(action='submit', tg_id=self.tg_id),
        )
        self.builder.button(
            text='❌ Отменить',
            callback_data=QuestionCreateCall(action='cancel', tg_id=self.tg_id),
        )
        return self.builder.adjust(1).as_markup()

    def create_edit_prompt(self, show_review: bool = False):
        self.builder.button(
            text='⚖️ Правила создания',
            url=settings.docs_url + 'question/base/#rules',
        )
        if show_review:
            self.builder.button(
                text='↩️ К проверке',
                callback_data=QuestionCreateCall(action='review', tg_id=self.tg_id),
            )
        self.builder.button(
            text='❌ Отменить создание',
            callback_data=QuestionCreateCall(action='cancel', tg_id=self.tg_id),
        )
        return self.builder.adjust(1).as_markup()

    def moderation_request(self, author_tg_id: int):
        self.builder.button(
            text='✅ Создать',
            callback_data=QuestionModerationCall(
                action='approve',
                tg_id=author_tg_id,
            ),
        )
        self.builder.button(
            text='✏️ Изменить',
            callback_data=QuestionModerationCall(
                action='edit',
                tg_id=author_tg_id,
            ),
        )
        self.builder.button(
            text='❌ Отклонить',
            callback_data=QuestionModerationCall(
                action='reject',
                tg_id=author_tg_id,
            ),
        )
        return self.builder.adjust(1).as_markup()

    def moderation_fields(self, author_tg_id: int):
        labels = {
            'body': '❔ Текст вопроса',
            'description': '📜 Описание',
            'correct_answers': '✅ Правильные ответы',
            'incorrect_answers': '❌ Неправильные ответы',
        }
        for field, label in labels.items():
            self.builder.button(
                text=label,
                callback_data=QuestionModerationCall(
                    action='field',
                    field=field,
                    tg_id=author_tg_id,
                ),
            )
        self.builder.button(
            text='↩️ К заявке',
            callback_data=QuestionModerationCall(
                action='back',
                tg_id=author_tg_id,
            ),
        )
        return self.builder.adjust(1).as_markup()