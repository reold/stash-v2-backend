from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Player(_message.Message):
    __slots__ = ("name", "id", "cards")
    NAME_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    CARDS_FIELD_NUMBER: _ClassVar[int]
    name: str
    id: int
    cards: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, name: _Optional[str] = ..., id: _Optional[int] = ..., cards: _Optional[_Iterable[int]] = ...) -> None: ...

class GameState(_message.Message):
    __slots__ = ("creator", "player_count", "card_count", "id", "creation", "current", "clockwise", "ref", "players")
    CREATOR_FIELD_NUMBER: _ClassVar[int]
    PLAYER_COUNT_FIELD_NUMBER: _ClassVar[int]
    CARD_COUNT_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    CREATION_FIELD_NUMBER: _ClassVar[int]
    CURRENT_FIELD_NUMBER: _ClassVar[int]
    CLOCKWISE_FIELD_NUMBER: _ClassVar[int]
    REF_FIELD_NUMBER: _ClassVar[int]
    PLAYERS_FIELD_NUMBER: _ClassVar[int]
    creator: str
    player_count: int
    card_count: int
    id: str
    creation: str
    current: int
    clockwise: bool
    ref: int
    players: _containers.RepeatedCompositeFieldContainer[Player]
    def __init__(self, creator: _Optional[str] = ..., player_count: _Optional[int] = ..., card_count: _Optional[int] = ..., id: _Optional[str] = ..., creation: _Optional[str] = ..., current: _Optional[int] = ..., clockwise: bool = ..., ref: _Optional[int] = ..., players: _Optional[_Iterable[_Union[Player, _Mapping]]] = ...) -> None: ...

class Opponent(_message.Message):
    __slots__ = ("name", "card_count", "id")
    NAME_FIELD_NUMBER: _ClassVar[int]
    CARD_COUNT_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    name: str
    card_count: int
    id: int
    def __init__(self, name: _Optional[str] = ..., card_count: _Optional[int] = ..., id: _Optional[int] = ...) -> None: ...

class PlayerState(_message.Message):
    __slots__ = ("creator", "player_count", "card_count", "id", "player_id", "creation", "current", "ref", "cards", "opponents")
    CREATOR_FIELD_NUMBER: _ClassVar[int]
    PLAYER_COUNT_FIELD_NUMBER: _ClassVar[int]
    CARD_COUNT_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    PLAYER_ID_FIELD_NUMBER: _ClassVar[int]
    CREATION_FIELD_NUMBER: _ClassVar[int]
    CURRENT_FIELD_NUMBER: _ClassVar[int]
    REF_FIELD_NUMBER: _ClassVar[int]
    CARDS_FIELD_NUMBER: _ClassVar[int]
    OPPONENTS_FIELD_NUMBER: _ClassVar[int]
    creator: str
    player_count: int
    card_count: int
    id: str
    player_id: int
    creation: str
    current: int
    ref: int
    cards: _containers.RepeatedScalarFieldContainer[int]
    opponents: _containers.RepeatedCompositeFieldContainer[Opponent]
    def __init__(self, creator: _Optional[str] = ..., player_count: _Optional[int] = ..., card_count: _Optional[int] = ..., id: _Optional[str] = ..., player_id: _Optional[int] = ..., creation: _Optional[str] = ..., current: _Optional[int] = ..., ref: _Optional[int] = ..., cards: _Optional[_Iterable[int]] = ..., opponents: _Optional[_Iterable[_Union[Opponent, _Mapping]]] = ...) -> None: ...
