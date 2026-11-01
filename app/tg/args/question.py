from telegram_click_aio.argument import Argument


question_mode = Argument(
    name=['question_mode', 'mode'],
    description='Подкоманда /question',
    type=str,
    example='mine',
    optional=True,
)
