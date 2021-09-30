class Bird:
    def __init__(self, name: str):
        self._name = name

    def fly(self) -> None:
        print(f"{self._name} bird can fly")

    def walk(self) -> None:
        print(f"{self._name} bird can fly")

    def __repr__(self) -> str:
        return f"{self._name} bird can walk and fly"


class FlyingBird(Bird):
    def __init__(self, name: str, ration: str = "worms"):
        super().__init__(name)

        self._ration = ration

    def eat(self) -> None:
        print(f"It eats mostly {self._ration}")

    def __repr__(self) -> str:
        return f"{self._name} bird can walk and fly and eat"


class NonFlyingBird:
    def __init__(self, name: str, ration: str = "fish"):
        self._name = name
        self._ration = ration

    def walk(self) -> None:
        print(f"{self._name} bird can walk")

    def eat(self) -> None:
        print(f"It eats mostly {self._ration}")

    def swim(self) -> None:
        print(f"{self._name} bird can swim")

    def __repr__(self) -> str:
        return f"{self._name} bird can eat, walk and swim"


class SuperBird(FlyingBird, NonFlyingBird):
    pass


if __name__ == "__main__":
    b = Bird("Any")
    b.walk()

    p = NonFlyingBird("Penguin", "fish")
    p.swim()
    try:
        p.fly()  # type: ignore
    except AttributeError as e:
        print(e)
    p.eat()

    c = FlyingBird("Canary")
    print(str(c))
    c.eat()

    s = SuperBird("Gull")
    print(str(s))
    s.eat()
