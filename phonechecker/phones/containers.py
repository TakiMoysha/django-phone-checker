from dishka import Container, Scope
from dishka import make_async_container
from dishka.provider import BaseProvider


class UserPhoneProvider(BaseProvider):
    scope = Scope.REQUEST

    def provide(self, container: Container):
        from .services import PhoneService

        return PhoneService()


UserPhoneContainer = make_async_container()

EventLogContainer = make_async_container()
