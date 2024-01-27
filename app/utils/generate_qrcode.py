# Copyright 2024 daneeke
# Licensed under the Apache License, Version 2.0 (the "License")

import io
import qrcode
from asyncio import get_event_loop


async def generate_qrcode(qrcode_data: str) -> bytes:
    def func() -> bytes:
        _qrcode = qrcode.make(qrcode_data)

        buffer = io.BytesIO()
        _qrcode.save(buffer)

        qrcode_byted = buffer.getvalue()
        return qrcode_byted
    
    loop = get_event_loop()
    result = await loop.run_in_executor(None, func)
    return result
