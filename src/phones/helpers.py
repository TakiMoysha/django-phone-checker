from phones.domain.repositories import MaterializedRepostiory


def get_defphone_repository():
    return MaterializedRepostiory("mv_def_phones")
