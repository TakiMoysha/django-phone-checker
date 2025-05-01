from logging import getLogger

from dishka import (
    Provider,
    Scope,
    provide,
)
from . import repositories as repos

logger = getLogger(__name__)


class RepositoriesProvider(Provider):
    scope = Scope.APP
    component = "repositories"

    def __init__(self, materialized_view_name: str, **kwargs):
        super().__init__(**kwargs)
        self.materialized_view_name = materialized_view_name

    @provide(scope=Scope.APP)
    def defphone_repository(self) -> repos.MaterializedRepostiory:
        return repos.MaterializedRepostiory(self.materialized_view_name)
