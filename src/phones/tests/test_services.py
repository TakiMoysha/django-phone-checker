import os
import unittest
from logging import getLogger
from pathlib import Path

from django.conf import settings

from phones.services import (
    bulk_download_registry_files,
    load_registry_from_file,
)


logger = getLogger(__name__)

TRUE_VALUES = settings.TRUE_VALUES

class TestServices(unittest.IsolatedAsyncioTestCase):
    test_file = Path("tmp/registry/DEF-9xx.csv")

    @unittest.skip("temporary disabled")
    async def test_download_registry_files(self) -> None:
        _ = await bulk_download_registry_files()

    @unittest.skipIf(os.getenv("TEST_WITH_DATABASE") not in TRUE_VALUES, "required postgres")
    async def test_load_def_to_database(self) -> None:
        _ = await load_registry_from_file(self.test_file, from_scratch=True)

    @unittest.skip("temporary disabled")
    async def test_update_local_registry_from_files(self) -> None:
        _ = await load_registry_from_file(self.test_file)
