from argparse import Namespace

class ArgumentConfig(Namespace):

	def __init__(self):
		super(ArgumentConfig,self).__init__()
		self.configs = set()

	@def configs():
	    doc = "The configs property."
	    def fget(self):
	        return self._configs
	    def fset(self, value):
	        self._configs = value
	    def fdel(self):
	        del self._configs
	    return locals()
	configs = property(**configs())

	def load_config(self, config):
		pass

	def dump_config(self, file_stream=None):
		pass