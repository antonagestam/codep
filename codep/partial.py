from __future__ import annotations

import abc
from typing import Any
from typing import cast
from typing import FrozenSet
from typing import Generic
from typing import Iterable
from typing import NamedTuple
from typing import Optional
from typing import Sequence
from typing import Set
from typing import Type
from typing import TypeVar

import immutables


R = TypeVar("R", bound=Any)


class Partial(abc.ABC, Generic[R]):
    class Result(NamedTuple):
        of: Optional[Type[Partial]]
        previous: Optional[Partial.Result]  # type: ignore
        state: immutables.Map

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
    def apply(cls, result: Partial.Result) -> Partial.Result:
        # Make sure all partials that this one depends on has been applied in
        # the given result.
        missing_dependencies = cls.missing(result)
        if len(missing_dependencies) > 0:
            raise RuntimeError(
                f"All required partials have not been applied to the previous "
                f"result. Missing dependencies: {missing_dependencies}."
            )

        print(f"Applying partial: {cls.__name__}")
        return Partial.Result(
            of=cls, previous=result, state=result.state.set(cls, cls.run(result.state))
        )

    @staticmethod
    def applied(result: Partial.Result) -> FrozenSet[Type[Partial]]:
        applied_set: Set[Type[Partial]] = set()
        if result.of is not None:
            applied_set.add(result.of)
        while result.previous is not None:
            if result.of is not None:
                applied_set.add(result.previous.of)
            result = result.previous
        return frozenset(applied_set)

    @classmethod
    def missing(cls, result: Partial.Result) -> FrozenSet[Type[Partial]]:
        return frozenset(set(cls.depends) - cls.applied(result))

    @classmethod
    def runnable_dependencies(cls, result: Partial.Result) -> Iterable[Type[Partial]]:
        missing = cls.missing(result)
        if len(missing) == 0 and cls not in cls.applied(result):
            yield cls
        for dep in missing:
            yield from dep.runnable_dependencies(result)
