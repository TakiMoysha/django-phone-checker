import asyncio
import os
from typing import override

import httpx
import unittest

import logging

import pytest

from phones.lib.proxy import get_proxy_from_env, is_proxy_working

logger = logging.getLogger(__name__)


class ProxyTest(unittest.IsolatedAsyncioTestCase):
    @override
    def setUp(self) -> None:
        self.loop = asyncio.get_event_loop()
        self.test_proxy_1 = "http://0.0.0.0:3128"
        self.test_proxy_2 = "http://0.0.0.0:3129"
        return super().setUp()

    async def test_obtaining_proxy_via_env(self):
        env = "TEST_HTTP_PROXY"
        separator = ";"
        os.environ[env] = f"{self.test_proxy_1}{separator}{self.test_proxy_2}"
        proxy_list = await get_proxy_from_env(env, separator)
        assert len(proxy_list) == 2

    @pytest.mark.skip("work in progress")
    async def test_healthcheck_proxy(self):
        proxy_list = list(map(httpx.Proxy, [self.test_proxy_1, self.test_proxy_2]))
        for proxy in proxy_list:
            await is_proxy_working(proxy)
