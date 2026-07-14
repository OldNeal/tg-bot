from telegram_click_aio.argument import Argument, Flag, Selection


seq_name = Argument(
            name=['seq_name', 'seq'],
            description='Название последовательности',
            type=str,
            example='Провидец',
            optional=True
        )

path_name = Argument(
            name=['path_name', 'path', 'p'],
            description='Название пути или последовательности',
            type=str,
            example='Шут',
            optional=True
        )

ga_name = Argument(
            name=['ga_name', 'ga', 'g'],
            description='Название Великого древнего',
            type=str,
            example='Провидец',
            optional=True
        )

group_name = Argument(
            name=['group_name', 'group'],
            description='Название группы путей',
            type=str,
            example='Земные',
            optional=True
        )

value = Argument(
            name=['value'],
            description='Поисковой запрос',
            type=str,
            example='Шут',
            optional=True
        )

is_all = Flag(['is_all', 'all', 'a'], 'Показать все пути/последовательности/вд/группы')