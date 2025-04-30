import asyncio
from datetime import datetime
from logging import getLogger
from pathlib import Path

import httpx

from phones.consts import REGISTRY_FILES_URLS
from phones.models import DEFPhone, RegistryFile
from phones.schemas import PhoneInfoRequestSchema

logger = getLogger(__name__)


async def find_def_phone_by_number(data: PhoneInfoRequestSchema) -> DEFPhone: ...


async def create_materialized_def_phones(): ...



async def load_registry_from_file(file: Path): ...


async def bulk_download_registry_files() -> list[RegistryFile]:
    """gov using cloudflare => proxy useless (or maybe it was bad proxy), mocking downloads"""

    async def _downlod_file(url, *, id: int | None = None) -> RegistryFile:
        logger.info(f"Start download {url}...")
        try:
            request = await httpx.get(url)
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
        # TODO: take target file_path from model storage
        with open("tmp/registry/" + file_name, "wb") as file:
            file.write(request.content)
            logger.info(f"Downloaded {url} as {file_name}")

            registry_file.save()

        return registry_file

    try:
        files = await asyncio.gather(*[_downlod_file(f) for f in REGISTRY_FILES_URLS])
        return files
    except httpx.HTTPError as err:
        logger.error(f"ConnectionError <probably cloudflare blocked>.", exc_info=True)
        return []
