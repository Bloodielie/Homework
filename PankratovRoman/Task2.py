def is_palindrome(string: str) -> bool:
    return string.lower() == string.lower()[::-1]


if __name__ == '__main__':
    print(is_palindrome('deed'))
    print(is_palindrome("levels"))
    print(is_palindrome("peep"))
