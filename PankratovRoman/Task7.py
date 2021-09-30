from functools import total_ordering
from typing import Dict, Any

RATES = {"USD": 1.0, "EUR": 0.86, "BYN": 2.51, "RUS": 72.83}


@total_ordering
class Money:
    def __init__(self, value: float, currency_name: str = "USD", rates: Dict[str, float] = RATES):
        self._currency_name = currency_name
        self._rate = rates.get(currency_name, 1.0)
        self._unified_value = value / self._rate

    @property
    def unified_value(self) -> float:
        return round(self._unified_value, 2)

    @property
    def value(self) -> float:
        return round(self.unified_value * self._rate, 2)

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, Money):
            return self.unified_value == other.unified_value
        return self.unified_value == other

    def __lt__(self, other: Any) -> bool:
        if isinstance(other, Money):
            return self.unified_value < other.unified_value
        return self.unified_value < other

    def __add__(self, other: Any) -> "Money":
        if isinstance(other, Money):
            new_value = round(self.unified_value + other.unified_value * self._rate, 2)
        else:
            new_value = self.value + other

        return Money(new_value, self._currency_name)

    __radd__ = __add__

    def __sub__(self, other: Any) -> "Money":
        if isinstance(other, Money):
            new_value = round(self.unified_value - other.unified_value * self._rate, 2)
        else:
            new_value = self.value - other

        return Money(new_value, self._currency_name)

    def __rsub__(self, other: Any) -> "Money":
        if isinstance(other, Money):
            new_value = round(other.unified_value - self.unified_value * self._rate, 2)
        else:
            new_value = other - self.value

        return Money(new_value, self._currency_name)

    def __mul__(self, other: Any) -> "Money":
        if isinstance(other, Money):
            new_value = round(self.unified_value * other.unified_value * self._rate, 2)
        else:
            new_value = self.value * other

        return Money(new_value, self._currency_name)

    __rmul__ = __mul__

    def __truediv__(self, other: Any) -> "Money":
        if isinstance(other, Money):
            new_value = round(self.unified_value / other.unified_value * self._rate, 2)
        else:
            new_value = self.value / other

        return Money(new_value, self._currency_name)

    def __rtruediv__(self, other: Any) -> "Money":
        if isinstance(other, Money):
            new_value = round(other.unified_value / self.unified_value * self._rate, 2)
        else:
            new_value = other / self.value

        return Money(new_value, self._currency_name)

    def __repr__(self) -> str:
        return f"{self.value} {self._currency_name}"


if __name__ == "__main__":
    x = Money(10, "BYN")
    y = Money(11)
    z = Money(12.34, "EUR")
    print(z + 3.11 * x + y * 0.8)

    lst = [Money(10, "BYN"), Money(11), Money(12.01, "RUS")]
    s = sum(lst)
    print(s)
