import logging
from pathlib import Path
from typing import AsyncGenerator

import aiofiles
from phones.schemas import DefPhoneSchema

logger = logging.getLogger(__name__)


async def def_file_parser(file: Path) -> AsyncGenerator:
    async with aiofiles.open(file, "r") as f:
        await f.readline()

        async for line in f:
            str_def = line.strip().split(";")
            def_number = DefPhoneSchema(
                avs=int(str_def[0]),
                from_=int(str_def[1]),
                to=int(str_def[2]),
                capacity=int(str_def[3]),
                operator=str_def[4],
                region=str_def[5],
                territory=str_def[6],
                inn=str_def[7],
            )

            yield def_number
