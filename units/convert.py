from heapq import heappop, heappush
import itertools

__all__ = ["convert"]


class PriorityQueue:
    def __init__(self):
        self.heap = []
        self.counter = itertools.count()

    def push(self, element, priority):
        heappush(self.heap, (priority, next(self.counter), element))

    def pop(self):
        return heappop(self.heap)[2]

    def __bool__(self):
        return bool(self.heap)


def complexity(unit):
    return len(unit.numerator) + len(unit.denominator)


def check(unit, units):
    for unit in unit.numerator + unit.denominator:
        if unit not in units:
            raise ValueError("unknown unit: '{}'".format(unit))


def convert(source, target):
    from .conversions import ones, units

    check(source.unit, units)
    check(target, units)

    checked = {source.unit}
    to_visit = PriorityQueue()
    to_visit.push(source, 0)

    max_comp = complexity(source.unit / target)

    while to_visit:
        value = to_visit.pop()

        for one in ones:
            result = value * one

            if result.unit == target:
                return result

            if result.unit not in checked:
                checked.add(result.unit)
                comp = complexity(result.unit / target)
                if comp <= max_comp:
                    to_visit.push(result, comp)

    raise ValueError(
        "no conversion found between '{}' and '{}'".format(source.unit, target)
    )
