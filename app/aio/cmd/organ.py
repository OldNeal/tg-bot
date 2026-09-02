from config import settings, bot, Router, Command, FSMContext, Message, F, InputRichMessage, CallbackQuery
from app.service.organ import OrganService
from telegram_click_aio.decorator import command
from app.aio.args import base_args, Requireds, Optionals
from app.exception.decor import exept, call_exept
from app.aio.cls.fsm.state import OrganState
from app.aio.cls.callback.organ import (OrganBackCall, 
                                        OrganSettingParametrCall, 
                                        OrganSettingRedactCall, 
                                        OrganSettingModeCall, 
                                        OrganSettingGroupCall, 
                                        OrganSettingParametrBooleanCall, 
                                        OrganSettingParametrDefaultCall,
                                        OrganInfoCall,
                                        OrganMemberCall,
                                        OrganInfoDescCall,
                                        OrganInfoMembersCall,
                                        OrganKickCall,
                                        OrganRankRedactCall,
                                        OrganSettingCall,
                                        OrganTitulRedactCall,
                                        OrganExitCall,
                                        OrganLoginCall,
                                        OrganTitulDeleteCall,
                                        OrganPageCall,
                                        OrganCaptureCall,
                                        OrganGiveCall,
                                        OrganMemberPageCall,
                                        OrganSearchCall)
from app.aio.cls.fsm.utils import OrganFSM
from app.aio.cls.callback.back import OrganBackValues

organ_router = Router()
    
@organ_router.message(Command('member'))
@command(
    name='member',
    description='Информация о участнике',  
    arguments=base_args
)
@exept()
async def cmd(message: Message, state: FSMContext, **kwargs):
    msgs = await OrganService(message, state, **kwargs).member()
    [await message.answer_rich(InputRichMessage(html=m), reply_markup=k) for m, k in msgs]

@organ_router.message(Command('organ'), F.text.contains('member'))
@command(
    name='organ member',
    description='Информация о участнике',  
    arguments=[Requireds.organ_mode] + base_args
)
@exept()
async def cmd(message: Message, state: FSMContext, **kwargs):
    msgs = await OrganService(message, state, **kwargs).member()
    [await message.answer_rich(InputRichMessage(html=m), reply_markup=k) for m, k in msgs]

@organ_router.callback_query(OrganMemberCall.filter())     
@call_exept()
async def call(callback: CallbackQuery, callback_data: OrganMemberCall, state: FSMContext, **kwargs):
    msgs = await OrganService(callback.message, state, callback, **kwargs).member(callback_data.purpose_tg_id)
    [await callback.message.edit_text(rich_message=InputRichMessage(html=m), reply_markup=k) for m, k in msgs]

@organ_router.message(Command('organ'), F.text.contains('search'))
@command(
    name='organ search',
    description='Найти организацию',  
    arguments=[Requireds.organ_mode, Requireds.organ_value] + base_args
)
@exept()
async def cmd(message: Message, state: FSMContext, **kwargs):
    msgs = await OrganService(message, state, **kwargs).search()
    [await message.answer_rich(InputRichMessage(html=m), reply_markup=k) for m, k in msgs]

@organ_router.callback_query(OrganBackCall.filter(F.where == OrganBackValues.search))     
@call_exept()
async def call(callback: CallbackQuery, callback_data: OrganBackCall, state: FSMContext, **kwargs):
    msgs = await OrganService(callback.message, state, callback, **kwargs).search(is_back=True)
    [await callback.message.edit_text(rich_message=InputRichMessage(html=m), reply_markup=k) for m, k in msgs]

@organ_router.callback_query(OrganSearchCall.filter())     
@call_exept()
async def call(callback: CallbackQuery, callback_data: OrganSearchCall, state: FSMContext, **kwargs):
    msgs = await OrganService(callback.message, state, callback, **kwargs).search(is_back=True)
    [await callback.message.edit_text(rich_message=InputRichMessage(html=m), reply_markup=k) for m, k in msgs]

