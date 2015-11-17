from collections import namedtuple
from math import sqrt, copysign

EPSILON = 0.00000000001


def sign(x):
    copysign(1, x)


def direction(x):
    if abs(x) < EPSILON:
        return 0
    else:
        return sign(x)


def is_between(a, b, c):
    crossproduct = (c.y - a.y) * (b.x - a.x) - (c.x - a.x) * (b.y - a.y)
    if abs(crossproduct) > EPSILON:
        return False

    dotproduct = (c.x - a.x) * (b.x - a.x) + (c.y - a.y)*(b.y - a.y)
    if dotproduct < 0:
        return False

    squaredlengthba = (b.x - a.x)*(b.x - a.x) + (b.y - a.y)*(b.y - a.y)
    if dotproduct > squaredlengthba:
        return False

    return True


def on_rectangle(p1, p2, q):
    return (
        min(p1.x, p2.x) <= q.x <= max(p1.x, p2.x) and
        min(p1.y, p2.y) <= q.y <= max(p1.y, p2.y)
    )


class SimplePoint(object):
    def __init__(self, x=None, y=None, point=None):
        if point:
            self.x = point.x
            self.y = point.y
        else:
            self.x = x
            self.y = y

    def __add__(self, other):
        return SimplePoint(x=self.x + other.x, y=self.y + other.y)

    def __sub__(self, other):
        return SimplePoint(x=self.x - other.x, y=self.y - other.y)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    @staticmethod
    def cross_product(p1, p2):
        return p1.x*p2.y - p1.y*p2.x

    @staticmethod
    def dot_product(p1, p2):
        return p1.x*p2.x + p1.y*p2.y

    def distance(self, other):
        dx = self.x - other.x
        dy = self.y - other.y
        return sqrt(dx*dx + dy*dy)


class Segment(object):
    def __init__(self, p1, p2):
        self.p1 = SimplePoint(point=p1)
        self.p2 = SimplePoint(point=p2)

    def direction(self, point):
        return SimplePoint.cross_product(self.p2 - self.p1, point - self.p1)

    @staticmethod
    def is_intersection(s1, s2):
        s1s_s2 = s2.direction(s1.p1)
        s1e_s2 = s2.direction(s1.p2)
        s2s_s1 = s1.direction(s2.p1)
        s2e_s1 = s1.direction(s2.p2)
        s12 = s1s_s2 * s1e_s2
        s21 = s2s_s1 * s2e_s1

        if s12 > 0 or s21 > 0:
            return False
        if s12 < 0 or s21 < 0:
            return True

        if s1s_s2 == 0 and on_rectangle(s2.p1, s2.p2, s1.p1):
            return True
        if s1e_s2 == 0 and on_rectangle(s2.p1, s2.p2, s1.p2):
            return True
        if s2s_s1 == 0 and on_rectangle(s1.p1, s1.p2, s2.p1):
            return True
        if s2e_s1 == 0 and on_rectangle(s1.p1, s1.p2, s2.p2):
            return True

        return False

    @staticmethod
    def intersection(s1, s2):

        # result = namedtuple('intersection', ['x', 'y'])
        A1, B1 = (s1.p2-s1.p1).y, (s1.p1 - s1.p2).x
        A2, B2 = (s2.p2-s2.p1).y, (s2.p1 - s2.p2).x

        C1, C2 = A1*s1.p1.x + B1*s1.p1.y, A2*s2.p1.x + B2*s2.p1.y

        det = A1*B2 - A2*B1

        if abs(det) < EPSILON:
            return None
        # return result((B2*C1 - B1*C2)/det, (A1*C2 - A2*C1)/det)
        return SimplePoint(x=(B2*C1 - B1*C2)/det, y=(A1*C2 - A2*C1)/det)

