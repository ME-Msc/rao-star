"""Minimal RMPyL definition objects required by the RAO* examples."""
from collections import namedtuple
from itertools import count


_event_ids = count()
_choice_ids = count()


class Event(object):
    """Event marker used by temporal constraints and episodes."""

    def __init__(self, name=None):
        self.name = name or "EVENT-%d" % next(_event_ids)
        self.id = self.name

    def __repr__(self):
        return self.name

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        return isinstance(other, Event) and self.id == other.id


class Choice(object):
    """Observation/choice variable for composite episodes."""

    def __init__(self, name=None, ctype="controllable", domain=None, probability=None):
        self.name = name or "Choice_%d" % next(_choice_ids)
        self.id = self.name
        self.type = ctype
        self.domain = list(domain or [])
        if probability is None and self.domain:
            probability = [1.0 / len(self.domain)] * len(self.domain)
        self.probability = list(probability or [])

    def __repr__(self):
        return self.name


ChoiceAssignment = namedtuple("ChoiceAssignment", ["var", "value", "utility"])