@organ_router.message(OrganState.search)
@exept()
async def text_state(message: Message, state: FSMContext, **kwargs):
    fsm = OrganFSM(state)
    msg0 = await fsm.get_value('msg')
    msgs = await OrganService(message, state, **kwargs).to_search()
    [await message.answer_rich(InputRichMessage(html=m), reply_markup=k) for m, k in msgs]
    await fsm.set_state()
    await msg0.delete()
    await fsm.remove_value('msg')

@organ_router.callback_query(OrganPageCall.filter(F.is_search == True))     
@call_exept()
async def call(callback: CallbackQuery, callback_data: OrganPageCall, state: FSMContext, **kwargs):
    msgs = await OrganService(callback.message, state, callback, **kwargs).search(is_back=True, page=callback_data.page)
    [await callback.message.edit_text(rich_message=InputRichMessage(html=m), reply_markup=k) for m, k in msgs]

@organ_router.message(Command('organ'), F.text.contains('info'))
@command(
    name='organ info',
    description='Информация о организации',  
    arguments=[Requireds.organ_mode, Optionals.organ_id] + base_args
)
@exept()
async def cmd(message: Message, state: FSMContext, **kwargs):
    msgs = await OrganService(message, state, **kwargs).info()
    [await message.answer_rich(InputRichMessage(html=m), reply_markup=k) for m, k in msgs]
    
@organ_router.callback_query(OrganBackCall.filter(F.where == OrganBackValues.info))     
@call_exept()
async def call(callback: CallbackQuery, callback_data: OrganBackCall, state: FSMContext, **kwargs):
    msgs = await OrganService(callback.message, state, callback, **kwargs).info(is_back=True)
    [await callback.message.edit_text(rich_message=InputRichMessage(html=m), reply_markup=k) for m, k in msgs]

@organ_router.callback_query(OrganInfoCall.filter())     
@call_exept()
async def call(callback: CallbackQuery, callback_data: OrganInfoCall, state: FSMContext, **kwargs):
    msgs = await OrganService(callback.message, state, callback, **kwargs).info(callback_data.organ_id, callback_data.purpose_tg_id)
    [await callback.message.edit_text(rich_message=InputRichMessage(html=m), reply_markup=k) for m, k in msgs]

@organ_router.message(Command('organ'), F.text.contains('members'))
@command(
    name='organ members',
    description='Участники организации',  
    arguments=[Requireds.organ_mode, Optionals.organ_id] + base_args
)
@exept()
async def cmd(message: Message, state: FSMContext, **kwargs):
    msgs = await OrganService(message, state, **kwargs).info_members()
    [await message.answer_rich(InputRichMessage(html=m), reply_markup=k) for m, k in msgs]

@organ_router.callback_query(OrganBackCall.filter(F.where == OrganBackValues.members))     
@call_exept()
async def call(callback: CallbackQuery, callback_data: OrganBackCall, state: FSMContext, **kwargs):
    msgs = await OrganService(callback.message, state, callback, **kwargs).info(is_back=True)
    [await callback.message.edit_text(rich_message=InputRichMessage(html=m), reply_markup=k) for m, k in msgs]

@organ_router.callback_query(OrganInfoMembersCall.filter())     
@call_exept()
async def call(callback: CallbackQuery, callback_data: OrganInfoMembersCall, state: FSMContext, **kwargs):
    msgs = await OrganService(callback.message, state, callback, **kwargs).info_members(callback_data.organ_id)
    [await callback.message.edit_text(rich_message=InputRichMessage(html=m), reply_markup=k) for m, k in msgs]

@organ_router.callback_query(OrganMemberPageCall.filter())     
@call_exept()
async def call(callback: CallbackQuery, callback_data: OrganMemberPageCall, state: FSMContext, **kwargs):
    msgs = await OrganService(callback.message, state, callback, **kwargs).info_members(callback_data.organ_id, callback_data.page)
    [await callback.message.edit_text(rich_message=InputRichMessage(html=m), reply_markup=k) for m, k in msgs]
    
@organ_router.message(Command('organ'), F.text.contains('description') | F.text.contains('desc'))
@command(
    name='organ description',
    description='Описание организации',  
    arguments=[Requireds.organ_mode, Optionals.organ_id] + base_args
)
@exept()
async def cmd(message: Message, state: FSMContext, **kwargs):
    msgs = await OrganService(message, state, **kwargs).info_description()
    [await message.answer_rich(InputRichMessage(html=m), reply_markup=k) for m, k in msgs]

