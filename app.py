import asyncio
from aiogram import Bot, Dispatcher
from decouple import config
from handlers import private, group, games
from optional import options


async def main():
    bot = Bot(token=config('TOKEN'))
    dp = Dispatcher()
    dp.include_routers(private.private_router, group.group_router, games.game_router)

    await bot.delete_webhook(drop_pending_updates=True)
    await bot.set_my_commands(commands=options.private)
    await dp.start_polling(bot)


asyncio.run(main())
