"""Tiny PARIS scheduler facade used by temporal rock-sample examples."""


class PARIS(object):
    def __init__(self, **kwargs):
        self.params = kwargs

    def schedule(self, constraints):
        return {}, 0.0, {}
