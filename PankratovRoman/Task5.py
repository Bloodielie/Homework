from typing import Callable, TypeVar, Any
from functools import wraps

T = TypeVar("T")


def remember_result_factory() -> Callable[[Callable[..., T]], Callable[..., T]]:
    last_result = None

    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> T:
            nonlocal last_result
            print(f"Last result = '{last_result}'")
            last_result = func(*args, **kwargs)
            return last_result

        return wrapper

    return decorator


remember_result = remember_result_factory()


@remember_result
def sum_list(*args: str) -> str:
    result = ""
    for item in args:
        result += item
    print(f"Current result = '{result}'")
    return result


if __name__ == "__main__":
    sum_list("a", "b")
    sum_list("abc", "cde")
    # sum_list(3, 4, 5)
