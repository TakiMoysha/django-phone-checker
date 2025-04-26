from pathlib import Path
from unittest import mock
import aiofiles
from aiofiles.threadpool import wrap as aiofiles_wrap
import pytest

from unittest.mock import patch, mock_open
from phones.lib.def_number_parser import def_file_parser

example = """АВС/ DEF;От;До;Емкость;Оператор;Регион;Территория ГАР;ИНН
900;0000000;0061999;62000;ООО "Т2 МОБАЙЛ";Краснодарский край;Краснодарский край;7743895280
900;0062000;0062999;1000;ООО "Т2 МОБАЙЛ";Ростовская обл.;Ростовская область;7743895280
900;0063000;0099999;37000;ООО "Т2 МОБАЙЛ";Краснодарский край;Краснодарский край;7743895280
900;0100000;0199999;100000;ООО "Т2 Мобайл";Тверская обл.;Тверская область;7743895280
900;0200000;0299999;100000;ООО "Т2 Мобайл";Челябинская обл.;Челябинская область;7743895280
900;0300000;0499999;200000;ООО "ЕКАТЕРИНБУРГ-2000";Свердловская обл.;Свердловская область;6661079603
"""
example_iter = iter(example.split("\n"))

aiofiles_wrap.register(mock.MagicMock)(
    lambda *args, **kwargs: aiofiles.threadpool.binary.AsyncBufferedIOBase(
        *args, **kwargs
    )
)


@pytest.mark.asyncio
@patch("aiofiles.threadpool.sync_open", mock_open(read_data=example))
async def test_def_file_parser(*args, **kwrags):
    gen = def_file_parser(Path("mockfile"))

    async for item in gen:
        print(item)
