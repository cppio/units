from collections import Counter
import re

__all__ = ["Unit"]

alpha = re.compile("[A-Za-z]+")
num = re.compile("[0-9]+")


class Unit:
    __slots__ = "numerator", "denominator"

    def __init__(self, numerator=(), denominator=()):
        numerator, denominator = Counter(numerator), Counter(denominator)
        common = numerator & denominator
        self.numerator = tuple(sorted((numerator - common).elements()))
        self.denominator = tuple(sorted((denominator - common).elements()))

    def __repr__(self):
        return "Unit({!r}, {!r})".format(self.numerator, self.denominator)

    def __str__(self):
        def str_unit(unit, exponent):
            if exponent > 1:
                return "{}^{}".format(unit, exponent)

            return str(unit)

        if self.numerator:
            components = []
            for unit, exponent in Counter(self.numerator).items():
                if components:
                    components.append("*")
                components.append(str_unit(unit, exponent))
        else:
            components = ["1"]

        if self.denominator:
            for unit, exponent in Counter(self.denominator).items():
                components.append("/")
                components.append(str_unit(unit, exponent))

        return "".join(components)

    def __eq__(self, other):
        if not isinstance(other, Unit):
            return NotImplemented

        this = self.numerator, self.denominator
        that = other.numerator, other.denominator

        return this == that

    def __hash__(self):
        return hash((self.numerator, self.denominator))

    def __bool__(self):
        return bool(self.numerator) or bool(self.denominator)

    def __mul__(self, other):
        if not isinstance(other, Unit):
            return NotImplemented

        return Unit(
            self.numerator + other.numerator, self.denominator + other.denominator
        )

    def __truediv__(self, other):
        if not isinstance(other, Unit):
            return NotImplemented

        return Unit(
            self.numerator + other.denominator, self.denominator + other.numerator
        )

    def __pow__(self, other):
        if not isinstance(other, int):
            return NotImplemented

        return Unit(
            self.numerator * other + self.denominator * -other,
            self.denominator * other + self.numerator * -other,
        )

    @classmethod
    def parse(cls, string):
        numerator = []

        if string.startswith("1"):
            string = string[1:]
        else:
            string = "*" + string

            while string and not string.startswith("/"):
                if not string.startswith("*"):
                    raise ValueError("expected '*'")

                match = alpha.match(string[1:])

                if not match:
                    raise ValueError("expected unit")

                string = string[match.end() + 1 :]
                numerator.append(match[0])

                if string.startswith("^"):
                    match = num.match(string[1:])

                    if not match:
                        raise ValueError("expected exponent")

                    string = string[match.end() + 1 :]
                    numerator[-1:] = numerator[-1:] * int(match[0])

        if not string:
            return Unit(numerator)

        denominator = []

        while string:
            if not string.startswith("/"):
                raise ValueError("expected '/'")

            match = alpha.match(string[1:])

            if not match:
                raise ValueError("expected unit")

            string = string[match.end() + 1 :]
            denominator.append(match[0])

            if string.startswith("^"):
                match = num.match(string[1:])

                if not match:
                    raise ValueError("expected exponent")

                string = string[match.end() + 1 :]
                denominator[-1:] = denominator[-1:] * int(match[0])

        return Unit(numerator, denominator)
