from Task5 import is_even


def is_prime(number: int) -> bool:
    for i in range(1, number):
        if not number % i:
            return False

    return True


def goldbach():
    while True:
        user_input = input("Enter an even number greater than 2 or 'q' to quit: ")
        if user_input == "q":
            print("Exit!")
            return None

        try:
            number = int(user_input)
            if not is_even(number):
                print("Please enter even number.")
                continue

            for i in range(1, number):
                j = number - i
                if is_prime(i) and is_prime(j):
                    print(f"{number} = {i} + {j}\n")
                    break

        except Exception as e:
            print(f"{e.__class__.__name__}: {e}")


if __name__ == "__main__":
    goldbach()
