from telegram_click_aio.argument import Argument, Flag, Selection

tg_id = Argument(
            name=['purpose_tg_id', 'tg_id'],
            description='id другого пользователя',
            type=int,
            validator=lambda x: len(str(x)) > 2,
            example='123456789',
            optional=True
        )

to_json = Flag(['to_json', 'json', 'j'], 'Показать в формате json')
is_reply = Flag(['is_reply', 'r'], 'Команда выполняется с учетом ответа (явно)')
is_admin = Flag(['is_admin', 'a'], 'Команда выполняется от лица админа (явно)')
is_delay = Flag(['is_delay', 'delay'], 'Команда выполняется с замеркой времени (таймер)')

