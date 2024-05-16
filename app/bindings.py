from enum import Enum
from pydantic import BaseModel


class MWStatus(Enum):
    OK = 0
    ERROR = 1


class MWSignal(Enum):
    CLIENT = 0
    CLIENT_AND_BROADCAST = 1
    BROADCAST = 2


class MWClient(Enum):
    APPEND = 0
    REMOVE = 1


class MiddlewareWork(BaseModel):
    status: MWStatus | None = None
    status_msg: str | None = None

    signal: MWSignal | None = None
    signal_name: str | None = None
    signal_content: dict | None = None
    client: MWClient | None = None
    client_id: int | None = None
