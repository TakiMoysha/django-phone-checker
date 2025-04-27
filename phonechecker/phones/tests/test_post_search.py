from django.test import TestCase
from ninja.testing import TestClient

from phones.views import api


class TestSearchPhone(TestCase):
    def test_unvalid_phones(self):
        client = TestClient(api)
        # response = client.post(
        #     "/api/phone/search",
        #     data={"phone": "+7 (999) 999-99-99"},
        # )
        #
        # assert response.status_code == 400
