from typing import Annotated
from logging import getLogger
from asgiref.sync import sync_to_async
from django.db.models.expressions import RawSQL

logger = getLogger(__name__)


class BaseRepository: ...


class MaterializedRepostiory(BaseRepository):
    name: Annotated[str, "this name was given to materialized view"]

    def __init__(self, name: str) -> None:
        self.name = name

    async def raw_sql(self, sql: str) -> RawSQL:
        return await sync_to_async(lambda: RawSQL(sql, ()))()

    async def create_view(self):
        sql = """
            CREATE MATERIALIZED VIEW mv_def_phones AS
            SELECT id, avs, start, to, capacity, operator, region, territory, inn
            FROM phones_defphone
        """
        mv_res = await sync_to_async(lambda: RawSQL(sql, ()))()
        logger.debug("Materialized view created: %s", mv_res)

    async def update_view(self):
        sql = f"REFRESH MATERIALIZED VIEW {self.name}"
        mv_res = await sync_to_async(lambda: RawSQL(sql, ()))()
        logger.debug("Materialized view updated: %s", mv_res)

    async def drop_view(self):
        sql = f"DROP MATERIALIZED VIEW IF EXISTS {self.name}"
        mv_res = await sync_to_async(lambda: RawSQL(sql, ()))()
        logger.debug("Materialized view dropped: %s", mv_res)
