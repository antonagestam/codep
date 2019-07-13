from __future__ import annotations

import abc
from typing import Callable
from typing import FrozenSet
from typing import Iterable
from typing import NamedTuple
from typing import Optional
from typing import Sequence
from typing import Set
from typing import Type

import immutables


class Partial(abc.ABC):
    class Result(NamedTuple):
        of: Optional[Type[Partial]]
        previous: Optional[Partial.Result]  # type: ignore
        state: immutables.Map

    depends: Sequence[Type[Partial]] = ()

    def __init__(self):
        raise RuntimeError("Partials cannot be instantiated")

    @classmethod
    @abc.abstractmethod
    def run(cls, state: immutables.Map) -> immutables.Map:
        ...

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
        return Partial.Result(of=cls, previous=result, state=cls.run(result.state))


def make_partial(
    depends: Sequence[Type[Partial]] = ()
) -> Callable[[Callable[[immutables.Map], immutables.Map]], Type[Partial]]:
    # We assign a new new name so that we can assign to the depends class
    # property of FunctionalPartial in the decorator, while maintaining the same
    # name in the API.
    _depends_on = depends

    def decorator(fn: Callable[[immutables.Map], immutables.Map]) -> Type[Partial]:
        class FunctionalPartial(Partial):
            depends = _depends_on

            @classmethod
            def run(cls, state: immutables.Map) -> immutables.Map:
                return fn(state)

        FunctionalPartial.__name__ = fn.__name__
        return FunctionalPartial

    return decorator
