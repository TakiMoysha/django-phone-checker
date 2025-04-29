from datetime import datetime
from logging import getLogger
from pathlib import Path

import pytest

from phonechecker.phones.storage import registry_files_storage

logger = getLogger(__name__)


async def load_files() -> list[Path]:  # type: ignore
    registry_files_storage


@pytest.mark.asyncio
async def update_database_from_registry() -> None:
    logger.debug(f"[{datetime.now()}] Start <update_database_from_registry>")
    files = await load_files()
