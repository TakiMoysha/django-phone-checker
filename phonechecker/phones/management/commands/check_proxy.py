import asyncio
import logging

from django.core.management.base import BaseCommand

from phones.lib.proxy import get_proxy_from_env, is_proxy_working

logger = logging.getLogger(__name__)


async def asyncio_run_proxy_check(): 
    proxies = await get_proxy_from_env()

    health_proxy = []
    for p in proxies:
        if await is_proxy_working(p):
            health_proxy.append(p)
    return (proxies, health_proxy)


class Command(BaseCommand):
    help = "Loaded proxies list from, example: $HTTP_PROXY=http://0.0.0.0:3128,http://127.0.0.1:3128"

    def handle(self, *args, **options):
        logger.info("Running...")
        res = asyncio.run(asyncio_run_proxy_check())
        self.stdout.write(
            self.style.SUCCESS(
                f"Checked: {res[0]}\nWorking: {res[1]}",
            )
        )
