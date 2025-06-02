import json
import os

CONFIG_PATH = "settings.json"


def save_ui_state(data: dict, path: str = CONFIG_PATH):
    with open(path, "w") as f:
        json.dump(data, f, indent=4)


def persist_value(key, value, config_path=CONFIG_PATH):
    """
    Saves or updates a single key-value pair in a JSON file.

    Args:
        key (str): The config key to save (e.g., 'salary_income')
        value (Any): The value to store
        config_path (str): Path to the JSON config file
    """
    config = {}

    # Load existing config if file exists
    if os.path.exists(config_path):
        with open(config_path, "r") as f:
            try:
                config = json.load(f)
            except json.JSONDecodeError:
                config = {}

    # Update with new value
    config[key] = value

    # Save updated config
    with open(config_path, "w") as f:
        json.dump(config, f, indent=4)


def persist_dict(values: dict[str, any], config_path=CONFIG_PATH):
    """
    Saves multiple key-value pairs to a JSON file, updating existing content if present.

    Args:
        config_path (str): Path to the JSON config file.
        values (Dict[str, Any]): Dictionary of values to persist.
    """
    config = {}

    # Load existing config if available
    if os.path.exists(config_path):
        try:
            with open(config_path, "r") as f:
                config = json.load(f)
        except (json.JSONDecodeError, IOError):
            config = {}

    # Update config with new values
    config.update(values)

    # Write back to file
    with open(config_path, "w") as f:
        json.dump(config, f, indent=4)


def get_value(key, default=None, config_path=CONFIG_PATH):
    """
    Retrieves a value by key from a JSON config file.

    Args:
        key (str): The key to look up.
        config_path (str): Path to the JSON file.
        default (Any): Value to return if key is not found.

    Returns:
        The value associated with the key, or default if not found.
    """
    if not os.path.exists(config_path):
        return default

    try:
        with open(config_path, "r") as f:
            config = json.load(f)
            return config.get(key, default)
    except (json.JSONDecodeError, IOError, TypeError):
        return default


def load_ui_state(path: str = CONFIG_PATH) -> dict:
    if os.path.exists(path):
        with open(path, "r") as f:
            return json.load(f)
    return {}


def save_all_inputs_to_json(layout, values_dict):
    """
    Traverses the layout and saves all input-like component values.

    Args:
        layout: The Dash layout object (e.g. app.layout)
        values_dict: A dictionary mapping {id: value} captured in callback
    """
    result = {}

    def recurse_components(component):
        if isinstance(component, (list, tuple)):
            for child in component:
                recurse_components(child)
        elif hasattr(component, "id") and hasattr(component, "type"):
            cid = getattr(component, "id", None)
            if cid and cid in values_dict:
                result[cid] = values_dict[cid]
        if hasattr(component, "children"):
            recurse_components(component.children)

    recurse_components(layout)

    with open(CONFIG_PATH, "w") as f:
        json.dump(result, f, indent=4)
