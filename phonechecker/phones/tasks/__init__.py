import logging
from datetime import datetime
from pathlib import Path

from background_task import background

logger = logging.getLogger(__name__)


async def load_files() -> list[Path]:
    pass


async def update_database_from_registry() -> None:
    files = await load_files()
