# Copyright 2024 daneeke
# Licensed under the Apache License, Version 2.0 (the "License")

from asyncio import get_event_loop
from html import escape


async def aescape(text: str) -> str:
    loop = get_event_loop()
    result = await loop.run_in_executor(None, escape, text)
    return result
