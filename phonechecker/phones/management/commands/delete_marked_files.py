import asyncio
import logging

import aiofiles.os
from django.core.files.storage import FileSystemStorage
from django.core.management.base import BaseCommand

from phones.models import RegistryFile

logger = logging.getLogger(__name__)


async def asyncio_find_and_delete_marked_files() -> list:
    storage = RegistryFile.get_file_storage()
    deleted_files: list = []
    logger.debug("Storage: %s", storage)
    if isinstance(storage, FileSystemStorage):
        files = await aiofiles.os.listdir(storage.location)
        logger.info(files)
        for f in files:
            if f.endswith(".del"):
                try:
                    await aiofiles.os.remove(f"{storage.location}/{f}")
                    deleted_files.append(f)
                    logger.info(f"Deleting file: {f}")
                except Exception as e:
                    logger.warning(f"Error while deleting file: {f}", exc_info=e)

    return deleted_files


class Command(BaseCommand):
    help = "Parse storage files, find *.del and delete them"

    def handle(self, *args, **options):
        logger.info("Running...")
        result = asyncio.run(asyncio_find_and_delete_marked_files())
        self.stdout.write(self.style.SUCCESS(f"Deleted files: {len(result)}"))
