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

HOME_DIR = os.path.expanduser("~")
def shorten_path(path):
    choices = []

    choices.append(path)

    abs_path = os.path.normpath(resolve_path(path))
    choices.append(os.path.join("~/", os.path.relpath(abs_path, HOME_DIR)))
    choices.append(abs_path)

    return min(choices, key = len)

def postfix_file_name(file_name, suffix):
    file_name, extension = os.path.splitext(file_name)

    return str(file_name) + str(suffix) + str(extension)

def find_available_file(file_path):
    """
    Find an available file name, adding a number if the file name is
    taken. For example, if a file myfile.tgz exists, we will use
    myfile (1).tgz. This is similar to how the browser chromium handles
    downloads.

    """

    directory, file_name = os.path.split(file_path)

    suffix = ""
    count = 1
    while os.path.isfile(os.path.join(directory,
            postfix_file_name(file_name, suffix))):
        suffix = " (%d)" % (count, )
        count += 1

    return os.path.join(directory, postfix_file_name(file_name, suffix))

