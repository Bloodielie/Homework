from collections import deque
from typing import Dict, Optional, Sequence, TypeVar, Generic, Deque

K = TypeVar("K")
V = TypeVar("V")


class HistoryDict(Generic[K, V]):
    def __init__(self, custom_dict: Optional[Dict[K, V]] = None):
        self._dict = custom_dict or {}
        self._key_history: Deque[K] = deque(maxlen=10)

    def set_value(self, key: K, value: V) -> None:
        self._key_history.append(key)
        self._dict[key] = value

    def get_history(self) -> Sequence[K]:
        return self._key_history


if __name__ == "__main__":
    d = HistoryDict[str, int]({"foo": 42})
    d.set_value("bar", 43)
    print(d.get_history())
