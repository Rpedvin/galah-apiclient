# Copyright (c) 2013 Galah Group LLC
# Copyright (c) 2013 Other contributers as noted in the CONTRIBUTERS file
#
# This file is part of galah-apiclient.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
#
# You may obtain a copy of the License at
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
This module contains any useful function that don't fit in any of the other
modules.

"""

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
    """
    Imports the request library and returns it.

    """

    try:
        import requests
    except ImportError:
        raise ImportError(
            "Could not load the requests library. Please install requests "
            "to correct this problem."
        )

    return requests

import os.path
def resolve_path(path):
    """
    Converts a path a user provided into its absolute path representation. This
    will behave as the user expects.

    :param path: A relative or absolute path to convert.
    :returns: An absolute path pointing to `path`

    """

    return os.path.abspath(os.path.expanduser(path))

def resolve_paths(paths):
    """
    Resolves a list of paths.

    Equivalent to

    .. code-block:: python

        [resolve_path(i) for i in paths]

    :param paths: An iterable containing paths to convert.
    :returns: A list containing the converted paths.

    """

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
    """
    Loads a YAML file safely.

    :param file: A file object to load.
    :returns: The deserialized contents of the file.

    """

    return yaml_module().safe_load(file)

import os.path
import os
def prepare_directory(path, permissions = 0o700):
    """
    Ensures a directory exists and creates it if necessary, including any
    necessary parent directories.

    :param path: The directory to create:
    :param permissions: The permissions to give the directories. Ignored on
            non nix systems.
    :returns: `True` iff a new directory was created, `False` otherwise.

    Permissions will not be changed if the directory was already created.

    """

    directory = os.path.dirname(path)

    if os.path.isdir(directory):
        return False

    os.makedirs(directory, permissions)
    return True

HOME_DIR = os.path.expanduser("~")
def shorten_path(path):
    """
    Attempts to return a "friendly" version of the given path.

    :param path: The path to shorten.
    :returns: A friendly version of `path`

    .. code-block:: text

        >>> utils.shorten_path("/tmp/walrus")
        '/tmp/walrus'
        >>> os.getcwd()
        '/home/john/Projects/galah-apiclient/apiclient'
        >>> utils.shorten_path("/home/john/Projects/galah-apiclient")
        '~/Projects/galah-apiclient'
        >>> utils.shorten_path("/home/john/Projects/galah-apiclient/apiclient")
        '~/Projects/galah-apiclient/apiclient'

    """

    choices = []

    choices.append(path)

    abs_path = os.path.normpath(resolve_path(path))
    choices.append(os.path.join("~/", os.path.relpath(abs_path, HOME_DIR)))
    choices.append(abs_path)

    return min(choices, key = len)

def postfix_file_name(file_name, suffix):
    """
    Adds a suffix to a filename while preserving the file extension.

    :returns: The modified file_name.

    .. code-block:: text

        >>> utils.postfix_file_name("myfile.exe", " walrus")
        'myfile walrus.exe'
    """

    file_name, extension = os.path.splitext(file_name)

    return str(file_name) + str(suffix) + str(extension)

def find_available_file(file_path):
    """
    Find an available file name, adding a number if the file name is
    taken. For example, if a file myfile.tgz exists, we will use
    myfile (1).tgz. This is similar to how the browser chromium handles
    downloads.

    :param file_path: The most desired file path.
    :returns: The first available file path, adding (#) to the end of the file
            name as necessary.

    .. code-block:: text

        >>> utils.find_available_file("/tmp/my_monkey.exe")
        '/tmp/my_monkey (3).exe'

    """

    directory, file_name = os.path.split(file_path)

    suffix = ""
    count = 1
    while os.path.isfile(os.path.join(directory,
            postfix_file_name(file_name, suffix))):
        suffix = " (%d)" % (count, )
        count += 1

    return os.path.join(directory, postfix_file_name(file_name, suffix))

