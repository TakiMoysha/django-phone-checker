from logging import getLogger
from typing import Callable, ParamSpec, TypeVar, override
from functools import wraps
from dishka import make_container
from dishka.integrations.base import wrap_injection

from django.http import HttpRequest
from django.utils.deprecation import MiddlewareMixin

T = TypeVar("T")
P = ParamSpec("P")

logger = getLogger(__name__)


def inject(fn: Callable[P, T]) -> Callable[[HttpRequest, P.args, P.kwargs], T]:
    @wraps(fn)
    def wrapper(request: HttpRequest, *args: P.args, **kwargs: P.kwargs) -> T:
        try:
            request_container = request.__getattribute__("container")
        except TypeError as err:
            msg = "Dishka container not implemented, added middleware to MIDDLEWARE"
            raise NotImplementedError(msg) from err

        logger.debug("container: %s", request_container)
        with request_container() as container:
            injected_fn = wrap_injection(
                func=fn,
                container_getter=lambda _, p: container,
                is_async=False,
            )
            return injected_fn(request, *args, **kwargs)

    logger.debug("Injecting %s", fn.__name__)
    return wrapper


class DishkaContainerMiddleware(MiddlewareMixin):
    async_capable = False
    sync_capable = True

    get_response: Callable[[HttpRequest], HttpRequest]

    def __init__(self, get_response: Callable[[HttpRequest], HttpRequest]) -> None:
        self.get_response = get_response
        self.base_container = make_container()

    @override
    def __call__(self, request: HttpRequest):
        request.container = self.base_container  # type: ignore
        response = self.get_response(request)
        return self.get_response(request)
