import asyncio
from config import dp, bot, to_menu_cmds, botlog
from app.aio.cmd.base import base_router
from app.aio.cls.middlewares import BotLogMessageMiddleware, BotLogCallbackQueryMiddleware
from app.logic.base import BaseLogic as logic

@botlog.logger.catch(reraise=True)
async def main():
    dp.message.middleware(BotLogMessageMiddleware())
    dp.callback_query.middleware(BotLogCallbackQueryMiddleware())
    dp.include_routers(base_router) 
    botlog.start()
    asyncio.gather(logic.test_api_connect())
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
    


