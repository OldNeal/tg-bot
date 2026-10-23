from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import CallbackQuery, Message
from telegram_click_aio.decorator import command

from app.service.news_paper import NewsPaperService
from app.service.utils import DEFAULT_BOT_ERROR_HANDLER
from app.tg.args import Optionals, Requireds
from app.tg.callback.news_paper import (
    NewsPaperFireEditorCall,
    NewsPaperGiveCall,
    NewsPaperInfoCall,
    NewsPaperActionCall,
    NewsPaperMakeEditorCall,
    NewsPaperCaptureCall,
    NewsPaperNotifyCall,
    NewsPaperPageCall,
    NewsPaperSearchCall,
    NewsPaperSubscribeCall,
    NewsPaperSettingsCall,
    NewsPaperSettingsDefaultCall,
    NewsPaperSettingsRedactCall,
    NewsPaperUnsubscribeCall,
    ReaderCall
)
from app.tg.fsm.state import NewsPaperState
from app.tg.middlewares import ServiceMiddleware

news_paper_router = Router()
news_paper_router.message.middleware(ServiceMiddleware(NewsPaperService))
news_paper_router.callback_query.middleware(ServiceMiddleware(NewsPaperService))


@news_paper_router.message(Command('newspaper'), F.text.contains('search'))
@command(
    name='newspaper search',
    description='Найти газету',
    arguments=[
        Requireds.news_paper_mode,
        Optionals.value,
        Optionals.to_json,
    ],
    error_handler=DEFAULT_BOT_ERROR_HANDLER
)
async def search(
    message: Message,
    service: NewsPaperService,
    mode: str,
    value: str,
    to_json: bool = False
):
    await service.search(value=value)

@news_paper_router.callback_query(NewsPaperSearchCall.filter())
async def search_call(callback: CallbackQuery, callback_data: NewsPaperSearchCall, service: NewsPaperService):
    await service.to_enter_search()

@news_paper_router.callback_query(NewsPaperPageCall.filter())
async def search_call(callback: CallbackQuery, callback_data: NewsPaperPageCall, service: NewsPaperService):
    if callback_data.mode == 'all':
        await service.all(page=callback_data.page)
    elif callback_data.mode == 'list':
        await service.list(page=callback_data.page)
    elif callback_data.mode == 'editors':
        await service.editors(page=callback_data.page)
    elif callback_data.mode == 'readers':
        if callback_data.news_paper_id is None:
            raise ValueError('Не указан ID газеты для списка читателей')
        await service.readers(
            news_paper_id=callback_data.news_paper_id,
            page=callback_data.page,
        )
    elif callback_data.mode in {'subscribe', 'unsubscribe', 'notify', 'make_editor', 'fire_editor'}:
        await service.select_news_paper(callback_data.mode, page=callback_data.page)
    else:
        await service.search(page=callback_data.page)

@news_paper_router.callback_query(NewsPaperActionCall.filter())
async def action_call(
    callback: CallbackQuery,
    callback_data: NewsPaperActionCall,
    service: NewsPaperService,
):
    await service.run_news_paper_action(
        callback_data.action,
        callback_data.news_paper_id,
    )

@news_paper_router.callback_query(NewsPaperInfoCall.filter())
async def search_call(callback: CallbackQuery, callback_data: NewsPaperInfoCall, service: NewsPaperService):
    await service.info(news_paper_id=callback_data.news_paper_id)

@news_paper_router.callback_query(NewsPaperSubscribeCall.filter())
async def subscribe_call(
    callback: CallbackQuery,
    callback_data: NewsPaperSubscribeCall,
    service: NewsPaperService,
):
    await service.subscribe(callback_data.news_paper_id)

@news_paper_router.callback_query(NewsPaperUnsubscribeCall.filter(F.accert == True))
async def confirm_unsubscribe_call(
    callback: CallbackQuery,
    callback_data: NewsPaperUnsubscribeCall,
    service: NewsPaperService,
):
    await service.unsubscribe(callback_data.news_paper_id)

@news_paper_router.callback_query(NewsPaperUnsubscribeCall.filter(F.cancel == True))
async def cancel_unsubscribe_call(
    callback: CallbackQuery,
    callback_data: NewsPaperUnsubscribeCall,
    service: NewsPaperService,
):
    await service.info(callback_data.news_paper_id)

@news_paper_router.callback_query(NewsPaperUnsubscribeCall.filter())
async def unsubscribe_call(
    callback: CallbackQuery,
    callback_data: NewsPaperUnsubscribeCall,
    service: NewsPaperService,
):
    await service.to_unsubscribe(callback_data.news_paper_id)

@news_paper_router.callback_query(NewsPaperNotifyCall.filter())
async def notify_call(
    callback: CallbackQuery,
    callback_data: NewsPaperNotifyCall,
    service: NewsPaperService,
):
    await service.to_notify(callback_data.news_paper_id)

