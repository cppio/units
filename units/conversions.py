import os.path

from .value import Value

__all__ = ["ones", "units"]


def load(path):
    with open(path) as file:
        contents = file.read()

    ones = []
    units = set()

    for line in contents.splitlines():
        left, right = line.split("=")
        left, right = Value.parse(left), Value.parse(right)

        ones.append(left / right)
        ones.append(right / left)

        for unit in (left.unit, right.unit):
            for unit in unit.numerator + unit.denominator:
                units.add(unit)

    return ones, units


path = os.path.join(os.path.dirname(__file__), "conversions.txt")
ones, units = load(path)
