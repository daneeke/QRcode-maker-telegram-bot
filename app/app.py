# Copyright 2024 daneeke
# Licensed under the Apache License, Version 2.0 (the "License")

from asyncio import run

from handlers import generate_qrcode_handler, start_handler
from loader import bot, dp


@dp.startup()
async def on_startup():
    dp.include_routers(
        start_handler.router,
        generate_qrcode_handler.router
    )

    print('Telegram-Bot has been launched successfully!')


@dp.shutdown()
async def on_shutdown():
    print('Telegram-Bot has been stopped!')


async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        run(main())
    except KeyboardInterrupt:
        exit()
