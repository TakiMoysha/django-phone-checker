import unittest
from logging import getLogger
from pathlib import Path

import httpx

from phones.models import DEFPhone, RegistryFile
from phones.services import (
    bulk_download_registry_files,
    load_registry_from_file,
)

from phones.lib.parsers import def_file_parser

logger = getLogger(__name__)


class TestServerTasks(unittest.IsolatedAsyncioTestCase):
    @unittest.skip("temporary disabled")
    async def test_download_registry_files(self) -> None:
        fiels = await bulk_download_registry_files()

    @unittest.skip("temporary disabled")
    async def test_update_local_registry_from_files(self) -> None:
        test_file = "tmp/registry/DEF-9xx.csv"
        files = await load_registry_from_file()

    @unittest.skip("temporary disabled")
    async def test_load_def_to_database(client: httpx.AsyncClient) -> None:
        registry_file = RegistryFile.objects.all()[0]
        _ = await load_local_registry_from_files(registry_file)


async def load_local_registry_from_files(registry_file: RegistryFile):
    entries = [entry async for entry in def_file_parser(Path(registry_file.file))]
    logger.info(f"Loaded {len(entries)} entries")
    res = await sync_to_async(
        DEFPhone.objects.using(DB_INMEMORY).bulk_create,
    )(objs=entries)
    logger.info(f"Loaded {len(res)} entries")
    input("Press Enter to continue...")
