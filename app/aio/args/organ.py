from telegram_click_aio.argument import Argument, Flag, Selection

organ_id = Argument(
            name=['organ_id', 'id'],
            description='ID организации',
            type=int,
            example='1',
            optional=True
        )

organ_name = Argument(
            name=['name'],
            description='Название организации',
            type=str,
            example='Орден Старых'
        )

rank = Argument(
            name=['rank'],
            description='Ранг участника',
            type=int,
            example='9',
            optional=True
        )

organ_value = Argument(
            name=['value'],
            description='Поисковой запрос',
            type=str,
            example='Орден'
        )

organ_mode = Argument(
            name=['organ_mode'],
            description='Подкоманда /organ',
            type=str,
            example='info'
        )

titul_mode = Argument(
            name=['titul_mode'],
            description='Подкоманда /titul',
            type=str,
            example='redact'
        )

titul = Argument(
            name=['titul'],
            description='Титул',
            type=str,
            example='Гнилой',
            optional=True
        )
