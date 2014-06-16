#! /usr/bin/env python

# Alex Braun 01.25.2014
# >> INSERT LICENSE HERE <<

'''
.. module:: instrument
	:date: 01.25.2014
	:platform: Unix
	:synopsis: Python dependency graph instrument
	
.. moduleauthor:: Alex Braun <ABraunCCS@gmail.com>
'''
# ------------------------------------------------------------------------------

from collections import *

from axon.utilities.errors import *
from axon.dependency.graph.nodes.components.dg import DG
# ------------------------------------------------------------------------------

class Instrument(DG):
	def __init__(self, spec, node):
		super(Instrument, self).__init__(node)
		self._class = 'Instrument'
		self._node = node
		self._spec = spec
		self._map = None
	# --------------------------------------------------------------------------

	@property
	def spec(self):
		return self._spec

	@property
	def map(self):
		return self._map

	@property
	def name(self):
		return self._map['name']

	@property
	def package_name(self):
		return self._map['package_name']

	@property
	def method_name(self):
		return self._map['method_name']

	@property
	def args(self):
		output = []
		for aspec in self._map['args']:
			if aspec['value'] == '<null>':
				output.append(aspec['default'])
			else:	
				output.append(aspec['value'])
		return output

	@property
	def kwargs(self):
		output = {}
		for kspec in self._map['kwargs']:
			if kspec['value'] == '<null>':
				output[kspec] = kspec['default'])
			else:
				output[kspec] = kspec['vaue'])
		return output

	def fire(self):
		# INFORMER HOOK
		message = 'fire', self.node.name, self.name, self.args, self.kwargs
		self.node.informer.log('instruments', message=message)
		# ----------------------------------------------------------------------

		method = self.node.packages[self.package_name]['methods'][self.method_name]
		method(*self.args.values(), **self.kwargs)
# ------------------------------------------------------------------------------

def main():
	'''
	Run help if called directly
	'''
	
	import __main__
	help(__main__)
# ------------------------------------------------------------------------------

__all__ = ['Instrument', 'Interface']

if __name__ == '__main__':
	main()