from telegram_click_aio.decorator import command
from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import CallbackQuery, Message

from app.service.question import QuestionService
from app.service.utils import DEFAULT_BOT_ERROR_HANDLER
from app.tg.args import Optionals
from app.tg.callback.base import MenuCall
from app.tg.callback.question import (
    QuestionCreateCall,
    QuestionMenuCall,
    QuestionPageCall,
    QuestionQuizAnswerCall,
    QuestionSelectCall,
)
from app.tg.fsm.state import QuestionState
from app.tg.middlewares import ServiceMiddleware

question_router = Router()
question_router.message.middleware(ServiceMiddleware(QuestionService))
question_router.callback_query.middleware(ServiceMiddleware(QuestionService))


@question_router.callback_query(MenuCall.filter(F.where == 'question'))
async def main_menu_call(
    callback: CallbackQuery,
    callback_data: MenuCall,
    service: QuestionService,
):
    await service.menu()


@question_router.message(Command('question'))
@command(
    name='question',
    description='Вопросы: random, mine, create, stats',
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
    elif question_mode == 'stats':
        await service.user_statistics()
    else:
        await service.invalid_subcommand(question_mode)


@question_router.callback_query(QuestionMenuCall.filter())
async def menu_action_call(
    callback: CallbackQuery,
    callback_data: QuestionMenuCall,
    service: QuestionService,
):
    if callback_data.action == 'mine':
        await service.questions(callback_data.page)
    elif callback_data.action == 'random':
        await service.random_question()
    elif callback_data.action == 'create':
        await service.start_create()
    elif callback_data.action == 'userstats':
        await service.user_statistics()
    else:
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
        await service.submit_create()
    elif callback_data.action == 'cancel':
        await service.cancel_create()
    else:
        await service.review_create()


@question_router.message(QuestionState.create, F.text)
async def create_text(message: Message, service: QuestionService):
    await service.create_input(message.text)
