from telegram_click_aio.decorator import command
from aiogram import F, Router, flags
from aiogram.filters import Command, CommandStart
from aiogram.types import CallbackQuery, Message

from app.service.question import QuestionService
from app.service.utils import DEFAULT_BOT_ERROR_HANDLER
from app.tg.args import Optionals
from app.tg.callback.base import MenuCall
from app.tg.callback.question import (
    QuestionCreateCall,
    QuestionModerationCall,
    QuestionMenuCall,
    QuestionMineCall, QuestionRandomCall, QuestionStartCreateCall,
    QuestionRandomDifficultyCall,
    QuestionStartJsonCreateCall, QuestionUserStatsCall, QuestionLimitsCall,
    QuestionLeaveQuizCall,
    QuestionEditCall,
    QuestionPageCall,
    QuestionQuizAnswerCall,
    QuestionSelectCall,
    PendingQuestionsRefreshCall,
)
from app.tg.deep.base import QuestionDeep
from app.tg.fsm.state import QuestionState
from app.tg.middlewares import ServiceMiddleware, PrivateChatMiddleware

question_router = Router()
question_router.message.middleware(ServiceMiddleware(QuestionService))
question_router.callback_query.middleware(ServiceMiddleware(QuestionService))

question_router.message.middleware(PrivateChatMiddleware())
question_router.callback_query.middleware(PrivateChatMiddleware())

@question_router.callback_query(MenuCall.filter(F.where == 'question'))
async def main_menu_call(
    callback: CallbackQuery,
    callback_data: MenuCall,
    service: QuestionService,
):
    await service.menu()

@question_router.message(CommandStart(deep_link=True), QuestionDeep.filter())
async def menu(message: Message, service: QuestionService, message_id: int | None = None, chat_id: int | None = None):
    await service.menu()
    if message_id and chat_id:
        await service.bot.delete_message(chat_id, message_id)

@question_router.message(Command('question'))
@command(
    name='question',
    description='Вопросы: random, mine, create, json, stats',
    arguments=[Optionals.question_mode],
    error_handler=DEFAULT_BOT_ERROR_HANDLER,
)
async def question_command(
    message: Message,
    service: QuestionService,
    question_mode: str | None = None,
):
    if question_mode is None:
        await service.menu()
    elif question_mode == 'random':
        await service.random_question()
    elif question_mode == 'mine':
        await service.questions()
    elif question_mode == 'create':
        await service.start_create()
    elif question_mode == 'json':
        await service.start_json_create()
    elif question_mode == 'stats':
        await service.user_statistics()
    else:
        await service.invalid_subcommand(question_mode)


@question_router.message(Command('pending_questions'))
@command(
    name='pending_questions',
    description='Показать необработанные вопросы',
    error_handler=DEFAULT_BOT_ERROR_HANDLER,
)
async def pending_questions_command(message: Message, service: QuestionService):
    await service.pending_questions()


@question_router.callback_query(PendingQuestionsRefreshCall.filter())
async def pending_questions_refresh_call(
    callback: CallbackQuery,
    callback_data: PendingQuestionsRefreshCall,
    service: QuestionService,
):
    await service.pending_questions()
    await callback.answer('Список обновлён')


@question_router.callback_query(QuestionMineCall.filter())
async def mine_call(callback: CallbackQuery, callback_data: QuestionMineCall, service: QuestionService):
    await service.questions(callback_data.page)

@question_router.callback_query(QuestionRandomCall.filter())
async def random_call(callback: CallbackQuery, callback_data: QuestionRandomCall, service: QuestionService):
    await service.random_question()

@question_router.callback_query(QuestionRandomDifficultyCall.filter())
async def random_difficulty_call(
    callback: CallbackQuery,
    callback_data: QuestionRandomDifficultyCall,
    service: QuestionService,
):
    await service.random_question(callback_data.difficulty)

@question_router.callback_query(QuestionStartCreateCall.filter())
async def start_create_call(callback: CallbackQuery, callback_data: QuestionStartCreateCall, service: QuestionService):
    await service.start_create()

@question_router.callback_query(QuestionStartJsonCreateCall.filter())
@flags.is_unavailable(True)
async def start_json_create_call(callback: CallbackQuery, callback_data: QuestionStartJsonCreateCall, service: QuestionService):
    await service.start_json_create()

