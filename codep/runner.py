from __future__ import annotations

from typing import Any
from typing import Iterable
from typing import Type
from typing import TypeVar

import immutables

from .partial import Partial

T = TypeVar("T", bound=Any)


def run_one(partial: Type[Partial[T]], state: immutables.Map) -> immutables.Map:
    runnable = tuple(partial.runnable_dependencies(state))

    while len(runnable) != 0:
        for dependency in runnable:
            state = dependency.apply(state)
        runnable = tuple(partial.runnable_dependencies(state))

    return state


def run(*partials: Type[Partial[T]]) -> Iterable[T]:
    state = immutables.Map()
    for partial in partials:
        state = run_one(partial, state)
        yield partial.value(state)
