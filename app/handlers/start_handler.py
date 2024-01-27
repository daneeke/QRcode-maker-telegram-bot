# Copyright 2024 daneeke
# Licensed under the Apache License, Version 2.0 (the "License")

from aiogram import Router
from aiogram.filters.command import CommandStart
from aiogram.types import Message

from keyboards.start_keyboard import StartKeyboard
from utils.escape import aescape

router = Router()


@router.message(CommandStart())
async def get_start_command_handler(message: Message):
    user_name = await aescape(message.from_user.first_name)

    markup = await StartKeyboard.markup(user_id=message.from_user.id)
    await message.answer(
        f'Привет, {user_name}! Это 🪄 QRcode Make - бот, который может сгенерировать тебе QR-code!'
        '\n  — Нажми на кнопку ниже, чтобы попробовать',
        reply_markup=markup
    )
