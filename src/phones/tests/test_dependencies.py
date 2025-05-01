import unittest
from logging import getLogger

from phones.domain.containers import repository_containers
from phones.domain import repositories as repos

logger = getLogger(__name__)


class TestDependencies(unittest.IsolatedAsyncioTestCase):
    @unittest.skip("dishka work in progress")
    async def test_service_container(self):
        repository = repository_containers.get(repos.MaterializedRepostiory)
        logger.debug("11111: ", repository)
