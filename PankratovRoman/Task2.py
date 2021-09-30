from collections import Counter
from typing import Iterator


def most_common_words(filepath: str, number_of_words: int = 3) -> Iterator[str]:
    with open(filepath, "r", encoding="utf-8") as f:
        data = f.read()

    words_counter = Counter(data.split())
    return (word[0] for word in words_counter.most_common(number_of_words))


if __name__ == "__main__":
    print(tuple(most_common_words("../data/lorem_ipsum.txt")))
