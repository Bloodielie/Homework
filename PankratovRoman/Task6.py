from functools import wraps
from typing import Callable, TypeVar, Any

T = TypeVar("T")


def call_once(func: Callable[..., T]) -> Callable[..., T]:
    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> T:
        cache = getattr(func, "__cache", None)
        if cache is None:
            cache = func(*args, **kwargs)
            setattr(func, "__cache", cache)

        return cache

    return wrapper


@call_once
def sum_of_numbers(a, b):
    return a + b


if __name__ == "__main__":
    print(sum_of_numbers(13, 42))
    print(sum_of_numbers(999, 100))
    print(sum_of_numbers(134, 412))
    print(sum_of_numbers(856, 232))
