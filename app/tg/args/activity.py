from telegram_click_aio.argument import Argument, Selection

action = Selection(
    name='action',
    description='Подкоманда управления очками активности',
    allowed_values=['add', 'deduct', 'reset', 'limit_reset'],
)

points = Argument(
    name='points',
    description='Количество очков',
    type=int,
    validator=lambda value: value > 0,
    example='10',
    optional=True,
)

reason = Argument(
    name='reason',
    description='Причина изменения очков',
    type=str,
    example='"Награда за активность"',
    optional=True,
)