@news_paper_router.callback_query(NewsPaperCaptureCall.filter())
async def capture_call(
    callback: CallbackQuery,
    callback_data: NewsPaperCaptureCall,
    service: NewsPaperService,
):
    await service.capture(callback_data.news_paper_id)

@news_paper_router.message(NewsPaperState.search, F.text)
async def search_text_state(message: Message, service: NewsPaperService):
    prompt_message = await service.fsm.get_message()
    await service.to_search()
    await service.fsm.set_state()
    await service.bot.delete_message(*prompt_message)
    await service.fsm.remove_message()


@news_paper_router.message(Command('newspaper'), F.text.contains('settings'))
@command(
    name='newspaper settings',
    description='Настройки газеты',
    arguments=[
        Requireds.news_paper_mode,
        Requireds.news_paper_id,
        Optionals.to_json,
    ],
    error_handler=DEFAULT_BOT_ERROR_HANDLER
)
async def settings(
    message: Message,
    service: NewsPaperService,
    mode: str,
    id: int | None = None,
    to_json: bool = False,
):
    await service.get_settings(news_paper_id=id)


@news_paper_router.callback_query(NewsPaperSettingsCall.filter())
async def settings_call(
    callback: CallbackQuery,
    callback_data: NewsPaperSettingsCall,
    service: NewsPaperService,
):
    await service.get_settings(news_paper_id=callback_data.news_paper_id)


@news_paper_router.callback_query(NewsPaperSettingsRedactCall.filter())
async def settings_redact_call(
    callback: CallbackQuery,
    callback_data: NewsPaperSettingsRedactCall,
    service: NewsPaperService,
):
    await service.to_redact_settings(callback_data.news_paper_id)


@news_paper_router.callback_query(NewsPaperSettingsDefaultCall.filter())
async def settings_default_call(
    callback: CallbackQuery,
    callback_data: NewsPaperSettingsDefaultCall,
    service: NewsPaperService,
):
    await service.default_settings(callback_data.news_paper_id)


@news_paper_router.message(NewsPaperState.settings, F.text)
async def settings_text_state(message: Message, service: NewsPaperService):
    prompt_message = await service.fsm.get_message()
    await service.redact_settings()
    await service.fsm.set_state()
    await service.bot.delete_message(*prompt_message)
    await service.fsm.remove_message()


@news_paper_router.message(Command('newspaper'), F.text.contains('all'))
@command(
    name='newspaper all',
    description='Показать все газеты',
    arguments=[
        Requireds.news_paper_mode,
        Optionals.to_json,
    ],
    error_handler=DEFAULT_BOT_ERROR_HANDLER
)
async def all_newspapers(
    message: Message,
    service: NewsPaperService,
    mode: str,
    to_json: bool = False,
):
    await service.all()


@news_paper_router.message(Command('newspaper'), F.text.contains('list'))
@command(
    name='newspaper list',
    description='Показать список газет',
    arguments=[
        Requireds.news_paper_mode,
        Optionals.to_json,
    ],
    error_handler=DEFAULT_BOT_ERROR_HANDLER
)
async def list_newspapers(
    message: Message,
    service: NewsPaperService,
    mode: str,
    to_json: bool = False
):
    await service.list()


@news_paper_router.message(Command('newspaper'), F.text.contains('editors'))
@command(
    name='newspaper editors',
    description='Найти газеты, где пользователь редактор',
    arguments=[
        Requireds.news_paper_mode,
        Optionals.to_json,
    ],
    error_handler=DEFAULT_BOT_ERROR_HANDLER
)
async def editors(
    message: Message,
    service: NewsPaperService,
    mode: str,
    to_json: bool = False
):
    await service.editors()


@news_paper_router.message(Command('newspaper'), F.text.contains('info'))
@command(
    name='newspaper info',
    description='Получить информацию о газете',
    arguments=[
        Requireds.news_paper_mode,
        Optionals.optional_news_paper_id,
        Optionals.to_json,
    ],
    error_handler=DEFAULT_BOT_ERROR_HANDLER
)
async def info(
    message: Message,
    service: NewsPaperService,
    mode: str,
    id: int | None = None,
    to_json: bool = False
):
    await service.info(news_paper_id=id)


@news_paper_router.message(Command('newspaper'), F.text.contains('capture'))
@command(
    name='newspaper capture',
    description='Захватить газету',
    arguments=[
        Requireds.news_paper_mode,
        Requireds.news_paper_id,
    ],
    error_handler=DEFAULT_BOT_ERROR_HANDLER
)
async def capture(
    message: Message,
    service: NewsPaperService,
    mode: str,
    id: int,
):
    await service.capture(news_paper_id=id)