@organ_router.callback_query(OrganInfoDescCall.filter())     
@call_exept()
async def call(callback: CallbackQuery, callback_data: OrganInfoDescCall, state: FSMContext, **kwargs):
    msgs = await OrganService(callback.message, state, callback, **kwargs).info_description(callback_data.organ_id)
    [await callback.message.edit_text(rich_message=InputRichMessage(html=m), reply_markup=k) for m, k in msgs]
    
@organ_router.message(Command('organ'), F.text.contains('list'))
@command(
    name='organ list',
    description='Организации',  
    arguments=[Requireds.organ_mode] + base_args
)
@exept()
async def cmd(message: Message, state: FSMContext, **kwargs):
    msgs = await OrganService(message, state, **kwargs).list()
    [await message.answer_rich(InputRichMessage(html=m), reply_markup=k) for m, k in msgs]

@organ_router.callback_query(OrganBackCall.filter(F.where == OrganBackValues.list))     
@call_exept()
async def call(callback: CallbackQuery, callback_data: OrganBackCall, state: FSMContext, **kwargs):
    msgs = await OrganService(callback.message, state, callback, **kwargs).list()
    [await callback.message.edit_text(rich_message=InputRichMessage(html=m), reply_markup=k) for m, k in msgs]

@organ_router.callback_query(OrganPageCall.filter())     
@call_exept()
async def call(callback: CallbackQuery, callback_data: OrganPageCall, state: FSMContext, **kwargs):
    msgs = await OrganService(callback.message, state, callback, **kwargs).list(callback_data.page)
    [await callback.message.edit_text(rich_message=InputRichMessage(html=m), reply_markup=k) for m, k in msgs]

@organ_router.message(Command('organ'), F.text.contains('top'))
@command(
    name='organ top',
    description='Топ организаций',  
    arguments=[Requireds.organ_mode] + base_args
)
@exept()
async def cmd(message: Message, state: FSMContext, **kwargs):
    msgs = await OrganService(message, state, **kwargs).top()
    [await message.answer_rich(InputRichMessage(html=m), reply_markup=k) for m, k in msgs]

@organ_router.callback_query(OrganBackCall.filter(F.where == OrganBackValues.top))     
@call_exept()
async def call(callback: CallbackQuery, callback_data: OrganBackCall, state: FSMContext, **kwargs):
    msgs = await OrganService(callback.message, state, callback, **kwargs).top()
    [await callback.message.edit_text(rich_message=InputRichMessage(html=m), reply_markup=k) for m, k in msgs]





@organ_router.message(Command('login'))
@command(
    name='login',
    description='Войти в организацию',  
    arguments=[Optionals.organ_id] + base_args
)
@exept()
async def cmd(message: Message, state: FSMContext, **kwargs):
    msgs = await OrganService(message, state, **kwargs).login()
    [await message.answer_rich(InputRichMessage(html=m), reply_markup=k) for m, k in msgs]

@organ_router.message(Command('organ'), F.text.contains('login'))
@command(
    name='organ login',
    description='Войти в организацию',  
    arguments=[Requireds.organ_mode] + base_args
)
@exept()
async def cmd(message: Message, state: FSMContext, **kwargs):
    msgs = await OrganService(message, state, **kwargs).login()
    [await message.answer_rich(InputRichMessage(html=m), reply_markup=k) for m, k in msgs]

@organ_router.callback_query(OrganLoginCall.filter())     
@call_exept()
async def call(callback: CallbackQuery, callback_data: OrganLoginCall, state: FSMContext, **kwargs):
    msgs = await OrganService(callback.message, state, callback, **kwargs).login(callback_data.organ_id)
    [await callback.message.edit_text(rich_message=InputRichMessage(html=m), reply_markup=k) for m, k in msgs]

