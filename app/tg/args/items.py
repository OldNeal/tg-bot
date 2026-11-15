from telegram_click_aio.argument import Argument, Selection

action = Selection(
    name='action',
    description='Подкоманда управления предметами',
    allowed_values=['give', 'take'],
)

item_id = Argument(
    name=['item_id', 'id'],
    description='ID предмета',
    type=int,
    validator=lambda value: value > 0,
    example='1',
)

quantity = Argument(
    name=['quantity', 'count', 'q'],
    description='Количество предметов',
    type=int,
    validator=lambda value: value > 0,
    example='1',
    optional=True,
)
