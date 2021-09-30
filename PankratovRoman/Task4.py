a = "I am global variable!"


def enclosing_func_1() -> None:
    a = "I am variable from enclosed function!"

    def inner_function() -> None:
        a = "I am local variable!"
        print(a)

    return inner_function()


def enclosing_func_2() -> None:
    a = "I am variable from enclosed function!"

    def inner_function() -> None:
        global a
        print(a)

    return inner_function()


def enclosing_func_3() -> None:
    a = "I am variable from enclosed function!"

    def inner_function() -> None:
        nonlocal a
        print(a)

    return inner_function()


if __name__ == "__main__":
    enclosing_func_1()
    enclosing_func_2()
    enclosing_func_3()
