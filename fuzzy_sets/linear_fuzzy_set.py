from __future__ import annotations

from typing import Callable

from helpers import signum
from points import Point
from .fuzzy_set import BaseFuzzySet

APPROXIMATIONS = 10 ** -10


class LinearFuzzySet(BaseFuzzySet):

    def belongs_value(self, x: float) -> float:
        if len(self.points) < 1:
            return 0

        elif len(self.points) == 1:
            return self.points[0].y

        if x < self.min:
            x = self.min
        elif x > self.max:
            x = self.max

        i = self.get_index_from_point(x)
        previous_point = self.points[i - 1]
        if x == previous_point.x:
            return previous_point.y
        next_point = self.points[i]
        return (previous_point.y - next_point.y) * (next_point.x - x) / (next_point.x - previous_point.x) + next_point.y

    def __or__(self, other):
        return self.__merge(other, True)

    def __and__(self, other):
        return self.__merge(other, False)

    def __merge(self, set2: LinearFuzzySet, maximise: bool):
        set1 = self
        result_set = LinearFuzzySet(min(set1.min, set2.min), max(set1.max, set2.max))

        set_1_len = len(set1.points)
        set_2_len = len(set2.points)

        pt_set1 = set1.points[0]
        pt_i_set1 = 1
        pt_set2 = set2.points[0]
        pt_i_set2 = 1

        pt_func = max if maximise else min
        signum_func: Callable[[], int] = (lambda: signum(pt_set1.y - pt_set2.y)) if maximise else \
            lambda: -signum(pt_set1.y - pt_set2.y)

        current_set: int = signum_func()  # 1 if set1 is the current set or, else -1
        previous_set: int

        while pt_i_set1 <= set_1_len or pt_i_set2 <= set_2_len:
            previous_set = current_set
            current_set = signum_func()
            if previous_set != current_set and previous_set != 0:
                # Order has changed, compute intersection point
                if pt_set1.x == pt_set2.x:
                    p1 = set1.points[0] if pt_i_set1 <= 2 else set1.points[pt_i_set1 - 2]
                    p2 = set2.points[0] if pt_i_set2 <= 2 else set2.points[pt_i_set2 - 2]

                    if p2 < p1 < pt_set1 or p2 >= pt_set1:
                        start_x = p1.x
                    else:
                        start_x = p2.x
                else:
                    start_x = min(pt_set1.x, pt_set2.x)
                end_x = max(pt_set1.x, pt_set2.x)

                s1 = (set1.belongs_value(end_x) - set1.belongs_value(start_x)) / (end_x - start_x)
                s2 = (set2.belongs_value(end_x) - set2.belongs_value(start_x)) / (end_x - start_x)

                delta = 0 if s1 == s2 else (set2.belongs_value(start_x) - set1.belongs_value(start_x)) / (s1 - s2)

                # assert set1.belongs_value(start_x + delta) == set2.belongs_value(start_x + delta)

                result_set.add_point_from_coord(start_x + delta, set1.belongs_value(start_x + delta))

            if pt_set1.x < pt_set2.x or \
                    (pt_set1.x == pt_set2.x and ((maximise and pt_set1.y <= pt_set2.y) or
                                                 (not maximise and pt_set1.y >= pt_set2.y))):
                result_set.add_point_from_coord(pt_set1.x, pt_func(pt_set1.y, set2.belongs_value(pt_set1.x)))

                if pt_i_set1 < set_1_len:
                    pt_set1 = set1.points[pt_i_set1]
                    pt_i_set1 += 1
                else:
                    pt_i_set1 += 1
                    pt_set1 = Point(result_set.max + 1, set1.belongs_value(result_set.max))
            else:
                result_set.add_point_from_coord(pt_set2.x, pt_func(set1.belongs_value(pt_set2.x), pt_set2.y))

                if pt_i_set2 < set_2_len:
                    pt_set2 = set2.points[pt_i_set2]
                    pt_i_set2 += 1
                else:
                    pt_i_set2 += 1
                    pt_set2 = Point(result_set.max + 1, set2.belongs_value(result_set.max))

        # Cleanup unnecessary points
        first_point: Point
        middle_point: Point = result_set.points[0]
        last_point: Point = result_set.points[1]
        nb_points = len(result_set.points)
        i = 2
        while i < nb_points:
            first_point = middle_point
            middle_point = last_point
            last_point = result_set.points[i]

            if first_point == last_point:
                result_set.remove_point(i - 1)
                middle_point = first_point
                nb_points -= 1
                continue

            s = (last_point.y - first_point.y) / (last_point.x - first_point.x)
            if abs(s * (middle_point.x - first_point.x) + first_point.y - middle_point.y) <= APPROXIMATIONS:
                result_set.remove_point(i - 1)
                middle_point = first_point
                nb_points -= 1
                continue

            i += 1

        return result_set

    def barycenter(self) -> float:
        if len(self.points) < 2:
            return 0.

        area_pondered: float = 0.
        area_total: float = 0.
        area_local: float
        previous_pt = None

        for pt in self.points:
            if previous_pt:
                if previous_pt.y == pt.y:
                    # it is a rectangle
                    area_local = pt.y * (pt.x - previous_pt.x)
                    area_total += area_local
                    area_pondered += area_local * ((pt.x - previous_pt.x) / 2 + previous_pt.x)
                else:
                    # it is a trapeze
                    # we decompose it as a rectangle and a triangle

                    # rectangle time
                    area_local = min(pt.y, previous_pt.y) * (pt.x - previous_pt.x)
                    area_total += area_local
                    area_pondered += area_local * ((pt.x - previous_pt.x) / 2 + previous_pt.x)

                    # triangle time
                    area_local = (pt.x - previous_pt.x) * abs(pt.y - previous_pt.y) / 2
                    area_total += area_local

                    if pt.y > previous_pt.y:
                        area_pondered += area_local * ((pt.x - previous_pt.x) * 2 / 3 + previous_pt.x)
                    else:
                        area_pondered += area_local * ((pt.x - previous_pt.x) / 3 + previous_pt.x)

            previous_pt = pt

        return area_pondered / area_total if area_total else 0
