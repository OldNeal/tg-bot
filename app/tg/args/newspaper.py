from telegram_click_aio.argument import Argument, Flag, Selection

news_paper_id = Argument(
            name=['id'],
            description='ID организации',
            type=int,
            example='1'
        )

optional_news_paper_id = Argument(
            name=['id'],
            description='ID газеты',
            type=int,
            example='1',
            optional=True
        )

news_paper_name = Argument(
            name=['name'],
            description='Название организации',
            type=str,
            example='Орден Старых',
            optional=True
        )

news_paper_value = Argument(
            name=['value'],
            description='Поисковой запрос',
            type=str,
            example='Орден',
            optional=True
        )

news_paper_mode = Argument(
            name=['mode'],
            description='Подкоманда /news_paper',
            type=str,
            example='info'
        )
