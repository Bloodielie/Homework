from typing import Sequence, Union, Optional


class MyNumberCollection:
    def __init__(self, start_or_sequence: Union[Sequence, int], end: Optional[int] = None, step: Optional[int] = None):
        self._collection = []
        self._iter_index = 0

        if isinstance(start_or_sequence, Sequence):
            for element in start_or_sequence:
                if not isinstance(element, int):
                    raise TypeError("MyNumberCollection supports only numbers!")
                self._collection.append(element)
        elif isinstance(start_or_sequence, int):
            if end is None or step is None:
                raise AttributeError("If start_or_sequence argument is int you must pass end and step.")
            self._collection.extend(range(start_or_sequence, end, step))
            if self._collection[-1] != end:
                self._collection.append(end)
        else:
            raise AttributeError("First argument of init supports only int and sequence.")

    def append(self, element: int) -> None:
        if not isinstance(element, int):
            raise TypeError(f"'{element.__class__.__name__}' - object is not a number!")

        self._collection.append(element)

    def __getitem__(self, element_index: int) -> int:
        return self._collection[element_index] ** 2

    def __repr__(self) -> str:
        return str(self._collection)

    def __add__(self, other: "MyNumberCollection") -> "MyNumberCollection":
        new_collection = self._collection.copy()
        return MyNumberCollection(new_collection + other._collection)

    def __iter__(self) -> "MyNumberCollection":
        self._iter_index = -1
        return self

    def __next__(self) -> int:
        self._iter_index += 1
        if self._iter_index >= len(self._collection):
            raise StopIteration

        return self._collection[self._iter_index]


if __name__ == "__main__":
    col1 = MyNumberCollection(0, 5, 2)
    print(col1)

    col2 = MyNumberCollection((1, 2, 3, 4, 5))
    print(col2)

    try:
        col3 = MyNumberCollection((1, 2, 3, "4", 5))
    except TypeError as e:
        print(f"{e.__class__.__name__}: {e}")

    col1.append(7)
    print(col1)

    try:
        col2.append("string")  # type: ignore
    except TypeError as e:
        print(f"{e.__class__.__name__}: {e}")

    print(col1 + col2)
    print(col1)
    print(col2)
    print(col2[4])

    for item in col1:
        print(item)
