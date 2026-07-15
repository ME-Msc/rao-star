"""Minimal Episode implementation for the local RMPyL shim."""
from .constraints import TemporalConstraint
from .defs import Event


class Episode(object):
    def __init__(self, start=None, end=None, action=None, duration=None, **kwargs):
        self.start = start or Event()
        self.end = end or Event()
        self.action = action
        self.duration = duration
        self.properties = dict(kwargs)
        self.temporal_constraints = set()
        self.internal_episodes = []
        self.composition = None
        self.terminal = False
        self.id = kwargs.pop("id", None)

        if duration is not None:
            self.temporal_constraints.add(self._duration_to_constraint(duration))

    @classmethod
    def composite(cls, composition, episodes, start=None):
        ep = cls(start=start, action=None)
        ep.composition = composition
        ep.internal_episodes = list(episodes)
        if ep.internal_episodes:
            first = ep.internal_episodes[0]
            last = ep.internal_episodes[-1]
            ep.start = getattr(first, "first_event", getattr(first, "start", ep.start))
            ep.end = getattr(last, "last_event", getattr(last, "end", ep.end))
        return ep

    @property
    def first_event(self):
        return self.start

    @property
    def last_event(self):
        return self.end

    def _duration_to_constraint(self, duration):
        if isinstance(duration, dict):
            duration_dict = dict(duration)
            ctype = duration_dict.pop("ctype", "controllable")
            lb = duration_dict.pop("lb", 0.0)
            ub = duration_dict.pop("ub", float("inf"))
            distribution = duration_dict.pop("distribution", None)
            if distribution is not None:
                lb = distribution.get("lb", lb)
                ub = distribution.get("ub", ub)
            return TemporalConstraint(
                self.start,
                self.end,
                ctype=ctype,
                lb=lb,
                ub=ub,
                distribution=distribution,
                **duration_dict
            )
        return TemporalConstraint(self.start, self.end, lb=0.0, ub=float(duration))

    def __repr__(self):
        if self.action is not None:
            return str(self.action)
        return self.composition or "episode"
