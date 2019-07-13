from __future__ import annotations

from typing import Iterable
from typing import Type

import immutables

from .partial import Partial


def run_one(partial: Type[Partial], result: Partial.Result) -> Partial.Result:
    runnable = tuple(partial.runnable_dependencies(result))

    while len(runnable) != 0:
        for dependency in runnable:
            result = dependency.apply(result)
        runnable = tuple(partial.runnable_dependencies(result))

    return result


def run(*partials: Type[Partial]) -> Iterable[Partial.Result]:
    result = Partial.Result(of=None, previous=None, state=immutables.Map())
    for partial in partials:
        result = run_one(partial, result)
        yield result
