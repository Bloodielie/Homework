def replacer(string: str) -> str:
    callbacks = {"\"": lambda _: "\'", "\'": lambda _: "\""}
    return "".join(callbacks.get(symbol, lambda s: s)(symbol) for symbol in string)


if __name__ == "__main__":
    print(replacer("a'b'c'd"))
    print(replacer('a"b"c"d'))
    print(replacer('abc'))
