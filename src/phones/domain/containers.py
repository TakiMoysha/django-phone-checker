from dishka import make_container

from phones.domain.providers import RepositoriesProvider


repository_containers = make_container(
    RepositoriesProvider("my_def_phone"),
)
