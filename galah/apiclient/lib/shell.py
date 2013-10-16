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
This module handles creating and defining the shell interface.

"""

import cmd
import shlex
import ui

class APIShell(cmd.Cmd):
	intro = "Welcome to the Galah API Client shell."
	prompt = "> "

	def __init__(self, session, *args, **kwargs):
		self.session = session

		cmd.Cmd.__init__(self, *args, **kwargs)

	def default(self, raw_args):
		"""
		This is called whenever a command is entered that the `cmd` library
		doesn't recognize, which should be all API commands.

		"""

		# Split up what the user typed in, just like how bash does it.
		args = shlex.split(raw_args)
		if not args:
			return
		command = args.pop(0)

		# Perform the command the user wants to execute
		command_args, command_kwargs = ui.parse_raw_args(args)

		try:
			self.session.call(command, *command_args, **command_kwargs)
		except SystemExit:
			pass
		except KeyboardInterrupt:
			print
			print "Interrupted..."

	def do_help(self, arg):
		if arg:
			func = self.session.api_info.get(arg)
			if func:
				print func
			else:
				print "No help for", arg
		else:
			for k, v in self.session.api_info.items():
				print v

	def do_exit(self, arg):
		return True
	do_quit = do_exit

	def do_EOF(self, arg):
		print
		return True

	def completedefault(self, text, line, begidx, endidx):
		cmd_args = shlex.split(line)
		cmd_info = self.session.api_info.get(cmd_args[0])
		print
		print "cmd_args:", cmd_args
		print "cmd_info:", cmd_info
		print text, line, begidx, endidx

	def get_names(self):
		"""
		Overrides undocumented `get_names` function to allow command
		completion.

		"""

		return ["do_" + i for i in self.session.api_info.keys()]

	def emptyline(self):
		return
