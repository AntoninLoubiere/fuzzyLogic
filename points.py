from __future__ import annotations


class Point:
    """
    A 2D point.
    """

    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def not_operator(self) -> Point:
        return Point(self.x, 1 - self.y)

    def __str__(self):
        return f"P({self.x};{self.y})"

    def __repr__(self):
        return self.__str__()

    def __mul__(self, other):
        return self.__class__(self.x, self.y * other)

    def __imul__(self, other):
        self.y *= other
        return self

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __ne__(self, other):
        return not isinstance(other, Point) or self.x != other.x or self.y != other.y

    def __lt__(self, other):
        return self.x < other.x

    def __le__(self, other):
        return self.x <= other.x

    def __gt__(self, other):
        return self.x > other.x

    def __ge__(self, other):
        return self.x >= other.x
