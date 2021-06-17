from netflix_mock.feature_flags import feature_flag, feature_flags


def test_feature_flag_usage_true():
    assert feature_flags.is_on("SHOW_BETA")


def test_feature_flag_usage_false():
    assert not feature_flags.is_on("FEATURE_ONE")


def test_unknown_feature_flag():
    assert feature_flags.is_on("UNKNOWN") is None


# toggling is for unit testing only


def test_feature_toggle_default():
    with feature_flag("FEATURE_ONE"):
        assert feature_flags.is_on("FEATURE_ONE")


def test_feature_toggle_on():
    with feature_flag("FEATURE_ONE", on=True):
        assert feature_flags.is_on("FEATURE_ONE")


def test_feature_toggle_off():
    with feature_flag("FEATURE_ONE", on=False):
        assert not feature_flags.is_on("FEATURE_ONE")
