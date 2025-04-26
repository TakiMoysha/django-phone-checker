from django.core.management.base import AppCommand


class CheckProxy(AppCommand):
    help = "Check proxy, from default env"

    async def handle(self, *args, **options):
        from phones.lib.proxy import get_proxy_from_env, get_first_health_proxy

        proxy = await get_proxy_from_env()
        proxy = await get_first_health_proxy(proxy)
        print(proxy)
