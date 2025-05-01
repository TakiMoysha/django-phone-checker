from dishka import Scope, provide, make_container

from .repositories import MaterializedRepostiory


@provide(scope=Scope.APP)
def provide_defphone_materialize_repository() -> MaterializedRepostiory:
    return MaterializedRepostiory("mv_def_phones")


container = make_container()
