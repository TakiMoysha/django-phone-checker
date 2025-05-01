import asyncio
from datetime import datetime
from logging import getLogger
from pathlib import Path
from typing import Annotated
from asgiref.sync import sync_to_async

from django.core.files.storage import FileSystemStorage
from django.db.models.expressions import RawSQL
import httpx

from phones.consts import REGISTRY_FILES_URLS
from phones.lib.parsers import def_file_parser
from phones.models import DEFPhone, RegistryFile
from phones.repositories import MaterializedRepostiory
from phones.schemas import PhoneInfoRequestSchema


logger = getLogger(__name__)


async def find_def_phone_by_number(data: PhoneInfoRequestSchema) -> DEFPhone: ...


async def create_materialized_def_phones(): ...


async def load_registry_from_file(
    file: Path,
    repository: Annotated[MaterializedRepostiory, "provide from dishka"],
    *,
    from_scratch=True,
):
    if from_scratch:
        _ = await sync_to_async(lambda: DEFPhone.objects.all().delete())()

    entries = [entry async for entry in def_file_parser(file)]
    logger.info(f"Loaded {file.name}: {len(entries)} entries")
    _ = await sync_to_async(lambda: DEFPhone.objects.bulk_create(objs=entries))()
    _ = await repository.create_view()
    mv_res = await repository.raw_sql(f"SELECT * FROM {repository.name} LIMIT 10")
    logger.debug("Materialized view content: %s", mv_res)


async def bulk_download_registry_files() -> list[RegistryFile]:
    """gov using cloudflare => proxy useless (or maybe it was bad proxy), mocking downloads"""

    time_checkout = str(datetime.now().timestamp()).replace(".", "_")

    async def _downlod_file(url, *, checkout_prefix: int | None = None) -> RegistryFile:
        logger.info(f"Start download {url}...")
        try:
            request = await httpx.get(url)
        except httpx.HTTPError as err:
            logger.error(f"Download error: {err}")
            raise err

        if checkout_prefix is None:
            file_name = f"{time_checkout}_{Path(url).name}"
        else:
            file_name = f"{str(checkout_prefix)}_{Path(url).name}"

        registry_file = RegistryFile(file=file_name)

        file_storage = RegistryFile.get_file_storage()
        if file_storage is FileSystemStorage:
            storage_path = file_storage.path
            with open(storage_path + file_name, "wb") as file:
                file.write(request.content)
                registry_file.save()
                logger.info(f"Downloaded {url} as {file_name}")

        else:
            raise NotImplementedError("File storage not implemented")

        return registry_file

    try:
        files = await asyncio.gather(*[_downlod_file(f) for f in REGISTRY_FILES_URLS])
        return files
    except httpx.HTTPError as err:
        logger.error(f"ConnectionError <probably cloudflare blocked>.", exc_info=True)
        return []
