from config import settings, bot, Router, Command, FSMContext, Message, InputRichMessage, F
from app.service.wiki import WikiService
from telegram_click_aio.decorator import command
from app.aio.args import base_args, Optionals, Requireds
from app.exception.decor import exept, call_exept

wiki_router = Router()

@wiki_router.message(Command('group'))
@command(
    name='group',
    description='Получить информацию о группах', 
    arguments=[Optionals.group_name] + base_args
)
@exept()
async def cmd_start(message: Message, state: FSMContext, **kwargs):
    msgs = await WikiService(message, state, **kwargs).group()
    [await message.answer_rich(InputRichMessage(html=m), reply_markup=k) for m, k in msgs]

@wiki_router.message(Command('ga'))
@command(
    name='ga',
    description='Получить информацию о великих древних', 
    arguments=[Optionals.value] + base_args
)
@exept()
async def cmd_start(message: Message, state: FSMContext, **kwargs):
    msgs = await WikiService(message, state, **kwargs).ga()
    [await message.answer_rich(InputRichMessage(html=m), reply_markup=k) for m, k in msgs]

#@wiki_router.message(Command('seq'))
#@command(
#    name='seq',
#    description='Получить карточку', 
#    arguments=base_args
#)
#async def cmd_start(message: Message, state: FSMContext, **kwargs):
#    msgs = await WikiService(message, state, **kwargs).info()
#    [await message.answer_rich(InputRichMessage(html=m), reply_markup=k) for m, k in msgs]

@wiki_router.message(Command('path'))
@command(
    name='path',
    description='Получить информацию о путях', 
    arguments=[Optionals.value] + base_args
)
@exept()
async def cmd_start(message: Message, state: FSMContext, **kwargs):
    msgs = await WikiService(message, state, **kwargs).path()
    [await message.answer_rich(InputRichMessage(html=m), reply_markup=k) for m, k in msgs]






