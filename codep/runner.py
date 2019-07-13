from __future__ import annotations

import asyncio
from typing import Any
from typing import Iterable
from typing import Type
from typing import TypeVar

import immutables

from .partial import Partial

T = TypeVar("T", bound=Any)


async def run_one(partial: Type[Partial[T]], state: immutables.Map) -> immutables.Map:
    runnable = tuple(partial.runnable_dependencies(state))

    while runnable:
        tasks = (dependency.run(state) for dependency in runnable)
        results = await asyncio.gather(*tasks)
        mutation = state.mutate()
        for dependency, result in zip(runnable, results):
            mutation.set(dependency, result)
        state = mutation.finish()
        runnable = tuple(partial.runnable_dependencies(state))

    if partial not in state:
        raise RuntimeError("Failed ")

    return state


def run(*partials: Type[Partial[T]]) -> Iterable[T]:
    state = immutables.Map()
    for partial in partials:
        state = asyncio.run(run_one(partial, state))
        yield partial.value(state)
