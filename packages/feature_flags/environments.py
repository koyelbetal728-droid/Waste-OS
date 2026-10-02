"""Per-environment overrides — production can disable something dev has on."""
from packages.core.config import settings
from packages.feature_flags.flags import DEFAULT_FLAGS

ENVIRONMENT_OVERRIDES = {
    "production": {"object_storage": False},  # flip to True once real cloud credentials exist
}


def get_flags_for_environment() -> dict:
    flags = DEFAULT_FLAGS.copy()
    flags.update(ENVIRONMENT_OVERRIDES.get(settings.app_env, {}))
    return flags