@organ_router.message(Command('exit'))
@command(
    name='exit',
    description='Выйти из организации',  
    arguments=base_args
)
@exept()
async def cmd(message: Message, state: FSMContext, **kwargs):
    msgs = await OrganService(message, state, **kwargs).to_exit()
    [await message.answer_rich(InputRichMessage(html=m), reply_markup=k) for m, k in msgs]

@organ_router.message(Command('organ'), F.text.contains('exit'))
@command(
    name='organ exit',
    description='Выйти из организации',  
    arguments=[Requireds.organ_mode] + base_args
)
@exept()
async def cmd(message: Message, state: FSMContext, **kwargs):
    msgs = await OrganService(message, state, **kwargs).to_exit()
    [await message.answer_rich(InputRichMessage(html=m), reply_markup=k) for m, k in msgs]

@organ_router.callback_query(OrganExitCall.filter(F.accert == True))     
@call_exept()
async def call(callback: CallbackQuery, callback_data: OrganExitCall, state: FSMContext, **kwargs):
    msgs = await OrganService(callback.message, state, callback, **kwargs).exit()
    [await callback.message.edit_text(rich_message=InputRichMessage(html=m), reply_markup=k) for m, k in msgs]

@organ_router.callback_query(OrganExitCall.filter(F.cancel == True))     
@call_exept()
async def call(callback: CallbackQuery, callback_data: OrganExitCall, state: FSMContext, **kwargs):
    msgs = await OrganService(callback.message, state, callback, **kwargs).cancel_exit()
    [await callback.message.edit_text(rich_message=InputRichMessage(html=m), reply_markup=k) for m, k in msgs]

@organ_router.callback_query(OrganExitCall.filter())     
@call_exept()
async def call(callback: CallbackQuery, callback_data: OrganExitCall, state: FSMContext, **kwargs):
    msgs = await OrganService(callback.message, state, callback, **kwargs).to_exit()
    [await callback.message.edit_text(rich_message=InputRichMessage(html=m), reply_markup=k) for m, k in msgs]


@organ_router.message(Command('organ'), F.text.contains('create') | F.text.contains('new'))
@command(
    name='organ create',
    description='Создать организацию',  
    arguments=[Requireds.organ_mode, Requireds.organ_name]
)
@exept()
async def cmd(message: Message, state: FSMContext, **kwargs):
    msgs = await OrganService(message, state, **kwargs).create()
    [await message.answer_rich(InputRichMessage(html=m), reply_markup=k) for m, k in msgs]
    
@organ_router.message(Command('organ'), F.text.contains('setting') | F.text.contains('settings'))
@command(
    name='organ setting',
    description='Настройки организации',  
    arguments=[Requireds.organ_mode] + base_args
)
@exept()
async def cmd(message: Message, state: FSMContext, **kwargs):
    msgs = await OrganService(message, state, **kwargs).get_settings()
    [await message.answer_rich(InputRichMessage(html=m), reply_markup=k) for m, k in msgs]

@organ_router.callback_query(OrganBackCall.filter(F.where == OrganBackValues.settings))     
@call_exept()
async def call(callback: CallbackQuery, callback_data: OrganBackCall, state: FSMContext, **kwargs):
    msgs = await OrganService(callback.message, state, callback, **kwargs).get_settings()
    [await callback.message.edit_text(rich_message=InputRichMessage(html=m), reply_markup=k) for m, k in msgs]

@organ_router.callback_query(OrganSettingCall.filter())     
@call_exept()
async def call(callback: CallbackQuery, callback_data: OrganSettingCall, state: FSMContext, **kwargs):
    msgs = await OrganService(callback.message, state, callback, **kwargs).get_settings()
    [await callback.message.edit_text(rich_message=InputRichMessage(html=m), reply_markup=k) for m, k in msgs]

@organ_router.callback_query(OrganSettingRedactCall.filter())     
@call_exept()
async def call(callback: CallbackQuery, callback_data: OrganSettingRedactCall, state: FSMContext, **kwargs):
    msgs = await OrganService(callback.message, state, callback, **kwargs).to_redact_settings()
    [await callback.message.edit_text(rich_message=InputRichMessage(html=m), reply_markup=k) for m, k in msgs]

