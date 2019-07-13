from typing import Any
from typing import Callable
from typing import Sequence
from typing import Type
from typing import TypeVar

import immutables

from .partial import Partial


T = TypeVar("T", bound=Any)


def make_partial(
    depends: Sequence[Type[Partial]] = ()
) -> Callable[[Callable[[immutables.Map], T]], Type[Partial[T]]]:
    # We assign a new new name so that we can assign to the depends class
    # property of FunctionalPartial in the decorator, while maintaining the same
    # name in the API.
    _depends_on = depends

    def decorator(fn: Callable[[immutables.Map], T]) -> Type[Partial[T]]:
        class FunctionalPartial(Partial[T]):
            depends = _depends_on

            @classmethod
            def run(cls, state: immutables.Map) -> T:
                return fn(state)

        FunctionalPartial.__name__ = fn.__name__
        return FunctionalPartial

    return decorator
