"""Minimal temporal and chance constraints for the local RMPyL shim."""


class TemporalConstraint(object):
    def __init__(self, start, end, ctype="controllable", lb=0.0, ub=float("inf"),
                 distribution=None, **kwargs):
        self.start = start
        self.end = end
        self.type = ctype
        self.ctype = ctype
        self.lb = lb
        self.ub = ub
        self.distribution = distribution
        self.properties = dict(kwargs)
        if distribution is not None:
            self.properties["distribution"] = distribution

    def __repr__(self):
        return "TemporalConstraint(%s -> %s, %s, [%s, %s])" % (
            self.start,
            self.end,
            self.ctype,
            self.lb,
            self.ub,
        )

    def __hash__(self):
        return hash((self.start, self.end, self.ctype, self.lb, self.ub,
                     repr(self.distribution)))

    def __eq__(self, other):
        return isinstance(other, TemporalConstraint) and self.is_equivalent(other)

    def is_equivalent(self, other):
        return (
            isinstance(other, TemporalConstraint)
            and self.start == other.start
            and self.end == other.end
            and self.ctype == other.ctype
            and self.lb == other.lb
            and self.ub == other.ub
            and self.distribution == other.distribution
        )


class ChanceConstraint(object):
    def __init__(self, constraint_scope=None, risk=0.0):
        self.constraint_scope = list(constraint_scope or [])
        self.risk = risk

    def __repr__(self):
        return "ChanceConstraint(risk=%s, scope=%d)" % (
            self.risk,
            len(self.constraint_scope),
        )

    def __hash__(self):
        return hash((tuple(self.constraint_scope), self.risk))
