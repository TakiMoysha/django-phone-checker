import pytest
import httpx


@pytest.fixture(scope="module")
def client():
    transport = httpx.AsyncHTTPTransport(retries=5)
    yield httpx.AsyncClient(transport=transport)
