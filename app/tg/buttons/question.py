from aiogram.types import InlineKeyboardButton

from config import settings
from app.tg.buttons.base import BotIKB, MenuCall
from app.tg.deep.base import QuestionDeep
from app.tg.callback.question import (
    QuestionCreateCall,
    QuestionModerationCall,
    PendingQuestionsRefreshCall,
    QuestionMenuCall,
    QuestionMineCall,
    QuestionRandomCall,
    QuestionRandomDifficultyCall,
    QuestionStartCreateCall,
    QuestionStartJsonCreateCall,
    QuestionUserStatsCall,
    QuestionLimitsCall,
    QuestionLeaveQuizCall,
    QuestionPageCall,
    QuestionQuizAnswerCall,
    QuestionSelectCall,
    QuestionEditCall,
)
from app.validate.core import Question, QuestionAnswer


class QuestionIKB(BotIKB):
    def pending_questions_refresh(self):
        self.builder.button(
            text='🔄 Обновить список',
            callback_data=PendingQuestionsRefreshCall(tg_id=self.tg_id),
        )
        return self.builder.as_markup()

    def menu(self):
        self.builder.button(
            text='🎲 Ответить на случайный вопрос',
            callback_data=QuestionRandomCall(tg_id=self.tg_id),
        )
        self.builder.button(
            text='📊 Моя статистика',
            callback_data=QuestionUserStatsCall(tg_id=self.tg_id),
        )
        self.builder.button(
            text='⚡ Лимиты ответов',
            callback_data=QuestionLimitsCall(tg_id=self.tg_id),
        )
        self.builder.button(
            text='📝 Мои вопросы',
            callback_data=QuestionMineCall(tg_id=self.tg_id),
        )
        self.builder.button(
            text='➕ Создать вопрос',
            callback_data=QuestionStartCreateCall(tg_id=self.tg_id),
        )
        self.builder.button(
            text='📋 Создать через JSON',
            callback_data=QuestionStartJsonCreateCall(tg_id=self.tg_id),
        )
        self.builder.button(
            text='↩️ В главное меню',
            callback_data=MenuCall(where='main', tg_id=self.tg_id),
        )
        return self.builder.adjust(1, 2, 1, 2, 1).as_markup()

    def random_difficulty(self):
        for difficulty in range(1, 11):
            self.builder.button(
                text=str(difficulty),
                callback_data=QuestionRandomDifficultyCall(
                    difficulty=difficulty,
                    tg_id=self.tg_id,
                ),
            )
        self.builder.button(
            text='↩️ К меню вопросов',
            callback_data=QuestionMenuCall(action='menu', tg_id=self.tg_id),
        )
        return self.builder.adjust(5, 5, 1).as_markup()

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

    def question(self, question: Question, page: int = 0):
        self.builder.button(
            text='✏️ Изменить вопрос',
            callback_data=QuestionEditCall(action='open', question_id=question.question_id, tg_id=self.tg_id),
        )
        self.builder.button(
            text='↩️ К моим вопросам',
            callback_data=QuestionMineCall(page=page, tg_id=self.tg_id),
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
                text='↩️ Отказаться отвечать',
                callback_data=QuestionLeaveQuizCall(tg_id=self.tg_id).pack(),
            ),
        )
        return self.builder.as_markup()

    def quiz_result(self):
        self.builder.button(
            text='🎲 Другой вопрос',
            callback_data=QuestionRandomCall(tg_id=self.tg_id),
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
            'difficulty': '⚖️ Изменить сложность',
            'tags': '🏷 Изменить теги',
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
            text='👻 Создать анонимно',
            callback_data=QuestionCreateCall(action='submit', tg_id=self.tg_id, is_anonim=True),
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

    def edit_confirmation(self, question_id: int):
        labels = {
            'body': '❔ Изменить вопрос', 'description': '📜 Изменить описание',
            'difficulty': '⚖️ Изменить сложность', 'tags': '🏷 Изменить теги',
            'correct_answers': '✏️ Изменить правильные ответы',
            'incorrect_answers': '✏️ Изменить неправильные ответы',
        }
        for field, label in labels.items():
            self.builder.button(text=label, callback_data=QuestionEditCall(action='field', question_id=question_id, field=field, tg_id=self.tg_id))
        self.builder.button(text='✅ Отправить на модерацию', callback_data=QuestionEditCall(action='submit', question_id=question_id, tg_id=self.tg_id))
        self.builder.button(text='❌ Отменить', callback_data=QuestionEditCall(action='cancel', question_id=question_id, tg_id=self.tg_id))
        return self.builder.adjust(1).as_markup()

    def edit_prompt(self, question_id: int, show_review: bool = False):
        if show_review:
            self.builder.button(text='↩️ К проверке', callback_data=QuestionEditCall(action='review', question_id=question_id, tg_id=self.tg_id))
        self.builder.button(text='❌ Отменить редактирование', callback_data=QuestionEditCall(action='cancel', question_id=question_id, tg_id=self.tg_id))
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

    def moderation_request(self, author_tg_id: int, moderator_tg_id: int | None = None, operation: str = 'create'):
        self.builder.button(
                text='✅ Опубликовать' if operation == 'update' else '✅ Создать',
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
            'difficulty': '⚖️ Сложность',
            'tags': '🏷 Теги',
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
    
    def deep_menu(self, message_id: int | None = None, chat_id: int | None = None):
        return self.builder.button(text='🗨️ Перейти в лс', url=QuestionDeep(message_id=message_id, chat_id=chat_id).url()).as_markup()
