# Copyright 2024 daneeke
# Licensed under the Apache License, Version 2.0 (the "License")

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode

from data.config import token

bot = Bot(
    token=token,
    parse_mode=ParseMode.HTML
)
dp = Dispatcher()