@organ_router.callback_query(OrganSettingParametrDefaultCall.filter(F.is_all == True))     
@call_exept()
async def cmd(callback: CallbackQuery, callback_data: OrganSettingParametrDefaultCall, state: FSMContext, **kwargs):
    msgs = await OrganService(callback.message, state, callback, **kwargs).default_settings()
    [await callback.message.edit_text(rich_message=InputRichMessage(html=m), reply_markup=k) for m, k in msgs]

@organ_router.message(OrganState.settings)
@exept()
async def text_state(message: Message, state: FSMContext, **kwargs):
    fsm = OrganFSM(state)
    msg0 = await fsm.get_value('msg')
    msgs = await OrganService(message, state, **kwargs).redact_settings()
    [await message.answer_rich(InputRichMessage(html=m), reply_markup=k) for m, k in msgs]
    await fsm.set_state()
    await msg0.delete()
    await fsm.remove_value('msg')

@organ_router.message(Command('organ'), F.text.contains('capture'))
@command(
    name='organ capture',
    description='Захватить организациб',  
    arguments=[Requireds.organ_mode] + base_args
)
@exept()
async def cmd(message: Message, state: FSMContext, **kwargs):
    msgs = await OrganService(message, state, **kwargs).capture()
    [await message.answer_rich(InputRichMessage(html=m), reply_markup=k) for m, k in msgs]

@organ_router.callback_query(OrganCaptureCall.filter())     
@call_exept()
async def cmd(callback: CallbackQuery, callback_data: OrganCaptureCall, state: FSMContext, **kwargs):
    msgs = await OrganService(callback.message, state, callback, **kwargs).capture()
    [await callback.message.edit_text(rich_message=InputRichMessage(html=m), reply_markup=k) for m, k in msgs]




    
@organ_router.message(Command('uprank'))
@command(
    name='uprank',
    description='Повысить ранг участника',  
    arguments=[Optionals.rank] + base_args
)
@exept()
async def cmd(message: Message, state: FSMContext, **kwargs):
    msgs = await OrganService(message, state, **kwargs).uprank()
    [await message.answer_rich(InputRichMessage(html=m), reply_markup=k) for m, k in msgs]
    
@organ_router.message(Command('organ'), F.text.contains('uprank'))
@command(
    name='organ uprank',
    description='Повысить ранг участника',  
    arguments=[Requireds.organ_mode, Optionals.rank] + base_args
)
@exept()
async def cmd(message: Message, state: FSMContext, **kwargs):
    msgs = await OrganService(message, state, **kwargs).uprank()
    [await message.answer_rich(InputRichMessage(html=m), reply_markup=k) for m, k in msgs]

@organ_router.message(Command('downrank'))
@command(
    name='downrank',
    description='Понизить ранг участника',  
    arguments=[Optionals.rank] + base_args
)
@exept()
async def cmd(message: Message, state: FSMContext, **kwargs):
    msgs = await OrganService(message, state, **kwargs).downrank()
    [await message.answer_rich(InputRichMessage(html=m), reply_markup=k) for m, k in msgs]

@organ_router.message(Command('organ'), F.text.contains('downrank'))
@command(
    name='organ downrank',
    description='Понизить ранг участника',  
    arguments=[Requireds.organ_mode, Optionals.rank] + base_args
)
@exept()
async def cmd(message: Message, state: FSMContext, **kwargs):
    msgs = await OrganService(message, state, **kwargs).downrank()
    [await message.answer_rich(InputRichMessage(html=m), reply_markup=k) for m, k in msgs]

@organ_router.callback_query(OrganRankRedactCall.filter(F.operation == 'up'))     
@call_exept()
async def call(callback: CallbackQuery, callback_data: OrganRankRedactCall, state: FSMContext, **kwargs):
    msgs = await OrganService(callback.message, state, callback, **kwargs).uprank(callback_data.purpose_tg_id)
    [await callback.message.edit_text(rich_message=InputRichMessage(html=m), reply_markup=k) for m, k in msgs]

