from typing import Any, Dict

from netflix_mock.settings import Settings


def update_settings(settings: Settings, settings_to_update: Dict[str, Any]) -> Dict[str, Any]:
    updated = {}
    for key, value in settings_to_update.items():
        if key in settings.dict():
            if isinstance(value, dict):
                if updated_ := update_settings(getattr(settings, key), settings_to_update[key]):
                    updated[key] = updated_
            elif isinstance(value, list):
                pass
            else:
                setattr(settings, key, value)  # validate_assignment = True
                updated[key] = value
    return updated
