from typing import Any, Dict, List

from netflix_mock.settings import Settings


def update_settings(settings: Settings, settings_to_update: Dict[str, Any]) -> List[str]:
    changed_keys = []
    for key, value in settings_to_update.items():
        if key in settings.dict():
            if isinstance(value, dict):
                changed_keys_ = update_settings(getattr(settings, key), settings_to_update[key])
                changed_keys.extend(changed_keys_)
            elif isinstance(value, list):
                pass
            else:
                setattr(settings, key, value)  # validate_assignment = True
                changed_keys.append(key)
    return changed_keys
