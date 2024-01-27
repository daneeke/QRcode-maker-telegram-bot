# Copyright 2024 daneeke
# Licensed under the Apache License, Version 2.0 (the "License")


from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message, BufferedInputFile

from keyboards.generate_qrcode_keyboard import GenerateQRcodeKeyboard
from keyboards.start_keyboard import StartKeyboard
from utils.escape import aescape
from utils.generate_qrcode import generate_qrcode

_alert = '⚠️ Вы можете взаимодействовать только с кнопками, прикреплённые к сообщениям, которые вызвали вы'

router = Router()


class GeneratingQRcodeState(StatesGroup):
    data = State()


@router.message(GeneratingQRcodeState.data)
async def get_generate_qrcode_data_text_message_handler(message: Message, state: FSMContext):
    qrcode_data = await aescape(message.text)

    if len(qrcode_data) > 1000:
        markup = await GenerateQRcodeKeyboard.markup(user_id=message.from_user.id)
        await message.answer(
            '🚫 Длина QRcode не может быть более, чем 1000 символов!'
            '\n  — Попробуйте ещё раз',
            reply_markup=markup
        )
        return
    
    qrcode = await generate_qrcode(qrcode_data)
    
    markup = await StartKeyboard.markup(user_id=message.from_user.id)
    await message.answer_photo(
        BufferedInputFile(qrcode, 'qrcode.png'),
        '😊 Вот ваш QR-code!'
        '\n  — Нажмите на кнопку ниже, чтобы сгенерировать ещё',
        reply_markup=markup
    )


@router.callback_query(F.data.startswith(StartKeyboard.button_callback_1))
async def get_generate_callback_query_handler(callback: CallbackQuery, state: FSMContext):
    callback_data = callback.data.split()[1:]
    required_id = int(callback_data[0])

    if callback.from_user.id != required_id:
        await callback.answer(_alert, show_alert=True)
        return
    
    markup = await GenerateQRcodeKeyboard.markup(user_id=required_id)
    await callback.message.answer(
        '🪄 Напишите текст, который вы хотите вставить в QR-code',
        reply_markup=markup
    )
    await state.set_state(GeneratingQRcodeState.data)
    
    await callback.answer()


@router.callback_query(F.data.startswith(GenerateQRcodeKeyboard.button_callback_1))
async def get_cancel_generate_qrcode_callback_query_handler(callback: CallbackQuery, state: FSMContext):
    callback_data = callback.data.split()[1:]
    required_id = int(callback_data[0])

    if callback.from_user.id != required_id:
        await callback.answer(_alert, show_alert=True)
        return
    
    await callback.answer()
    
    current_state = await state.get_state()
    if current_state is None or current_state.split(':')[0] != GeneratingQRcodeState.__name__:
        await callback.message.answer('🚫 Вы не пытаетесь сгенерировать QR-code, поэтому нам нечего отменять!')
        return
    
    await state.clear()

    await callback.message.answer(
        '✅ Вы успешно отменили генерацию QR-code!'
        '\n  — Напишите команду /start, чтобы попробовать ещё раз'
    )
