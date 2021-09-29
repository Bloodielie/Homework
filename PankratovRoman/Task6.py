def get_longest_word(string: str) -> str:
    return max(string.split(), key=len)


if __name__ == "__main__":
    print(get_longest_word('Python is simple and effective!'))
    print(get_longest_word('Any pythonista like namespaces a lot.'))
