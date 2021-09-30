from typing import Optional


class Singleton:
    __instance = None

    def __new__(cls, *args, **kwargs):
        if Singleton.__instance is None:
            Singleton.__instance = super().__new__(cls)
        return Singleton.__instance

    @classmethod
    def get_instance(cls) -> Optional["Singleton"]:
        return cls.__instance


if __name__ == "__main__":
    s1 = Singleton()
    s2 = Singleton()
    print(s1 == s2)
    print(s1 is s2)

    print(s1 == Singleton.get_instance())
    print(s2 == Singleton.get_instance())
