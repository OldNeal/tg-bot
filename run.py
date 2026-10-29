import asyncio
from aiogram.exceptions import TelegramBadRequest
from aiogram_sentinel import Sentinel

from config import dp, bot, to_menu_cmds, settings, sentinel_config
from app.tg.handlers.base import base_router
from app.tg.middlewares import (BotLogMessageMiddleware,
                                BotLogCallbackQueryMiddleware,
                                ExceptionMessageMiddleware,
                                ExceptionCallbackQueryMiddleware)
from app.logic.base import BaseLogic as logic
from app.logging.base import botlog
from app.redis.base import redis_client, redis_ping

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
    try:
        botlog.logger.info('Бот запускается')
        bot_info = await update_bot_info()
        await logic.test_api_connect(True)
        await redis_ping(True)
        if bot_info:
            dp.message.middleware(BotLogMessageMiddleware())
            dp.callback_query.middleware(BotLogCallbackQueryMiddleware())
            dp.message.middleware(ExceptionMessageMiddleware())
            dp.callback_query.middleware(ExceptionCallbackQueryMiddleware())
            await Sentinel().setup(dp, sentinel_config, base_router)
            botlog.start()
            await bot.delete_webhook(drop_pending_updates=True)
            await to_menu_cmds()
            await dp.start_polling(bot)
    except:
        pass
    finally:
        botlog.stop()


@dp.shutdown()
async def stop(bot):
    await dp.storage.close()
    await redis_client.aclose()

if __name__ == "__main__": 
    try:
        asyncio.run(main())
    except RuntimeError as e:
        botlog.stop()
    

