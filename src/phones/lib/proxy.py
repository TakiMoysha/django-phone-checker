import logging
import os

import httpx

logger = logging.getLogger(__name__)

proxy_transport = httpx.AsyncHTTPTransport(retries=5)


async def get_proxy_from_env(
    env: str = "HTTP_PROXY",
    separator: str = ",",
) -> tuple[httpx.Proxy, ...]:
    """
    Return proxy from env var HTTP_PROXY, split by comma.
    Example: HTTP_PROXY="http://0.0.0.0:3128,http://127.0.0.1:3128"

    Args:
        env (str, optional): Defaults to "HTTP_PROXY".
        separator (str, optional): Defaults to ",".

    Returns:
        tuple[httpx.Proxy]: list of proxies from env
    """

    try:
        raw_proxy = os.getenv(env, "")
        proxy = tuple(map(httpx.Proxy, raw_proxy.split(separator)))
        return proxy
    except httpx.UnsupportedProtocol as err:
        logger.error("Error parsing proxy: %s", raw_proxy, exc_info=err)
        return ()


async def is_proxy_working(p: httpx.Proxy) -> bool:
    """Check if proxy is working

    Args:
        p (httpx.Proxy): proxy object

    Returns:
        bool: True if proxy is working
    """
    async with httpx.AsyncClient(
        proxy=p,
        headers={"User-Agent": "Mozilla/5.0"},
        transport=proxy_transport,
    ) as client:
        try:
            response = await client.get("https://8.8.8.8", timeout=10)
            return True
        except httpx.ProxyError as err:
            logger.warning("Proxy not working: %s", err)
            return False
