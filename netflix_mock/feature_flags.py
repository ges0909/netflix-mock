from contextlib import contextmanager
from typing import Optional

import yaml
from pydantic import BaseModel


class Feature(BaseModel):
    description: Optional[str] = None
    active: bool

    class Config:
        extra = "forbid"


class FeatureFlags:
    flags = {}

    @classmethod
    def is_on(cls, name):
        return cls.flags.get(name)

    @classmethod
    def toggle(cls, name, value):
        cls.flags[name] = value

    @classmethod
    def __init__(cls):
        with open("../features.yaml", "r") as stream:
            features = yaml.load(stream, Loader=yaml.FullLoader)
        for key, value in features.items():
            feature = Feature(**value)  # validate
            setattr(cls, key, feature.description)
            cls.flags[key] = feature.active


@contextmanager
def feature_flag(name, on=True):
    """turn feature temporarily on/off for unit testing"""
    value_ = feature_flags.is_on(name)
    feature_flags.toggle(name, on)
    yield
    feature_flags.toggle(name, value_)


feature_flags = FeatureFlags()
