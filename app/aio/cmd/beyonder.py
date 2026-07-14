from config import settings, bot, Router, Command, FSMContext, Message, F
from app.service.beyonder import BeyonderService
from telegram_click_aio.decorator import command
from app.aio.args import base_args, Requireds, Optionals
from app.exception.decor import exept, call_exept

beyonder_router = Router()

@beyonder_router.message(Command('drink'))
@command(
    name='drink',
    description='Выпить зелье',  
    arguments=[Optionals.path_name] + [Optionals.drink_seq] + base_args
)
@exept
async def cmd_drink(message: Message, state: FSMContext, **kwargs):
    msgs = await BeyonderService(message, state, **kwargs).drink()
    [await message.answer(m, reply_markup=k) for m, k in msgs]

@beyonder_router.message(Command('upseq'))
@command(
    name='upseq',
    description='Поднять последовательонсть',  
    arguments=[Optionals.seq] + [Optionals.path_name] + base_args
)
@exept
async def cmd_drink(message: Message, state: FSMContext, **kwargs):
    msgs = await BeyonderService(message, state, **kwargs).upseq()
    [await message.answer(m, reply_markup=k) for m, k in msgs]

@beyonder_router.message(Command('downseq'))
@command(
    name='downseq',
    description='Понизить последовательонсть',  
    arguments=[Optionals.seq] + [Optionals.path_name] + base_args
)
@exept
async def cmd_drink(message: Message, state: FSMContext, **kwargs):
    msgs = await BeyonderService(message, state, **kwargs).dowseq()
    [await message.answer(m, reply_markup=k) for m, k in msgs]

@beyonder_router.message(Command('kill'))
@command(
    name='kill',
    description='Потерять контроль',  
    arguments=base_args
)
@exept
async def cmd_drink(message: Message, state: FSMContext, **kwargs):
    msgs = await BeyonderService(message, state, **kwargs).kill()
    [await message.answer(m, reply_markup=k) for m, k in msgs]

@beyonder_router.message(Command('time'), F.text.contains('info'))
@command(
    name='time info',
    description='Узнать информацию о продвижении',  
    arguments=[Optionals.time_mode] + base_args
)
@exept
async def cmd_drink(message: Message, state: FSMContext, **kwargs):
    msgs = await BeyonderService(message, state, **kwargs).time_info()
    [await message.answer(m, reply_markup=k) for m, k in msgs]

@beyonder_router.message(Command('time'), F.text.contains('redact'))
@command(
    name='time redact',
    description='Изменить время продвижения',  
    arguments=[Requireds.time_mode] + [Requireds.duration] + base_args
)
@exept
async def cmd_drink(message: Message, state: FSMContext, **kwargs):
    msgs = await BeyonderService(message, state, **kwargs).time_redact()
    [await message.answer(m, reply_markup=k) for m, k in msgs]

@beyonder_router.message(Command('time'), F.text.contains('replace'))
@command(
    name='time replace',
    description='Заменить время продвижения',  
    arguments=[Requireds.time_mode] + [Requireds.date] + base_args
)
@exept
async def cmd_drink(message: Message, state: FSMContext, **kwargs):
    msgs = await BeyonderService(message, state, **kwargs).time_replace()
    [await message.answer(m, reply_markup=k) for m, k in msgs]
