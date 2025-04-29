import logging

from unittest_parametrize import ParametrizedTestCase, parametrize

from phones.lib import validators
from phones.schemas import PhoneInfoRequestSchema

logger = logging.getLogger(__name__)


class TestSearchPhone(ParametrizedTestCase):
    @parametrize(
        "phone,email",
        [
            ("+77366", None),
            ("+712312312121", None),
            ("8(999) ooo-77-86", None),
            ("+7 (999) 888877-66", None),
        ],
    )
    def test_should_catch_bad_phones(self, phone: str, email: str | None = None):
        self.assertRaises(
            validators.ValidationError,
            lambda: PhoneInfoRequestSchema(phone=phone, email=email),
        )

    @parametrize(
        "phone,email",
        [
            ("8 (999) 888-77-66", None),
            ("+7 (999) 888-77-66", None),
            ("+7 999  888 77 66", None),
        ],
    )
    def test_should_pass_good_phones(self, phone: str, email: str | None = None):
        PhoneInfoRequestSchema(phone=phone, email=email)
