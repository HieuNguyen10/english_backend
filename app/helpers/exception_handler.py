from __future__ import annotations
import enum
from typing import ClassVar
from collections.abc import Callable
from contextlib import contextmanager

from fastapi import Request
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from app.serializers.base import ResponseSchemaBase

__all__ = ["Callback", "add_callbacks"]


class ExceptionType(enum.Enum):
    MS_UNAVAILABLE = 500, '990', 'Hệ thống đang bảo trì, quý khách vui lòng thử lại sau'
    MS_INVALID_API_PATH = 500, '991', 'Hệ thống đang bảo trì, quý khách vui lòng thử lại sau'
    DATA_RESPONSE_MALFORMED = 500, '992', 'Có lỗi xảy ra, vui lòng liên hệ admin!'

    def __new__(cls, *args, **kwds):
        value = len(cls.__members__) + 1
        obj = object.__new__(cls)
        obj._value_ = value
        return obj

    def __init__(self, http_code, code, message):
        self.http_code = http_code
        self.code = code
        self.message = message


class RemoteException(Exception):
    """Remote Exception
    Contains the exception and traceback from a remotely run task
    """

    def __init__(self, exception, traceback):
        self.exception = exception
        self.traceback = traceback

    def __str__(self):
        return str(self.exception) + "\n\nTraceback\n---------\n" + self.traceback

    def __dir__(self):
        return sorted(set(dir(type(self)) + list(self.__dict__) + dir(self.exception)))

    def __getattr__(self, key):
        try:
            return object.__getattribute__(self, key)
        except AttributeError:
            return getattr(self.exception, key)


class CustomException(Exception):
    http_code: int
    code: str
    message: str

    def __init__(self, http_code: int = None, code: str = None, message: str = None):
        self.http_code = http_code if http_code else 500
        self.code = code if code else str(self.http_code)
        self.message = message


exceptions: dict[type[Exception], type[Exception]] = {}


class ServiceException(Exception):
    def __init__(self, code, message):
        self.code = code
        self.message = message


def remote_exception(exc: Exception, tb) -> Exception:
    """Metaclass that wraps exception type in RemoteException"""
    if type(exc) in exceptions:
        typ = exceptions[type(exc)]
        return typ(exc, tb)
    else:
        try:
            typ = type(
                exc.__class__.__name__,
                (RemoteException, type(exc)),
                {"exception_type": type(exc)},
            )
            exceptions[type(exc)] = typ
            return typ(exc, tb)
        except TypeError:
            return


async def http_exception_handler(request: Request, exc: CustomException):
    return JSONResponse(
        status_code=exc.http_code,
        content=jsonable_encoder(ResponseSchemaBase().custom_response(exc.code, exc.message))
    )


async def validation_exception_handler(request, exc):
    return JSONResponse(
        status_code=400,
        content=jsonable_encoder(ResponseSchemaBase().custom_response('400', get_message_validation(exc)))
    )


async def fastapi_error_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content=jsonable_encoder(ResponseSchemaBase().custom_response('500', "Có lỗi xảy ra, vui lòng liên hệ admin!"))
    )


def get_message_validation(exc):
    message = ""
    for error in exc.errors():
        message += "/'" + str(error.get("loc")[1]) + "'/" + ': ' + error.get("msg") + ", "

    message = message[:-2]

    return message


class Callback:
    """Base oc_class for using the callback mechanism
    Create a callback with functions of the following signatures:
    """

    active: ClassVar[set[tuple[Callable | None, ...]]] = set()

    def __init__(
            self, start=None, start_state=None, pretask=None, posttask=None, finish=None
    ):
        if start:
            self._start = start
        if start_state:
            self._start_state = start_state
        if pretask:
            self._pretask = pretask
        if posttask:
            self._posttask = posttask
        if finish:
            self._finish = finish

    @property
    def _callback(self) -> tuple[Callable | None, ...]:
        fields = ["_start", "_start_state", "_pretask", "_posttask", "_finish"]
        return tuple(getattr(self, i, None) for i in fields)

    def __enter__(self):
        self._cm = add_callbacks(self)
        self._cm.__enter__()
        return self

    def __exit__(self, *args):
        self._cm.__exit__(*args)

    def register(self) -> None:
        Callback.active.add(self._callback)

    def unregister(self) -> None:
        Callback.active.remove(self._callback)


def unpack_callbacks(cbs):
    """Take an iterable of callbacks, return a list of each callback."""
    if cbs:
        return [[i for i in f if i] for f in zip(*cbs)]
    else:
        return [(), (), (), (), ()]


@contextmanager
def local_callbacks(callbacks=None):
    """Allows callbacks to work with nested schedulers.
    Callbacks will only be used by the first started scheduler they encounter.
    This means that only the outermost scheduler will use global callbacks."""
    global_callbacks = callbacks is None
    if global_callbacks:
        callbacks, Callback.active = Callback.active, set()
    try:
        yield callbacks or ()
    finally:
        if global_callbacks:
            Callback.active = callbacks


def normalize_callback(cb):
    """Normalizes a callback to a tuple"""
    if isinstance(cb, Callback):
        return cb._callback
    elif isinstance(cb, tuple):
        return cb
    else:
        raise TypeError("Callbacks must be either `Callback` or `tuple`")


class add_callbacks:
    """Context manager for callbacks.
    Takes several callbacks and applies them only in the enclosed context.
    Callbacks can either be represented as a ``Callback`` object, or as a tuple
    of length 4.
    Examples
    --------
    """

    def __init__(self, *callbacks):
        self.callbacks = [normalize_callback(c) for c in callbacks]
        Callback.active.update(self.callbacks)

    def __enter__(self):
        return

    def __exit__(self, type, value, traceback):
        for c in self.callbacks:
            Callback.active.discard(c)
