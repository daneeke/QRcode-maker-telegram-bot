# Copyright 2024 daneeke
# Licensed under the Apache License, Version 2.0 (the "License")

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


class GenerateQRcodeKeyboard:
    button_1 = '🚫 Отмена'
    button_callback_1 = 'cancel'

    @classmethod
    async def markup(self, user_id: int) -> InlineKeyboardMarkup:
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text=self.button_1,
                        callback_data=f'{self.button_callback_1} {user_id}'
                    )
                ]
            ]
        )
