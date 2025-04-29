import logging
from datetime import datetime
from pathlib import Path

from background_task import background

logger = logging.getLogger(__name__)

registry_metadata = {
    "url": "https://opendata.digital.gov.ru/registry/numeric/downloads",
}


def _download_datasets() -> list[Path]: ...


def _parse_dataset() -> None: ...


def _update_database_by_dataset() -> None: ...


async def load_files() -> list[Path]:
    pass
    


@background(schedule=60)
async def update_database_from_registry() -> None:
    logger.info(f"[{datetime.now()}] Start <update_database_from_registry>")
    files = await load_files()
