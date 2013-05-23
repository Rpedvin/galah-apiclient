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
This module houses the useful :class:`Function` class.

"""

import logging
logger = logging.getLogger("apiclient.function")

class Function:
    """
    This class represents a command that can be executed on the server.

    :ivar name: The name of the command.
    :ivar params: A list of :class:`Function.Parameter` objects representing the
            paramaters the command will accept.

    """

    class Parameter:
        def __init__(self, name, default_value = None, param_type = None):
            self.name = str(name)
            self.param_type = param_type

            self.default_value = default_value
            if isinstance(self.default_value, basestring):
                self.default_value = str(self.default_value)

        def __str__(self):
            result = [self.name]

            if self.param_type and self.param_type is not str:
                result.append(":" + self.param_type.__name__)

            if self.default_value is not None:
                result.append(" = " + repr(self.default_value))

            if self.default_value is not None:
                return "[" + "".join(result) + "]"
            else:
                return "".join(result)

    def __init__(self, name, params):
        self.name = name
        self.params = params

    def resolve_arguments(self, *args, **kwargs):
        """
        Takes a list of positional arguments and keyword arguments and
        determines which parameter each argument is a value for.

        :returns: A dictionary of paramater names and the values for each of
                them.

        """

        # TODO: Implement type checking.
        result = {}

        params_copy = self.params[:]

        # Grab all of the positional arguments and associate them correctly.
        for i in args:
            if not params_copy:
                raise TypeError(
                    "%s has %d argument(s) (%d given)." %
                        (self.name, len(self.params), len(args) + len(kwargs))
                )

            current_param = params_copy.pop(0)

            result[current_param.name] = i

        # Grab all of the keyword arguments.
        parameter_names = set(i.name for i in self.params)
        for k, v in kwargs.items():
            if k not in parameter_names:
                raise TypeError(
                    "%s received unknown keyword argument %s." %
                        (self.name, k)
                )
            elif k not in (j.name for j in params_copy):
                raise TypeError(
                    "%s got multiple values for keyword argument %s." %
                        (self.name, k)
                )

            result[k] = v

            # Delete the item from the list (by creating a new list without that
            # item in it).
            params_copy = [j for j in params_copy if j.name != k]

        for i in self.params:
            if i.name not in result and i.default_value is not None:
                result[i.name] = i.default_value

        for i in self.params:
            if i.name not in result:
                raise TypeError(
                    "%s expected %d arguments, got %d." % (
                        self.name,
                        len(self.params),
                        len(args) + len(kwargs)
                    )
                )

        return result

    def __str__(self):
        return self.name + " " + " ".join(str(i) for i in self.params)

