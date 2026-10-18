import asyncio
from aiogram.exceptions import TelegramBadRequest

from config import dp, bot, to_menu_cmds, settings
from app.aio.cmd.base import base_router
from app.aio.cls.middlewares import (BotLogMessageMiddleware,
                                BotLogCallbackQueryMiddleware,
                                ExceptionMessageMiddleware,
                                ExceptionCallbackQueryMiddleware)
from app.logic.base import BaseLogic as logic
from app.logging.base import botlog

async def update_bot_info():
    try:
        bot_info = await bot.get_me()
        settings.info['main'] = bot_info
        return bot_info
    except TelegramBadRequest:
        botlog.logger.critical('Телеграм недоступен')
        await bot.session.close()
        asyncio.get_running_loop().stop()

@botlog.logger.catch(reraise=True)
async def main():
    botlog.logger.info('Бот запускается')
    bot_info = await update_bot_info()
    if bot_info:
        dp.message.middleware(BotLogMessageMiddleware())
        dp.callback_query.middleware(BotLogCallbackQueryMiddleware())
        dp.message.middleware(ExceptionMessageMiddleware())
        dp.callback_query.middleware(ExceptionCallbackQueryMiddleware())
        dp.include_router(base_router)
        botlog.start()
        await bot.delete_webhook(drop_pending_updates=True)
        await to_menu_cmds()
        await dp.start_polling(bot)

@dp.shutdown()
async def stop(bot):
    await dp.storage.close()
    botlog.stop()

if __name__ == "__main__": 
    try:
        asyncio.run(main())
    except RuntimeError as e:
        botlog.stop()
    