@news_paper_router.message(Command('newspaper'), F.text.contains('readers'))
@command(
    name='newspaper readers',
    description='Показать список подписок',
    arguments=[
        Requireds.news_paper_mode,
        Optionals.news_paper_id,
        Optionals.to_json,
    ],
    error_handler=DEFAULT_BOT_ERROR_HANDLER
)
async def readers(
    message: Message,
    service: NewsPaperService,
    mode: str,
    id: int | None = None,
    to_json: bool = False
):
    await service.readers(news_paper_id=id)

@news_paper_router.callback_query(ReaderCall.filter())
async def settings_call(
    callback: CallbackQuery,
    callback_data: ReaderCall,
    service: NewsPaperService,
):
    await service.reader(callback_data.news_paper_id, callback_data.purpose_tg_id)

@news_paper_router.callback_query(NewsPaperMakeEditorCall.filter())
async def make_editor_call(
    callback: CallbackQuery,
    callback_data: NewsPaperMakeEditorCall,
    service: NewsPaperService,
):
    await service.make_editor(
        callback_data.news_paper_id,
        callback_data.purpose_tg_id,
    )

@news_paper_router.callback_query(NewsPaperFireEditorCall.filter())
async def fire_editor_call(
    callback: CallbackQuery,
    callback_data: NewsPaperFireEditorCall,
    service: NewsPaperService,
):
    await service.fire_editor(
        callback_data.news_paper_id,
        callback_data.purpose_tg_id,
    )

@news_paper_router.callback_query(NewsPaperGiveCall.filter(F.accert == True))
async def give_news_paper_call(
    callback: CallbackQuery,
    callback_data: NewsPaperGiveCall,
    service: NewsPaperService,
):
    await service.give(
        callback_data.news_paper_id,
        callback_data.purpose_tg_id,
    )

@news_paper_router.callback_query(NewsPaperGiveCall.filter(F.cancel == True))
async def cancel_give_news_paper_call(
    callback: CallbackQuery,
    callback_data: NewsPaperGiveCall,
    service: NewsPaperService,
):
    await service.reader(
        callback_data.news_paper_id,
        callback_data.purpose_tg_id,
    )

@news_paper_router.callback_query(NewsPaperGiveCall.filter())
async def to_give_news_paper_call(
    callback: CallbackQuery,
    callback_data: NewsPaperGiveCall,
    service: NewsPaperService,
):
    await service.to_give(
        callback_data.news_paper_id,
        callback_data.purpose_tg_id,
    )

@news_paper_router.message(Command('newspaper'), F.text.contains('create'))
@command(
    name='newspaper create',
    description='Создать газету',
    arguments=[
        Requireds.news_paper_mode,
        Optionals.news_paper_name,
        Optionals.to_json,
    ],
    error_handler=DEFAULT_BOT_ERROR_HANDLER
)
async def create(
    message: Message,
    service: NewsPaperService,
    mode: str,
    name: str | None = None,
    to_json: bool = False
):
    await service.create(name=name)


@news_paper_router.message(NewsPaperState.create, F.text)
async def create_text_state(message: Message, service: NewsPaperService):
    prompt_message = await service.fsm.get_message()
    await service.enter_name_for_create()
    await service.fsm.set_state()
    await service.bot.delete_message(*prompt_message)
    await service.fsm.remove_message()


@news_paper_router.message(Command('newspaper'), F.text.contains('subscribe'), F.text.not_contains('unsubscribe'))
@news_paper_router.message(Command('newspaper'), F.text.contains('sub'), F.text.not_contains('unsub'))
@command(
    name='newspaper subscribe',
    description='Подписаться на газету',
    arguments=[
        Requireds.news_paper_mode,
        Optionals.optional_news_paper_id,
        Optionals.to_json,
    ],
    error_handler=DEFAULT_BOT_ERROR_HANDLER
)
async def subscribe(
    message: Message,
    service: NewsPaperService,
    mode: str,
    id: int | None = None,
    to_json: bool = False
):
    await service.subscribe(news_paper_id=id)


@news_paper_router.message(Command('newspaper'), F.text.contains('unsubscribe'))
@news_paper_router.message(Command('newspaper'), F.text.contains('unsub'))
@command(
    name='newspaper unsubscribe',
    description='Отписаться от газеты',
    arguments=[
        Requireds.news_paper_mode,
        Optionals.optional_news_paper_id,
        Optionals.to_json,
    ],
    error_handler=DEFAULT_BOT_ERROR_HANDLER
)
async def unsubscribe(
    message: Message,
    service: NewsPaperService,
    mode: str,
    id: int | None = None,
    to_json: bool = False
):
    await service.unsubscribe(news_paper_id=id)


