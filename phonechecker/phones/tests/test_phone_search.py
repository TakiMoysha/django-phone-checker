from logging import getLogger
from django.test import TestCase


logger = getLogger(__name__)


class TestPhonesAPI(TestCase):
    def test_should_return_bad_request_by_validation(self):
        response = self.client.post(
            path="/api/phones/search",
            data={"phone": "+7 (999) 888-77-66"},
        )
        self.assertEqual(response.status_code, 400)
