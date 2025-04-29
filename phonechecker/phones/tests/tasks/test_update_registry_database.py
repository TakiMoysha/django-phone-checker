import unittest
from datetime import datetime
from logging import getLogger
from pathlib import Path

import httpx
import pytest
from asgiref.sync import sync_to_async

from app.settings import DB_INMEMORY
from phones.lib.parsers import def_file_parser
from phones.models import DEFPhone, RegistryFile
from phones.tasks.consts import REGISTRY_FILES

logger = getLogger(__name__)


async def download_files() -> list[RegistryFile]:
    """gov.ru using cloudflare => proxy useless (or maybe it was bad proxy) => required mocking downloads"""

    def _downlod_file(url, *, id: int | None = None) -> RegistryFile:
        logger.info(f"Start download {url}...")
        try:
            request = httpx.get(url)
        except httpx.HTTPError as err:
            logger.error(f"Download error: {err}")
            raise err

        if id is None:
            file_name = (
                f"{str(datetime.now().timestamp()).replace('.', '_')}_{Path(url).name}"
            )
        else:
            file_name = f"{str(id)}_{Path(url).name}"

        registry_file = RegistryFile(file=file_name)
        with open("tmp/registry/" + file_name, "wb") as file:
            file.write(request.content)
            logger.info(f"Downloaded {url} as {file_name}")

            registry_file.save()

        return registry_file

    try:
        files = [_downlod_file(url) for url in REGISTRY_FILES]
        return files
    except httpx.HTTPError as err:
        logger.error(f"ConnectionError <probably cloudflare blocked>.", exc_info=True)
        return []


async def load_local_registry_from_files(registry_file: RegistryFile):
    entries = [entry async for entry in def_file_parser(Path(registry_file.file))]
    logger.info(f"Loaded {len(entries)} entries")
    res = await sync_to_async(
        DEFPhone.objects.using(DB_INMEMORY).bulk_create,
    )(objs=entries)
    logger.info(f"Loaded {len(res)} entries")
    input("Press Enter to continue...")


async def task_update_database_from_registry() -> list[Path]:  # type: ignore
    logger.info("Start download files...")
    files = await download_files()


class TestServerTasks(unittest.IsolatedAsyncioTestCase):
    @pytest.mark.django_db
    @unittest.skip("temporary disabled")
    async def test_update_database_from_registry(client: httpx.AsyncClient) -> None:
        logger.info(f"Start <{task_update_database_from_registry.__name__}>")
        files = await task_update_database_from_registry()

    @pytest.mark.django_db(database=DB_INMEMORY)
    async def test_load_def_to_database(client: httpx.AsyncClient) -> None:
        registry_file = RegistryFile.objects.all()[0]
        _ = await load_local_registry_from_files(registry_file)