@organ_router.callback_query(OrganRankRedactCall.filter(F.operation == 'down'))     
@call_exept()
async def call(callback: CallbackQuery, callback_data: OrganRankRedactCall, state: FSMContext, **kwargs):
    msgs = await OrganService(callback.message, state, callback, **kwargs).downrank(callback_data.purpose_tg_id)
    [await callback.message.edit_text(rich_message=InputRichMessage(html=m), reply_markup=k) for m, k in msgs]

@organ_router.message(Command('organ'), F.text.contains('kick'))
@command(
    name='organ kick',
    description='Выгнать участника',  
    arguments=[Requireds.organ_mode] + base_args
)
@exept()
async def cmd(message: Message, state: FSMContext, **kwargs):
    msgs = await OrganService(message, state, **kwargs).kick()
    [await message.answer_rich(InputRichMessage(html=m), reply_markup=k) for m, k in msgs]

@organ_router.callback_query(OrganKickCall.filter(F.accert == True))     
@call_exept()
async def call(callback: CallbackQuery, callback_data: OrganKickCall, state: FSMContext, **kwargs):
    msgs = await OrganService(callback.message, state, callback, **kwargs).accert_kick(callback_data.purpose_tg_id)
    [await callback.message.edit_text(rich_message=InputRichMessage(html=m), reply_markup=k) for m, k in msgs]

@organ_router.callback_query(OrganKickCall.filter(F.cancel == True))     
@call_exept()
async def call(callback: CallbackQuery, callback_data: OrganKickCall, state: FSMContext, **kwargs):
    msgs = await OrganService(callback.message, state, callback, **kwargs).cancel_kick()
    [await callback.message.edit_text(rich_message=InputRichMessage(html=m), reply_markup=k) for m, k in msgs]

@organ_router.callback_query(OrganKickCall.filter())     
@call_exept()
async def call(callback: CallbackQuery, callback_data: OrganKickCall, state: FSMContext, **kwargs):
    msgs = await OrganService(callback.message, state, callback, **kwargs).kick(callback_data.purpose_tg_id)
    [await callback.message.edit_text(rich_message=InputRichMessage(html=m), reply_markup=k) for m, k in msgs]

@organ_router.message(Command('titul'), F.text.contains('delete') | F.text.contains('del'))
@command(
    name='titul delete',
    description='Убрать титул участника',  
    arguments=[Requireds.titul_mode] + base_args
)
@exept()
async def cmd(message: Message, state: FSMContext, **kwargs):
    msgs = await OrganService(message, state, **kwargs).titul_delete()
    [await message.answer_rich(InputRichMessage(html=m), reply_markup=k) for m, k in msgs]

@organ_router.message(Command('organ'), F.text.contains('titul delete') | F.text.contains('titul del'))
@command(
    name='organ titul delete',
    description='Убрать титул участника',  
    arguments=[Requireds.organ_mode, Requireds.titul_mode] + base_args
)
@exept()
async def cmd(message: Message, state: FSMContext, **kwargs):
    msgs = await OrganService(message, state, **kwargs).titul_delete()
    [await message.answer_rich(InputRichMessage(html=m), reply_markup=k) for m, k in msgs]

@organ_router.callback_query(OrganTitulDeleteCall.filter())     
@call_exept()
async def call(callback: CallbackQuery, callback_data: OrganTitulDeleteCall, state: FSMContext, **kwargs):
    msgs = await OrganService(callback.message, state, callback, **kwargs).titul_delete(callback_data.purpose_tg_id)
    [await callback.message.edit_text(rich_message=InputRichMessage(html=m), reply_markup=k) for m, k in msgs]

@organ_router.message(Command('titul'), F.text.contains('redact'))
@command(
    name='titul redact',
    description='Поменять титул участника',  
    arguments=[Requireds.titul_mode, Optionals.titul] + base_args
)
@exept()
async def cmd(message: Message, state: FSMContext, **kwargs):
    msgs = await OrganService(message, state, **kwargs).titul()
    [await message.answer_rich(InputRichMessage(html=m), reply_markup=k) for m, k in msgs]

@organ_router.message(Command('organ'), F.text.contains('titul redact'))
@command(
    name='organ titul redact',
    description='Редактировать титул участника',  
    arguments=[Requireds.organ_mode, Requireds.titul_mode, Optionals.titul] + base_args
)
@exept()
async def cmd(message: Message, state: FSMContext, **kwargs):
    msgs = await OrganService(message, state, **kwargs).titul()
    [await message.answer_rich(InputRichMessage(html=m), reply_markup=k) for m, k in msgs]

