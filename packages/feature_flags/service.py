from packages.feature_flags.environments import get_flags_for_environment


def is_enabled(flag_name: str) -> bool:
    return get_flags_for_environment().get(flag_name, False)
