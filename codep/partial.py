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


R = TypeVar("R", bound=Any)


class Partial(abc.ABC, Generic[R]):
    depends: Sequence[Type[Partial]] = ()

    def __init__(self):
        raise RuntimeError("Partials cannot be instantiated")

    @classmethod
    def value(cls, state: immutables.Map) -> R:
        return cast(R, state[cls])

    @classmethod
    @abc.abstractmethod
    def run(cls, state: immutables.Map) -> R:
        ...

    @classmethod
    def apply(cls, state: immutables.Map) -> immutables.Map:
        # Make sure all partials that this one depends on has been applied in
        # the given result.
        missing_dependencies = cls.missing(state)
        if len(missing_dependencies) > 0:
            raise RuntimeError(
                f"All required partials have not been applied to the previous "
                f"result. Missing dependencies: {missing_dependencies}."
            )

        print(f"Applying partial: {cls.__name__}")
        return state.set(cls, cls.run(state))

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