@news_paper_router.message(Command('newspaper'), F.text.contains('notify'))
@command(
    name='newspaper notify',
    description='Уведомить читателей газеты',
    arguments=[
        Requireds.news_paper_mode,
        Optionals.optional_news_paper_id,
    ],
    error_handler=DEFAULT_BOT_ERROR_HANDLER
)
async def notify(
    message: Message,
    service: NewsPaperService,
    mode: str,
    id: int | None = None
):
    await service.notify(news_paper_id=id)


@news_paper_router.message(Command('newspaper'), F.text.contains('make'))
@command(
    name='newspaper make',
    description='Назначить редактора газеты',
    arguments=[
        Requireds.news_paper_mode,
        Optionals.optional_news_paper_id,
        Optionals.tg_id,
        Optionals.to_json,
        Optionals.is_reply,
    ],
    error_handler=DEFAULT_BOT_ERROR_HANDLER
)
async def make_editor(
    message: Message,
    service: NewsPaperService,
    mode: str,
    id: int | None = None,
    purpose_tg_id: int | None = None,
    to_json: bool = False,
    is_reply: bool = False
):
    await service.make_editor(news_paper_id=id, purpose_tg_id=purpose_tg_id)


@news_paper_router.message(Command('newspaper'), F.text.contains('fire'))
@command(
    name='newspaper fire',
    description='Снять редактора газеты',
    arguments=[
        Requireds.news_paper_mode,
        Optionals.optional_news_paper_id,
        Optionals.tg_id,
        Optionals.to_json,
        Optionals.is_reply,
    ],
    error_handler=DEFAULT_BOT_ERROR_HANDLER
)
async def fire_editor(
    message: Message,
    service: NewsPaperService,
    mode: str,
    id: int | None = None,
    purpose_tg_id: int | None = None,
    to_json: bool = False,
    is_reply: bool = False
):
    await service.fire_editor(news_paper_id=id, purpose_tg_id=purpose_tg_id)


@news_paper_router.message(Command('sub'))
@command(
    name='sub',
    description='Подписаться на газету',
    arguments=[
        Optionals.optional_news_paper_id,
        Optionals.to_json,
    ],
    error_handler=DEFAULT_BOT_ERROR_HANDLER
)
async def subscribe_command(
    message: Message,
    service: NewsPaperService,
    id: int | None = None,
    to_json: bool = False,
):
    await service.subscribe(news_paper_id=id)


@news_paper_router.message(Command('unsub'))
@command(
    name='unsub',
    description='Отписаться от газеты',
    arguments=[
        Optionals.optional_news_paper_id,
        Optionals.to_json,
    ],
    error_handler=DEFAULT_BOT_ERROR_HANDLER
)
async def unsubscribe_command(
    message: Message,
    service: NewsPaperService,
    id: int | None = None,
    to_json: bool = False,
):
    await service.unsubscribe(news_paper_id=id)


@news_paper_router.message(Command('notify'))
@command(
    name='notify',
    description='Уведомить читателей газеты',
    arguments=[
        Optionals.optional_news_paper_id,
    ],
    error_handler=DEFAULT_BOT_ERROR_HANDLER
)
async def notify_command(
    message: Message,
    service: NewsPaperService,
    id: int | None = None,
):
    await service.notify(news_paper_id=id)


@news_paper_router.message(Command('make'))
@command(
    name='make',
    description='Назначить редактора газеты',
    arguments=[
        Requireds.news_paper_id,
        Optionals.tg_id,
        Optionals.to_json,
        Optionals.is_reply,
    ],
    error_handler=DEFAULT_BOT_ERROR_HANDLER
)
async def make_editor_command(
    message: Message,
    service: NewsPaperService,
    id: int,
    purpose_tg_id: int | None = None,
    to_json: bool = False,
    is_reply: bool = False,
):
    await service.make_editor(news_paper_id=id, purpose_tg_id=purpose_tg_id)


@news_paper_router.message(Command('fire'))
@command(
    name='fire',
    description='Снять редактора газеты',
    arguments=[
        Requireds.news_paper_id,
        Optionals.tg_id,
        Optionals.to_json,
        Optionals.is_reply,
    ],
    error_handler=DEFAULT_BOT_ERROR_HANDLER
)
async def fire_editor_command(
    message: Message,
    service: NewsPaperService,
    id: int,
    purpose_tg_id: int | None = None,
    to_json: bool = False,
    is_reply: bool = False,
):
    await service.fire_editor(news_paper_id=id, purpose_tg_id=purpose_tg_id)

@news_paper_router.message(Command('newspaper'))
@command(
    name='newspaper',
    description='Уведомить читателей газеты',
    error_handler=DEFAULT_BOT_ERROR_HANDLER
)
async def newspaper_menu(
    message: Message,
    service: NewsPaperService
):
    await service.menu()
