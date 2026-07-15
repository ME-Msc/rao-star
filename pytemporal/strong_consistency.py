"""Strong-consistency facade for legacy RMPyL unraveler examples."""


class PTPNStrongConsistency(object):
    def __init__(self, paris_params=None, verbose=False):
        self.paris_params = paris_params or {}
        self.verbose = verbose

    def strong_consistency(self, decisions, constraints):
        return 1.0