@question_router.callback_query(QuestionUserStatsCall.filter())
async def user_stats_call(callback: CallbackQuery, callback_data: QuestionUserStatsCall, service: QuestionService):
    await service.user_statistics()

@question_router.callback_query(QuestionLimitsCall.filter())
async def limits_call(callback: CallbackQuery, callback_data: QuestionLimitsCall, service: QuestionService):
    await service.limits()

@question_router.callback_query(QuestionLeaveQuizCall.filter())
async def leave_quiz_call(callback: CallbackQuery, callback_data: QuestionLeaveQuizCall, service: QuestionService):
    await service.leave_quiz()

@question_router.callback_query(QuestionEditCall.filter())
async def edit_call(callback: CallbackQuery, callback_data: QuestionEditCall, service: QuestionService):
    if callback_data.action == 'field':
        await service.edit_field(callback_data.question_id, callback_data.field)
    elif callback_data.action == 'submit':
        await service.submit_edit(callback_data.question_id)
    elif callback_data.action == 'review':
        await service.edit_review(callback_data.question_id)
    elif callback_data.action == 'cancel':
        await service.cancel_edit()
    else:
        await service.start_edit(callback_data.question_id)

@question_router.callback_query(QuestionMenuCall.filter())
async def menu_action_call(
    callback: CallbackQuery,
    callback_data: QuestionMenuCall,
    service: QuestionService,
):
    await service.menu()


@question_router.callback_query(QuestionPageCall.filter())
async def page_call(
    callback: CallbackQuery,
    callback_data: QuestionPageCall,
    service: QuestionService,
):
    await service.questions(callback_data.page)


@question_router.callback_query(QuestionSelectCall.filter())
async def select_call(
    callback: CallbackQuery,
    callback_data: QuestionSelectCall,
    service: QuestionService,
):
    await service.open_question(
        callback_data.page,
        callback_data.index,
    )


@question_router.callback_query(QuestionQuizAnswerCall.filter())
async def quiz_answer_call(
    callback: CallbackQuery,
    callback_data: QuestionQuizAnswerCall,
    service: QuestionService,
):
    await service.submit_quiz_answer(
        callback_data.question_id,
        callback_data.answer_id,
    )


@question_router.callback_query(QuestionCreateCall.filter())
async def create_call(
    callback: CallbackQuery,
    callback_data: QuestionCreateCall,
    service: QuestionService,
):
    if callback_data.action == 'edit':
        await service.edit_create_field(callback_data.field)
    elif callback_data.action == 'submit':
        await service.submit_create(callback_data.is_anonim)
    elif callback_data.action == 'cancel':
        await service.cancel_create()
    else:
        await service.review_create()


@question_router.callback_query(QuestionModerationCall.filter())
async def moderation_call(
    callback: CallbackQuery,
    callback_data: QuestionModerationCall,
    service: QuestionService,
):
    await service.moderate(
        callback_data.action,
        callback_data.field,
        callback_data.tg_id,
    )


@question_router.message(QuestionState.create, F.text, ~F.text.startswith('/'))
async def create_text(message: Message, service: QuestionService):
    await service.create_input()
    await service.bot.delete_message(message.chat.id, message.message_id)

@question_router.message(QuestionState.edit, F.text, ~F.text.startswith('/'))
async def edit_text(message: Message, service: QuestionService):
    await service.edit_input()
    await service.bot.delete_message(message.chat.id, message.message_id)


@question_router.message(QuestionState.json_create, F.text, ~F.text.startswith('/'))
async def create_json_text(message: Message, service: QuestionService):
    await service.create_json_input()


@question_router.message(QuestionState.moderation_edit, F.text, ~F.text.startswith('/'))
async def moderation_edit_text(message: Message, service: QuestionService):
    msg0 = await service.fsm.get_message()
    await service.moderation_edit_input()
    await service.bot.delete_message(*msg0)

@question_router.message(QuestionState.moderation_reason, F.text, ~F.text.startswith('/'))
async def moderation_reason_text(message: Message, service: QuestionService):
    msg0 = await service.fsm.get_message()
    await service.moderation_rejection_reason()
    await service.bot.delete_message(*msg0)
