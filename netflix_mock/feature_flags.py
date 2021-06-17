from contextlib import contextmanager


class FeatureFlags:
    """
    How to use?
    >>> if feature_flags.is_on(FeatureFlags.SHOW_BETA):
    ...
    """

    SHOW_BETA = "Show Beta version of Home Page"

    flags = {SHOW_BETA: True}

    @classmethod
    def is_on(cls, name):
        return cls.flags[name]

    @classmethod
    def toogle(cls, name, value):
        cls.flags[name] = value


@contextmanager
def feature_flag(name, on=True):
    """Turn feature temporarily on and off for unit testing.

    How to use?
    >>> with feature_flag(FeatureFlags.SHOW_BETA):
    ...
    >>> with feature_flag(FeatureFlags.SHOW_BETA, on=False):
    """
    old_value = feature_flags.is_on(name)
    feature_flags.toogle(name, on)
    yield
    feature_flags.toogle(name, old_value)


feature_flags = FeatureFlags()
