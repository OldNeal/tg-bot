from telegram_click_aio.argument import Argument, Flag, Selection
from app.aio.args.func import parse_date, parse_duration, is_time_pattern, is_datetime
from datetime import datetime, timedelta

seq = Selection(
    name=['seq', 's'],
    description='Последовательность',
    allowed_values=list(range(-1, 10)),
    type=int,
    optional=True,
)

drink_seq = Selection(
    name=['seq', 's'],
    description='Последовательность',
    allowed_values=list(range(-1, 10)),
    type=int,
    optional=True,
    default=9,
)

time_mode = Selection(
    name=['time_mode', 'mode', 'm'],
    description='Режим команды /time',
    allowed_values=['info', 'redact', 'replace'],
    type=str
)

optional_time_mode = Selection(
    name=['time_mode', 'mode', 'm'],
    description='Режим команды /time',
    allowed_values=['info', 'redact', 'replace'],
    type=str,
    optional=True,
    default='info',
)

duration = Argument(
            name=['duration', 'd'],
            description='Промежуток времени',
            type=timedelta,
            example='+5h7m',
            converter=parse_duration
        )

datetime_arg = Argument(
            name=['datetime_arg', 'date'],
            description='Новая дата',
            type=datetime,
            example='12-11-2013',
            converter=parse_date
        )

