from points import Point
from .linear_fuzzy_set import LinearFuzzySet


def trapeze_set(minimum: float, maximum: float, start_base: float, start_plateau: float,
                end_plateau: float, end_base: float) -> LinearFuzzySet:
    assert minimum < start_base < start_plateau < end_plateau < end_base < maximum
    s = LinearFuzzySet(minimum, maximum)
    s.add_point(Point(minimum, 0))
    s.add_point(Point(start_base, 0))
    s.add_point(Point(start_plateau, 1))
    s.add_point(Point(end_plateau, 1))
    s.add_point(Point(end_base, 0))
    s.add_point(Point(maximum, 0))
    return s


def left_trapeze_set(minimum: float, maximum: float, end_plateau: float, end_base: float) -> LinearFuzzySet:
    assert minimum < end_plateau < end_base < maximum
    s = LinearFuzzySet(minimum, maximum)
    s.add_point(Point(minimum, 1))
    s.add_point(Point(end_plateau, 1))
    s.add_point(Point(end_base, 0))
    s.add_point(Point(maximum, 0))
    return s


def right_trapeze_set(minimum: float, maximum: float, start_base: float, start_plateau: float) -> LinearFuzzySet:
    assert minimum < start_base < start_plateau < maximum
    s = LinearFuzzySet(minimum, maximum)
    s.add_point(Point(minimum, 0))
    s.add_point(Point(start_base, 0))
    s.add_point(Point(start_plateau, 1))
    s.add_point(Point(maximum, 1))
    return s


def triangle_set(minimum: float, maximum: float, start_base: float, vertex: float, end_base: float) -> LinearFuzzySet:
    assert minimum < start_base < vertex < end_base < maximum
    s = LinearFuzzySet(minimum, maximum)
    s.add_point(Point(minimum, 0))
    s.add_point(Point(start_base, 0))
    s.add_point(Point(vertex, 1))
    s.add_point(Point(end_base, 0))
    s.add_point(Point(maximum, 0))
    return s


def constant_set(minimum: float, maximum: float, value: float) -> LinearFuzzySet:
    assert minimum < maximum
    s = LinearFuzzySet(minimum, maximum)
    s.add_point_from_coord(minimum, value)
    s.add_point_from_coord(maximum, value)
    return s
