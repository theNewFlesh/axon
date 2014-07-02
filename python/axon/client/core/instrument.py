#! /usr/bin/env python

# Alex Braun 01.25.2014
# >> INSERT LICENSE HERE <<

'''
.. module:: instrument
	:date: 01.25.2014
	:platform: Unix
	:synopsis: Client dependency graph instrument
	
.. moduleauthor:: Alex Braun <ABraunCCS@gmail.com>
'''
# ------------------------------------------------------------------------------

from collections import *

from axon.utilities.errors import *
from axon.utilities.utils import *
from axon.client.core.dg import Component
# ------------------------------------------------------------------------------

class Instrument(Component):
	def __init__(self, spec, node):
		super(Instrument, self).__init__(spec, node)
		self._cls = 'Instrument'
	# --------------------------------------------------------------------------

	@property
	def package_name(self):
		return self._map['package_name']

	@property
	def method_name(self):
		return self._map['method_name']

	@property
	def args(self):
		output = []  
		for aspec in self._map['args'].values():
			if aspec['value'] == self.node.null:
				output.append(aspec['default'])
			else:	
				output.append(aspec['value'])
		return output

	@property
	def kwargs(self):
		output = {}
		for kspec in self._map['kwargs']:
			if kspec['value'] == self.node.null:
				output[kspec] = kspec['default']
			else:
				output[kspec] = kspec['vaue']
		return output
	# --------------------------------------------------------------------------
	
	def build(self, spec):
		self._spec = spec
		self._map['name'] = spec['name']
		self._map['package_name'] = spec['package_name']
		self._map['method_name'] = spec['method_name']

		package = self.node.all_packages[self.package_name]
		method = package.methods[self.method_name]

		args = spec_to_ordereddict(spec['args'])
		for key, val in args.iteritems():
			if val['default'] == self.node.null:
				val['default'] = method['args'][key]['default']
		self._map['args'] = args

		kwargs = spec_to_ordereddict(spec['kwargs'])
		for key, val in kwargs.iteritems():
			if val['default'] == self.node.null:
				val['default'] = method['kwargs'][key]['default']
		self._map['kwargs'] = kwargs
	# --------------------------------------------------------------------------
	
	def fire(self):
		pass
# ------------------------------------------------------------------------------

def main():
	'''
	Run help if called directly
	'''
	
	import __main__
	help(__main__)
# ------------------------------------------------------------------------------

__all__ = ['Instrument']

if __name__ == '__main__':
	main()