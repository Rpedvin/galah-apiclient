def json_module():
    """
    A handy function that will try to find a suitable JSON module to import and
    return that module (already loaded).

    Basically, it tries to load the ``json`` module, and if that doesn't exist
    it tries to load the ``simplejson`` module. If that doesn't exist, a
    friendly ``ImportError`` is raised.

    """

    try:
        import json
    except ImportError:
        try:
            import simplejson as json
        except ImportError:
            raise ImportError(
                "Could not load a suitable JSON module. You can try upgrading "
                "your version of Python or installing the simplejson library."
            )

    return json

def yaml_module():
    """
    A handy function that will try to find a suitable YAML module to import and
    return that module (already loaded).

    Currently it only searches for PyYAML and fails if it isn't found.
    Conceivably we'd want to support other YAML libraries in the future.

    """

    try:
        import yaml
    except ImportError:
        raise ImportError(
            "Could not load a suitable YAML module. Please install PyYAML to "
            "correct this problem."
        )

    return yaml

def requests_module():
    try:
        import requests
    except ImportError:
        logger.critical(
            "Could not load the requests library.",
            exc_info = sys.exc_info()
        )
    return requests

import os.path
def resolve_path(path):
    return os.path.abspath(os.path.expanduser(path))

def resolve_paths(paths):
	return [resolve_path(i) for i in paths]

def to_json(obj):
    """
    Serializes an object into a JSON representation.

    :param obj: The object to serialize.

    :returns: A JSON object (encoded as a string) representing ``obj`` that is
            compressed apprropriately for network transfer.

    """

    return json_module().dumps(obj, separators = (",", ":"))

def load_yaml(file):
    return yaml_module().safe_load(file)

import os.path
import os
def prepare_directory(path):
    directory = os.path.dirname(path)

    if os.path.isdir(directory):
        return False

    os.makedirs(directory, 0o700)
    return True
