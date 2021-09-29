from typing import Sequence, TypeVar, Tuple, List, Optional

T = TypeVar("T")


def get_pairs(sequence: Sequence[T]) -> Optional[List[Tuple[T, T]]]:
    if len(sequence) == 1:
        return None
    return [(sequence[i], sequence[i+1]) for i in range(len(sequence)-1)]


if __name__ == "__main__":
    print(get_pairs([1, 2, 3, 8, 9]))
    print(get_pairs(['need', 'to', 'sleep', 'more']))
    print(get_pairs([1]))
    