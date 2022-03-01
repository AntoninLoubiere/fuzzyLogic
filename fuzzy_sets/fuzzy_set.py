from __future__ import annotations

from itertools import zip_longest

from fuzzy_parser import parse_assert
from points import Point


class BaseFuzzySet:
    def __init__(self, _min: float, _max: float):
        self.min = _min
        self.max = _max
        self.points: list[Point] = []

    def belongs_value(self, x: float) -> float:
        raise NotImplementedError()

    def barycenter(self) -> float:
        raise NotImplementedError()

    def add_point(self, point: Point) -> None:
        if len(self.points) < 1 or self.points[-1] < point:  # points are generally added in the right order
            self.points.append(point)
        else:
            self.points.insert(self.get_index_from_point(point.x), point)

    def add_point_from_coord(self, x: float, y: float) -> Point:
        p = Point(x, y)
        self.add_point(p)
        return p

    def remove_point(self, i: int) -> Point:
        return self.points.pop(i)

    def get_index_from_point(self, x) -> int:
        """
        Get the index of the point just after x
        """
        start = 0
        end = len(self.points) - 1

        while start <= end:
            mid = (start + end) // 2
            p = self.points[mid]
            if p.x == x:
                return mid + 1
            elif p.x < x:
                start = mid + 1
            else:
                end = mid - 1
        return start

    def not_operator(self) -> BaseFuzzySet:
        f = BaseFuzzySet(self.min, self.max)
        for p in self.points:
            f.add_point(p.not_operator())
        return f

    def show(self, block=False):
        from matplotlib import pyplot
        x = []
        y = []
        for p in self.points:
            x.append(p.x)
            y.append(p.y)
        pyplot.plot(x, y)
        pyplot.show(block=block)

    def __str__(self):
        return f"|{self.min}{self.points}{self.max}|"

    def __repr__(self):
        return f"<FuzzySet min={self.min}, max={self.max}, points={self.points}>"

    def __eq__(self, other):
        if self.min != other.min or self.max != other.max:
            return False

        for p, op in zip_longest(self.points, other.points):
            if p != op:
                return False

        return True

    def __ne__(self, other):
        return not self.__eq__(other)

    def __mul__(self, other):
        f = self.__class__(self.min, self.max)
        if other:
            for p in self.points:
                f.add_point(p * other)
            return f
        else:
            f.add_point(Point(self.min, 0))
            f.add_point(Point(self.max, 0))
            return f

    def __imul__(self, other):
        for p in self.points:
            p *= other
        return self

    def __or__(self, other):
        raise NotImplementedError()

    def __and__(self, other):
        raise NotImplementedError()

    @classmethod
    def load_from_data(cls, data: str) -> BaseFuzzySet:
        points: list[Point] = []

        for p in data.split(';'):
            coord = p.split(',')
            parse_assert(len(coord) == 2, "Point should have exactly 2 coordinates.")
            points.append(Point(float(coord[0].strip()), float(coord[1].strip())))

        result = cls(min(points).x, max(points).x)
        for p in points:
            result.add_point(p)

        return result
