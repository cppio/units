from .unit import Unit

__all__ = ["Value"]


class Value:
    __slots__ = "value", "unit"

    def __init__(self, value=1, unit=Unit()):
        self.value, self.unit = value, unit

    def __repr__(self):
        if not self.unit:
            return "Value({!r})".format(self.value)

        return "Value({!r}, {!r})".format(self.value, self.unit)

    def __str__(self):
        if not self.unit:
            return str(self.value)

        return "{} {}".format(self.value, self.unit)

    def __lt__(self, other):
        if isinstance(other, Value):
            if self.unit != other.unit:
                raise ValueError("cannot compare values with differing units")

            return self.value < other.value

        if not self.unit:
            return self.value < other

        return NotImplemented

    def __le__(self, other):
        if isinstance(other, Value):
            if self.unit != other.unit:
                raise ValueError("cannot compare values with differing units")

            return self.value <= other.value

        if not self.unit:
            return self.value <= other

        return NotImplemented

    def __gt__(self, other):
        if isinstance(other, Value):
            if self.unit != other.unit:
                raise ValueError("cannot compare values with differing units")

            return self.value > other.value

        if not self.unit:
            return self.value > other

        return NotImplemented

    def __ge__(self, other):
        if isinstance(other, Value):
            if self.unit != other.unit:
                raise ValueError("cannot compare values with differing units")

            return self.value >= other.value

        if not self.unit:
            return self.value >= other

        return NotImplemented

    def __eq__(self, other):
        if isinstance(other, Value):
            return (self.value, self.unit) == (other.value, other.unit)

        if not self.unit:
            return self.value == other

        return NotImplemented

    def __hash__(self):
        if not self.unit:
            return hash(self.value)

        return hash((self.value, self.unit))

    def __bool__(self):
        return bool(self.value)

    def __add__(self, other):
        if isinstance(other, Value):
            if self.unit != other.unit:
                raise ValueError("cannot add values with differing units")

            return Value(self.value + other.value, self.unit)

        if not self.unit:
            return Value(self.value + other)

        return NotImplemented

    def __radd__(self, other):
        if not self.unit:
            return Value(other + self.value)

        return NotImplemented

    def __sub__(self, other):
        if isinstance(other, Value):
            if self.unit != other.unit:
                raise ValueError("cannot subtract values with differing units")

            return Value(self.value - other.value, self.unit)

        if not self.unit:
            return Value(self.value - other)

        return NotImplemented

    def __rsub__(self, other):
        if not self.unit:
            return Value(other - self.value)

        return NotImplemented

    def __mul__(self, other):
        if isinstance(other, Value):
            return Value(self.value * other.value, self.unit * other.unit)

        if isinstance(other, Unit):
            return Value(self.value, self.unit * other)

        return Value(self.value * other, self.unit)

    def __rmul__(self, other):
        if isinstance(other, Unit):
            return Value(self.value, other * self.unit)

        return Value(other * self.value, self.unit)

    def __truediv__(self, other):
        if isinstance(other, Value):
            return Value(self.value / other.value, self.unit / other.unit)

        return Value(self.value / other, self.unit)

    def __rtruediv__(self, other):
        return Value(other / self.value, self.unit ** -1)

    def __pow__(self, other):
        if not self.unit:
            return Value(self.value ** other)

        if not isinstance(other, int):
            return NotImplemented

        return Value(self.value ** other, self.unit ** other)

    def __neg__(self):
        return Value(-self.value, self.unit)

    def __pos__(self):
        return Value(+self.value, self.unit)

    def __abs__(self):
        return Value(abs(self.value), self.unit)

    @classmethod
    def parse(cls, string):
        value, *unit = string.split(" ", maxsplit=1)
        value = float(value)

        if unit:
            return cls(value, Unit.parse(*unit))
        else:
            return cls(value)