@organ_router.callback_query(OrganTitulRedactCall.filter())     
@call_exept()
async def call(callback: CallbackQuery, callback_data: OrganTitulRedactCall, state: FSMContext, **kwargs):
    msgs = await OrganService(callback.message, state, callback, **kwargs).titul(callback_data.purpose_tg_id)
    [await callback.message.edit_text(rich_message=InputRichMessage(html=m), reply_markup=k) for m, k in msgs]

@organ_router.message(OrganState.titul)
@exept()
async def text_state(message: Message, state: FSMContext, **kwargs):
    fsm = OrganFSM(state)
    msg0 = await fsm.get_value('msg')
    msgs = await OrganService(message, state, **kwargs).titul_redact()
    [await message.answer_rich(InputRichMessage(html=m), reply_markup=k) for m, k in msgs]
    await fsm.set_state()
    await msg0.delete()
    await fsm.remove_value('msg')

@organ_router.message(Command('titul'))
@command(
    name='titul',
    description='Редактировать титул участника',  
    arguments=[Optionals.titul] + base_args
)
@exept()
async def cmd(message: Message, state: FSMContext, **kwargs):
    msgs = await OrganService(message, state, **kwargs).titul()
    [await message.answer_rich(InputRichMessage(html=m), reply_markup=k) for m, k in msgs]

@organ_router.message(Command('organ'), F.text.contains('titul'))
@command(
    name='organ titul',
    description='Редактировать титул участника',  
    arguments=[Requireds.organ_mode] + base_args
)
@exept()
async def cmd(message: Message, state: FSMContext, **kwargs):
    msgs = await OrganService(message, state, **kwargs).titul()
    [await message.answer_rich(InputRichMessage(html=m), reply_markup=k) for m, k in msgs]

@organ_router.message(Command('organ'), F.text.contains('give'))
@command(
    name='organ give',
    description='Передать организацию',  
    arguments=[Requireds.organ_mode] + base_args
)
@exept()
async def cmd(message: Message, state: FSMContext, **kwargs):
    msgs = await OrganService(message, state, **kwargs).to_give()
    [await message.answer_rich(InputRichMessage(html=m), reply_markup=k) for m, k in msgs]

@organ_router.callback_query(OrganGiveCall.filter(F.accert == True))     
@call_exept()
async def call(callback: CallbackQuery, callback_data: OrganGiveCall, state: FSMContext, **kwargs):
    msgs = await OrganService(callback.message, state, callback, **kwargs).give(callback_data.purpose_tg_id)
    [await callback.message.edit_text(rich_message=InputRichMessage(html=m), reply_markup=k) for m, k in msgs]

@organ_router.callback_query(OrganGiveCall.filter(F.cancel == True))     
@call_exept()
async def call(callback: CallbackQuery, callback_data: OrganGiveCall, state: FSMContext, **kwargs):
    msgs = await OrganService(callback.message, state, callback, **kwargs).cancel_give()
    [await callback.message.edit_text(rich_message=InputRichMessage(html=m), reply_markup=k) for m, k in msgs]

@organ_router.callback_query(OrganGiveCall.filter())     
@call_exept()
async def call(callback: CallbackQuery, callback_data: OrganGiveCall, state: FSMContext, **kwargs):
    msgs = await OrganService(callback.message, state, callback, **kwargs).to_give(callback_data.purpose_tg_id)
    [await callback.message.edit_text(rich_message=InputRichMessage(html=m), reply_markup=k) for m, k in msgs]









@organ_router.message(Command('organ'))
@command(
    name='organ',
    description='Меню организации',  
    arguments=[Optionals.organ_id] + base_args
)
@exept()
async def cmd_organ_info(message: Message, state: FSMContext, **kwargs):
    msgs = await OrganService(message, state, **kwargs).menu()
    [await message.answer_rich(InputRichMessage(html=m), reply_markup=k) for m, k in msgs]