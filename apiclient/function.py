import logging
logger = logging.getLogger("apiclient.session")

class Function:
	class Parameter:
		def __init__(self, name, default_value = None, param_type = None):
			self.name = name
			self.default_value = default_value
			self.param_type = param_type

		def __str__(self):
			result = [self.name]

			if self.param_type:
				result.append(":" + self.param_type.__name__)

			if self.default_value:
				result.append(" = " + str(self.default_value))

			return "".join(result)

	def __init__(self, name, params):
		self.name = name
		self.params = params

	def validate_params(self, raise_exception = True):
		default_values = False
		for i in self.params:
			if i.default_value:
				default_values = True
			elif i.default_value != default_values:
				if not raise_exception:
					return False

				raise ValueError(
					"The parameters specified after a parameter with a default "
					"value has been specified must also have default "
					"parameters."
				)

		return True

	def resolve_arguments(self, *args, **kwargs):
		# TODO: Implement type checking.
	    result = {}

	    params_copy = self.params[:]

	    for i in args:
	    	if not params_copy:
	    		raise TypeError(
	    			"%s has %d argument(s) (%d given)." %
	    				(self.name, len(self.params), len(args) + len(kwargs))
	    		)

    		current_param = params_copy.pop(0)

	    	result[current_param.name] = i

	    PARAMETER_NAMES = set(i.name for i in self.params)
	    for k, v in kwargs.items():
	    	if k not in PARAMETER_NAMES:
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
	    	if i.name not in result and i.default_value:
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
		return self.name + "(" + ", ".join(str(i) for i in self.params) + ")"

