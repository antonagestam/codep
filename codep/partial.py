from __future__ import annotations

import abc
from typing import Any
from typing import cast
from typing import FrozenSet
from typing import Generic
from typing import Iterable
from typing import Sequence
from typing import Type
from typing import TypeVar

import immutables
from typing_extensions import final


R = TypeVar("R", bound=Any)


class Partial(abc.ABC, Generic[R]):
    depends: Sequence[Type[Partial]] = ()

    @final
    def __init__(self):
        raise RuntimeError("Partials cannot be instantiated")

    @classmethod
    def value(cls, state: immutables.Map) -> R:
        return cast(R, state[cls])

    @classmethod
    @abc.abstractmethod
    async def run(cls, state: immutables.Map) -> R:
        ...

    @staticmethod
    def applied(state: immutables.Map) -> FrozenSet[Type[Partial]]:
        return frozenset(state.keys())

    @classmethod
    def missing(cls, state: immutables.Map) -> FrozenSet[Type[Partial]]:
        return frozenset(set(cls.depends) - cls.applied(state))

    @classmethod
    def runnable_dependencies(cls, state: immutables.Map) -> Iterable[Type[Partial]]:
        missing = cls.missing(state)
        if len(missing) == 0 and cls not in cls.applied(state):
            yield cls
        for dep in missing:
            yield from dep.runnable_dependencies(state)
