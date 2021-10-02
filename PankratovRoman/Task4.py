from functools import wraps
from typing import Any, Callable, TypeVar, Optional

T = TypeVar("T")


def suppress_exceptions(func: Callable[..., T]) -> Callable[..., Optional[T]]:
    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Optional[T]:
        try:
            result = func(*args, **kwargs)
        except Exception:
            return None
        else:
            print(f"The {func.__name__} function worked without errors.")
            return result

    return wrapper


@suppress_exceptions
def zero_division() -> float:
    return 1 / 0


@suppress_exceptions
def test() -> float:
    return 1.0


if __name__ == "__main__":
    print(zero_division())
    print("-" * 40)
    print(test())
